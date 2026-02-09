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

class BaseDiscordClient(discord.Client):
    def __init__(self, db):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        super().__init__(intents=intents)
        self.db = db
        self.token = db.token

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

class LeaveServer(BaseDiscordClient):
    async def on_ready(self):
        print(f"[LeaveServer] Logged in as {self.user} (ID: {self.user.id})")

    async def on_member_remove(self, member):
        guild_id = str(member.guild.id)
        config = self.db.get_config(guild_id, "leave") or {}
        if not config.get("enabled"):
            return

        channel_id = config.get("channel")
        if not channel_id:
            return

        try:
            channel_id_int = int(channel_id)
            channel = member.guild.get_channel(channel_id_int) or await member.guild.fetch_channel(channel_id_int)
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
        if not channel_id:
            return

        try:
            channel_id_int = int(channel_id)
            channel = member.guild.get_channel(channel_id_int) or await member.guild.fetch_channel(channel_id_int)
            
            mode = config.get("mode") or config.get("type") or "text"
            if mode == "card":
                await self._send_welcome_card(channel, member, config, is_dm=False)
            elif mode == "embed":
                await self._send_embed_message(channel, member, config, is_dm=False)
            else:
                template = config.get("text") or "Hey {user}, welcome to **{server}**!"
                await channel.send(self._render_message(template, member))
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
            await target.send(content=None if is_dm else f"Welcome {member.mention}!", embed=embed, file=file)
        else:
            if image_url: embed.set_image(url=image_url)
            await target.send(content=None if is_dm else f"Welcome {member.mention}!", embed=embed)

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

        title_text = card_cfg.get('title', '{user.idname} just joined').replace('{user.idname}', member.display_name).replace('{server.name}', member.guild.name)
        subtitle_text = card_cfg.get('subtitle', 'Member # {server.member_count}').replace('{server.member_count}', str(member.guild.member_count or ""))

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

        # Draw text (simplified font loading)
        font_title = ImageFont.load_default() # In production, use ImageFont.truetype
        draw.text((280, 110), title_text, fill=text_color, font=font_title)
        draw.text((280, 170), subtitle_text, fill=text_color, font=font_title)

        img_byte_arr = BytesIO()
        base.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        file = discord.File(fp=img_byte_arr, filename="welcome.jpg")
        await target.send(content=f"Welcome {member.mention}!" if not is_dm else None, file=file)

class PrivateMessageServer(JoinServer):
    async def on_ready(self):
        print(f"[PrivateMessageServer] Logged in as {self.user} (ID: {self.user.id})")

    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        config = self.db.get_config(guild_id, "dm") or {}
        if not config.get("enabled"): return
        
        mode = config.get("mode") or config.get("type") or "text"
        try:
            if mode == "card": await self._send_welcome_card(member, member, config, is_dm=True)
            elif mode == "embed": await self._send_embed_message(member, member, config, is_dm=True)
            else: await member.send(self._render_message(config.get("text") or "Welcome!", member))
        except Exception as exc:
            print(f"[PrivateMessageServer] Error: {exc}")

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
