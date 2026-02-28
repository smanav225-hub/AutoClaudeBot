import time
from datetime import datetime, timedelta
from typing import Any, Dict, List


class LeaderboardProService:
    """Time-sliced leaderboard with metric and search filtering."""

    _METRIC_ALIASES = {
        "xp": "xp",
        "total_xp": "xp",
        "messages": "messages",
        "total_messages": "messages",
        "words": "words",
        "reputation": "reputation",
        "rep": "reputation",
        "level": "level",
        "streak": "streak",
    }

    def __init__(self, msg_db):
        self.msg_db = msg_db

    @staticmethod
    def _normalize_period(period: str) -> str:
        p = (period or "all").strip().lower()
        if p in {"today", "daily"}:
            return "today"
        if p in {"weekly", "week", "7d"}:
            return "weekly"
        if p in {"monthly", "month", "this_month", "30d"}:
            return "monthly"
        return "all"

    @classmethod
    def _normalize_metric(cls, metric: str) -> str:
        m = (metric or "xp").strip().lower()
        return cls._METRIC_ALIASES.get(m, "xp")

    @staticmethod
    def _period_start_ts(period: str) -> float:
        now = datetime.utcnow()
        if period == "today":
            return now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        if period == "weekly":
            return (now - timedelta(days=7)).timestamp()
        if period == "monthly":
            return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0).timestamp()
        return 0.0

    def _fetch_all_time_rows(self, guild_id: str) -> List[Dict[str, Any]]:
        conn = self.msg_db.get_connection()
        conn.row_factory = __import__("sqlite3").Row
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT user_id,
                       COALESCE(username, user_id) AS username,
                       COALESCE(user_discriminator, '0') AS user_discriminator,
                       COALESCE(avatar_url, '') AS avatar_url,
                       COALESCE(level, 0) AS level,
                       COALESCE(xp_total, 0) AS xp,
                       COALESCE(messages_total, 0) AS messages,
                       COALESCE(words_total, 0) AS words,
                       COALESCE(reputation, 0) AS reputation
                FROM user_levels
                WHERE guild_id=?
                """,
                (str(guild_id),),
            )
            rows = [dict(r) for r in cur.fetchall()]
            if rows:
                return rows
        finally:
            conn.close()

        # Fallback to messages if user_levels has not been built yet.
        return self._fetch_window_rows(guild_id, start_ts=0.0)

    def _fetch_window_rows(self, guild_id: str, start_ts: float) -> List[Dict[str, Any]]:
        conn = self.msg_db.get_connection()
        conn.row_factory = __import__("sqlite3").Row
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT m.user_id,
                       COALESCE(MAX(m.username), m.user_id) AS username,
                       COALESCE(MAX(m.user_discriminator), '0') AS user_discriminator,
                       COALESCE(MAX(m.avatar_url), '') AS avatar_url,
                       COUNT(*) AS messages,
                       COALESCE(SUM(m.word_count), 0) AS words,
                       COALESCE(SUM(m.xp_gain), 0) AS xp
                FROM messages m
                WHERE m.guild_id=? AND m.created_at >= ? AND COALESCE(m.is_deleted, 0)=0
                GROUP BY m.user_id
                """,
                (str(guild_id), float(start_ts)),
            )
            rows = [dict(r) for r in cur.fetchall()]
            by_user = {str(r["user_id"]): r for r in rows}

            cur.execute(
                """
                SELECT receiver_id AS user_id, COUNT(*) AS rep_received
                FROM reputation_events
                WHERE guild_id=? AND created_at >= ?
                GROUP BY receiver_id
                """,
                (str(guild_id), float(start_ts)),
            )
            for row in cur.fetchall():
                uid = str(row["user_id"])
                if uid not in by_user:
                    by_user[uid] = {
                        "user_id": uid,
                        "username": uid,
                        "user_discriminator": "0",
                        "avatar_url": "",
                        "messages": 0,
                        "words": 0,
                        "xp": 0,
                    }
                by_user[uid]["reputation"] = int(row["rep_received"] or 0)

            cur.execute(
                """
                SELECT user_id, COALESCE(level, 0) AS level, COALESCE(reputation, 0) AS reputation_total
                FROM user_levels
                WHERE guild_id=?
                """,
                (str(guild_id),),
            )
            for row in cur.fetchall():
                uid = str(row["user_id"])
                if uid not in by_user:
                    continue
                by_user[uid]["level"] = int(row["level"] or 0)
                by_user[uid].setdefault("reputation", int(row["reputation_total"] or 0))

            cur.execute(
                """
                SELECT user_id, COALESCE(current_count, 0) AS streak
                FROM user_streaks
                WHERE guild_id=? AND streak_type='message'
                """,
                (str(guild_id),),
            )
            for row in cur.fetchall():
                uid = str(row["user_id"])
                if uid in by_user:
                    by_user[uid]["streak"] = int(row["streak"] or 0)

            normalized = []
            for uid, data in by_user.items():
                normalized.append(
                    {
                        "user_id": uid,
                        "username": str(data.get("username", uid)),
                        "user_discriminator": str(data.get("user_discriminator", "0")),
                        "avatar_url": str(data.get("avatar_url", "")),
                        "xp": int(data.get("xp", 0) or 0),
                        "messages": int(data.get("messages", 0) or 0),
                        "words": int(data.get("words", 0) or 0),
                        "reputation": int(data.get("reputation", 0) or 0),
                        "level": int(data.get("level", 0) or 0),
                        "streak": int(data.get("streak", 0) or 0),
                    }
                )
            return normalized
        finally:
            conn.close()

    @staticmethod
    def _apply_search(rows: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
        q = (search or "").strip().lower()
        if not q:
            return rows
        filtered = []
        for row in rows:
            user_id = str(row.get("user_id", ""))
            username = str(row.get("username", ""))
            discrim = str(row.get("user_discriminator", "0"))
            tag = f"{username}#{discrim}" if discrim and discrim != "0" else username
            haystack = f"{user_id} {username} {tag}".lower()
            if q in haystack:
                filtered.append(row)
        return filtered

    def get_rankings(
        self,
        guild_id: str,
        period: str = "all",
        metric: str = "xp",
        limit: int = 25,
        search: str = "",
    ) -> List[Dict[str, Any]]:
        guild_id = str(guild_id)
        period_norm = self._normalize_period(period)
        metric_norm = self._normalize_metric(metric)
        limit = max(1, min(int(limit or 25), 100))

        if period_norm == "all":
            rows = self._fetch_all_time_rows(guild_id)
        else:
            rows = self._fetch_window_rows(guild_id, self._period_start_ts(period_norm))

        cleaned: List[Dict[str, Any]] = []
        for row in rows:
            username = str(row.get("username", row.get("user_id", "Unknown")))
            discrim = str(row.get("user_discriminator", "0"))
            user_tag = f"{username}#{discrim}" if discrim and discrim != "0" else username
            cleaned.append(
                {
                    "user_id": str(row.get("user_id", "")),
                    "username": username,
                    "user_discriminator": discrim,
                    "user_tag": user_tag,
                    "avatar_url": str(row.get("avatar_url", "")),
                    "xp": int(row.get("xp", 0) or 0),
                    "messages": int(row.get("messages", 0) or 0),
                    "words": int(row.get("words", 0) or 0),
                    "reputation": int(row.get("reputation", 0) or 0),
                    "level": int(row.get("level", 0) or 0),
                    "streak": int(row.get("streak", 0) or 0),
                    "period": period_norm,
                }
            )

        cleaned = self._apply_search(cleaned, search)
        cleaned.sort(
            key=lambda r: (
                int(r.get(metric_norm, 0) or 0),
                int(r.get("xp", 0) or 0),
                int(r.get("messages", 0) or 0),
                -int(r.get("user_id", "0") if str(r.get("user_id", "")).isdigit() else 0),
            ),
            reverse=True,
        )

        output: List[Dict[str, Any]] = []
        for idx, row in enumerate(cleaned[:limit], start=1):
            row_out = dict(row)
            row_out["rank"] = idx
            row_out["metric"] = metric_norm
            row_out["metric_value"] = int(row_out.get(metric_norm, 0) or 0)
            row_out["generated_at"] = int(time.time())
            output.append(row_out)
        return output

