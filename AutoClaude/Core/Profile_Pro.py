import time
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


class ProfileProService:
    """Expanded profile payloads for pro UI with Discord API and Database integration."""

    def __init__(self, msg_db, db_manager=None):
        self.msg_db = msg_db
        self.db_manager = db_manager
        self.api_url = "https://discord.com/api/v10"

    def _get_connection(self):
        conn = self.msg_db.get_connection()
        conn.row_factory = __import__("sqlite3").Row
        return conn

    def _safe_eval(self, expr, variables):
        expr = (expr or "").replace("^", "**")
        return eval(expr, {"__builtins__": {}}, variables)

    def _xp_needed(self, level, formula="5 * (level ** 2) + (50 * level) + 100"):
        try:
            return int(self._safe_eval(formula, {"level": level}))
        except Exception:
            return 5 * (level ** 2) + (50 * level) + 100

    async def _fetch_discord_member(self, guild_id: str, user_id: str) -> Dict[str, Any]:
        """Fetch joined_at and avatar from Discord API."""
        if not self.db_manager:
            return {}
        
        token = self.db_manager.get_token()
        if not token:
            return {}

        headers = {"Authorization": f"Bot {token}"}
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                resp = await client.get(f"{self.api_url}/guilds/{guild_id}/members/{user_id}", headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    user = data.get("user", {})
                    
                    # Avatar logic: Guild avatar -> User avatar -> Default
                    avatar = data.get("avatar") or user.get("avatar")
                    avatar_url = ""
                    if avatar:
                        ext = "gif" if avatar.startswith("a_") else "png"
                        if data.get("avatar"):
                            avatar_url = f"https://cdn.discordapp.com/guilds/{guild_id}/users/{user_id}/avatars/{avatar}.{ext}"
                        else:
                            avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar}.{ext}"
                    else:
                        discrim = int(user.get("discriminator", 0))
                        avatar_url = f"https://cdn.discordapp.com/embed/avatars/{discrim % 5}.png"

                    # Role logic
                    role_ids = data.get("roles", [])
                    roles_list = []
                    try:
                        # We might need to fetch all guild roles to get names/colors
                        guild_roles_resp = await client.get(f"{self.api_url}/guilds/{guild_id}/roles", headers=headers)
                        if guild_roles_resp.status_code == 200:
                            all_guild_roles = {r["id"]: r for r in guild_roles_resp.json()}
                            for rid in role_ids:
                                if rid in all_guild_roles:
                                    r = all_guild_roles[rid]
                                    roles_list.append({
                                        "name": r["name"],
                                        "color": f"#{r['color']:06x}" if r["color"] else "#99aab5"
                                    })
                    except Exception as re:
                        print(f"[ProfilePro] Role fetch error: {re}")

                    return {
                        "joined_at": data.get("joined_at"),
                        "avatar_url": avatar_url,
                        "display_name": data.get("nick") or user.get("global_name") or user.get("username"),
                        "roles": roles_list
                    }
            except Exception as e:
                print(f"[ProfilePro] Discord API error: {e}")
        return {}

    def _query_user_level(self, guild_id: str, user_id: str) -> Dict[str, Any]:
        conn = self._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT * FROM user_levels WHERE guild_id=? AND user_id=?",
                (str(guild_id), str(user_id)),
            )
            row = cur.fetchone()
            return dict(row) if row else {}
        finally:
            conn.close()

    def _query_rank(self, guild_id: str, user_id: str) -> int:
        conn = self._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                WITH ranked AS (
                    SELECT user_id, ROW_NUMBER() OVER (ORDER BY COALESCE(xp_total, 0) DESC) AS rk
                    FROM user_levels
                    WHERE guild_id=?
                )
                SELECT rk FROM ranked WHERE user_id=?
                """,
                (str(guild_id), str(user_id)),
            )
            row = cur.fetchone()
            return int(row["rk"]) if row else 0
        finally:
            conn.close()

    def _query_heatmap(self, guild_id: str, user_id: str, days: int = 42) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        cur = conn.cursor()
        try:
            # Get actual counts
            since_ts = (datetime.utcnow() - timedelta(days=max(1, int(days)))).timestamp()
            cur.execute(
                """
                SELECT strftime('%Y-%m-%d', datetime(created_at, 'unixepoch')) AS day,
                       COUNT(*) AS count
                FROM messages
                WHERE guild_id=? AND user_id=? AND created_at >= ? AND COALESCE(is_deleted, 0)=0
                GROUP BY day
                ORDER BY day ASC
                """,
                (str(guild_id), str(user_id), since_ts),
            )
            rows = {r["day"]: r["count"] for r in cur.fetchall()}
            
            # Fill gaps for a continuous 42-day timeline
            heatmap = []
            now = datetime.utcnow()
            for i in range(days - 1, -1, -1):
                d_str = (now - timedelta(days=i)).strftime("%Y-%m-%d")
                heatmap.append({"day": d_str, "count": rows.get(d_str, 0)})
            return heatmap
        finally:
            conn.close()

    def _query_streak(self, guild_id: str, user_id: str) -> Dict[str, Any]:
        conn = self._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT current_count, best_count, last_active_day FROM user_streaks WHERE guild_id=? AND user_id=? AND streak_type='message'",
                (str(guild_id), str(user_id)),
            )
            row = cur.fetchone()
            return dict(row) if row else {"current_count": 0, "best_count": 0, "last_active_day": None}
        finally:
            conn.close()

    def _badges(self, profile: Dict[str, Any]) -> List[str]:
        badges: List[str] = []
        level = int(profile.get("level", 0) or 0)
        messages = int(profile.get("messages_total", 0) or 0)
        reputation = int(profile.get("reputation", 0) or 0)
        streak = int(profile.get("streak_current", 0) or 0)

        if level >= 50: badges.append("Elite Legend")
        elif level >= 25: badges.append("Legend Rank")
        elif level >= 10: badges.append("Level Veteran")
        
        if messages >= 5000: badges.append("Chat Master")
        elif messages >= 1000: badges.append("Message Engine")
        
        if reputation >= 50: badges.append("Community Pillar")
        elif reputation >= 20: badges.append("Trusted Contributor")
        
        if streak >= 30: badges.append("Month Streak")
        elif streak >= 7: badges.append("Weekly Streak")
        
        if not badges: badges.append("Rising Member")
        return badges

    async def get_profile(self, guild_id: str, user_id: str) -> Dict[str, Any]:
        guild_id = str(guild_id)
        user_id = str(user_id)
        
        # 1. Fetch DB data
        base = self._query_user_level(guild_id, user_id)
        rank = self._query_rank(guild_id, user_id)
        streak = self._query_streak(guild_id, user_id)
        heatmap = self._query_heatmap(guild_id, user_id, days=42)
        
        # 2. Fetch Live Discord data
        discord_data = await self._fetch_discord_member(guild_id, user_id)
        
        # 3. Calculate XP Progression
        level = int(base.get("level", 0) or 0)
        xp_current = int(base.get("xp_current", 0) or 0)
        
        # Get formula from config or default
        formula = "5 * (level ** 2) + (50 * level) + 100"
        if self.db_manager:
            config = self.db_manager.get_config(guild_id, "levels") or {}
            formula = config.get("formula", formula)
            
        xp_needed = self._xp_needed(level, formula)
        xp_progress = round(xp_current / max(1, xp_needed), 4)

        profile = {
            "id": user_id,
            "username": discord_data.get("display_name") or base.get("username") or f"User {user_id}",
            "avatar_url": discord_data.get("avatar_url") or base.get("avatar_url", ""),
            "joined_at": discord_data.get("joined_at"),
            "level": level,
            "xp_total": int(base.get("xp_total", 0) or 0),
            "xp_current": xp_current,
            "xp_to_next_level": xp_needed,
            "xp_progress": xp_progress,
            "messages_total": int(base.get("messages_total", 0) or 0),
            "reputation": int(base.get("reputation", 0) or 0),
            "rank": rank,
            "streak_current": streak.get("current_count", 0),
            "streak_best": streak.get("best_count", 0),
            "roles": discord_data.get("roles", []),
            "heatmap": heatmap,
            "badges": []
        }
        profile["badges"] = self._badges(profile)
        return profile

    def search_profiles(self, guild_id: str, query: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        guild_id = str(guild_id)
        q = (query or "").strip().lower()
        limit = max(1, min(int(limit or 20), 100))

        conn = self._get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT user_id, username, user_discriminator, avatar_url, level, xp_total, reputation, messages_total
                FROM user_levels
                WHERE guild_id=?
                ORDER BY xp_total DESC
                LIMIT 500
                """,
                (guild_id,),
            )
            rows = [dict(r) for r in cur.fetchall()]
        finally:
            conn.close()

        if q:
            rows = [
                r for r in rows
                if q in str(r.get("user_id", "")).lower()
                or q in str(r.get("username", "")).lower()
            ]

        out = []
        for row in rows[:limit]:
            out.append({
                "user_id": str(row["user_id"]),
                "username": str(row["username"]),
                "level": int(row["level"] or 0),
                "xp_total": int(row["xp_total"] or 0),
                "avatar_url": str(row["avatar_url"] or "")
            })
        return out
