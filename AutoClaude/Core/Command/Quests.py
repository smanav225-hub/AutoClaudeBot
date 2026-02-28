import discord
from discord import app_commands
from discord.ext import commands

QUESTS = [
    {"id": "visit_introductions", "label": "Introduce yourself"},
    {"id": "pick_role", "label": "Pick a role"}
]

class QuestsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_quests", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="quests", description="View your onboarding quest progress")
    async def execute(self, interaction: discord.Interaction):
        if not self._check_enabled(interaction): return
        
        await interaction.response.defer(ephemeral=True)
        
        progress = await self.bot.msg_db.get_quest_progress(interaction.guild_id, interaction.user.id)
        completed_ids = [p['quest_id'] for p in progress if p['completed_at']]
        
        lines = []
        for q in QUESTS:
            done = q['id'] in completed_ids
            check = "~~" if done else ""
            icon = "✅" if done else "⬜"
            lines.append(f"{icon} {check}{q['label']}{check}")
            
        completed_count = len(completed_ids)
        total_count = len(QUESTS)
        
        embed = discord.Embed(
            title="🎯 Onboarding Quests",
            description="\n".join(lines),
            color=0xC4A35B
        )
        embed.set_footer(text=f"{completed_count}/{total_count} complete")
        
        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(QuestsCog(bot))
