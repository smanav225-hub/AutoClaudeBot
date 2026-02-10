import asyncio
import json
import uvicorn
import discord
import ast
from fastapi import FastAPI, Request, Body, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import httpx
import random
import time
from datetime import datetime
from io import BytesIO
import requests
from typing import Dict, List
from Database import db_manager, rr_db
from uuid import uuid4

# Import specialized bot clients
from Core.Welcome_Goodbye import LeaveServer, JoinServer, PrivateMessageServer, JoinRoleServer, BaseDiscordClient
from Core.Reaction_Roles import ReactionRoles
from Core.Setting import HiEmojiReactor
from Core.Commands import IntegratedCommandBot
from Core.Level import LevelServer
from Core.scheduled_announcements import (
    ScheduledAnnouncementsData,
    ScheduledAnnouncementConfig,
    ScheduledAnnouncementSender
)
from Message_Database import MessageDBHandler, MessageLoggerClient

msg_db = MessageDBHandler()
msg_logger_instance = None
clients = []

app = FastAPI()

# Normalize emoji strings (fix common mojibake like "ðŸ‘‹" -> "👋")
def _normalize_emoji(value: str, fallback: str = "👋") -> str:
    if not isinstance(value, str):
        return fallback
    cleaned = value.strip()
    if not cleaned:
        return fallback
    try:
        repaired = cleaned.encode("latin-1").decode("utf-8")
        if repaired:
            return repaired
    except UnicodeError:
        pass
    return cleaned

# Absolute path to the directory containing this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "Database")
IMAGES_DIR = os.path.join(DATABASE_DIR, "Images")
os.makedirs(IMAGES_DIR, exist_ok=True)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global storage for the currently active server context to avoid re-fetching
active_context = {
    "guild_id": None,
    "data": None
}

# API ENDPOINTS
@app.get("/")
async def get_index():
    path = os.path.join(BASE_DIR, "GUI.html")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return JSONResponse({"error": "GUI.html not found"}, status_code=404)

@app.get("/gui/welcome-goodbye")
async def get_welcome_goodbye():
    path = os.path.join(BASE_DIR, "GUI", "Welcome_Goodbye.html")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return JSONResponse({"error": "Welcome_Goodbye.html not found"}, status_code=404)

@app.get("/gui/reaction-roles")
async def get_reaction_roles():
    path = os.path.join(BASE_DIR, "GUI", "Reaction_Roles.html")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return JSONResponse({"error": "Reaction_Roles.html not found"}, status_code=404)

@app.get("/gui/scheduled-announcement")
async def get_scheduled_announcement():
    path = os.path.join(BASE_DIR, "GUI", "Scheduled_Announcement.html")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return JSONResponse({"error": "Scheduled_Announcement.html not found"}, status_code=404)

# Serve static JS/CSS files from the GUI folder
app.mount("/gui", StaticFiles(directory=os.path.join(BASE_DIR, "GUI")), name="gui")
# Mount the Welcome_Goodbye directory as well for script loading
app.mount("/Welcome_Goodbye", StaticFiles(directory=os.path.join(BASE_DIR, "GUI", "Welcome_Goodbye")), name="gui_components")
# Serve saved images
app.mount("/database/images", StaticFiles(directory=IMAGES_DIR), name="db_images")

@app.get("/api/servers")
async def get_servers():
    servers = await db_manager.get_servers()
    last_server = db_manager.get_last_server()
    return {"success": True, "servers": servers, "last_server": last_server}

@app.get("/api/settings/token")
async def get_settings_token():
    return {"success": True, "token": db_manager.get_token()}

@app.post("/api/settings/token")
async def save_settings_token(payload: Dict = Body(...)):
    token = (payload or {}).get("token", "")
    db_manager.set_token(token)
    return {"success": True}

@app.get("/api/settings/github-token")
async def get_github_token():
    return {"success": True, "token": db_manager.get_github_token()}

@app.post("/api/settings/github-token")
async def save_github_token(payload: Dict = Body(...)):
    token = (payload or {}).get("token", "")
    db_manager.set_github_token(token)
    if command_bot_instance:
        try:
            asyncio.create_task(command_bot_instance.refresh_permissions())
        except Exception:
            pass
    return {"success": True}

@app.get("/api/settings/hi-emoji")
async def get_hi_emoji_settings():
    settings = db_manager.get_settings()
    return {
        "success": True,
        "emoji": _normalize_emoji(settings.get("hi_emoji", "👋")),
        "enabled": bool(settings.get("hi_enabled", False))
    }

@app.post("/api/settings/hi-emoji")
async def save_hi_emoji_settings(payload: Dict = Body(...)):
    emoji = _normalize_emoji((payload or {}).get("emoji", "👋"))
    enabled = bool((payload or {}).get("enabled", False))
    db_manager.save_settings({"hi_emoji": emoji, "hi_enabled": enabled})
    return {"success": True}

