import discord
from discord import app_commands
from discord.ext import commands

ACHIEVEMENTS = [
    {"id": "level_5", "name": "Novice", "level": 5, "description": "Reached Level 5"},
    {"id": "level_10", "name": "Apprentice", "level": 10, "description": "Reached Level 10"},
    {"id": "level_20", "name": "Expert", "level": 20, "description": "Reached Level 20"},
    {"id": "level_50", "name": "Master", "level": 50, "description": "Reached Level 50"},
]

class AchievementsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_achievements", {})
        return self.bot._check_perms(interaction, cfg)

    async def check_and_award_achievements(self, guild_id, user_id, current_level):
        for ach in ACHIEVEMENTS:
            if current_level >= ach['level']:
                self.bot.msg_db.award_achievement(guild_id, user_id, ach['id'])

    @app_commands.command(name="achievements", description="View achievement progress")
    @app_commands.describe(user="User to view (defaults to you)")
    async def execute(self, interaction: discord.Interaction, user: discord.Member = None):
        if not self._check_enabled(interaction): return
        
        target = user or interaction.user
        await interaction.response.defer(ephemeral=True)
        
        # Sync achievements based on current level
        user_data = self.bot.msg_db.get_user_level(interaction.guild_id, target.id)
        if user_data:
            await self.check_and_award_achievements(interaction.guild_id, target.id, user_data.get('level', 0))
            
        unlocked = self.bot.msg_db.get_user_achievements(interaction.guild_id, target.id)
        unlocked_ids = {a['achievement_id']: a['unlocked_at'] for a in unlocked}
        
        lines = []
        for ach in ACHIEVEMENTS:
            unlocked_at = unlocked_ids.get(ach['id'])
            if unlocked_at:
                date_str = datetime.fromtimestamp(unlocked_at).strftime("%b %d, %Y")
                lines.append(f"✅ **{ach['name']}** — Level {ach['level']}\n*    {ach['description']}* • {date_str}")
            else:
                lines.append(f"◽ ~~{ach['name']}~~ — Level {ach['level']}\n*    {ach['description']}*")
                
        count = len(unlocked_ids)
        total = len(ACHIEVEMENTS)
        
        embed = discord.Embed(
            title=f"🏆 {target.display_name}'s Achievements",
            description="\n\n".join(lines),
            color=0xC4A35B
        )
        embed.set_footer(text=f"{count} / {total} achievements unlocked")
        embed.set_thumbnail(url=target.display_avatar.url)
        
        await interaction.followup.send(embed=embed, ephemeral=True)

from datetime import datetime

async def setup(bot: commands.Bot):
    await bot.add_cog(AchievementsCog(bot))
