import discord
from discord import app_commands
from discord.ext import commands

import re
import time
import datetime
import io
import sqlite3
from discord.ext import tasks

def parse_duration(duration_str: str) -> float | None:
    match = re.match(r"^(\d+)\s*(m|h|d|w)$", duration_str.lower())
    if not match:
        return None
    amount = int(match.group(1))
    unit = match.group(2)
    if unit == 'm': return amount * 60
    if unit == 'h': return amount * 3600
    if unit == 'd': return amount * 86400
    if unit == 'w': return amount * 604800
    return None

class PunishmentCog(commands.GroupCog, group_name="punishment", group_description="Manage user punishments and history"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_punishment", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="ban", description="Ban a user from the server")
    @app_commands.describe(user="User to ban", duration="Duration (e.g. 7d, 24h, 30m)", reason="Reason for the ban")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban_user(self, interaction: discord.Interaction, user: discord.User, duration: str = None, reason: str = "No reason provided"):
        if not self._check_enabled(interaction): return
        
        expires_at = None
        if duration:
            seconds = parse_duration(duration)
            if seconds is None:
                await interaction.response.send_message("❌ Invalid duration. Use formats like `7d`, `24h`, `30m`.", ephemeral=True)
                return
            expires_at = time.time() + seconds
            
        try:
            await interaction.guild.ban(user, reason=reason)
            self.bot.msg_db.create_punishment(interaction.guild_id, user.id, "ban", reason, expires_at, interaction.user.id)
            
            dur_msg = f"until <t:{int(expires_at)}:F>" if expires_at else "permanently"
            await interaction.response.send_message(f"✅ Banned {user.mention} {dur_msg}. Reason: {reason}", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to ban that user.", ephemeral=True)

    @app_commands.command(name="unban", description="Unban a user from the server")
    @app_commands.describe(user_id="ID of the user to unban")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban_user(self, interaction: discord.Interaction, user_id: str):
        if not self._check_enabled(interaction): return
        
        try:
            user = await self.bot.fetch_user(int(user_id))
            await interaction.guild.unban(user)
            self.bot.msg_db.deactivate_punishments(interaction.guild_id, user_id, "ban")
            await interaction.response.send_message(f"✅ Unbanned user ID {user_id}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to unban: {str(e)}", ephemeral=True)

    @app_commands.command(name="mute", description="Mute (timeout) a user")
    @app_commands.describe(member="Member to mute", duration="Duration (e.g. 7d, 24h, 30m)", reason="Reason for the mute")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute_user(self, interaction: discord.Interaction, member: discord.Member, duration: str, reason: str = "No reason provided"):
        if not self._check_enabled(interaction): return
        
        seconds = parse_duration(duration)
        if seconds is None:
            await interaction.response.send_message("❌ Invalid duration. Use formats like `7d`, `24h`, `30m`.", ephemeral=True)
            return
            
        expires_at = time.time() + seconds
        duration_td = datetime.timedelta(seconds=seconds)
        
        try:
            await member.timeout(duration_td, reason=reason)
            self.bot.msg_db.create_punishment(interaction.guild_id, member.id, "mute", reason, expires_at, interaction.user.id)
            await interaction.response.send_message(f"✅ Muted {member.mention} until <t:{int(expires_at)}:F>. Reason: {reason}", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to mute that member.", ephemeral=True)

    @app_commands.command(name="unmute", description="Unmute a user")
    @app_commands.describe(member="Member to unmute")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def unmute_user(self, interaction: discord.Interaction, member: discord.Member):
        if not self._check_enabled(interaction): return
        
        try:
            await member.timeout(None)
            self.bot.msg_db.deactivate_punishments(interaction.guild_id, member.id, "mute")
            await interaction.response.send_message(f"✅ Unmuted {member.mention}.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to unmute that member.", ephemeral=True)

    @app_commands.command(name="list", description="Export a list of all banned users with IDs and reasons")
    @app_commands.checks.has_permissions(ban_members=True)
    async def list_bans(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        conn = self.bot.msg_db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM punishments WHERE type='ban' ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        # Also get current Discord bans for cross-reference
        try:
            discord_bans = {ban.user.id: ban async for ban in interaction.guild.bans()}
        except Exception:
            discord_bans = {}
        
        if not rows and not discord_bans:
            await interaction.followup.send("✅ No ban records found in the database or Discord.")
            return
            
        lines = [
            f"AutoClaude Ban List — {interaction.guild.name}",
            f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "=" * 40,
            ""
        ]
        
        # DB bans from our punishment system
        if rows:
            lines.append("=== BOT-ISSUED BANS (Database) ===")
            for r in rows:
                status = "ACTIVE" if r['is_active'] else "EXPIRED/REVOKED"
                expires_str = f"Expires: {datetime.datetime.fromtimestamp(r['expires_at']).strftime('%Y-%m-%d %H:%M')}" if r['expires_at'] else "Duration: Permanent"
                issued = datetime.datetime.fromtimestamp(r['created_at']).strftime('%Y-%m-%d %H:%M') if r['created_at'] else "Unknown"
                lines.append(f"User ID:  {r['user_id']}")
                lines.append(f"Reason:   {r['reason'] or 'None given'}")
                lines.append(f"Status:   {status}")
                lines.append(f"Issued:   {issued}")
                lines.append(f"{expires_str}")
                lines.append("-" * 30)
            lines.append("")
        
        # Active Discord bans (may include manual bans not in DB)
        if discord_bans:
            lines.append("=== ALL ACTIVE DISCORD BANS ===")
            for user_id, ban_entry in discord_bans.items():
                lines.append(f"User: {ban_entry.user.name}#{ban_entry.user.discriminator} (ID: {user_id})")
                lines.append(f"Reason: {ban_entry.reason or 'No reason given'}")
                lines.append("-" * 30)
            
        content = "\n".join(lines)
        file = discord.File(io.BytesIO(content.encode()), filename=f"ban_list_{interaction.guild.id}.txt")
        await interaction.followup.send(
            f"📋 Ban list exported! Found **{len(rows)}** DB record(s) and **{len(discord_bans)}** active Discord ban(s).",
            file=file
        )

    @tasks.loop(minutes=1)
    async def punishment_cleanup(self):
        """Background task to lift expired bans and mutes"""
        now = time.time()
        conn = self.bot.msg_db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 1. Find expired active punishments
        cursor.execute(
            "SELECT * FROM punishments WHERE is_active=1 AND expires_at IS NOT NULL AND expires_at <= ?",
            (now,)
        )
        expired = cursor.fetchall()
        
        for p in expired:
            guild = self.bot.get_guild(int(p['guild_id']))
            if not guild: continue
            
            user_id = int(p['user_id'])
            
            try:
                if p['type'] == 'ban':
                    user = await self.bot.fetch_user(user_id)
                    await guild.unban(user, reason="Auto-unban: Punishment expired")
                    print(f"[Punishment] Auto-unbanned {user_id} in {guild.name}")
                elif p['type'] == 'mute':
                    member = guild.get_member(user_id)
                    if member:
                        await member.timeout(None, reason="Auto-unmute: Punishment expired")
                        print(f"[Punishment] Auto-unmuted {user_id} in {guild.name}")
            except Exception as e:
                print(f"[Punishment] Error lifting {p['type']} for {user_id}: {e}")
            
            # Deactivate in DB regardless of success (to prevent retrying failed ones infinitely)
            cursor.execute("UPDATE punishments SET is_active=0 WHERE id=?", (p['id'],))
            
        conn.commit()
        conn.close()

    @punishment_cleanup.before_loop
    async def before_cleanup(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    # Need tasks from discord.ext
    from discord.ext import tasks
    cog = PunishmentCog(bot)
    await bot.add_cog(cog)
    cog.punishment_cleanup.start()
