import discord
from discord import app_commands
from discord.ext import commands

class Ticket_SetupCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_ticket_setup", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="ticket-setup", description="Configure the ticket system")
    @app_commands.describe(category="Category where tickets will be created")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def execute(self, interaction: discord.Interaction, category: discord.CategoryChannel):
        if not self._check_enabled(interaction): return
        
        # Save to guild config
        guild_id = str(interaction.guild_id)
        config = self.db.get_config(guild_id, "tickets") or {}
        config["category_id"] = str(category.id)
        self.db.save_config(guild_id, "tickets", config)
        
        await interaction.response.send_message(f"✅ Ticket system configured! Category: **{category.name}**", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Ticket_SetupCog(bot))
