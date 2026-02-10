import os
import discord
import asyncio
from datetime import datetime
from io import BytesIO
import requests
from typing import Dict, List, Optional

# Helper for image paths - assuming it's in AutoClaude/Database/Images
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, "Database", "Images")
LOCKS_DIR = os.path.join(BASE_DIR, "Database", "Locks")
os.makedirs(LOCKS_DIR, exist_ok=True)

class BaseDiscordClient(discord.Client):
    def __init__(self, db):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        super().__init__(intents=intents)
        self.db = db
        self.token = db.token
        self._debug_counts = {"join_card": 0, "join_embed": 0, "join_text": 0, "dm_card": 0, "dm_embed": 0, "dm_text": 0}

    def _debug_log(self, key: str, guild=None, channel=None, extra: str = ""):
        try:
            self._debug_counts[key] = self._debug_counts.get(key, 0) + 1
            gname = guild.name if guild else "UnknownGuild"
            cname = f"#{channel.name}" if channel and hasattr(channel, "name") else "DM"
            print(f"[DEBUG] {key} count={self._debug_counts[key]} guild={gname} channel={cname} {extra}".strip())
        except Exception:
            pass

    async def start_bot(self):
        if not self.token:
            print(f"[WARN] Discord token missing; {self.__class__.__name__} not started.")
            return
        try:
            await self.start(self.token)
        except Exception as exc:
            print(f"[{self.__class__.__name__}] Bot stopped: {exc}")

    def _render_message(self, template, member):
        now = datetime.now()
        replacements = {
            "{user}": member.display_name,
            "{mention}": member.mention,
            "{userid}": str(member.id),
            "{usertag}": str(member),
            "{avatar}": str(member.display_avatar.url) if member.display_avatar else "",
            "{server}": member.guild.name,
            "{serverid}": str(member.guild.id),
            "{membercount}": str(member.guild.member_count or ""),
            "{members}": str(member.guild.member_count or ""),
            "{role}": member.top_role.name if member and member.top_role else "",
            "{date}": now.strftime("%Y-%m-%d"),
            "{time}": now.strftime("%H:%M:%S"),
        }
        message = template
        for key, value in replacements.items():
            message = message.replace(key, value)
        return message

    def _local_image_path(self, url):
        if not url or not isinstance(url, str):
            return None
        if url.startswith("/database/images/"):
            filename = url.split("/")[-1]
            path = os.path.join(IMAGES_DIR, filename)
            return path if os.path.exists(path) else None
        return None

    async def _resolve_channel(self, guild, channel_id=None, channel_name=None):
        channel = None
        if channel_id:
            try:
                channel_id_int = int(str(channel_id))
                channel = guild.get_channel(channel_id_int)
                if channel is None:
                    try:
                        channel = await guild.fetch_channel(channel_id_int)
                    except Exception:
                        channel = None
            except Exception:
                if not channel_name:
                    channel_name = str(channel_id)
        if channel is None and channel_name:
            name = str(channel_name).lstrip("#").lower()
            for ch in guild.text_channels:
                if ch.name.lower() == name:
                    channel = ch
                    break
        return channel

class LeaveServer(BaseDiscordClient):
    async def on_ready(self):
        print(f"[LeaveServer] Logged in as {self.user} (ID: {self.user.id})")

    async def on_member_remove(self, member):
        guild_id = str(member.guild.id)
        config = self.db.get_config(guild_id, "leave") or {}
        if not config.get("enabled"):
            return

        channel_id = config.get("channel")
        channel_name = config.get("channel_name")
        if not channel_id and not channel_name:
            return

        try:
            channel = await self._resolve_channel(member.guild, channel_id, channel_name)
            if not channel:
                return
            template = config.get("text") or "{user} just left the server."
            message = self._render_message(template, member)
            await channel.send(message)
            print(f"[LeaveServer] Sent leave message in {member.guild.name}")
        except Exception as exc:
            print(f"[LeaveServer] Error: {exc}")

