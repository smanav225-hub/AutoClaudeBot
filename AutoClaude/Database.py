import json
import os
import httpx
import asyncio
from typing import Dict, List, Optional

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "data.db")
TOKEN_FILE = os.path.join(BASE_DIR, "Token.txt")
DISCORD_API_URL = "https://discord.com/api/v10"

def load_token() -> str:
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                data = json.load(f)
                return data.get("token", "") or ""
            except:
                pass
    return ""

class Database:
    def __init__(self):
        self.token = load_token()
        self.headers = self._build_headers(self.token)
        self.data = self._load_db()

    @staticmethod
    def _build_headers(token: str) -> Dict[str, str]:
        token = (token or "").strip()
        if not token:
            return {}
        return {"Authorization": f"Bot {token}"}

    def _load_db(self) -> Dict:
        # Ensure default structure
        default_db = {
            "token": "",
            "settings": {
                "hi_emoji": "👋",
                "hi_enabled": False,
                "github_token": "",
                "commands_analytics": {
                    "enabled": False,
                    "role_ids": []
                },
                "commands_github": {
                    "enabled": False,
                    "role_ids": []
                },
                "commands_level": {
                    "enabled": False,
                    "role_ids": []
                },
                "commands_leaderboard": {
                    "enabled": False,
                    "role_ids": []
                }
            },
            "recent_dm": {},
            "last_server": None,
            "servers": {}
        }
        
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as f:
                try:
                    data = json.load(f)
                    # Merge with default to ensure keys exist
                    if "token" not in data: data["token"] = ""
                    if "settings" not in data:
                        data["settings"] = {
                            "hi_emoji": "👋",
                            "hi_enabled": False,
                            "commands_analytics": {"enabled": False, "role_ids": []},
                            "commands_github": {"enabled": False, "role_ids": []}
                        }
                    
                    # Ensure specific hi-emoji keys exist within settings
                    if "hi_emoji" not in data["settings"]:
                        data["settings"]["hi_emoji"] = "👋"
                    if "hi_enabled" not in data["settings"]:
                        data["settings"]["hi_enabled"] = False
                    if "commands_analytics" not in data["settings"]:
                        data["settings"]["commands_analytics"] = {"enabled": False, "role_ids": []}
                    if "commands_github" not in data["settings"]:
                        data["settings"]["commands_github"] = {"enabled": False, "role_ids": []}
                    if "commands_level" not in data["settings"]:
                        data["settings"]["commands_level"] = {"enabled": False, "role_ids": []}
                    if "commands_leaderboard" not in data["settings"]:
                        data["settings"]["commands_leaderboard"] = {"enabled": False, "role_ids": []}
                    if "recent_dm" not in data:
                        data["recent_dm"] = {}
                    if "servers" not in data: data["servers"] = {}
                    if "last_server" not in data: data["last_server"] = None
                    return data
                except:
                    pass
        return default_db

    def save_db(self):
        with open(DB_FILE, "w") as f:
            ordered = {
                "token": self.data.get("token", ""),
                "settings": self.data.get("settings", {
                    "hi_emoji": "👋",
                    "hi_enabled": False,
                    "commands_analytics": {"enabled": False, "role_ids": []},
                    "commands_github": {"enabled": False, "role_ids": []},
                    "commands_level": {"enabled": False, "role_ids": []},
                "commands_leaderboard": {"enabled": False, "role_ids": []}
                }),
                "recent_dm": self.data.get("recent_dm", {}),
                "last_server": self.data.get("last_server"),
                "servers": self.data.get("servers", {})
            }
            for key, value in self.data.items():
                if key not in ordered:
                    ordered[key] = value
            json.dump(ordered, f, indent=4)

    async def get_servers(self) -> List[Dict]:
        if not self.token:
            return []
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{DISCORD_API_URL}/users/@me/guilds", headers=self.headers)
            if resp.status_code == 200:
                guilds = resp.json()
                # Fetch detailed counts for each guild (optional optimization: cache this or do it lazy)
                # For now, we do it here to populate member counts in UI
                tasks = [self._fetch_guild_details(client, g) for g in guilds]
                return await asyncio.gather(*tasks)
        return []

    async def _fetch_guild_details(self, client, guild) -> Dict:
        # We need member count, which requires fetching the specific guild endpoint
        resp = await client.get(f"{DISCORD_API_URL}/guilds/{guild['id']}?with_counts=true", headers=self.headers)
        if resp.status_code == 200:
            data = resp.json()
            guild['member_count'] = data.get('approximate_member_count', 0)
        else:
            guild['member_count'] = "N/A"
            
        if guild.get('icon'):
            guild['icon'] = f"https://cdn.discordapp.com/icons/{guild['id']}/{guild['icon']}.png"
        
        return guild

    async def get_guild_payload(self, guild_id: str) -> Dict:
        if not self.token:
            return {"success": False, "error": "token_missing", "guild": {}, "channels": [], "roles": []}
        async with httpx.AsyncClient() as client:
            # Parallel fetching for speed
            g_task = client.get(f"{DISCORD_API_URL}/guilds/{guild_id}?with_counts=true", headers=self.headers)
            c_task = client.get(f"{DISCORD_API_URL}/guilds/{guild_id}/channels", headers=self.headers)
            r_task = client.get(f"{DISCORD_API_URL}/guilds/{guild_id}/roles", headers=self.headers)
            
            responses = await asyncio.gather(g_task, c_task, r_task)
            
            payload = {"success": False}
            if responses[0].status_code == 200:
                payload["success"] = True
                payload["guild"] = responses[0].json()
                # Filter for text channels (type 0)
                payload["channels"] = [c for c in responses[1].json() if c.get('type') == 0] if responses[1].status_code == 200 else []
                payload["roles"] = responses[2].json() if responses[2].status_code == 200 else []
                
                # Fix icon URL
                if payload["guild"].get("icon"):
                    payload["guild"]["icon_url"] = f"https://cdn.discordapp.com/icons/{guild_id}/{payload['guild']['icon']}.png"
            
            return payload

    async def get_channels(self, server_id: str) -> List[Dict]:
        if not self.token:
            return []
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{DISCORD_API_URL}/guilds/{server_id}/channels", headers=self.headers)
            if resp.status_code == 200:
                # Return only text channels
                return [c for c in resp.json() if c.get('type') == 0]
        return []

    def get_config(self, server_id: str, feature: str) -> Optional[Dict]:
        # Always read latest data.db so join/dm/leave use persisted state
        try:
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r") as f:
                    self.data = json.load(f)
        except Exception:
            pass
        cfg = self.data.get("servers", {}).get(server_id, {}).get(feature)
        if feature in ("join", "dm") and isinstance(cfg, dict):
            return self._normalize_join_dm_config(cfg)
        return cfg

    def save_config(self, server_id: str, feature: str, config: Dict):
        if server_id not in self.data["servers"]:
            self.data["servers"][server_id] = {}
        if feature in ("join", "dm") and isinstance(config, dict):
            config = self._normalize_join_dm_config(config)
        self.data["servers"][server_id][feature] = config
        self.save_db()

    def _normalize_join_dm_config(self, config: Dict) -> Dict:
        # Normalize join/dm config so card+mode+type stay consistent
        if not isinstance(config, dict):
            return {}
        out = dict(config)
        card = out.get("card")
        if not isinstance(card, dict):
            card = {}
        # Preserve card.enabled if set; otherwise derive from mode
        card_enabled = bool(card.get("enabled"))
        if out.get("mode") == "card":
            card_enabled = True
        card["enabled"] = card_enabled
        out["card"] = card

        msg_type = out.get("type") or out.get("mode") or "text"
        if msg_type not in ("text", "embed"):
            msg_type = "text"
        out["type"] = msg_type

        if card_enabled:
            out["mode"] = "card"
        elif msg_type == "embed":
            out["mode"] = "embed"
        else:
            out["mode"] = "text"
        return out

    def get_scheduled_announcements(self, server_id: str) -> List[Dict]:
        return self.data["servers"].get(server_id, {}).get("scheduled_announcements", [])

    def save_scheduled_announcement(self, server_id: str, announcement: Dict):
        if server_id not in self.data["servers"]:
            self.data["servers"][server_id] = {}
        if "scheduled_announcements" not in self.data["servers"][server_id]:
            self.data["servers"][server_id]["scheduled_announcements"] = []

        announcements = self.data["servers"][server_id]["scheduled_announcements"]
        ann_id = announcement.get("id")
        if ann_id:
            for i, ann in enumerate(announcements):
                if ann.get("id") == ann_id:
                    announcements[i] = announcement
                    self.save_db()
                    return
        announcements.append(announcement)
        self.save_db()

    def delete_scheduled_announcement(self, server_id: str, announcement_id: str):
        if server_id in self.data["servers"]:
            announcements = self.data["servers"][server_id].get("scheduled_announcements", [])
            self.data["servers"][server_id]["scheduled_announcements"] = [
                a for a in announcements if a.get("id") != announcement_id
            ]
            self.save_db()

    def set_last_server(self, server_id: str):
        self.data["last_server"] = server_id
        self.save_db()

    def get_last_server(self) -> Optional[str]:
        return self.data.get("last_server")

    def get_settings(self) -> Dict:
        # Refresh from disk to ensure we have the latest settings across processes
        try:
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r") as f:
                    self.data = json.load(f)
        except Exception:
            pass
        
        settings = self.data.get("settings", {})
        if "hi_emoji" not in settings: settings["hi_emoji"] = "👋"
        if "hi_enabled" not in settings: settings["hi_enabled"] = False
        return settings

    def save_settings(self, settings: Dict):
        if "settings" not in self.data:
            self.data["settings"] = {"hi_emoji": "👋", "hi_enabled": False}
        self.data["settings"].update(settings or {})
        self.save_db()

    def get_token(self) -> str:
        return self.data.get("token", "")

    def set_token(self, token: str):
        self.data["token"] = token or ""
        self.save_db()
        self.token = self.data["token"]
        self.headers = self._build_headers(self.token)

    def get_github_token(self) -> str:
        return self.data.get("settings", {}).get("github_token", "")

    def set_github_token(self, token: str):
        if "settings" not in self.data:
            self.data["settings"] = {}
        self.data["settings"]["github_token"] = token or ""
        self.save_db()

    def get_recent_dm_ts(self, guild_id: str, user_id: str) -> float:
        # Refresh from disk to reduce duplicate DMs across multiple processes
        try:
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r") as f:
                    data = json.load(f)
                    if "recent_dm" in data:
                        self.data["recent_dm"] = data.get("recent_dm", {})
        except Exception:
            pass
        recent = self.data.get("recent_dm", {})
        return float(recent.get(guild_id, {}).get(user_id, 0) or 0)

    def set_recent_dm_ts(self, guild_id: str, user_id: str, ts: float):
        if "recent_dm" not in self.data:
            self.data["recent_dm"] = {}
        if guild_id not in self.data["recent_dm"]:
            self.data["recent_dm"][guild_id] = {}
        if len(self.data["recent_dm"][guild_id]) > 5000:
            self.data["recent_dm"][guild_id] = {}
        self.data["recent_dm"][guild_id][user_id] = float(ts)
        self.save_db()

