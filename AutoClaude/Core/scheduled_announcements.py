import os
import asyncio
from datetime import datetime, timezone
from io import BytesIO
from typing import Dict

import requests
import discord

# Helper for image paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, "Database", "Images")


class ScheduledAnnouncementsData:
    def __init__(self, db_manager):
        self.db = db_manager

    async def get_channels_list(self, guild_id: str):
        channels = await self.db.get_channels(guild_id)
        return {"success": True, "channels": channels}


class ScheduledAnnouncementConfig:
    def __init__(self, db_manager):
        self.db = db_manager

    def format_payload(self, raw: Dict) -> Dict:
        msg_type = raw.get("message_type", "text")
        message = raw.get("message", {}) if isinstance(raw.get("message"), dict) else {}

        payload = {
            "id": raw.get("id"),
            "channel_id": raw.get("channel"),
            "channel_name": raw.get("channel_name"),
            "scheduled_time": raw.get("scheduled_time"),
            "message_type": msg_type,
            "status": raw.get("status", "draft"),
            "message": {}
        }

        if msg_type == "card":
            payload["message"]["card"] = message.get("card", {})
        elif msg_type == "embed":
            embed = message.get("embed", {}) if isinstance(message.get("embed"), dict) else {}
            payload["message"]["embed"] = embed
        else:
            payload["message"]["content"] = message.get("content", "")

        return payload