@app.get("/api/settings/commands-analytics")
async def get_commands_analytics_settings():
    settings = db_manager.get_settings()
    cfg = settings.get("commands_analytics", {})
    return {
        "success": True,
        "enabled": bool(cfg.get("enabled", False)),
        "role_ids": cfg.get("role_ids", [])
    }

@app.post("/api/settings/commands-analytics")
async def save_commands_analytics_settings(payload: Dict = Body(...)):
    enabled = bool((payload or {}).get("enabled", False))
    role_ids = (payload or {}).get("role_ids", [])
    if not isinstance(role_ids, list):
        role_ids = []
    db_manager.save_settings({"commands_analytics": {"enabled": enabled, "role_ids": role_ids}})
    if command_bot_instance:
        try:
            asyncio.create_task(command_bot_instance.refresh_permissions())
        except Exception:
            pass
    return {"success": True}

@app.get("/api/settings/commands-level")
async def get_commands_level_settings():
    settings = db_manager.get_settings()
    cfg = settings.get("commands_level", {})
    return {
        "success": True,
        "enabled": bool(cfg.get("enabled", False)),
        "role_ids": cfg.get("role_ids", [])
    }

@app.post("/api/settings/commands-level")
async def save_commands_level_settings(payload: Dict = Body(...)):
    enabled = bool((payload or {}).get("enabled", False))
    role_ids = (payload or {}).get("role_ids", [])
    if not isinstance(role_ids, list):
        role_ids = []
    db_manager.save_settings({"commands_level": {"enabled": enabled, "role_ids": role_ids}})
    if command_bot_instance:
        try:
            asyncio.create_task(command_bot_instance.refresh_permissions())
        except Exception:
            pass
    return {"success": True}

@app.get("/api/settings/commands-leaderboard")
async def get_commands_leaderboard_settings():
    settings = db_manager.get_settings()
    cfg = settings.get("commands_leaderboard", {})
    return {
        "success": True,
        "enabled": bool(cfg.get("enabled", False)),
        "role_ids": cfg.get("role_ids", [])
    }

@app.post("/api/settings/commands-leaderboard")
async def save_commands_leaderboard_settings(payload: Dict = Body(...)):
    enabled = bool((payload or {}).get("enabled", False))
    role_ids = (payload or {}).get("role_ids", [])
    if not isinstance(role_ids, list):
        role_ids = []
    db_manager.save_settings({"commands_leaderboard": {"enabled": enabled, "role_ids": role_ids}})
    if command_bot_instance:
        try:
            asyncio.create_task(command_bot_instance.refresh_permissions())
        except Exception:
            pass
    return {"success": True}

@app.get("/api/settings/commands-github")
async def get_commands_github_settings():
    settings = db_manager.get_settings()
    cfg = settings.get("commands_github", {})
    return {
        "success": True,
        "enabled": bool(cfg.get("enabled", False)),
        "role_ids": cfg.get("role_ids", [])
    }

@app.post("/api/settings/commands-github")
async def save_commands_github_settings(payload: Dict = Body(...)):
    enabled = bool((payload or {}).get("enabled", False))
    role_ids = (payload or {}).get("role_ids", [])
    if not isinstance(role_ids, list):
        role_ids = []
    db_manager.save_settings({"commands_github": {"enabled": enabled, "role_ids": role_ids}})
    if command_bot_instance:
        try:
            asyncio.create_task(command_bot_instance.refresh_permissions())
        except Exception:
            pass
    return {"success": True}

@app.get("/api/guilds/{guild_id}/select")
async def select_guild(guild_id: str):
    db_manager.set_last_server(guild_id)
    payload = await db_manager.get_guild_payload(guild_id)
    if payload["success"]:
        active_context["guild_id"] = guild_id
        active_context["data"] = payload
        return payload
    return {"success": False, "error": "Failed to fetch guild info"}

@app.get("/api/guilds/{guild_id}/channels")
async def get_channels(guild_id: str):
    if active_context["guild_id"] == guild_id and active_context["data"]:
        return {"success": True, "channels": active_context["data"]["channels"]}
    channels = await db_manager.get_channels(guild_id)
    return {"success": True, "channels": channels}

@app.get("/api/guilds/{guild_id}/roles")
async def get_roles(guild_id: str):
    if active_context["guild_id"] == guild_id and active_context["data"]:
        return {"success": True, "roles": active_context["data"]["roles"]}
    headers = {"Authorization": f"Bot {db_manager.token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://discord.com/api/v10/guilds/{guild_id}/roles", headers=headers)
        if resp.status_code == 200:
            return {"success": True, "roles": resp.json()}
    return {"success": False, "error": "Failed to fetch roles"}

