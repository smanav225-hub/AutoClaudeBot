import discord
from discord import app_commands
from discord.ext import commands

class Help_AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_help_admin", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="help-admin", description="View administrative help and commands")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def execute(self, interaction: discord.Interaction):
        if not self._check_enabled(interaction): return
        
        admin_cmds = ["xp", "moderation", "backup", "role_config", "reputation_config", "ticket_setup", "level_rewards", "autorole"]
        
        grouped = {}
        for cmd in self.bot.tree.get_commands():
            if cmd.name not in admin_cmds:
                continue
                
            cat = ADMIN_CATEGORY_MAPPING.get(cmd.name, "Configuration")
            if cat not in grouped: grouped[cat] = []
            
            if isinstance(cmd, app_commands.Group):
                for sub in cmd.commands:
                    grouped[cat].append(f"`/{cmd.name} {sub.name}` — {sub.description}")
            else:
                grouped[cat].append(f"`/{cmd.name}` — {cmd.description}")

        embed = discord.Embed(
            title="🛡️ AutoClaude Bot — Admin Commands",
            description="Restricted to server administrators:",
            color=discord.Color.red()
        )
        
        for cat, lines in sorted(grouped.items()):
            if lines:
                embed.add_field(name=cat, value="\n".join(lines), inline=False)
                
        await interaction.response.send_message(embed=embed, ephemeral=True)

ADMIN_CATEGORY_MAPPING = {
    "xp": "XP Management",
    "moderation": "Moderation",
    "backup": "System",
    "role_config": "Roles",
    "reputation_config": "Reputation",
    "ticket_setup": "Tickets",
    "level_rewards": "Xp & Leveling",
    "autorole": "Roles"
}

async def setup(bot: commands.Bot):
    await bot.add_cog(Help_AdminCog(bot))
