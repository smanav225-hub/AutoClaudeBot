import discord
from discord import app_commands
from discord.ext import commands

import datetime

class Health_CheckCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_health_check", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="health-check", description="Force an immediate health metrics rollup for the previous hour")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def execute(self, interaction: discord.Interaction):
        if not self._check_enabled(interaction): return
        
        await interaction.response.defer(ephemeral=True)
        
        # Current bucket: previous full hour
        now = datetime.datetime.now(datetime.timezone.utc)
        bucket_end = now.replace(minute=0, second=0, microsecond=0)
        bucket_start = bucket_end - datetime.timedelta(hours=1)
        
        start_ts = bucket_start.timestamp()
        end_ts = bucket_end.timestamp()
        
        guild_id = str(interaction.guild_id)
        # These are synchronous in Message_Database.py
        self.bot.msg_db.compute_hourly_rollup(guild_id, start_ts, end_ts)
        row = self.bot.msg_db.get_health_rollup(guild_id, start_ts)
        
        fmt = lambda ts: datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime("%H:%M")
        
        embed = discord.Embed(
            title="📊 Health Metrics Rollup",
            description=f"Bucket: **{fmt(start_ts)} – {fmt(end_ts)} UTC**",
            color=0xC4A35B
        )
        
        if row:
            embed.add_field(name="Messages", value=str(row.get('message_count', 0)), inline=True)
            embed.add_field(name="Active Users", value=str(row.get('active_users', 0)), inline=True)
            embed.add_field(name="Reputation Given", value=str(row.get('reputation_given', 0)), inline=True)
        else:
            embed.description += "\n\n*No data found for this period.*"
            
        embed.timestamp = discord.utils.utcnow()
        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Health_CheckCog(bot))
