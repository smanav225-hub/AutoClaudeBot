import discord
from discord import app_commands
from discord.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_ping", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def execute(self, interaction: discord.Interaction):
        if not self._check_enabled(interaction): return
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! Latency: {latency}ms")

async def setup(bot: commands.Bot):
    await bot.add_cog(PingCog(bot))
