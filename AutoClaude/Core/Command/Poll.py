import discord
from discord import app_commands
from discord.ext import commands
import json
import time

class PollView(discord.ui.View):
    def __init__(self, bot, poll_id, options):
        super().__init__(timeout=None)
        self.bot = bot
        self.poll_id = poll_id
        self.options = options
        
        # Add buttons for each option
        for i in range(len(options)):
            button = discord.ui.Button(
                label=str(i + 1),
                custom_id=f"poll_vote_{poll_id}_{i}",
                style=discord.ButtonStyle.primary
            )
            button.callback = self.make_callback(i)
            self.add_item(button)

    def make_callback(self, index):
        async def callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)
            self.bot.msg_db.cast_poll_vote(self.poll_id, interaction.user.id, index)
            
            # Update the embed
            results, total = self.bot.msg_db.get_poll_results(self.poll_id)
            
            embed = interaction.message.embeds[0]
            new_desc = []
            for i, opt in enumerate(self.options):
                count = results.get(i, 0)
                pct = (count / total * 100) if total > 0 else 0
                new_desc.append(f"**{i+1}.** {opt} — {count} votes ({int(pct)}%)")
            
            embed.description = "\n".join(new_desc)
            embed.set_footer(text=f"Poll #{self.poll_id} · {total} total votes")
            
            await interaction.message.edit(embed=embed)
            await interaction.followup.send(f"✅ You voted for: **{self.options[index]}**", ephemeral=True)
        return callback

class PollCog(commands.GroupCog, group_name="poll", group_description="Create and manage polls"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    def _check_enabled(self, interaction: discord.Interaction):
        cfg = self.db.get_settings().get("commands_poll", {})
        return self.bot._check_perms(interaction, cfg)

    @app_commands.command(name="create", description="Create a new poll")
    @app_commands.describe(question="The poll question", options="Comma-separated options (2-10)", duration="Minutes until auto-close (optional)")
    async def create(self, interaction: discord.Interaction, question: str, options: str, duration: int = None):
        if not self._check_enabled(interaction): return
        
        opt_list = [o.strip() for o in options.split(",") if o.strip()]
        if len(opt_list) < 2 or len(opt_list) > 10:
            await interaction.response.send_message("❌ Please provide between 2 and 10 options.", ephemeral=True)
            return

        await interaction.response.defer()
        
        ends_at = time.time() + (duration * 60) if duration else None
        poll_id = self.bot.msg_db.create_poll(interaction.guild_id, interaction.channel_id, interaction.user.id, question, opt_list, ends_at)
        
        option_lines = [f"**{i+1}.** {opt} — 0 votes" for i, opt in enumerate(opt_list)]
        embed = discord.Embed(
            title=f"📊 Poll: {question}",
            description="\n".join(option_lines),
            color=0xC4A35B
        )
        footer = f"Poll #{poll_id}"
        if duration:
            footer += f" · Ends in {duration} minutes"
        embed.set_footer(text=footer)
        
        view = PollView(self.bot, poll_id, opt_list)
        message = await interaction.followup.send(embed=embed, view=view)
        
        self.bot.msg_db.set_poll_message(poll_id, message.id)

    @app_commands.command(name="close", description="Close a poll and show final results")
    @app_commands.describe(poll_id="The ID of the poll to close")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def close(self, interaction: discord.Interaction, poll_id: int):
        if not self._check_enabled(interaction): return
        
        await interaction.response.defer()
        poll = self.bot.msg_db.close_poll(poll_id)
        
        if not poll:
            await interaction.followup.send("❌ Poll not found.", ephemeral=True)
            return
            
        results, total = self.bot.msg_db.get_poll_results(poll_id)
        options = json.loads(poll['options'])
        
        result_lines = []
        for i, opt in enumerate(options):
            count = results.get(i, 0)
            pct = (count / total * 100) if total > 0 else 0
            result_lines.append(f"**{i+1}.** {opt} — {count} votes ({int(pct)}%)")
            
        embed = discord.Embed(
            title=f"🔒 Poll Closed: {poll['question']}",
            description="\n".join(result_lines),
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Final Result · {total} total votes")
        
        await interaction.followup.send(embed=embed)
        
        # Optionally edit the original message if found
        if poll['channel_id'] and poll['message_id']:
            try:
                channel = self.bot.get_channel(int(poll['channel_id']))
                if channel:
                    message = await channel.fetch_message(int(poll['message_id']))
                    await message.edit(embed=embed, view=None)
            except: pass

async def setup(bot: commands.Bot):
    await bot.add_cog(PollCog(bot))
