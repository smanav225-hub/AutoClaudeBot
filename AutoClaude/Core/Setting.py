import re
import discord


class HiEmojiReactor(discord.Client):
    def __init__(self, db):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.message_content = True
        super().__init__(intents=intents)
        self.db = db
        self.token = db.token

    async def start_bot(self):
        if not self.token:
            print("[WARN] Discord token missing; HiEmojiReactor not started.")
            return
        try:
            await self.start(self.token)
        except Exception as exc:
            print(f"[HiEmojiReactor] Bot stopped: {exc}")

    async def on_ready(self):
        print(f"[HiEmojiReactor] Logged in as {self.user} (ID: {self.user.id})")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if not message.guild:
            return

        settings = self.db.get_settings()
        if not settings.get("hi_enabled"):
            return

        user_message = (message.content or "").lower()
        if re.search(r"\b(hi+|hello+)\b", user_message):
            emoji = settings.get("hi_emoji") or "👋"
            try:
                await message.add_reaction(emoji)
            except Exception as exc:
                print(f"[HiEmojiReactor] Failed to react: {exc}")