class ScheduledAnnouncementSender(discord.Client):
    def __init__(self, db):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        super().__init__(intents=intents)
        self.db = db
        self.token = db.token
        self._task = None

    async def start_bot(self):
        if not self.token:
            print("[WARN] Discord token missing; ScheduledAnnouncementSender not started.")
            return
        try:
            await self.start(self.token)
        except Exception as exc:
            print(f"[ScheduledAnnouncements] Bot stopped: {exc}")

    async def on_ready(self):
        print(f"[ScheduledAnnouncements] Logged in as {self.user} (ID: {self.user.id})")
        if not self._task:
            self._task = asyncio.create_task(self._poll_loop())

    async def _poll_loop(self):
        while not self.is_closed():
            try:
                await self._check_and_send()
            except Exception as exc:
                print(f"[ScheduledAnnouncements] Poll error: {exc}")
            await asyncio.sleep(20)

    def _parse_time(self, value):
        if not value:
            return None
        try:
            return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        except Exception:
            return None

    def _is_due(self, dt):
        if dt is None:
            return False
        if dt.tzinfo:
            now = datetime.now(dt.tzinfo)
        else:
            now = datetime.now()
        return now >= dt

    def _local_image_path(self, url):
        if not url or not isinstance(url, str):
            return None
        if url.startswith("/database/images/"):
            filename = url.split("/")[-1]
            path = os.path.join(IMAGES_DIR, filename)
            return path if os.path.exists(path) else None
        return None

    def _render_placeholders(self, text: str, guild: discord.Guild):
        if not text:
            return text
        now = datetime.now()
        bot_user = self.user
        
        # Get bot member in the specific guild to resolve role
        bot_role = ""
        if guild and bot_user:
            bot_member = guild.get_member(bot_user.id)
            if bot_member and bot_member.top_role:
                bot_role = bot_member.top_role.name

        replacements = {
            "{user}": bot_user.display_name if bot_user else "",
            "{userid}": str(bot_user.id) if bot_user else "",
            "{usertag}": str(bot_user) if bot_user else "",
            "{mention}": bot_user.mention if bot_user else "",
            "{avatar}": str(bot_user.display_avatar.url) if bot_user and bot_user.display_avatar else "",
            "{server}": guild.name if guild else "",
            "{serverid}": str(guild.id) if guild else "",
            "{membercount}": str(guild.member_count or "") if guild else "",
            "{members}": str(guild.member_count or "") if guild else "",
            "{role}": bot_role,
            "{date}": now.strftime("%Y-%m-%d"),
            "{time}": now.strftime("%H:%M:%S"),
        }
        result = text
        for key, value in replacements.items():
            result = result.replace(key, value)
        return result

    async def _send_text(self, channel, message, guild):
        if not message:
            return
        await channel.send(self._render_placeholders(message, guild))

    async def _send_embed(self, channel, msg_data, guild):
        embed_data = msg_data.get("embed", {}) if isinstance(msg_data, dict) else {}
        color_int = 0xffffff
        try:
            color_int = int(str(embed_data.get("color", "#ffffff")).lstrip("#"), 16)
        except Exception:
            color_int = 0xffffff

        embed = discord.Embed(
            title=self._render_placeholders(embed_data.get("title") or "", guild) or None,
            description=self._render_placeholders(embed_data.get("description") or "", guild) or None,
            color=color_int
        )

        files = []

        def attach_img(url, setter_func, filename):
            path = self._local_image_path(url)
            if path and os.path.exists(path):
                f = discord.File(path, filename=filename)
                files.append(f)
                setter_func(url=f"attachment://{filename}")
                return True
            return False

        if embed_data.get("author", {}).get("name"):
            name = self._render_placeholders(embed_data["author"]["name"], guild)
            url = embed_data["author"].get("icon_url")
            if not attach_img(url, lambda url: embed.set_author(name=name, icon_url=url), "author.png"):
                embed.set_author(name=name)

        if embed_data.get("footer", {}).get("text"):
            text = self._render_placeholders(embed_data["footer"]["text"], guild)
            url = embed_data["footer"].get("icon_url")
            if not attach_img(url, lambda url: embed.set_footer(text=text, icon_url=url), "footer.png"):
                embed.set_footer(text=text)

        attach_img(embed_data.get("thumbnail"), embed.set_thumbnail, "thumb.png")
        attach_img(embed_data.get("image"), embed.set_image, "main.png")

        for field in embed_data.get("fields", []):
            try:
                name = self._render_placeholders(field.get("name", ""), guild)
                value = self._render_placeholders(field.get("value", ""), guild)
                embed.add_field(name=name, value=value, inline=False)
            except Exception:
                continue

        content = self._render_placeholders(msg_data.get("content") if isinstance(msg_data, dict) else None, guild)
        await channel.send(content=content or None, embed=embed, files=files)

    async def _send_welcome_card(self, channel, card_cfg, guild):
        try:
            from PIL import Image, ImageDraw, ImageFont
        except Exception as exc:
            print(f"[ScheduledAnnouncements] PIL missing: {exc}")
            return

        def hex_to_rgb(hex_color, fallback=(255, 255, 255)):
            try:
                h = str(hex_color).lstrip('#')
                if len(h) == 3:
                    h = "".join([c * 2 for c in h])
                return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            except Exception:
                return fallback

        width, height = 900, 350
        text_color = hex_to_rgb(card_cfg.get('textColor', '#ffffff'))
        bg_color = hex_to_rgb(card_cfg.get('bgColor', '#1e1f22'))
        try:
            opacity = float(card_cfg.get('opacity', 50)) / 100.0
        except Exception:
            opacity = 0.5

        title_text = self._render_placeholders(card_cfg.get('title', 'Scheduled Announcement'), guild)
        subtitle_text = self._render_placeholders(card_cfg.get('subtitle', ''), guild)

        base = Image.new('RGB', (width, height), bg_color)
        bg_image = card_cfg.get("bgImage")
        if bg_image:
            try:
                local_path = self._local_image_path(bg_image)
                if local_path:
                    bg = Image.open(local_path).convert("RGB")
                else:
                    url = bg_image
                    if bg_image.startswith("/"):
                        port = os.getenv("AUTOCLAUDE_PORT", "5000")
                        url = f"http://127.0.0.1:{port}{bg_image}"
                    resp = requests.get(url, timeout=8)
                    resp.raise_for_status()
                    bg = Image.open(BytesIO(resp.content)).convert("RGB")
                bg = bg.resize((width, height), Image.Resampling.LANCZOS)
                base.paste(bg, (0, 0))
            except Exception:
                pass

        overlay = Image.new('RGBA', (width, height), (0, 0, 0, int(255 * (1 - opacity))))
        base = Image.alpha_composite(base.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(base)

        try:
            avatar_url = str(self.user.display_avatar.url) if self.user and self.user.display_avatar else None
            if avatar_url:
                resp = requests.get(avatar_url, timeout=8)
                resp.raise_for_status()
                avatar = Image.open(BytesIO(resp.content)).convert("RGBA").resize((180, 180), Image.Resampling.LANCZOS)
                mask = Image.new('L', (180, 180), 0)
                ImageDraw.Draw(mask).ellipse((0, 0, 180, 180), fill=255)
                base.paste(avatar, (60, (height - 180) // 2), mask)
        except Exception:
            pass

        def get_font(size):
            for f in ["arial.ttf", "segoeui.ttf", "DejaVuSans.ttf"]:
                try:
                    return ImageFont.truetype(f, size)
                except Exception:
                    continue
            return ImageFont.load_default()

        font_title = get_font(42)
        font_subtitle = get_font(28)
        draw.text((280, 110), title_text, fill=text_color, font=font_title)
        draw.text((280, 170), subtitle_text, fill=text_color, font=font_subtitle)

        img_byte_arr = BytesIO()
        base.save(img_byte_arr, format='JPEG', quality=95)
        img_byte_arr.seek(0)
        file = discord.File(fp=img_byte_arr, filename="scheduled.jpg")
        await channel.send(file=file)

    async def _check_and_send(self):
        data = self.db.data.get("servers", {})
        for guild_id, server_data in data.items():
            announcements = server_data.get("scheduled_announcements", [])
            if not announcements:
                continue
            for item in announcements:
                if item.get("status") != "scheduled":
                    continue
                dt = self._parse_time(item.get("scheduled_time"))
                if not self._is_due(dt):
                    continue

                try:
                    guild = self.get_guild(int(guild_id))
                    if not guild:
                        raise Exception("Guild not found")
                    channel_id = int(item.get("channel_id")) if item.get("channel_id") else None
                    if not channel_id:
                        raise Exception("Channel missing")
                    channel = guild.get_channel(channel_id)
                    if channel is None:
                        channel = await guild.fetch_channel(channel_id)

                    msg_type = item.get("message_type", "text")
                    msg_data = item.get("message", {}) if isinstance(item.get("message"), dict) else {}

                    if msg_type == "card":
                        await self._send_welcome_card(channel, msg_data.get("card", {}), guild)
                    elif msg_type == "embed":
                        await self._send_embed(channel, msg_data, guild)
                    else:
                        await self._send_text(channel, msg_data.get("content", ""), guild)

                    item["status"] = "sent"
                    item["sent_at"] = datetime.now(timezone.utc).isoformat()
                    self.db.save_scheduled_announcement(str(guild_id), item)
                    print(f"[ScheduledAnnouncements] Sent scheduled message in {guild.name}")
                except Exception as exc:
                    item["status"] = "failed"
                    item["error"] = str(exc)
                    self.db.save_scheduled_announcement(str(guild_id), item)
                    print(f"[ScheduledAnnouncements] Failed to send: {exc}")
