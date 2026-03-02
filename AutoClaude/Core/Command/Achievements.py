import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

ACHIEVEMENTS = [
    # --- Level Milestones ---
    {"id": "level_5", "name": "Novice", "type": "level", "threshold": 5, "description": "Reach Level 5"},
    {"id": "level_10", "name": "Apprentice", "type": "level", "threshold": 10, "description": "Reach Level 10"},
    {"id": "level_20", "name": "Expert", "type": "level", "threshold": 20, "description": "Reach Level 20"},
    {"id": "level_25", "name": "Veteran", "type": "level", "threshold": 25, "description": "Reach Level 25"},
    {"id": "level_30", "name": "Elite", "type": "level", "threshold": 30, "description": "Reach Level 30"},
    {"id": "level_35", "name": "Champion", "type": "level", "threshold": 35, "description": "Reach Level 35"},
    {"id": "level_40", "name": "Legend", "type": "level", "threshold": 40, "description": "Reach Level 40"},
    {"id": "level_45", "name": "Mythic", "type": "level", "threshold": 45, "description": "Reach Level 45"},
    {"id": "level_50", "name": "Master", "type": "level", "threshold": 50, "description": "Reach Level 50"},
    
    # --- Message Count Milestones ---
    {"id": "msgs_100", "name": "Chatter", "type": "messages", "threshold": 100, "description": "Send 100 messages"},
    {"id": "msgs_1000", "name": "Talkative", "type": "messages", "threshold": 1000, "description": "Send 1,000 messages"},
    {"id": "msgs_10000", "name": "Socialite", "type": "messages", "threshold": 10000, "description": "Send 10,000 messages"},
]

class AchievementsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_achievements", {})
        return self.bot._check_perms(interaction, cfg)

    async def check_and_award_achievements(self, guild_id, user_id, user_data):
        current_level = int(user_data.get('level', 0))
        total_msgs = int(user_data.get('messages_total', 0))
        
        for ach in ACHIEVEMENTS:
            awarded = False
            if ach['type'] == "level" and current_level >= ach['threshold']:
                awarded = True
            elif ach['type'] == "messages" and total_msgs >= ach['threshold']:
                awarded = True
                
            if awarded:
                self.bot.msg_db.award_achievement(guild_id, user_id, ach['id'])

    def _generate_progress_bar(self, current, total, length=10):
        if total <= 0: return "░" * length
        filled = min(length, int((current / total) * length))
        return "▰" * filled + "▱" * (length - filled)

    @app_commands.command(name="achievements", description="View achievement progress and live levels")
    @app_commands.describe(user="User to view (defaults to you)")
    async def execute(self, interaction: discord.Interaction, user: discord.Member = None):
        if not self._check_enabled(interaction): return
        
        target = user or interaction.user
        await interaction.response.defer(ephemeral=False)
        
        # 1. Fetch Live Level Data
        user_data = self.bot.msg_db.get_user_level(interaction.guild_id, target.id)
        if not user_data:
            return await interaction.followup.send(f"No level data found for {target.display_name}. Start chatting first!", ephemeral=True)

        current_level = int(user_data.get('level', 0))
        xp_total = int(user_data.get('xp_total', 0))
        xp_current = int(user_data.get('xp_current', 0))
        total_msgs = int(user_data.get('messages_total', 0))
        
        # 2. Get Formula and calculate next level
        xp_cfg = self.db.get_xp_config(str(interaction.guild_id))
        xp_needed = self.bot.msg_db._xp_needed(current_level, xp_cfg['formula'])
        
        # 3. Sync achievements (Additive & Live)
        await self.check_and_award_achievements(interaction.guild_id, target.id, user_data)
            
        # 4. Get unlocked list
        unlocked = self.bot.msg_db.get_user_achievements(interaction.guild_id, target.id)
        unlocked_ids = {a['achievement_id']: a['unlocked_at'] for a in unlocked}
        
        # 5. Build Achievement List
        lines = []
        for ach in ACHIEVEMENTS:
            unlocked_at = unlocked_ids.get(ach['id'])
            if unlocked_at:
                date_str = datetime.fromtimestamp(unlocked_at).strftime("%b %d, %Y")
                lines.append(f"✅ **{ach['name']}** — {ach['description']}\n*Unlocked on {date_str}*")
            else:
                lines.append(f"◽ ~~{ach['name']}~~ — {ach['description']}")
        
        # 6. Get Rank
        rank = self.bot.msg_db.get_user_rank(interaction.guild_id, target.id)
        
        # 7. Create Embed
        progress_bar = self._generate_progress_bar(xp_current, xp_needed)
        pct = int((xp_current / xp_needed) * 100) if xp_needed > 0 else 0
        
        embed = discord.Embed(
            title=f"🏆 {target.display_name}'s Achievements",
            color=0xC4A35B
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        
        embed.add_field(name="Live Level Stats", value=(
            f"**Level {current_level}** | **Rank #{rank or 'N/A'}**\n"
            f"XP: `{xp_current:,} / {xp_needed:,}`\n"
            f"`{progress_bar}` **{pct}%**"
        ), inline=False)
        
        # Split milestones into groups if too long
        embed.add_field(name="Milestones", value="\n\n".join(lines[:10]), inline=False)
        if len(lines) > 10:
            embed.add_field(name="Advanced Milestones", value="\n\n".join(lines[10:]), inline=False)
        
        count = len(unlocked_ids)
        total = len(ACHIEVEMENTS)
        embed.set_footer(text=f"{count} / {total} achievements unlocked • Total Messages: {total_msgs:,}")
        
        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(AchievementsCog(bot))
