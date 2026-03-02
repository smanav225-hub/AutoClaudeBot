import discord
from discord import app_commands
from discord.ext import commands

class AutoroleCog(commands.GroupCog, group_name="autorole", group_description="Configure automatic role assignment for new members"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_autorole", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="set", description="Set the role to auto-assign to new members")
    @app_commands.describe(role="Role to assign on join")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def set_role(self, interaction: discord.Interaction, role: discord.Role):
        if not self._check_enabled(interaction): return
        
        # Bot role hierarchy check
        bot_top_role = interaction.guild.me.top_role
        if bot_top_role.position <= role.position:
            await interaction.response.send_message(
                f"❌ Cannot assign **{role.name}** as an auto-role!\n\n"
                f"📊 **Discord Role Hierarchy:**\n"
                f"• Bot's highest role: **{bot_top_role.name}** (position {bot_top_role.position})\n"
                f"• Role you selected: **{role.name}** (position {role.position})\n\n"
                f"✅ **Fix:** Go to Server Settings → Roles and move **AutoClaude Bot**'s role **above** `{role.name}`",
                ephemeral=True
            )
            return
            
        guild_id = str(interaction.guild_id)
        config = self.db.get_config(guild_id, "autorole") or {}
        config["role_id"] = str(role.id)
        config["enabled"] = True
        self.db.save_config(guild_id, "autorole", config)
        
        await interaction.response.send_message(
            f"✅ Auto-role set to {role.mention}.\n"
            f"New members will automatically receive this role when they join.",
            ephemeral=True
        )

    @app_commands.command(name="remove", description="Remove the auto-role setting")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def remove_role(self, interaction: discord.Interaction):
        if not self._check_enabled(interaction): return
        
        guild_id = str(interaction.guild_id)
        config = self.db.get_config(guild_id, "autorole") or {}
        if not config.get("role_id"):
            await interaction.response.send_message("❌ No auto-role is currently configured.", ephemeral=True)
            return
            
        config["role_id"] = None
        self.db.save_config(guild_id, "autorole", config)
        await interaction.response.send_message("✅ Auto-role has been removed.", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild_id = str(member.guild.id)
        config = self.db.get_config(guild_id, "autorole") or {}
        role_id = config.get("role_id")
        
        if role_id:
            role = member.guild.get_role(int(role_id))
            if role:
                try:
                    await member.add_roles(role, reason="Auto-role on join")
                except discord.Forbidden:
                    print(f"[Autorole] Failed to add role to {member.name} in {member.guild.name} (Forbidden)")

async def setup(bot: commands.Bot):
    await bot.add_cog(AutoroleCog(bot))
