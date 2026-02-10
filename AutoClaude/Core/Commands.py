import discord
from discord import app_commands
from discord.ext import commands
import requests
import io
import os
import re
import asyncio
from typing import List, Optional, Tuple
import ast
from Message_Database import MessageDBHandler
from Core.Leaderboard_Command import LeaderboardQueryView, build_ui_text

def _get_color_emoji(color: discord.Color) -> str:
    if color.value == 0: return "⚪"
    target_rgb = (color.r, color.g, color.b)
    emoji_colors = {
        "🔴": (221, 46, 68), "🟠": (244, 144, 12), "🟡": (253, 203, 88),
        "🟢": (120, 177, 89), "🔵": (85, 172, 238), "🟣": (170, 142, 214),
        "🟤": (193, 105, 79), "⚫": (49, 55, 61), "⚪": (230, 231, 232)
    }
    def color_distance(c1, c2): return sum((a - b) ** 2 for a, b in zip(c1, c2))
    return min(emoji_colors.keys(), key=lambda e: color_distance(emoji_colors[e], target_rgb))

# --- GitHub Logic Helper (Optimized for Images & Files) ---
class GitHubRepo:
    def __init__(self, token=None):
        self.token = token
        self.owner = "AndyMik90"
        self.repo = "Auto-Claude"
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if token and token.strip():
            self.headers["Authorization"] = f"token {token.strip()}"
        self.tree_cache = []

    async def fetch_tree(self) -> bool:
        self.tree_cache = []
        for branch in ["main", "master"]:
            url = f"https://api.github.com/repos/{self.owner}/{self.repo}/git/trees/{branch}?recursive=1"
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    self.tree_cache = response.json().get("tree", [])
                    return True
            except: continue
        return False

    def search(self, query: str) -> List[str]:
        if not self.tree_cache: return []
        q = query.lower()
        results = []
        for item in self.tree_cache:
            if item["type"] != "blob": continue
            path = item["path"]
            filename = path.split("/")[-1].lower()
            if not q or q in path.lower() or q == filename:
                results.append(path)
        
        results.sort(key=lambda x: (q not in x.split("/")[-1].lower(), len(x)))
        return results[:25]

    async def download_file(self, path: str) -> Tuple[Optional[bytes], Optional[str]]:
        target_item = next((item for item in self.tree_cache if item["path"] == path and item["type"] == "blob"), None)
        if not target_item or not target_item.get("url"):
            return None, None

        headers = self.headers.copy()
        headers["Accept"] = "application/vnd.github.v3.raw"
        try:
            response = requests.get(target_item["url"], headers=headers, timeout=20)
            if response.status_code == 200:
                return response.content, path
        except:
            pass
        return None, None

