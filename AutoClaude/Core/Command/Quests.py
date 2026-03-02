import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import time

QUESTS = [
    {"id": "msgs_20", "label": "Chatter", "desc": "Send 20 messages", "type": "count", "target": 20},
    {"id": "replies_5", "label": "Engager", "desc": "Reply to 5 people messages", "type": "reply_count", "target": 5},
    {"id": "level_5", "label": "Rising Star", "desc": "Reach level 5 in the server", "type": "level", "target": 5},
    {"id": "emojis_10", "label": "Expressive", "desc": "Use 10 emoji", "type": "emoji_sum", "target": 10}
]

class QuestsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_quests", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="quests", description="View your server quest progress")
    async def execute(self, interaction: discord.Interaction):
        if not self._check_enabled(interaction): return
        
        await interaction.response.defer(ephemeral=True)
        guild_id = str(interaction.guild_id)
        user_id = str(interaction.user.id)
        
        # 1. Fetch live user data
        user_level_data = self.bot.msg_db.get_user_level(guild_id, user_id) or {}
        existing_progress = await self.bot.msg_db.get_quest_progress(guild_id, user_id)
        completed_ids = [p['quest_id'] for p in existing_progress]
        
        lines = []
        newly_completed = 0
        conn = self.bot.msg_db.get_connection()
        cur = conn.cursor()
        
        for q in QUESTS:
            is_done = q['id'] in completed_ids
            current_val = 0
            
            if not is_done:
                # LIVE BACKEND CHECKS
                if q['type'] == "count":
                    current_val = int(user_level_data.get('messages_total', 0))
                elif q['type'] == "level":
                    current_val = int(user_level_data.get('level', 0))
                elif q['type'] == "reply_count":
                    cur.execute("SELECT COUNT(*) FROM messages WHERE user_id=? AND reply_to_user_id IS NOT NULL", (user_id,))
                    current_val = cur.fetchone()[0]
                elif q['type'] == "emoji_sum":
                    cur.execute("SELECT SUM(emoji_count) FROM messages WHERE user_id=?", (user_id,))
                    res = cur.fetchone()[0]
                    current_val = int(res) if res else 0
                
                if current_val >= q['target']:
                    await self.bot.msg_db.complete_quest(guild_id, user_id, q['id'])
                    is_done = True
                    newly_completed += 1

            # Build Display Line
            icon = "✅" if is_done else "⬜"
            strike = "~~" if is_done else ""
            prog = f" ({current_val}/{q['target']})" if not is_done and current_val > 0 else ""
            lines.append(f"{icon} {strike}**{q['label']}**: {q['desc']}{strike}{prog}")
            
        conn.close()
        
        embed = discord.Embed(
            title="🎯 Server Quests",
            description="\n".join(lines),
            color=0x5865F2 if newly_completed == 0 else 0x57F287
        )
        if newly_completed > 0:
            embed.set_author(name=f"🎉 Congratulations! You finished {newly_completed} new quests!")
            
        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(QuestsCog(bot))