# --- CONFIG ENDPOINTS ---

@app.get("/api/config/join/{guild_id}")
async def get_join_config(guild_id: str):
    config = db_manager.get_config(guild_id, "join")
    return {"success": True, "config": config}

@app.post("/api/config/join/{guild_id}")
async def save_join_config(guild_id: str, data: Dict = Body(...)):
    db_manager.save_config(guild_id, "join", data)
    return {"success": True}

@app.get("/api/config/leave/{guild_id}")
async def get_leave_config(guild_id: str):
    config = db_manager.get_config(guild_id, "leave")
    return {"success": True, "config": config}

@app.post("/api/config/leave/{guild_id}")
async def save_leave_config(guild_id: str, data: Dict = Body(...)):
    db_manager.save_config(guild_id, "leave", data)
    return {"success": True}

@app.get("/api/config/dm/{guild_id}")
async def get_dm_config(guild_id: str):
    config = db_manager.get_config(guild_id, "dm")
    return {"success": True, "config": config}

@app.post("/api/config/dm/{guild_id}")
async def save_dm_config(guild_id: str, data: Dict = Body(...)):
    db_manager.save_config(guild_id, "dm", data)
    return {"success": True}

@app.get("/api/config/role/{guild_id}")
async def get_role_config(guild_id: str):
    config = db_manager.get_config(guild_id, "role")
    return {"success": True, "config": config}

@app.post("/api/config/role/{guild_id}")
async def save_role_config(guild_id: str, data: Dict = Body(...)):
    db_manager.save_config(guild_id, "role", data)
    return {"success": True}

@app.get("/api/config/levels/{guild_id}")
async def get_levels_config(guild_id: str):
    config = db_manager.get_config(guild_id, "levels")
    return {"success": True, "config": config}

@app.post("/api/config/levels/{guild_id}")
async def save_levels_config(guild_id: str, data: Dict = Body(...)):
    db_manager.save_config(guild_id, "levels", data)
    return {"success": True}

@app.get("/api/config/reaction-roles/{guild_id}")
async def get_reaction_roles_config(guild_id: str):
    config = db_manager.get_config(guild_id, "reaction_roles")
    return {"success": True, "config": config}

@app.post("/api/config/reaction-roles/{guild_id}")
async def save_reaction_roles_config(guild_id: str, data: Dict = Body(...)):
    formatted_data = rr_db.format_payload(data)
    db_manager.save_config(guild_id, "reaction_roles", formatted_data)
    return {"success": True}

@app.post("/api/publish/reaction-roles/{guild_id}")
async def publish_reaction_roles(guild_id: str):
    config = db_manager.get_config(guild_id, "reaction_roles")
    if not config:
        return {"success": False, "error": "No configuration found. Please save first."}
    
    if rr_bot_instance:
        return await rr_bot_instance.publish_message(guild_id, config)
    return {"success": False, "error": "Bot not active"}

# --- Scheduled Announcements Phase 2 Helpers ---
sa_data_helper = ScheduledAnnouncementsData(db_manager)
sa_config_helper = ScheduledAnnouncementConfig(db_manager)

@app.get("/api/scheduled-announcements/channels/{guild_id}")
async def get_sa_channels(guild_id: str):
    return await sa_data_helper.get_channels_list(guild_id)

# --- End of Phase 2 Helpers ---

@app.get("/api/config/scheduled-announcement/{guild_id}")
async def get_scheduled_announcement(guild_id: str):
    config = db_manager.get_config(guild_id, "scheduled_announcement") or {}
    return {"success": True, "config": config}

@app.get("/api/config/scheduled-announcements/{guild_id}")
async def get_scheduled_announcements(guild_id: str):
    announcements = db_manager.get_scheduled_announcements(guild_id)
    return {"success": True, "announcements": announcements}

@app.post("/api/config/scheduled-announcement/{guild_id}")
async def save_scheduled_announcement(guild_id: str, payload: Dict = Body(...)):
    announcement = sa_config_helper.format_payload(payload or {})
    if not announcement.get("id"):
        announcement["id"] = str(uuid4())
    db_manager.save_config(guild_id, "scheduled_announcement", announcement)
    return {"success": True, "config": announcement}

@app.post("/api/publish/scheduled-announcement/{guild_id}")
async def publish_scheduled_announcement(guild_id: str, payload: Dict = Body(...)):
    announcement = sa_config_helper.format_payload(payload or {})
    if not announcement.get("id"):
        announcement["id"] = str(uuid4())
    announcement["status"] = "scheduled"
    db_manager.save_scheduled_announcement(guild_id, announcement)
    return {"success": True, "config": announcement}

