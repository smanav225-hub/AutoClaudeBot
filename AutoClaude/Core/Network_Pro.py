import json
import re
import time
from collections import defaultdict
from typing import Any, Dict, List, Set, Tuple


class NetworkProService:
    """Builds an interaction graph from mentions + reputation events."""

    def __init__(self, msg_db):
        self.msg_db = msg_db

    @staticmethod
    def _parse_mentioned_users(raw: Any, content: str) -> List[str]:
        users: Set[str] = set()
        if isinstance(raw, list):
            users.update(str(u) for u in raw if u is not None)
        elif isinstance(raw, str) and raw.strip():
            try:
                decoded = json.loads(raw)
                if isinstance(decoded, list):
                    users.update(str(u) for u in decoded if u is not None)
            except Exception:
                pass

        for match in re.findall(r"<@!?(\d+)>", content or ""):
            users.add(str(match))
        return [u for u in users if u]

    def _load_recent_messages(self, guild_id: str, since_ts: float, limit: int) -> List[Dict[str, Any]]:
        conn = self.msg_db.get_connection()
        conn.row_factory = __import__("sqlite3").Row
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT message_id, user_id, username, user_discriminator, content,
                       mentioned_users, reply_to_user_id, created_at
                FROM messages
                WHERE guild_id=? AND created_at >= ? AND COALESCE(is_deleted, 0)=0
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (str(guild_id), float(since_ts), int(limit)),
            )
            return [dict(r) for r in cur.fetchall()]
        finally:
            conn.close()

    def _load_recent_reputation(self, guild_id: str, since_ts: float) -> List[Dict[str, Any]]:
        conn = self.msg_db.get_connection()
        conn.row_factory = __import__("sqlite3").Row
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT giver_id, receiver_id, created_at
                FROM reputation_events
                WHERE guild_id=? AND created_at >= ?
                ORDER BY created_at DESC
                """,
                (str(guild_id), float(since_ts)),
            )
            return [dict(r) for r in cur.fetchall()]
        finally:
            conn.close()

    def _load_known_usernames(self, guild_id: str) -> Dict[str, str]:
        conn = self.msg_db.get_connection()
        conn.row_factory = __import__("sqlite3").Row
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT user_id, COALESCE(username, user_id) AS username
                FROM user_levels
                WHERE guild_id=?
                """,
                (str(guild_id),),
            )
            return {str(r["user_id"]): str(r["username"]) for r in cur.fetchall()}
        finally:
            conn.close()

    def build_graph(self, guild_id: str, hours: int = 72, limit: int = 80) -> Dict[str, Any]:
        guild_id = str(guild_id)
        hours = max(1, min(int(hours or 72), 720))
        limit = max(5, min(int(limit or 80), 250))
        now_ts = time.time()
        since_ts = now_ts - (hours * 3600)

        messages = self._load_recent_messages(guild_id, since_ts=since_ts, limit=limit * 25)
        rep_events = self._load_recent_reputation(guild_id, since_ts=since_ts)
        name_map = self._load_known_usernames(guild_id)

        node_stats: Dict[str, Dict[str, Any]] = {}
        edge_stats: Dict[Tuple[str, str], Dict[str, Any]] = defaultdict(
            lambda: {
                "source": "",
                "target": "",
                "mention_count": 0,
                "reputation_count": 0,
                "weight": 0.0,
                "last_event_at": 0.0,
            }
        )

        def ensure_node(user_id: str, fallback_name: str = "") -> Dict[str, Any]:
            uid = str(user_id)
            if uid not in node_stats:
                node_stats[uid] = {
                    "id": uid,
                    "username": fallback_name or name_map.get(uid, f"User {uid}"),
                    "message_count": 0,
                    "sent_mentions": 0,
                    "received_mentions": 0,
                    "reputation_given": 0,
                    "reputation_received": 0,
                    "activity_score": 0.0,
                    "last_seen_at": 0.0,
                }
            return node_stats[uid]

        for msg in messages:
            src = str(msg.get("user_id", "") or "")
            if not src:
                continue
            src_node = ensure_node(src, fallback_name=str(msg.get("username", "")))
            src_node["message_count"] += 1
            src_node["last_seen_at"] = max(float(msg.get("created_at", 0) or 0), float(src_node["last_seen_at"]))

            # 1. Check for True Replies
            reply_tgt = str(msg.get("reply_to_user_id", "") or "")
            if reply_tgt and reply_tgt != src:
                ensure_node(reply_tgt)
                src_node["sent_replies"] = src_node.get("sent_replies", 0) + 1
                edge = edge_stats[(src, reply_tgt)]
                edge["source"] = src
                edge["target"] = reply_tgt
                edge["type"] = "reply"
                edge["reply_count"] = edge.get("reply_count", 0) + 1
                edge["weight"] += 2.0  # Replies carry high weight
                edge["last_event_at"] = max(float(edge.get("last_event_at", 0)), float(msg.get("created_at", 0) or 0))

            # 2. Check for Mentions
            mentioned = self._parse_mentioned_users(msg.get("mentioned_users"), msg.get("content", ""))
            unique_targets = {u for u in mentioned if u and u != src and u != reply_tgt}
            src_node["sent_mentions"] += len(unique_targets)

            for tgt in unique_targets:
                tgt_node = ensure_node(tgt)
                tgt_node["received_mentions"] += 1

                edge = edge_stats[(src, tgt)]
                edge["source"] = src
                edge["target"] = tgt
                edge["type"] = "mention"
                edge["mention_count"] = edge.get("mention_count", 0) + 1
                edge["weight"] += 1.0
                edge["last_event_at"] = max(
                    float(edge.get("last_event_at", 0)),
                    float(msg.get("created_at", 0) or 0),
                )

        for rep in rep_events:
            giver = str(rep.get("giver_id", "") or "")
            receiver = str(rep.get("receiver_id", "") or "")
            if not giver or not receiver or giver == receiver:
                continue

            giver_node = ensure_node(giver)
            receiver_node = ensure_node(receiver)
            giver_node["reputation_given"] += 1
            receiver_node["reputation_received"] += 1

            edge = edge_stats[(giver, receiver)]
            edge["source"] = giver
            edge["target"] = receiver
            edge["type"] = "thank"
            edge["reputation_count"] += 1
            edge["weight"] += 2.0
            edge["last_event_at"] = max(float(edge["last_event_at"]), float(rep.get("created_at", 0) or 0))

        for node in node_stats.values():
            node["activity_score"] = round(
                float(node["message_count"])
                + (2.0 * float(node.get("sent_replies", 0)))
                + (1.0 * float(node["sent_mentions"]))
                + (1.25 * float(node["received_mentions"]))
                + (1.5 * float(node["reputation_given"]))
                + (2.0 * float(node["reputation_received"])),
                3,
            )

        nodes = sorted(
            node_stats.values(),
            key=lambda n: (float(n.get("activity_score", 0.0)), float(n.get("last_seen_at", 0.0))),
            reverse=True,
        )
        nodes = nodes[: max(limit * 2, 20)]
        visible_ids = {n["id"] for n in nodes}

        edges = []
        for e in edge_stats.values():
            sid = e.get("source")
            tid = e.get("target")
            if sid in visible_ids and tid in visible_ids:
                e["source_name"] = node_stats[sid]["username"]
                e["target_name"] = node_stats[tid]["username"]
                edges.append(e)

        edges.sort(
            key=lambda e: (
                float(e.get("weight", 0.0)),
                int(e.get("mention_count", 0)),
                int(e.get("reputation_count", 0)),
                float(e.get("last_event_at", 0.0)),
            ),
            reverse=True,
        )
        edges = edges[:limit]

        return {
            "guild_id": guild_id,
            "window_hours": hours,
            "from_ts": float(since_ts),
            "to_ts": float(now_ts),
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "node_count": len(nodes),
                "edge_count": len(edges),
                "message_events": len(messages),
                "reputation_events": len(rep_events),
            },
        }

