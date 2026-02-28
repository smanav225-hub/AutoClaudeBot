import discord
from discord import app_commands
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_help", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="help", description="View all available user commands")
    async def execute(self, interaction: discord.Interaction):
        # Help is always public - don't gatekeep it
        grouped = {}
        for cmd in self.bot.tree.get_commands():
            # Skip admin-only commands
            if cmd.name in ["xp", "moderation", "help_admin", "backup", "role_config", "reputation_config", "punishment", "analytics"]:
                continue
                
            cat = CATEGORY_MAPPING.get(cmd.name, "Other")
            if cat not in grouped:
                grouped[cat] = []
            
            if isinstance(cmd, app_commands.Group):
                for sub in cmd.commands:
                    grouped[cat].append(f"`/{cmd.name} {sub.name}` — {sub.description}")
            else:
                grouped[cat].append(f"`/{cmd.name}` — {cmd.description}")

        embed = discord.Embed(
            title="📖 AutoClaude Bot — Commands",
            description="Here's everything you can do:",
            color=0xC4A35B
        )
        
        for cat, lines in sorted(grouped.items()):
            if lines:
                embed.add_field(name=cat, value="\n".join(lines[:10]), inline=False)
                
        embed.set_footer(text="Moderators: use /help_admin for admin commands")
        await interaction.response.send_message(embed=embed, ephemeral=True)

# Add mapping outside the class or as class attribute
CATEGORY_MAPPING = {
    "xp": "XP & Leveling",
    "level": "XP & Leveling",
    "leaderboard": "XP & Leveling",
    "thank": "Reputation",
    "profile": "XP & Leveling",
    "quests": "Quests & Roles",
    "poll": "Community",
    "moderation": "Moderation",
    "afk": "Community",
    "ping": "Utility",
    "help": "Utility",
    "achievements": "XP & Leveling",
    "events": "Events",
}

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCog(bot))
