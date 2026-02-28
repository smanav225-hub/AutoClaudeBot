import os
import discord
from discord.ui import View, Select
from typing import Dict, List
from .Welcome_Goodbye import BaseDiscordClient

# Helper for image paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, "Database", "Images")

class RoleDropdown(Select):
    def __init__(self, options_data):
        discord_options = []
        for opt in options_data:
            discord_options.append(discord.SelectOption(
                label=opt.get("label", "Option"), 
                value=str(opt.get("roleId")),
                description=opt.get("roleName", "")
            ))
        
        super().__init__(
            placeholder="Select your roles...",
            min_values=0,
            max_values=len(discord_options),
            options=discord_options,
            custom_id="rr_dropdown_persistent" 
        )

    async def callback(self, interaction: discord.Interaction):
        selected_ids = set(self.values)
        all_ids = set(o.value for o in self.options)
        
        to_add = []
        to_remove = []
        
        guild = interaction.guild
        user = interaction.user
        
        for role_id in all_ids:
            role = guild.get_role(int(role_id))
            if not role: continue
            
            if role_id in selected_ids:
                if role not in user.roles: to_add.append(role)
            else:
                if role in user.roles: to_remove.append(role)
        
        response_text = []
        try:
            if to_add:
                await user.add_roles(*to_add)
                response_text.append(f"✅ Added: {', '.join(r.name for r in to_add)}")
            if to_remove:
                await user.remove_roles(*to_remove)
                response_text.append(f"❌ Removed: {', '.join(r.name for r in to_remove)}")
            
            if not response_text:
                await interaction.response.send_message("Roles updated.", ephemeral=True)
            else:
                await interaction.response.send_message("\n".join(response_text), ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error updating roles: {str(e)}", ephemeral=True)

class ReactionRoles(BaseDiscordClient):
    async def on_ready(self):
        print(f"[ReactionRoles] Logged in as {self.user} (ID: {self.user.id})")

    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.user.id: return
        await self._handle_reaction(payload, "add")

    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == self.user.id: return
        await self._handle_reaction(payload, "remove")

    async def _handle_reaction(self, payload, action):
        guild_id = str(payload.guild_id)
        config = self.db.get_config(guild_id, "reaction_roles")
        if not config: return
        
        rr_config = config.get("reaction_config", {})
        if rr_config.get("type") != "emoji": return

        emoji_rows = rr_config.get("emoji_rows", [])
        target_row = next((r for r in emoji_rows if r["emoji"] == str(payload.emoji)), None)
        
        if not target_row: return

        guild = self.get_guild(payload.guild_id)
        if not guild: return
        
        member = guild.get_member(payload.user_id)
        if not member: return

        role_id = int(target_row["roleId"])
        role = guild.get_role(role_id)
        if not role: return

        mode = config.get("mode", "default") 

        try:
            if mode == "default":
                if action == "add":
                    await member.add_roles(role)
                    print(f"[RR] Added {role.name} to {member.name}")
                else: 
                    await member.remove_roles(role)
                    print(f"[RR] Removed {role.name} from {member.name}")
            
            elif mode == "reverse":
                if action == "add":
                    await member.remove_roles(role)
                    print(f"[RR] Removed {role.name} from {member.name} (Reverse)")
                else: 
                    await member.add_roles(role)
                    print(f"[RR] Added {role.name} to {member.name} (Reverse)")
                    
        except Exception as e:
            print(f"[RR] Error managing role: {e}")

    async def publish_message(self, guild_id: str, config: Dict):
        try:
            guild = self.get_guild(int(guild_id))
            if not guild: return {"success": False, "error": "Guild not found"}

            channel_id = int(config.get("channel_id"))
            channel = guild.get_channel(channel_id)
            if not channel: return {"success": False, "error": "Channel not found"}

            msg_data = config.get("message", {})
            embed_data = msg_data.get("embed", {})
            
            color_int = 0xffffff
            try: color_int = int(str(embed_data.get("color", "#ffffff")).lstrip("#"), 16)
            except: pass

            embed = discord.Embed(
                title=embed_data.get("title") or None,
                description=embed_data.get("description") or None,
                color=color_int
            )
            
            files = []
            
            def attach_img(url, setter_func, filename):
                path = self._get_local_path(url)
                if path and os.path.exists(path):
                    f = discord.File(path, filename=filename)
                    files.append(f)
                    setter_func(url=f"attachment://{filename}")
                    return True
                return False

            if embed_data.get("author", {}).get("name"):
                name = embed_data["author"]["name"]
                url = embed_data["author"].get("icon_url")
                if not attach_img(url, lambda url: embed.set_author(name=name, icon_url=url), "author.png"):
                    embed.set_author(name=name)
            
            if embed_data.get("footer", {}).get("text"):
                text = embed_data["footer"]["text"]
                url = embed_data["footer"].get("icon_url")
                if not attach_img(url, lambda url: embed.set_footer(text=text, icon_url=url), "footer.png"):
                    embed.set_footer(text=text)
                
            attach_img(embed_data.get("thumbnail"), embed.set_thumbnail, "thumb.png")
            attach_img(embed_data.get("image"), embed.set_image, "main.png")

            for field in embed_data.get("fields", []):
                embed.add_field(name=field["name"], value=field["value"], inline=False)

            content = msg_data.get("content") or None
            
            rr_config = config.get("reaction_config", {})
            view = None
            
            if rr_config.get("type") == "dropdown":
                rows = rr_config.get("dropdown_rows", [])
                if rows:
                    view = View(timeout=None)
                    view.add_item(RoleDropdown(rows))

            message = await channel.send(content=content, embed=embed, view=view, files=files)
            
            if rr_config.get("type") == "emoji":
                for row in rr_config.get("emoji_rows", []):
                    try: await message.add_reaction(row["emoji"])
                    except: pass
            
            config["active_message_id"] = str(message.id)
            self.db.save_config(guild_id, "reaction_roles", config)
            
            return {"success": True}
        except Exception as e:
            print(f"[PUBLISH] Error: {e}")
            return {"success": False, "error": str(e)}

    def _get_local_path(self, url):
        if not url or not url.startswith("/database"): return None
        filename = url.split("/")[-1]
        return os.path.join(IMAGES_DIR, filename)

    def _resolve_url(self, url):
        if not url: return None
        if url.startswith("/database"):
            port = os.getenv("AUTOCLAUDE_PORT", "5000")
            return f"http://127.0.0.1:{port}{url}"
        return url
