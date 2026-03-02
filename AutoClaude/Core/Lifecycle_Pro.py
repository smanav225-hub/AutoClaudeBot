import asyncio
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None


class LifecycleProManager:
    """
    Pro lifecycle scheduler:
    - Auto-unban / auto-unmute expired punishments
    - Hourly health rollups
    - Midnight weekly/monthly XP resets (config-driven)
    """

    def __init__(self, db_manager, msg_db, bot_client=None, poll_interval_seconds: int = 30):
        self.db = db_manager
        self.msg_db = msg_db
        self.bot = bot_client
        self.poll_interval_seconds = max(10, int(poll_interval_seconds))
        self._task: Optional[asyncio.Task] = None
        self._last_global_hour_bucket: Optional[int] = None

    async def start(self) -> None:
        if self._task and not self._task.done():
            return
        self._task = asyncio.create_task(self._loop(), name="lifecycle-pro-loop")
        print("[LifecyclePro] Started lifecycle loop.")

    async def stop(self) -> None:
        if not self._task:
            return
        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass
        finally:
            self._task = None
        print("[LifecyclePro] Stopped lifecycle loop.")

    async def _loop(self) -> None:
        while True:
            try:
                await self.run_once()
            except Exception as exc:
                print(f"[LifecyclePro] Loop error: {exc}")
            await asyncio.sleep(self.poll_interval_seconds)

    async def run_once(self, now_ts: Optional[float] = None) -> Dict[str, Any]:
        now = float(now_ts or time.time())
        guild_ids = self.msg_db.get_guild_ids() if hasattr(self.msg_db, "get_guild_ids") else []
        unban_count = await self._process_expired_punishments(now)
        rollup_count = self._run_hourly_rollups(guild_ids, now)
        reset_count = self._run_midnight_resets(guild_ids, now)
        return {
            "timestamp": now,
            "guild_count": len(guild_ids),
            "expired_processed": unban_count,
            "rollups_computed": rollup_count,
            "resets_applied": reset_count,
        }

    async def _process_expired_punishments(self, now_ts: float) -> int:
        if not hasattr(self.msg_db, "get_expired_punishments"):
            return 0

        expired = self.msg_db.get_expired_punishments(now_ts)
        processed = 0
        for record in expired:
            guild_id = str(record.get("guild_id", ""))
            user_id = str(record.get("user_id", ""))
            p_type = str(record.get("type", "")).lower()
            p_id = record.get("id")

            try:
                if self.bot and guild_id and user_id:
                    guild = self.bot.get_guild(int(guild_id))
                    if guild:
                        uid = int(user_id)
                        if p_type == "ban":
                            user = await self.bot.fetch_user(uid)
                            await guild.unban(user, reason="Auto-unban: Punishment expired")
                        elif p_type == "mute":
                            member = guild.get_member(uid)
                            if member:
                                await member.timeout(None, reason="Auto-unmute: Punishment expired")
            except Exception as exc:
                print(f"[LifecyclePro] Failed lifting punishment {p_id}: {exc}")
            finally:
                if p_id is not None and hasattr(self.msg_db, "deactivate_punishment_by_id"):
                    try:
                        self.msg_db.deactivate_punishment_by_id(p_id)
                    except Exception:
                        pass
                processed += 1

        return processed

    def _run_hourly_rollups(self, guild_ids: List[str], now_ts: float) -> int:
        if not guild_ids or not hasattr(self.msg_db, "compute_hourly_rollup"):
            return 0

        # Compute only complete hours (not current in-progress hour).
        target_bucket = int(now_ts // 3600) * 3600 - 3600
        if target_bucket < 0:
            return 0
        if self._last_global_hour_bucket == target_bucket:
            return 0

        computed = 0
        for guild_id in guild_ids:
            last_bucket = None
            if hasattr(self.msg_db, "get_last_rollup_bucket"):
                try:
                    last_bucket = self.msg_db.get_last_rollup_bucket(guild_id)
                except Exception:
                    last_bucket = None

            if last_bucket is None:
                start_bucket = target_bucket
            else:
                start_bucket = int(float(last_bucket)) + 3600

            bucket = start_bucket
            while bucket <= target_bucket:
                try:
                    self.msg_db.compute_hourly_rollup(guild_id, bucket, bucket + 3600)
                    computed += 1
                except Exception as exc:
                    print(f"[LifecyclePro] Rollup error guild={guild_id} bucket={bucket}: {exc}")
                bucket += 3600

        self._last_global_hour_bucket = target_bucket
        return computed

    def _timezone(self, tz_name: str):
        tz_name = (tz_name or "UTC").strip()
        if ZoneInfo is None:
            return timezone.utc
        try:
            return ZoneInfo(tz_name)
        except Exception:
            return timezone.utc

    def _run_midnight_resets(self, guild_ids: List[str], now_ts: float) -> int:
        if not guild_ids:
            return 0
        if not hasattr(self.msg_db, "reset_guild_levels"):
            return 0

        resets = 0
        for guild_id in guild_ids:
            cfg = self.db.get_config(str(guild_id), "pro_lifecycle") or {}
            tz = self._timezone(cfg.get("timezone", "UTC"))
            local_now = datetime.fromtimestamp(now_ts, tz=tz)

            # Run in midnight window (00:00 - 00:04 local time)
            if local_now.hour != 0 or local_now.minute > 4:
                continue

            weekly_enabled = bool(cfg.get("weekly_reset_enabled", True))
            monthly_enabled = bool(cfg.get("monthly_reset_enabled", True))
            weekly_day = int(cfg.get("weekly_reset_day", 0))  # Monday

            today_str = local_now.date().isoformat()
            changed = False

            if weekly_enabled and local_now.weekday() == weekly_day:
                if cfg.get("last_weekly_reset") != today_str:
                    resets += self.msg_db.reset_guild_levels(str(guild_id))
                    cfg["last_weekly_reset"] = today_str
                    changed = True

            if monthly_enabled and local_now.day == 1:
                if cfg.get("last_monthly_reset") != today_str:
                    resets += self.msg_db.reset_guild_levels(str(guild_id))
                    cfg["last_monthly_reset"] = today_str
                    changed = True

            if changed:
                self.db.save_config(str(guild_id), "pro_lifecycle", cfg)

        return resets