class ReactionRoleDB:
    """
    Helper class to structure Reaction Role configuration data
    before saving it to the main database.
    """
    def __init__(self, db_manager: Database):
        self.db = db_manager

    def format_payload(self, raw_data: Dict) -> Dict:
        # Ensure the payload structure matches our requirements
        msg = raw_data.get("message", {})
        embed = msg.get("embed", {}) if isinstance(msg, dict) else {}
        
        # Handle case where message might already be in the correct format
        if "embed" not in msg and any(k in msg for k in ["title", "description", "color", "fields"]):
            # Message data is flat, wrap it in embed
            embed = {
                "title": msg.get("title", ""),
                "description": msg.get("description", ""),
                "color": msg.get("color", "#ffffff"),
                "fields": msg.get("fields", []),
                "footer": msg.get("footer", {}),
                "author": msg.get("author", {}),
                "thumbnail": msg.get("thumbnail", ""),
                "image": msg.get("image", "")
            }
            content = msg.get("content", "")
        else:
            # Message data has proper structure
            content = msg.get("content", "")
        
        return {
            "channel_id": raw_data.get("channel"),
            "channel_name": raw_data.get("channel_name"),
            "mode": raw_data.get("mode", "default"),
            "message": {
                "content": content,
                "embed": embed
            },
            "reaction_config": {
                "type": raw_data.get("reaction_config", {}).get("type", "emoji"), # emoji or dropdown
                "allow_multiple": raw_data.get("reaction_config", {}).get("allow_multiple", True),
                "emoji_rows": raw_data.get("reaction_config", {}).get("emoji_rows", []),
                "dropdown_rows": raw_data.get("reaction_config", {}).get("dropdown_rows", []),
                "dropdown_placeholder": raw_data.get("reaction_config", {}).get("dropdown_placeholder", "")
            }
        }

db_manager = Database()
rr_db = ReactionRoleDB(db_manager)
