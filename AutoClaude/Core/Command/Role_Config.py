import discord
from discord import app_commands
from discord.ext import commands

class Role_ConfigCog(commands.GroupCog, group_name="role-config", group_description="Configure self-assignable roles"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    @app_commands.command(name="add", description="Add a role to the self-assignable list")
    @app_commands.describe(role="Role to make self-assignable")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def add_assignable(self, interaction: discord.Interaction, role: discord.Role):
        try:
            self.bot.msg_db.set_self_assignable_role(interaction.guild_id, role.id, True)
            await interaction.response.send_message(f"✅ {role.mention} is now self-assignable. Members can use `/role add` to get it.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to update role config: {str(e)}", ephemeral=True)

    @app_commands.command(name="remove", description="Remove a role from the self-assignable list")
    @app_commands.describe(role="Role to remove from self-assignable list")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def remove_assignable(self, interaction: discord.Interaction, role: discord.Role):
        try:
            self.bot.msg_db.set_self_assignable_role(interaction.guild_id, role.id, False)
            await interaction.response.send_message(f"✅ {role.mention} is no longer self-assignable.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to update role config: {str(e)}", ephemeral=True)

    @app_commands.command(name="list", description="View all self-assignable roles")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def list_assignable(self, interaction: discord.Interaction):
        try:
            role_ids = self.bot.msg_db.get_self_assignable_roles(str(interaction.guild_id))
            if not role_ids:
                await interaction.response.send_message("No self-assignable roles configured. Use `/role-config add` to add some.", ephemeral=True)
                return
            lines = []
            for rid in role_ids:
                role = interaction.guild.get_role(int(rid))
                lines.append(f"• {role.mention if role else f'Unknown Role ({rid})'}")
            embed = discord.Embed(title="🎭 Self-Assignable Roles", description="\n".join(lines), color=0xC4A35B)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

    @app_commands.command(name="give", description="Give a role to a specific member")
    @app_commands.describe(member="Member to give the role to", role="Role to give")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def give_role(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        try:
            await member.add_roles(role)
            await interaction.response.send_message(f"✅ Given {role.mention} to {member.mention}.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to give that role. Check role hierarchy.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Role_ConfigCog(bot))