class JoinServer(BaseDiscordClient):
    async def on_ready(self):
        print(f"[JoinServer] Logged in as {self.user} (ID: {self.user.id})")

    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        config = self.db.get_config(guild_id, "join") or {}
        if not config.get("enabled"):
            return

        channel_id = config.get("channel")
        channel_name = config.get("channel_name")
        if not channel_id and not channel_name:
            return

        try:
            channel = await self._resolve_channel(member.guild, channel_id, channel_name)
            if not channel:
                return
            
            card_enabled = bool((config.get("card") or {}).get("enabled"))
            msg_type = config.get("type") or "text"
            if card_enabled:
                await self._send_welcome_card(channel, member, config, is_dm=False)
            elif msg_type == "embed":
                await self._send_embed_message(channel, member, config, is_dm=False)
            else:
                template = config.get("text") or "Hey {user}, welcome to **{server}**!"
                await channel.send(self._render_message(template, member))
                self._debug_log("join_text", guild=member.guild, channel=channel)
        except Exception as exc:
            print(f"[JoinServer] Error: {exc}")

    async def _send_embed_message(self, target, member, config, is_dm=False):
        embed_cfg = config.get("embed") or {}
        color_hex = embed_cfg.get("color", "#6b7280")
        try:
            color_int = int(str(color_hex).lstrip("#"), 16)
        except:
            color_int = 0x6b7280

        description = self._render_message(embed_cfg.get("description") or "Hey {user}, welcome to **{server}**!", member)
        embed = discord.Embed(title=embed_cfg.get("title") or None, description=description, color=color_int)

        if embed_cfg.get("author"):
            embed.set_author(name=embed_cfg["author"], icon_url=str(self.user.display_avatar.url))
        if embed_cfg.get("footer"):
            embed.set_footer(text=embed_cfg["footer"], icon_url=str(member.guild.icon.url) if member.guild.icon else None)

        image_url = embed_cfg.get("image")
        local_path = self._local_image_path(image_url)
        
        if local_path:
            filename = os.path.basename(local_path)
            file = discord.File(fp=local_path, filename=filename)
            embed.set_image(url=f"attachment://{filename}")
            sent = await target.send(content=None if is_dm else f"Welcome {member.mention}!", embed=embed, file=file)
            self._debug_log("dm_embed" if is_dm else "join_embed", guild=member.guild, channel=(None if is_dm else target))
            return sent
        else:
            if image_url: embed.set_image(url=image_url)
            sent = await target.send(content=None if is_dm else f"Welcome {member.mention}!", embed=embed)
            self._debug_log("dm_embed" if is_dm else "join_embed", guild=member.guild, channel=(None if is_dm else target))
            return sent

    async def _send_welcome_card(self, target, member, config, is_dm=False):
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            print("[JoinServer] PIL missing")
            return

        card_cfg = config.get("card") or {}
        
        def hex_to_rgb(hex_color, fallback=(255, 255, 255)):
            try:
                h = str(hex_color).lstrip('#')
                return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            except: return fallback

        width, height = 900, 350
        text_color = hex_to_rgb(card_cfg.get('textColor', '#ffffff'))
        bg_color = hex_to_rgb(card_cfg.get('bgColor', '#1e1f22'))
        opacity = float(card_cfg.get('opacity', 50)) / 100.0

        title_template = card_cfg.get('title', '{user} just joined')
        subtitle_template = card_cfg.get('subtitle', 'Member # {members}')
        
        title_text = self._render_message(title_template, member)
        subtitle_text = self._render_message(subtitle_template, member)

        base = Image.new('RGB', (width, height), bg_color)
        bg_image = card_cfg.get("bgImage")
        if bg_image:
            try:
                local_path = self._local_image_path(bg_image)
                if local_path:
                    bg = Image.open(local_path).convert("RGB")
                else:
                    resp = requests.get(bg_image if not bg_image.startswith("/") else f"http://127.0.0.1:5000{bg_image}", timeout=5)
                    bg = Image.open(BytesIO(resp.content)).convert("RGB")
                bg = bg.resize((width, height), Image.Resampling.LANCZOS)
                base.paste(bg, (0, 0))
            except: pass

        overlay = Image.new('RGBA', (width, height), (0, 0, 0, int(255 * (1 - opacity))))
        base = Image.alpha_composite(base.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(base)

        try:
            resp = requests.get(str(member.display_avatar.url), timeout=5)
            avatar = Image.open(BytesIO(resp.content)).convert("RGBA").resize((180, 180), Image.Resampling.LANCZOS)
            mask = Image.new('L', (180, 180), 0)
            ImageDraw.Draw(mask).ellipse((0, 0, 180, 180), fill=255)
            base.paste(avatar, (60, (height - 180) // 2), mask)
        except: pass

        def get_font(size):
            font_name = str(card_cfg.get("font") or "").strip()
            fonts_dir = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
            candidates = []
            if font_name:
                base = font_name.replace(" ", "")
                candidates.extend([
                    f"{font_name}.ttf",
                    f"{base}.ttf",
                    f"{base}-Regular.ttf",
                    f"{base}Regular.ttf"
                ])
            candidates.extend(["arial.ttf", "segoeui.ttf"])
            for fname in candidates:
                try:
                    path = fname if os.path.isabs(fname) else os.path.join(fonts_dir, fname)
                    return ImageFont.truetype(path, size)
                except Exception:
                    continue
            return ImageFont.load_default()

        def scale_size(base, text, limit, min_size):
            if not text:
                return base
            if len(text) <= limit:
                return base
            extra = len(text) - limit
            return max(min_size, int(base - extra * 0.6))

        def fit_font(text, base_size, min_size, max_width_px):
            size = max(min_size, int(base_size))
            while size > min_size:
                font = get_font(size)
                try:
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_w = bbox[2] - bbox[0]
                except Exception:
                    text_w = font.getlength(text) if hasattr(font, "getlength") else len(text) * size
                if text_w <= max_width_px:
                    return font
                size -= 2
            return get_font(min_size)

        base_title_size = int(card_cfg.get("titleSize") or 56)
        base_subtitle_size = int(card_cfg.get("subtitleSize") or 36)
        title_size = scale_size(base_title_size, title_text, 28, 24)
        subtitle_size = scale_size(base_subtitle_size, subtitle_text, 40, 18)

        max_text_width = width - 320
        font_title = fit_font(title_text, title_size, 24, max_text_width)
        font_subtitle = fit_font(subtitle_text, subtitle_size, 18, max_text_width)
        draw.text((280, 95), title_text, fill=text_color, font=font_title)
        draw.text((280, 170), subtitle_text, fill=text_color, font=font_subtitle)

        img_byte_arr = BytesIO()
        base.save(img_byte_arr, format='JPEG', quality=95)
        img_byte_arr.seek(0)
        file = discord.File(fp=img_byte_arr, filename="welcome.jpg")
        await target.send(content=f"Welcome {member.mention}!" if not is_dm else None, file=file)
        self._debug_log("dm_card" if is_dm else "join_card", guild=member.guild, channel=(None if is_dm else target))

class PrivateMessageServer(JoinServer):
    def __init__(self, db):
        super().__init__(db)
        self._recent_dm = {}  # (guild_id, user_id) -> last_sent_ts
        self._dedupe_window_s = 300

    def _dm_lock_path(self, guild_id: str, user_id: str) -> str:
        return os.path.join(LOCKS_DIR, f"dm_{guild_id}_{user_id}.lock")

    def _try_acquire_dm_lock(self, guild_id: str, user_id: str, now: float) -> bool:
        path = self._dm_lock_path(guild_id, user_id)
        try:
            if os.path.exists(path):
                try:
                    with open(path, "r") as f:
                        ts = float((f.read() or "0").strip() or 0)
                except Exception:
                    ts = 0
                if now - ts < self._dedupe_window_s:
                    return False
                try:
                    os.remove(path)
                except Exception:
                    pass
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, "w") as f:
                f.write(str(now))
            return True
        except FileExistsError:
            return False
        except Exception:
            # Fail open if lock can't be used
            return True

    async def on_ready(self):
        print(f"[PrivateMessageServer] Logged in as {self.user} (ID: {self.user.id})")

    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        user_id = str(member.id)
        now = datetime.now().timestamp()
        last_ts = self._recent_dm.get((guild_id, user_id), 0)
        db_last_ts = self.db.get_recent_dm_ts(guild_id, user_id)
        if (now - last_ts < self._dedupe_window_s) or (now - db_last_ts < self._dedupe_window_s):
            return
        if not self._try_acquire_dm_lock(guild_id, user_id, now):
            return
        self._recent_dm[(guild_id, user_id)] = now
        self.db.set_recent_dm_ts(guild_id, user_id, now)

        config = self.db.get_config(guild_id, "dm") or {}
        if not config.get("enabled"): return
        
        card_enabled = bool((config.get("card") or {}).get("enabled"))
        msg_type = config.get("type") or "text"
        try:
            sent_msg = None
            if card_enabled:
                await self._send_welcome_card(member, member, config, is_dm=True)
            elif msg_type == "embed":
                sent_msg = await self._send_embed_message(member, member, config, is_dm=True)
            else:
                sent_msg = await member.send(self._render_message(config.get("text") or "Welcome!", member))
                self._debug_log("dm_text", guild=member.guild, channel=None)

            if sent_msg:
                await self._cleanup_recent_dm_messages(member, sent_msg.id)
        except Exception as exc:
            print(f"[PrivateMessageServer] Error: {exc}")

    async def _cleanup_recent_dm_messages(self, member, keep_message_id: int, window_s: int = 20, limit: int = 10):
        try:
            channel = member.dm_channel or await member.create_dm()
            now = None
            async for msg in channel.history(limit=limit):
                if msg.id == keep_message_id:
                    continue
                if msg.author.id != self.user.id:
                    continue
                if now is None:
                    now = datetime.now(tz=msg.created_at.tzinfo)
                age = (now - msg.created_at).total_seconds()
                if age <= window_s:
                    try:
                        await msg.delete()
                    except Exception:
                        pass
        except Exception:
            pass

class JoinRoleServer(BaseDiscordClient):
    async def on_ready(self):
        print(f"[JoinRoleServer] Logged in as {self.user} (ID: {self.user.id})")

    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        config = self.db.get_config(guild_id, "role") or {}
        if not config.get("enabled"): return

        role_ids = config.get("selected_roles") or []
        bot_member = member.guild.me
        
        if not bot_member.guild_permissions.manage_roles:
            print(f"[JoinRoleServer] Missing permissions in {member.guild.name}")
            return

        roles_to_add = []
        for rid in role_ids:
            role = member.guild.get_role(int(rid))
            if role and role < bot_member.top_role and not role.managed:
                roles_to_add.append(role)

        if roles_to_add:
            try:
                await member.add_roles(*roles_to_add, reason="Auto-assign on join")
                print(f"[JoinRoleServer] Added roles to {member} in {member.guild.name}")
            except Exception as exc:
                print(f"[JoinRoleServer] Error: {exc}")
