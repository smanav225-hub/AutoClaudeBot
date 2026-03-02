import discord
from discord import app_commands
from discord.ext import commands

class Leaderboard_PostCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_leaderboard_post", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="leaderboard-post", description="Post the leaderboard to the current channel")
    @app_commands.describe(period="Time period (weekly, monthly, alltime)", limit="Number of users to show (max 20)")
    @app_commands.choices(period=[
        app_commands.Choice(name="Weekly", value="weekly"),
        app_commands.Choice(name="Monthly", value="monthly"),
        app_commands.Choice(name="All Time", value="all")
    ])
    @app_commands.checks.has_permissions(manage_guild=True)
    async def execute(self, interaction: discord.Interaction, period: str = "all", limit: int = 15):
        if not self._check_enabled(interaction): return
        
        await interaction.response.defer(ephemeral=True)
        
        limit = min(max(1, limit), 20)
        entries = self.bot.msg_db.get_guild_leaderboard(str(interaction.guild_id), period, limit)
        
        if not entries:
            await interaction.followup.send("❌ No leaderboard data available for this period.", ephemeral=True)
            return
            
        medals = ['🥇', '🥈', '🥉']
        lines = []
        for e in entries:
            medal = medals[e['rank']-1] if e['rank'] <= 3 else f"`{e['rank']}.`"
            lines.append(f"{medal} **{e['username']}** — Level {e.get('level', 0)} · {e.get('xp_total', e.get('total_xp', 0)):,} XP")
            
        period_label = "All Time" if period == "all" else period.capitalize()
        embed = discord.Embed(
            title=f"📊 {period_label} Leaderboard",
            description="\n".join(lines),
            color=0xC4A35B
        )
        embed.set_footer(text=f"Top {len(entries)} members")
        embed.timestamp = discord.utils.utcnow()
        
        await interaction.channel.send(embed=embed)
        await interaction.followup.send("✅ Leaderboard posted!", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Leaderboard_PostCog(bot))
