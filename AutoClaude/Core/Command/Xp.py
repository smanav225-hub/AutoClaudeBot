import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

class XpCog(commands.GroupCog, group_name="xp", group_description="Manage XP settings and adjustments"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_xp", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="grant", description="Grant XP to a user")
    @app_commands.describe(user="User to grant XP to", amount="XP amount")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def grant(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        if not self._check_enabled(interaction): return
        if amount <= 0:
            await interaction.response.send_message("❌ Amount must be positive.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        guild_id = str(interaction.guild_id)
        
        # Get formula
        levels_cfg = self.db.get_config(guild_id, "levels") or {}
        formula = levels_cfg.get("formula", "")
        
        new_total, new_level = await self.bot.msg_db.adjust_user_xp(guild_id, str(user.id), amount, formula)
        
        await interaction.followup.send(
            f"✅ Granted **{amount:,} XP** to {user.mention}.\n"
            f"New total: **{new_total:,} XP** (Level {new_level})"
        )

    @app_commands.command(name="revoke", description="Revoke XP from a user")
    @app_commands.describe(user="User to revoke XP from", amount="XP amount")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def revoke(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        if not self._check_enabled(interaction): return
        if amount <= 0:
            await interaction.response.send_message("❌ Amount must be positive.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        guild_id = str(interaction.guild_id)
        
        # Get formula
        levels_cfg = self.db.get_config(guild_id, "levels") or {}
        formula = levels_cfg.get("formula", "")
        
        new_total, new_level = await self.bot.msg_db.adjust_user_xp(guild_id, str(user.id), -amount, formula)
        
        await interaction.followup.send(
            f"✅ Revoked **{amount:,} XP** from {user.mention}.\n"
            f"New total: **{new_total:,} XP** (Level {new_level})"
        )

    @app_commands.command(name="config", description="View or update XP settings")
    @app_commands.describe(
        min_xp="Min XP per message", 
        max_xp="Max XP per message",
        cooldown="Cooldown in seconds",
        levelup_channel="Channel for announcements"
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    async def config(self, interaction: discord.Interaction, 
                     min_xp: Optional[int] = None, 
                     max_xp: Optional[int] = None, 
                     cooldown: Optional[int] = None,
                     levelup_channel: Optional[discord.TextChannel] = None):
        if not self._check_enabled(interaction): return
        
        guild_id = str(interaction.guild_id)
        current_cfg = self.db.get_config(guild_id, "levels") or {}
        
        if any([min_xp, max_xp, cooldown, levelup_channel]):
            if min_xp is not None: current_cfg["xp_min"] = min_xp
            if max_xp is not None: current_cfg["xp_max"] = max_xp
            if cooldown is not None: current_cfg["cooldown"] = cooldown
            if levelup_channel is not None: current_cfg["levelup_channel_id"] = str(levelup_channel.id)
            
            self.db.save_config(guild_id, "levels", current_cfg)
            await interaction.response.send_message("✅ XP settings updated.", ephemeral=True)
        else:
            # View current config
            xp_min = current_cfg.get("xp_min", 15)
            xp_max = current_cfg.get("xp_max", 25)
            cd = current_cfg.get("cooldown", 60)
            lvl_ch = current_cfg.get("levelup_channel_id")
            
            ch_text = f"<#{lvl_ch}>" if lvl_ch else "Same channel"
            embed = discord.Embed(title="⚙️ XP Configuration", color=discord.Color.blue())
            embed.add_field(name="Range", value=f"{xp_min} - {xp_max} XP per message")
            embed.add_field(name="Cooldown", value=f"{cd} seconds")
            embed.add_field(name="Level-Up Channel", value=ch_text)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(XpCog(bot))
