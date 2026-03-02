import discord
from discord import app_commands
from discord.ext import commands
import httpx
from typing import Optional

class SearchCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    @app_commands.command(name="search", description="Search the web for information")
    @app_commands.describe(query="The search query")
    async def search(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer(thinking=True)
        
        try:
            # Use DuckDuckGo Instant Answer API or similar
            async with httpx.AsyncClient() as client:
                # This is a simple API for quick answers. For full results, more complex scraping or Google Search API would be needed.
                url = f"https://api.duckduckgo.com/?q={query}&format=json"
                r = await client.get(url)
                data = r.json()
                
                abstract = data.get("AbstractText", "")
                image_url = data.get("Image", "")
                source_url = data.get("AbstractURL", "")
                
                if not abstract:
                    # Fallback search results if no direct answer
                    results = data.get("RelatedTopics", [])
                    if results:
                        abstract = results[0].get("Text", "No direct answer found, check the link.")
                        source_url = results[0].get("FirstURL", "")

                if not abstract:
                    await interaction.followup.send(f"❌ No results found for: `{query}`", ephemeral=True)
                    return

                embed = discord.Embed(
                    title=f"🔍 Search: {query}",
                    description=abstract,
                    url=source_url,
                    color=0x00f2ff
                )
                if image_url:
                    if not image_url.startswith("http"):
                        image_url = "https://duckduckgo.com" + image_url
                    embed.set_thumbnail(url=image_url)
                
                embed.set_footer(text="Powered by DuckDuckGo", icon_url="https://duckduckgo.com/favicon.ico")
                
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            print(f"[Search] Error: {e}")
            await interaction.followup.send(f"❌ An error occurred while searching: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(SearchCog(bot))
