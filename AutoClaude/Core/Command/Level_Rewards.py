import discord
from discord import app_commands
from discord.ext import commands

class Level_RewardsCog(commands.GroupCog, group_name="level-rewards", group_description="Manage level-up DM notifications and milestone role rewards"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_level_rewards", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="dm", description="Toggle DM notifications on level-up")
    @app_commands.describe(enabled="Enable or disable level-up DMs")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def toggle_dm(self, interaction: discord.Interaction, enabled: bool):
        if not self._check_enabled(interaction): return
        
        guild_id = str(interaction.guild_id)
        config = self.db.get_config(guild_id, "levels") or {}
        config["dm_enabled"] = enabled
        self.db.save_config(guild_id, "levels", config)
        
        status = "enabled" if enabled else "disabled"
        await interaction.response.send_message(f"✅ Level-up DMs **{status}**.", ephemeral=True)

    @app_commands.command(name="set", description="Assign a role to be granted at a specific level")
    @app_commands.describe(level="The level to reward", role="The role to grant")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def set_reward(self, interaction: discord.Interaction, level: int, role: discord.Role):
        if not self._check_enabled(interaction): return
        
        guild_id = str(interaction.guild_id)
        config = self.db.get_config(guild_id, "levels") or {}
        rewards = config.get("milestone_roles", {})
        rewards[str(level)] = str(role.id)
        config["milestone_roles"] = rewards
        self.db.save_config(guild_id, "levels", config)
        
        await interaction.response.send_message(f"✅ Level **{level}** will now grant the {role.mention} role.", ephemeral=True)

    @app_commands.command(name="remove", description="Remove a milestone role for a level")
    @app_commands.describe(level="The level to remove")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def remove_reward(self, interaction: discord.Interaction, level: int):
        if not self._check_enabled(interaction): return
        
        guild_id = str(interaction.guild_id)
        config = self.db.get_config(guild_id, "levels") or {}
        rewards = config.get("milestone_roles", {})
        if str(level) in rewards:
            del rewards[str(level)]
            config["milestone_roles"] = rewards
            self.db.save_config(guild_id, "levels", config)
            await interaction.response.send_message(f"✅ Milestone role for level **{level}** removed.", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ No milestone role configured for level **{level}**.", ephemeral=True)

    @app_commands.command(name="list", description="List all milestone role rewards")
    async def list_rewards(self, interaction: discord.Interaction):
        if not self._check_enabled(interaction): return
        
        guild_id = str(interaction.guild_id)
        config = self.db.get_config(guild_id, "levels") or {}
        rewards = config.get("milestone_roles", {})
        
        if not rewards:
            dm_status = "enabled" if config.get("dm_enabled") else "disabled"
            await interaction.response.send_message(f"No milestone roles configured. DMs: **{dm_status}**", ephemeral=True)
            return
            
        # Sort by level
        sorted_rewards = sorted(rewards.items(), key=lambda x: int(x[0]))
        lines = [f"Level **{lvl}** → <@&{rid}>" for lvl, rid in sorted_rewards]
        
        embed = discord.Embed(
            title="🏆 Level Rewards",
            description="\n".join(lines),
            color=0xC4A35B
        )
        dm_status = "enabled" if config.get("dm_enabled") else "disabled"
        embed.set_footer(text=f"Level-up DMs: {dm_status}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Level_RewardsCog(bot))
