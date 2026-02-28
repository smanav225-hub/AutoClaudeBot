import discord
from discord import app_commands
from discord.ext import commands

class Reputation_ConfigCog(commands.GroupCog, group_name="reputation-config", group_description="Manage reputation system settings"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_reputation_config", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="set", description="Update reputation settings")
    @app_commands.describe(daily_cap="Max thanks per user per day", reciprocal_hours="Hours before reciprocal thank is allowed")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def set_config(self, interaction: discord.Interaction, daily_cap: int = None, reciprocal_hours: int = None):
        if not self._check_enabled(interaction): return
        
        guild_id = str(interaction.guild_id)
        config = self.db.get_config(guild_id, "reputation") or {}
        
        updated = False
        if daily_cap is not None:
            config["daily_cap"] = daily_cap
            updated = True
        if reciprocal_hours is not None:
            config["reciprocal_hours"] = reciprocal_hours
            updated = True
            
        if updated:
            self.db.save_config(guild_id, "reputation", config)
            await interaction.response.send_message("✅ Reputation settings updated.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ No changes provided.", ephemeral=True)

    @app_commands.command(name="view", description="View current reputation settings")
    async def view_config(self, interaction: discord.Interaction):
        if not self._check_enabled(interaction): return
        
        guild_id = str(interaction.guild_id)
        config = self.db.get_config(guild_id, "reputation") or {}
        
        daily_cap = config.get("daily_cap", 5) # Default 5
        reciprocal_hours = config.get("reciprocal_hours", 24) # Default 24
        
        embed = discord.Embed(
            title="✨ Reputation Settings",
            description=(
                f"**Daily Cap:** {daily_cap} thanks/day\n"
                f"**Reciprocal Window:** {reciprocal_hours}h"
            ),
            color=0xC4A35B
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Reputation_ConfigCog(bot))
