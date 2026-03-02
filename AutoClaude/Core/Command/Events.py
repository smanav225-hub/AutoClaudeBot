import discord
from discord import app_commands
from discord.ext import commands

class EventsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_events", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="events", description="List all upcoming server events")
    async def execute(self, interaction: discord.Interaction):
        if not self._check_enabled(interaction): return
        
        await interaction.response.defer(ephemeral=True)
        
        events = self.bot.msg_db.list_upcoming_events(interaction.guild_id)
        if not events:
            await interaction.followup.send("No upcoming events scheduled.", ephemeral=True)
            return
            
        lines = []
        for e in events:
            ts = int(e['scheduled_at'])
            lines.append(f"📅 **{e['title']}** — <t:{ts}:R>\nID: `#{e['id']}` · In: <#{e['channel_id']}>")
            
        embed = discord.Embed(
            title="🎯 Upcoming Server Events",
            description="\n\n".join(lines),
            color=0xC4A35B
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(EventsCog(bot))