@app.delete("/api/config/scheduled-announcement/{guild_id}/{announcement_id}")
async def delete_scheduled_announcement(guild_id: str, announcement_id: str):
    db_manager.delete_scheduled_announcement(guild_id, announcement_id)
    return {"success": True}

@app.post("/api/roles/create")
async def create_role(payload: Dict = Body(...)):
    guild_id = payload.get("guild_id")
    name = payload.get("name")
    color = payload.get("color", "#5865f2")
    if not guild_id or not name:
        return {"success": False, "error": "guild_id and name are required"}

    try: color_int = int(str(color).lstrip("#"), 16)
    except: color_int = 0x5865F2

    headers = {"Authorization": f"Bot {db_manager.token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"https://discord.com/api/v10/guilds/{guild_id}/roles", headers=headers, json={"name": name, "color": color_int})
        if resp.status_code in (200, 201):
            role = resp.json()
            return {"success": True, "role": {"id": role.get("id"), "name": role.get("name"), "color": f"#{int(role.get('color') or 0):06x}"}}
        return {"success": False, "error": resp.text}

@app.post("/api/upload/image")
async def upload_image(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename or "")[1].lower()
    filename = f"{uuid4().hex}{ext if ext else '.png'}"
    path = os.path.join(IMAGES_DIR, filename)
    try:
        content = await file.read()
        with open(path, "wb") as f: f.write(content)
        return {"success": True, "url": f"/database/images/{filename}"}
    except Exception as exc: return {"success": False, "error": str(exc)}

@app.get("/api/stats/messages-today/{guild_id}")
async def get_messages_today(guild_id: str):
    count = msg_db.get_messages_today_count(guild_id)
    return {"success": True, "count": count}

# Store active download tasks
active_downloads = {}

@app.get("/api/messages/download/{guild_id}")
async def start_download(guild_id: str):
    # Check if already running
    if guild_id in active_downloads and active_downloads[guild_id]["status"] in ("downloading", "rebuilding"):
        return {"success": False, "error": "Download already in progress"}

    # Use the logger client instance
    if not msg_logger_instance:
        return {"success": False, "error": "Logger not active"}
    
    # Initialize status
    active_downloads[guild_id] = {
        "status": "starting",
        "progress_text": "Evaluating channels...",
        "total_downloaded": 0,
        "error": None
    }
    
    # Start task
    asyncio.create_task(msg_logger_instance.download_history_background(guild_id, active_downloads[guild_id]))
    
    return {"success": True, "message": "Download started"}

@app.get("/api/messages/download/status/{guild_id}")
async def check_download_status(guild_id: str):
    status = active_downloads.get(guild_id)
    if not status:
        return {"success": False, "status": "idle"}
    return {
        "success": True,
        "status": status["status"],
        "progress_text": status.get("progress_text"),
        "total": status.get("total_downloaded"),
        "total_users": status.get("total_users")
    }

@app.get("/api/messages/export/{guild_id}")
async def export_messages(guild_id: str):
    # This generates the file AFTER download is done
    try:
        messages = msg_db.get_all_messages(guild_id)
        if not messages:
             return {"success": False, "error": "No messages found"}
             
        filename = f"messages_{guild_id}_{int(time.time())}.json"
        filepath = os.path.join(IMAGES_DIR, filename) 
        
        # Write to JSON file
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, default=str)
            
        return {"success": True, "download_url": f"/database/images/{filename}", "count": len(messages)}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Global ref for the API to use
rr_bot_instance = None
command_bot_instance = None

async def main():
    port = int(os.getenv("AUTOCLAUDE_PORT", "5000"))
    print(f"[INFO] Starting Backend server on http://127.0.0.1:{port}")
    
    # Initialize bot clients
    global rr_bot_instance
    rr_bot = ReactionRoles(db_manager)
    rr_bot_instance = rr_bot
    global command_bot_instance
    command_bot_instance = IntegratedCommandBot(db_manager)
    
    # Message Logger
    global msg_logger_instance
    msg_logger_instance = MessageLoggerClient(db_manager, msg_db)
    
    global clients
    clients = [
        LeaveServer(db_manager),
        JoinServer(db_manager),
        PrivateMessageServer(db_manager),
        JoinRoleServer(db_manager),
        LevelServer(db_manager, msg_db),
        rr_bot,
        ScheduledAnnouncementSender(db_manager),
        HiEmojiReactor(db_manager),
        command_bot_instance,
        msg_logger_instance
    ]
    
    # Start bot tasks
    bot_tasks = [asyncio.create_task(client.start_bot()) for client in clients]

    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="info")
    server = uvicorn.Server(config)
    try:
        await server.serve()
    finally:
        for client in clients: await client.close()

if __name__ == "__main__":
    try: asyncio.run(main())
    except KeyboardInterrupt: pass
