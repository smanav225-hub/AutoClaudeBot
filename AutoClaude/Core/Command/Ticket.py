import discord
from discord import app_commands
from discord.ext import commands

import json

class TicketCog(commands.GroupCog, group_name="ticket", group_description="Create and manage support tickets"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_ticket", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="create", description="Create a new support ticket")
    @app_commands.describe(subject="Brief description of your issue")
    async def create(self, interaction: discord.Interaction, subject: str):
        if not self._check_enabled(interaction): return
        
        guild_id = str(interaction.guild_id)
        config = self.db.get_config(guild_id, "tickets") or {}
        category_id = config.get("category_id")
        
        if not category_id:
            await interaction.response.send_message("❌ Ticket system is not configured. An admin must run `/ticket-setup` first.", ephemeral=True)
            return
            
        category = interaction.guild.get_channel(int(category_id))
        if not category or not isinstance(category, discord.CategoryChannel):
            await interaction.response.send_message("❌ Configuration error: Ticket category not found.", ephemeral=True)
            return
            
        await interaction.response.defer(ephemeral=True)
        
        # Create private channel
        user_clean = "".join(c for c in interaction.user.name.lower() if c.isalnum())
        channel_name = f"ticket-{user_clean}-{interaction.user.id % 1000}"
        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, manage_channels=True)
        }
        
        try:
            channel = await interaction.guild.create_text_channel(
                name=channel_name,
                category=category,
                overwrites=overwrites,
                reason=f"Ticket created by {interaction.user}"
            )
            
            ticket_row = self.bot.msg_db.create_ticket(guild_id, channel.id, interaction.user.id, subject)
            
            embed = discord.Embed(
                title=f"Ticket #{ticket_row['id']}",
                description=f"**Subject:** {subject}",
                color=0xC4A35B
            )
            embed.add_field(name="Opened by", value=interaction.user.mention, inline=True)
            embed.add_field(name="Status", value="🟢 Open", inline=True)
            embed.set_footer(text="Use /ticket close to close this ticket")
            embed.timestamp = discord.utils.utcnow()
            
            await channel.send(embed=embed)
            await interaction.followup.send(f"✅ Ticket created: {channel.mention}", ephemeral=True)
            
        except discord.Forbidden:
            await interaction.followup.send("❌ I don't have permission to create channels in that category.", ephemeral=True)

    @app_commands.command(name="close", description="Close the current ticket")
    async def close(self, interaction: discord.Interaction):
        if not self._check_enabled(interaction): return
        
        ticket_row = self.bot.msg_db.get_ticket_by_channel(interaction.channel_id)
        if not ticket_row:
            await interaction.response.send_message("❌ This channel is not an open ticket.", ephemeral=True)
            return
            
        # Permission check
        is_creator = str(interaction.user.id) == ticket_row['user_id']
        is_admin = interaction.user.guild_permissions.manage_channels
        
        if not (is_creator or is_admin):
            await interaction.response.send_message("❌ Only the ticket creator or an admin can close this ticket.", ephemeral=True)
            return
            
        await interaction.response.defer()
        
        # Collect transcript (simplified)
        messages = []
        async for msg in interaction.channel.history(limit=100, oldest_first=True):
            messages.append({
                "author": msg.author.name,
                "content": msg.content or "[Embed/Attachment]",
                "ts": msg.created_at.timestamp()
            })
            
        transcript_json = json.dumps(messages)
        self.bot.msg_db.close_ticket(ticket_row['id'], interaction.user.id, transcript_json)
        
        # Update permissions
        try:
            creator = interaction.guild.get_member(int(ticket_row['user_id']))
            if creator:
                await interaction.channel.set_permissions(creator, view_channel=False, send_messages=False)
        except:
            pass
            
        embed = discord.Embed(
            title=f"Ticket #{ticket_row['id']} Closed",
            description=f"Closed by {interaction.user.mention}\nTranscript saved ({len(messages)} messages).",
            color=0xED4245
        )
        await interaction.followup.send(embed=embed)
        
        # Add delete button (optional - skipping complex view for now to stay fast)
        await interaction.followup.send("This channel can now be deleted manually by an admin.")

    @app_commands.command(name="list", description="List all open tickets in this server")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def list_tickets(self, interaction: discord.Interaction):
        try:
            conn = self.bot.msg_db.get_connection()
            conn.row_factory = __import__('sqlite3').Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM tickets WHERE guild_id=? AND status='open' ORDER BY id ASC",
                (str(interaction.guild_id),)
            )
            rows = cursor.fetchall()
            conn.close()

            if not rows:
                await interaction.response.send_message("✅ No open tickets right now.", ephemeral=True)
                return

            embed = discord.Embed(title="🎟️ Open Tickets", color=0xC4A35B)
            for t in rows:
                channel = interaction.guild.get_channel(int(t['channel_id']))
                ch_str = channel.mention if channel else f"Unknown channel"
                embed.add_field(
                    name=f"Ticket #{t['id']}",
                    value=f"**Subject:** {t['subject']}\n**User:** <@{t['user_id']}>\n**Channel:** {ch_str}",
                    inline=False
                )
            embed.set_footer(text=f"{len(rows)} open ticket(s) | Use /ticket close in the ticket channel to close")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(TicketCog(bot))
