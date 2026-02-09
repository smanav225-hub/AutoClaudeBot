import time
import random
import ast
import discord


class LevelServer(discord.Client):
    def __init__(self, db, msg_db_handler):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        intents.messages = True
        intents.message_content = True
        super().__init__(intents=intents)
        self.db = db
        self.token = db.token
        self.cooldowns = {}  # {guild_id: {user_id: timestamp}}
        self.msg_db = msg_db_handler

    async def start_bot(self):
        if not self.token:
            print("[WARN] Discord token missing; LevelServer not started.")
            return
        await self.start(self.token)

    async def close_bot(self):
        await self.close()

    async def on_ready(self):
        print(f"[LevelServer] Logged in as {self.user} (ID: {self.user.id})")

    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        guild_id = str(message.guild.id)
        config = self.db.get_config(guild_id, "levels") or {}
        user_id = str(message.author.id)

        # Check if system is active
        if not config.get("enabled", False):
            return

        # 1. Check No-XP Channels
        no_xp_channels = config.get("no_xp_channels", [])
        if str(message.channel.id) in no_xp_channels:
            current = self.msg_db.get_user_level(guild_id, user_id) or {}
            self.msg_db.update_user_level_from_message(
                message,
                xp_gain=0,
                level=int(current.get("level", 0) or 0),
                xp_current=int(current.get("xp_current", 0) or 0),
                xp_total=int(current.get("xp_total", 0) or 0)
            )
            return

        # 2. Check No-XP Roles
        no_xp_roles = config.get("no_xp_roles", [])
        if any(str(role.id) in no_xp_roles for role in message.author.roles):
            current = self.msg_db.get_user_level(guild_id, user_id) or {}
            self.msg_db.update_user_level_from_message(
                message,
                xp_gain=0,
                level=int(current.get("level", 0) or 0),
                xp_current=int(current.get("xp_current", 0) or 0),
                xp_total=int(current.get("xp_total", 0) or 0)
            )
            return

        # 3. Cooldown Check
        now = time.time()
        cooldown = int(config.get("cooldown", 60))

        if guild_id not in self.cooldowns:
            self.cooldowns[guild_id] = {}

        last_msg = self.cooldowns[guild_id].get(user_id, 0)
        if now - last_msg < cooldown:
            current = self.msg_db.get_user_level(guild_id, user_id) or {}
            self.msg_db.update_user_level_from_message(
                message,
                xp_gain=0,
                level=int(current.get("level", 0) or 0),
                xp_current=int(current.get("xp_current", 0) or 0),
                xp_total=int(current.get("xp_total", 0) or 0)
            )
            return

        self.cooldowns[guild_id][user_id] = now

        # 4. Calculate XP
        min_xp = int(config.get("xp_min", 15))
        max_xp = int(config.get("xp_max", 25))
        rate = float(config.get("xp_rate", 1.0))

        xp_gain = int(random.randint(min_xp, max_xp) * rate)

        # 5. Update DB (Message_Database user_levels)
        current = self.msg_db.get_user_level(guild_id, user_id) or {}
        old_level = int(current.get("level", 0) or 0)
        xp_total = int(current.get("xp_total", 0) or 0) + xp_gain

        new_level, xp_current = self._compute_level_from_total(
            xp_total,
            config.get("formula", "5 * (level ** 2) + (50 * level) + 100")
        )

        self.msg_db.update_user_level_from_message(
            message,
            xp_gain=xp_gain,
            level=new_level,
            xp_current=xp_current,
            xp_total=xp_total
        )

        try:
            print(
                f"[Levels] {message.author.name} gained {xp_gain} XP | "
                f"Total XP: {xp_total} | Level: {new_level}"
            )
        except Exception:
            pass

        if new_level > old_level:
            await self.handle_level_up(message, config, new_level, xp_current, xp_total)

    async def handle_level_up(self, message, config, new_level, xp_current, xp_total):
        guild = message.guild
        member = message.author
        channel = message.channel
        announce_channel_id = config.get("announce_channel_id")
        if announce_channel_id:
            target = guild.get_channel(int(announce_channel_id))
            if target:
                channel = target

        # A. Role Rewards
        if config.get("role_rewards_enabled", True):
            rewards = config.get("rewards", [])  # List of {level: 5, role_id: "123"}
            remove_prev = config.get("remove_previous_role", True)

            roles_to_add = []
            roles_to_remove = []

            # Find rewards for this level
            current_rewards = [r for r in rewards if int(r.get("level", 0)) == new_level]

            # Find previous rewards (if removing)
            if remove_prev:
                prev_rewards = [r for r in rewards if int(r.get("level", 0)) < new_level]
                for pr in prev_rewards:
                    rid = pr.get("role_id")
                    if rid:
                        role = guild.get_role(int(rid))
                        if role and role in member.roles:
                            roles_to_remove.append(role)

            for cr in current_rewards:
                rid = cr.get("role_id")
                if rid:
                    role = guild.get_role(int(rid))
                    if role:
                        roles_to_add.append(role)

            if roles_to_remove:
                try:
                    await member.remove_roles(*roles_to_remove, reason=f"Level Up to {new_level}")
                except Exception as e:
                    print(f"[LevelServer] Role removal failed: {e}")

            if roles_to_add:
                try:
                    await member.add_roles(*roles_to_add, reason=f"Level Up to {new_level}")
                except Exception as e:
                    print(f"[LevelServer] Role addition failed: {e}")

        # B. Announcement
        if config.get("announce_enabled", False):
            mode = "text"
            active_tab = (config.get("active_tab") or "").lower()
            if "rank" in active_tab:
                mode = "card"

            if mode == "card":
                rank = self.msg_db.get_user_rank(str(guild.id), str(member.id)) or 0
                xp_needed = self._xp_needed(new_level, config.get("formula", "5 * (level ** 2) + (50 * level) + 100"))
                embed = discord.Embed(color=0x5865F2, title="Level Up!")
                embed.set_author(name=member.name, icon_url=str(member.display_avatar.url))
                embed.add_field(name="Rank", value=f"#{rank}" if rank else "N/A", inline=True)
                embed.add_field(name="Level", value=str(new_level), inline=True)
                embed.add_field(name="XP", value=f"{xp_current}/{xp_needed} XP", inline=True)
                await channel.send(embed=embed)
            else:
                msg_template = config.get("announce_message", "GG {user}, you hit Level {level}!")
                msg = self._render_message(msg_template, member)
                msg = msg.replace("{level}", str(new_level))
                rank = self.msg_db.get_user_rank(str(guild.id), str(member.id)) or 0
                msg = msg.replace("{ordinal}", str(rank) if rank else "N/A")

                await channel.send(msg)

    def _render_message(self, template, member):
        msg = template or ""
        msg = msg.replace("{user}", member.mention)
        msg = msg.replace("{username}", member.name)
        return msg

    def _xp_needed(self, level, formula):
        default_formula = "5 * (level ** 2) + (50 * level) + 100"
        try:
            return int(self._safe_eval(formula or default_formula, {"level": level}))
        except Exception:
            return int(self._safe_eval(default_formula, {"level": level}))

    def _compute_level_from_total(self, xp_total, formula):
        level = 0
        remaining = int(xp_total)
        safety = 0
        while True:
            needed = self._xp_needed(level, formula)
            if remaining >= needed:
                remaining -= needed
                level += 1
            else:
                break
            safety += 1
            if safety > 10000:
                break
        return level, remaining

    def _safe_eval(self, expr, variables):
        expr = (expr or "").replace("^", "**")
        node = ast.parse(expr, mode="eval")

        allowed_nodes = (
            ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.FloorDiv,
            ast.USub, ast.UAdd, ast.Load, ast.Name, ast.Call
        )

        for n in ast.walk(node):
            if not isinstance(n, allowed_nodes):
                raise ValueError("Invalid formula")
            if isinstance(n, ast.Call):
                raise ValueError("Calls not allowed")
            if isinstance(n, ast.Name) and n.id not in variables:
                raise ValueError("Unknown variable")

        return eval(compile(node, "<formula>", "eval"), {"__builtins__": {}}, variables)
