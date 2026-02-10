import re
import discord
import asyncio

class HiEmojiReactor:
    """
    Component that automatically reacts to 'hi' or 'hello' messages with a configured emoji.
    Integrated into the main bot as an event listener.
    """
    def __init__(self, db):
        self.db = db

    async def on_message(self, message):
        # Ignore messages from the bot itself or outside of a guild
        if not message.author or message.author.bot:
            return
        if not message.guild:
            return

        # Fetch current settings from database
        settings = self.db.get_settings()
        enabled = settings.get("hi_enabled")
        selected_emoji = settings.get("hi_emoji") or "👋"

        # Check for matching keywords (hi, hello)
        user_message = (message.content or "").lower()
        if re.search(r"\b(hi+|hello+)\b", user_message):
            try:
                # Wait a split second to catch reactions from other stale bot processes
                await asyncio.sleep(0.5)
                
                # Proactive Cleanup Phase
                # We re-fetch the message to get the absolute latest reaction state
                full_msg = await message.channel.fetch_message(message.id)
                
                for reaction in full_msg.reactions:
                    if reaction.me:
                        # If feature is disabled, remove all our reactions.
                        # If enabled, remove any reaction that isn't the currently selected emoji.
                        if not enabled or str(reaction.emoji) != selected_emoji:
                            await full_msg.remove_reaction(reaction.emoji, message.guild.me)

                # Add Phase: Only add if enabled AND we haven't already reacted with it
                if enabled:
                    # Refresh check after potential cleanup
                    already_reacted = any(
                        r.me and str(r.emoji) == selected_emoji 
                        for r in full_msg.reactions
                    )
                    if not already_reacted:
                        await full_msg.add_reaction(selected_emoji)
            except Exception:
                # Silently fail if we lack permissions or message is gone
                pass
