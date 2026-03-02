import json
import re
import time
from typing import Any, Dict, List, Optional, Tuple


class ModerationProService:
    """Rule manager + message triage for Pro moderation."""

    _ACTION_PRIORITY = {
        "delete": 100,
        "timeout": 90,
        "mute": 80,
        "kick": 70,
        "ban": 60,
        "warn": 40,
        "flag": 30,
        "allow": 0,
    }

    _TOXIC_TERMS = {
        "kys": 0.65,
        "kill yourself": 0.65,
        "retard": 0.40,
        "idiot": 0.20,
        "moron": 0.20,
        "stupid": 0.20,
        "hate you": 0.30,
        "loser": 0.20,
        "trash": 0.20,
    }

    def __init__(self, msg_db, db_manager=None):
        self.msg_db = msg_db
        self.db_manager = db_manager
        self._ensure_action_table()

    def _ensure_action_table(self) -> None:
        conn = self.msg_db.get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS moderation_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id TEXT,
                    rule_id INTEGER,
                    message_id TEXT,
                    actor_id TEXT,
                    target_user_id TEXT,
                    action TEXT,
                    reason TEXT,
                    metadata_json TEXT,
                    created_at REAL
                )
                """
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_mod_actions_guild ON moderation_actions(guild_id, created_at)"
            )
            conn.commit()
        finally:
            conn.close()

    def add_rule(
        self,
        guild_id: str,
        rule_type: str,
        pattern: str,
        action: str,
        reason: str,
        creator_id: str,
    ) -> Optional[Dict[str, Any]]:
        guild_id = str(guild_id)
        pattern = (pattern or "").strip()
        if not pattern:
            return None

        rule_type = (rule_type or "blocklist").strip().lower()
        if rule_type not in {"regex", "blocklist", "link_filter"}:
            rule_type = "blocklist"

        action = (action or "warn").strip().lower()
        if action not in self._ACTION_PRIORITY:
            action = "warn"

        reason = (reason or "Pro moderation rule").strip()
        creator_id = str(creator_id or "system")

        try:
            if hasattr(self.msg_db, "add_mod_rule"):
                self.msg_db.add_mod_rule(guild_id, rule_type, pattern, action, reason, creator_id)
            else:
                conn = self.msg_db.get_connection()
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO moderation_rules (guild_id, type, pattern, action, reason, creator_id, enabled, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, 1, ?)
                    """,
                    (guild_id, rule_type, pattern, action, reason, creator_id, time.time()),
                )
                conn.commit()
                conn.close()
        except Exception:
            return None

        # Return the newest matching rule to make API responses deterministic.
        rules = self.get_rules(guild_id)
        for rule in reversed(rules):
            if (
                str(rule.get("type", "")).lower() == rule_type
                and str(rule.get("pattern", "")).strip() == pattern
                and str(rule.get("action", "")).lower() == action
            ):
                return rule
        return None

    def remove_rule(self, guild_id: str, rule_id: int) -> None:
        try:
            if hasattr(self.msg_db, "remove_mod_rule"):
                self.msg_db.remove_mod_rule(rule_id, str(guild_id))
                return
        except Exception:
            pass

        conn = self.msg_db.get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "UPDATE moderation_rules SET enabled=0 WHERE guild_id=? AND id=?",
                (str(guild_id), int(rule_id)),
            )
            conn.commit()
        finally:
            conn.close()

    def get_rules(self, guild_id: str) -> List[Dict[str, Any]]:
        try:
            if hasattr(self.msg_db, "get_mod_rules"):
                return self.msg_db.get_mod_rules(str(guild_id)) or []
        except Exception:
            pass

        conn = self.msg_db.get_connection()
        conn.row_factory = __import__("sqlite3").Row
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT *
                FROM moderation_rules
                WHERE guild_id=? AND COALESCE(enabled, 1)=1
                ORDER BY id ASC
                """,
                (str(guild_id),),
            )
            return [dict(r) for r in cur.fetchall()]
        finally:
            conn.close()

    def _matches_rule(self, rule: Dict[str, Any], content: str) -> Tuple[bool, str]:
        rule_type = str(rule.get("type", "blocklist")).lower()
        pattern = str(rule.get("pattern", "") or "")
        text = content or ""
        lower_text = text.lower()

        if not pattern:
            return False, ""

        if rule_type == "regex":
            try:
                match = re.search(pattern, text, re.IGNORECASE)
                return (bool(match), match.group(0) if match else "")
            except re.error:
                return False, ""

        if rule_type == "link_filter":
            urls = re.findall(r"https?://\S+", text, flags=re.IGNORECASE)
            if not urls:
                return False, ""
            # If no pattern, any link matches.
            if pattern.strip() in {"*", "any", "all"}:
                return True, urls[0]
            p = pattern.strip().lower()
            for url in urls:
                if p in url.lower():
                    return True, url
            return False, ""

        # Default blocklist behavior.
        tokens = [t.strip().lower() for t in re.split(r"[,\n;|]+", pattern) if t.strip()]
        if not tokens:
            tokens = [pattern.strip().lower()]
        for token in tokens:
            if token and token in lower_text:
                return True, token
        return False, ""

    def _toxicity_score(self, content: str) -> Dict[str, Any]:
        text = content or ""
        lower_text = text.lower()
        reasons: List[str] = []
        score = 0.0

        for term, weight in self._TOXIC_TERMS.items():
            if term in lower_text:
                count = lower_text.count(term)
                increment = min(weight * count, weight * 2)
                score += increment
                reasons.append(f"term:{term}")

        alpha_chars = [c for c in text if c.isalpha()]
        if alpha_chars:
            upper_ratio = sum(1 for c in alpha_chars if c.isupper()) / float(len(alpha_chars))
            if len(alpha_chars) >= 10 and upper_ratio >= 0.75:
                score += 0.20
                reasons.append("excessive_caps")

        if re.search(r"([!?])\1{3,}", text):
            score += 0.10
            reasons.append("punctuation_spam")

        if re.search(r"(.)\1{7,}", text):
            score += 0.10
            reasons.append("character_spam")

        score = min(1.0, round(score, 4))
        if score >= 0.75:
            band = "high"
        elif score >= 0.45:
            band = "medium"
        elif score > 0:
            band = "low"
        else:
            band = "none"
        return {"score": score, "band": band, "signals": reasons}

    def _pick_action(self, matched_rules: List[Dict[str, Any]], toxicity_score: float) -> Tuple[str, str]:
        best_action = "allow"
        best_reason = "clean"

        for match in matched_rules:
            action = str(match.get("action", "warn")).lower()
            if self._ACTION_PRIORITY.get(action, 0) > self._ACTION_PRIORITY.get(best_action, 0):
                best_action = action
                best_reason = str(match.get("reason", "rule_match"))

        if best_action == "allow":
            if toxicity_score >= 0.85:
                return "delete", "toxicity_high"
            if toxicity_score >= 0.60:
                return "warn", "toxicity_medium"
            if toxicity_score >= 0.35:
                return "flag", "toxicity_low"
        return best_action, best_reason

    def _log_action(
        self,
        guild_id: str,
        rule_id: Optional[int],
        message_id: Optional[str],
        actor_id: Optional[str],
        target_user_id: Optional[str],
        action: str,
        reason: str,
        username: Optional[str] = None,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        try:
            if hasattr(self.msg_db, "log_moderation_action"):
                self.msg_db.log_moderation_action(
                    guild_id=guild_id,
                    rule_id=rule_id,
                    message_id=message_id,
                    actor_id=actor_id,
                    target_user_id=target_user_id,
                    username=username or "Unknown",
                    content=content or "-",
                    action=action,
                    reason=reason,
                    metadata=metadata or {},
                )
                return
        except Exception as e:
            print(f"[ModerationPro] Database log error: {e}")

        conn = self.msg_db.get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO moderation_actions
                    (guild_id, rule_id, message_id, actor_id, target_user_id, username, content, action, reason, metadata_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(guild_id),
                    rule_id,
                    str(message_id) if message_id is not None else None,
                    str(actor_id) if actor_id is not None else None,
                    str(target_user_id) if target_user_id is not None else None,
                    str(username) if username is not None else "Unknown",
                    str(content) if content is not None else "-",
                    str(action or ""),
                    str(reason or ""),
                    json.dumps(metadata or {}),
                    time.time(),
                ),
            )
            conn.commit()
        finally:
            conn.close()

    def triage_message(
        self,
        guild_id: str,
        content: str,
        user_id: Optional[str] = None,
        message_id: Optional[str] = None,
        actor_id: Optional[str] = "system",
        username: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        guild_id = str(guild_id)
        text = content or ""

        rules = self.get_rules(guild_id)
        matched_rules: List[Dict[str, Any]] = []
        for rule in rules:
            matched, matched_text = self._matches_rule(rule, text)
            if not matched:
                continue
            matched_rules.append(
                {
                    "id": rule.get("id"),
                    "type": str(rule.get("type", "")),
                    "action": str(rule.get("action", "warn")).lower(),
                    "reason": str(rule.get("reason", "rule_match")),
                    "pattern": str(rule.get("pattern", "")),
                    "matched_text": matched_text,
                }
            )

        tox = self._toxicity_score(text)
        action, reason = self._pick_action(matched_rules, tox["score"])
        
        # Merge passed metadata with triage results
        log_metadata = {"toxicity": tox, "matched_rules": matched_rules}
        if metadata:
            log_metadata.update(metadata)

        result = {
            "guild_id": guild_id,
            "message_id": str(message_id) if message_id is not None else None,
            "user_id": str(user_id) if user_id is not None else None,
            "username": username,
            "content": text,
            "matched": bool(matched_rules),
            "action": action,
            "reason": reason,
            "matched_rules": matched_rules,
            "toxicity": tox,
            "metadata": log_metadata,
            "timestamp": time.time(),
        }

        if action != "allow" or matched_rules or tox["score"] >= 0.35:
            top_rule_id = matched_rules[0]["id"] if matched_rules else None
            # Ensure we don't log None for required display fields
            safe_username = username or "Unknown"
            safe_content = text or "-"
            
            self._log_action(
                guild_id=guild_id,
                rule_id=top_rule_id,
                message_id=message_id,
                actor_id=actor_id,
                target_user_id=user_id,
                username=safe_username,
                content=safe_content,
                action=action,
                reason=reason,
                metadata=log_metadata,
            )

        return result

    def get_recent_actions(self, guild_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        limit = max(1, min(int(limit or 20), 200))
        try:
            if hasattr(self.msg_db, "get_moderation_actions"):
                return self.msg_db.get_moderation_actions(str(guild_id), limit=limit) or []
        except Exception:
            pass

        conn = self.msg_db.get_connection()
        conn.row_factory = __import__("sqlite3").Row
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT *
                FROM moderation_actions
                WHERE guild_id=?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (str(guild_id), limit),
            )
            rows = [dict(r) for r in cur.fetchall()]
            for row in rows:
                raw = row.get("metadata_json")
                if isinstance(raw, str):
                    try:
                        row["metadata"] = json.loads(raw)
                    except Exception:
                        row["metadata"] = {}
            return rows
        finally:
            conn.close()