# --- Unified Command Bot ---
class IntegratedCommandBot(commands.Bot):
    def __init__(self, db):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)
        self.db = db
        self.token = db.token
        self.github_token = self._get_best_github_token()
        self.repo_manager = GitHubRepo(self.github_token)
        self.msg_db = MessageDBHandler()
        self.analytics_group = app_commands.Group(name="analytics", description="Server analytics commands")

    def _get_best_github_token(self):
        # 1. Try Database (Primary Source)
        db_token = self.db.get_github_token()
        if db_token: return db_token
        # 2. Try Token.txt (Fallback)
        try:
            paths = [
                os.path.join(os.getcwd(), "Token.txt"),
                os.path.join(os.path.dirname(__file__), "..", "Token.txt")
            ]
            for p in paths:
                if os.path.exists(p):
                    with open(p, "r") as f:
                        for line in f:
                            if "github_pat_" in line: return line.strip()
        except: pass
        return None

    async def setup_hook(self):
        # 1. Analytics Command
        @self.analytics_group.command(name="member", description="View server member analytics by role")
        async def member_analytics(interaction: discord.Interaction):
            cfg = self.db.get_settings().get("commands_analytics", {})
            if not self._check_perms(interaction, cfg): return
            
            await interaction.response.defer()
            guild = interaction.guild
            human_members = [m for m in guild.members if not m.bot]
            roles = sorted(guild.roles, key=lambda r: r.position, reverse=True)
            
            booster_role = guild.premium_subscriber_role
            booster_emoji = "🟣"
            if booster_role: booster_emoji = _get_color_emoji(booster_role.color)
            
            lines = ["**Server Member Analytics**", "", f"🟡 Members: {len(human_members)}"]
            boosters = len([m for m in guild.premium_subscribers if not m.bot])
            lines.append(f"{booster_emoji} Server Boosters: {boosters}")
            lines.append("\n**Roles Breakdown:**")
            
            for role in roles:
                if role.name == "@everyone" or role.managed: continue
                count = len([m for m in role.members if not m.bot])
                emoji = _get_color_emoji(role.color)
                lines.append(f"{emoji} {role.name}: {count}")
                
            await interaction.followup.send("\n".join(lines)[:2000])

        # 2. GitHub Command
        @self.tree.command(name="github", description="Search and download files/images from Auto-Claude repository")
        @app_commands.describe(query="Path or name of the file to download")
        async def github(interaction: discord.Interaction, query: str):
            cfg = self.db.get_settings().get("commands_github", {})
            if not self._check_perms(interaction, cfg): return
            
            if not self.repo_manager.tree_cache:
                await interaction.response.send_message("❌ GitHub repository data not loaded.", ephemeral=True)
                return

            await interaction.response.defer()
            file_data, filename = await self.repo_manager.download_file(query)
            
            if file_data:
                if len(file_data) > 8 * 1024 * 1024:
                    await interaction.followup.send(f"❌ File `{filename}` is too large (max 8MB).")
                    return
                
                is_image = filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
                display_name = filename.split("/")[-1]
                file_obj = discord.File(io.BytesIO(file_data), filename=display_name)
                
                if is_image:
                    await interaction.followup.send(content=f"📸 **{filename}**", file=file_obj)
                else:
                    await interaction.followup.send(content=f"📄 **{filename}**", file=file_obj)
            else:
                results = self.repo_manager.search(query)
                if results:
                    embed = discord.Embed(title="Search Results", description="\n".join([f"📄 {r}" for r in results[:10]]), color=discord.Color.blue())
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.followup.send(f"❌ Could not find file `{query}`.")

        @github.autocomplete("query")
        async def github_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
            if not self.repo_manager: return []
            choices = self.repo_manager.search(current)
            return [app_commands.Choice(name=f"📄 {c}", value=c) for c in choices]

        # 3. Level Command
        @self.tree.command(name="level", description="Show your rank card")
        async def level(interaction: discord.Interaction):
            cfg = self.db.get_settings().get("commands_level", {})
            if not self._check_perms(interaction, cfg): return

            await interaction.response.defer(ephemeral=False)
            guild_id = str(interaction.guild_id)
            user_id = str(interaction.user.id)
            user_data = self.msg_db.get_user_level(guild_id, user_id)
            if not user_data:
                await interaction.followup.send("No level data found yet. Send some messages first.")
                return

            levels_cfg = self.db.get_config(guild_id, "levels") or {}
            formula = levels_cfg.get("formula", "5 * (level ** 2) + (50 * level) + 100")
            level_val = int(user_data.get("level", 0) or 0)
            xp_current = int(user_data.get("xp_current", 0) or 0)
            xp_needed = self._xp_needed(level_val, formula)
            rank = self.msg_db.get_user_rank(guild_id, user_id) or 0

            embed = discord.Embed(color=0x5865F2, title="Rank Card")
            embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.display_avatar.url))
            embed.add_field(name="Rank", value=f"#{rank}" if rank else "N/A", inline=True)
            embed.add_field(name="Level", value=str(level_val), inline=True)
            embed.add_field(name="XP", value=f"{xp_current}/{xp_needed} XP", inline=True)
            await interaction.followup.send(embed=embed)

        # 4. Leaderboard Command
        @self.tree.command(name="leaderboard", description="Query the leaderboard with custom filters")
        async def leaderboard(interaction: discord.Interaction):
            cfg = self.db.get_settings().get("commands_leaderboard", {})
            if not self._check_perms(interaction, cfg): return

            view = LeaderboardQueryView(interaction.guild_id)
            embed = discord.Embed(title="📊 Leaderboard Query Builder", color=discord.Color.blurple())
            embed.description = build_ui_text(view)

            try:
                if interaction.response.is_done():
                    view.message = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
                else:
                    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
                    try:
                        view.message = await interaction.original_response()
                    except Exception:
                        view.message = None
            except Exception:
                return

        self.tree.add_command(self.analytics_group)
        await self.repo_manager.fetch_tree()

    def _xp_needed(self, level, formula):
        default_formula = "5 * (level ** 2) + (50 * level) + 100"
        try:
            return int(self._safe_eval(formula or default_formula, {"level": level}))
        except Exception:
            return int(self._safe_eval(default_formula, {"level": level}))

    def _safe_eval(self, expr, variables):
        expr = (expr or "").replace("^", "**")
        node = ast.parse(expr, mode="eval")
        allowed_nodes = (
            ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.FloorDiv,
            ast.USub, ast.UAdd, ast.Load, ast.Name
        )
        for n in ast.walk(node):
            if not isinstance(n, allowed_nodes):
                raise ValueError("Invalid formula")
            if isinstance(n, ast.Name) and n.id not in variables:
                raise ValueError("Unknown variable")
        return eval(compile(node, "<formula>", "eval"), {"__builtins__": {}}, variables)

    def _check_perms(self, interaction, cfg):
        if not cfg.get("enabled", False):
            asyncio.create_task(self._send_error(interaction, "❌ This command is disabled in settings."))
            return False
        allowed = [str(rid) for rid in (cfg.get("role_ids") or [])]
        user_roles = {str(r.id) for r in getattr(interaction.user, "roles", [])}
        if not allowed or not user_roles.intersection(allowed):
            asyncio.create_task(self._send_error(interaction, "❌ You do not have permission to use this command."))
            return False
        return True

    async def _send_error(self, interaction, text):
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(text, ephemeral=True)
            else:
                await interaction.followup.send(text, ephemeral=True)
        except: pass

    async def on_ready(self):
        print(f"[INFO] IntegratedCommandBot logged in as {self.user}")
        try:
            await self.tree.sync()
            print("[INFO] Slash commands synced.")
        except Exception as e:
            print(f"[ERROR] Sync failed: {e}")
        await self.refresh_permissions()

    async def refresh_permissions(self):
        self.github_token = self._get_best_github_token()
        self.repo_manager = GitHubRepo(self.github_token)
        await self.repo_manager.fetch_tree()

    async def start_bot(self):
        if self.token: await self.start(self.token)
