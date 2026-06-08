import discord
from discord.ext import commands
from discord.ext.commands import BucketType
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import numpy as np
import random
import asyncio
import math
import io
import copy
from datetime import datetime, timezone
from collections import defaultdict
import re

from bot_utils import asset_font


# ---------------------------------------------------------------------------
# In-memory store:  guild_id -> { tournament_name -> TournamentData }
# ---------------------------------------------------------------------------
_tournaments: dict[int, dict[str, dict]] = defaultdict(dict)


def utc_now():
    return datetime.now(timezone.utc)


def _tid(guild_id: int, name: str) -> str:
    return f"{guild_id}:{name.lower()}"


# ---------------------------------------------------------------------------
# Helper: extract participants from mentions
# ---------------------------------------------------------------------------
def _extract_participants_from_mentions(msg: discord.Message) -> list[dict]:
    """Extract participants from a message's mentions, excluding bots and duplicates."""
    participants = []
    seen = set()

    for member in msg.mentions:
        if member.bot:
            continue
        if member.id in seen:
            continue

        seen.add(member.id)
        participants.append({
    "id": member.id,
    "name": member.display_name,
    "mention": member.mention,
    "avatar": member.display_avatar.url
})

    return participants


# ---------------------------------------------------------------------------
# Bracket helpers
# ---------------------------------------------------------------------------

def _get_avatar(url: str) -> Image.Image:
    try:
        import requests
        r = requests.get(url)
        img = Image.open(io.BytesIO(r.content)).convert("RGBA")
        return img
    except:
        return None
    
def _make_bracket(players: list[str]) -> list[list[list[str | None]]]:
    """
    Build a seeded single-elimination bracket.
    Returns rounds: rounds[r] = list of matches, each match = [p1, p2]
    """
    n = len(players)
    size = 1
    while size < n:
        size *= 2

    seeded = players[:] + [None] * (size - n)
    random.shuffle(seeded)

    rounds = []
    current = [[seeded[i], seeded[i + 1]] for i in range(0, size, 2)]
    rounds.append(current)

    num_rounds = int(math.log2(size))
    for _ in range(num_rounds - 1):
        next_round = []
        for i in range(0, len(current), 2):
            next_round.append([None, None])
        rounds.append(next_round)
        current = next_round

    return rounds


def _advance(rounds: list, round_idx: int, match_idx: int, winner: str):
    """Advance a winner to the next round."""
    if round_idx + 1 >= len(rounds):
        return  # finals done
    next_match_idx = match_idx // 2
    slot = match_idx % 2
    rounds[round_idx + 1][next_match_idx][slot] = winner


# ---------------------------------------------------------------------------
# Image rendering
# ---------------------------------------------------------------------------

BRACKET_BG = (8, 10, 22)
BRACKET_FG = (235, 240, 255)

MATCH_BOX_W = 420
MATCH_BOX_H = 54
MATCH_PADDING = 18
ROUND_GAP = 180
SIDE_MARGIN = 80
TOP_MARGIN = 120
BOTTOM_MARGIN = 80

TITLE_SIZE = 42
PLAYER_FONT_SIZE = 24
ROUND_FONT_SIZE = 18

LINE_COLOR = (120, 180, 255, 255)
LINE_GLOW = (80, 140, 255, 110)

WIN_BOX = (46, 120, 76, 255)
WIN_GLOW = (90, 220, 130, 120)

BOX_FILL = (26, 30, 54, 235)
BOX_BORDER = (120, 130, 220, 255)
TBD_FILL = (24, 24, 36, 220)
TITLE_GOLD = (255, 220, 90, 255)

RENDER_SCALE = 2
MAX_OUTPUT_WIDTH = 2200

def _load_font(size: int):
    return asset_font("ARIAL.TTF", size)

def _fit_output(img: Image.Image, max_width: int = MAX_OUTPUT_WIDTH) -> Image.Image:
    if img.width <= max_width:
        return img
    ratio = max_width / img.width
    return img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)


def _apply_vignette(img: Image.Image, strength: int = 160) -> Image.Image:
    w, h = img.size
    vignette = Image.radial_gradient("L").resize((w, h))
    vignette = ImageOps.invert(vignette)
    vignette = vignette.point(lambda p: int(p * (strength / 255)))
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    overlay.putalpha(vignette)
    return Image.alpha_composite(img, overlay)


def _make_noise_overlay(size: tuple[int, int], alpha: int = 18) -> Image.Image:
    noise = Image.effect_noise(size, 18).convert("L")
    rgba = Image.new("RGBA", size, (255, 255, 255, 0))
    rgba.putalpha(noise.point(lambda p: int((p / 255) * alpha)))
    return rgba


def _draw_glow_line(draw, glow_layer, points, glow_color=(80, 140, 255, 110), core_color=(140, 180, 255, 255)):
    g = ImageDraw.Draw(glow_layer)
    g.line(points, fill=glow_color, width=10)
    g.line(points, fill=glow_color, width=18)
    draw.line(points, fill=core_color, width=3)


def _draw_box_with_glow(base, draw, x1, y1, x2, y2, fill, outline, winner=False):
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)

    if winner:
        glow_color = WIN_GLOW
        gd.rounded_rectangle([x1 - 6, y1 - 6, x2 + 6, y2 + 6], radius=16, fill=glow_color)
        glow = glow.filter(ImageFilter.GaussianBlur(18))
        base.alpha_composite(glow)

    draw.rounded_rectangle([x1, y1, x2, y2], radius=14, fill=fill, outline=outline, width=2)


def _draw_title_glow(base, pos, text, font):
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for offset, alpha in [(0, 80), (2, 60), (4, 35), (8, 18)]:
        gd.text(pos, text, fill=(255, 210, 80, alpha), font=font, anchor="mm")
    glow = glow.filter(ImageFilter.GaussianBlur(10))
    base.alpha_composite(glow)


def _add_spotlights(base: Image.Image):
    w, h = base.size
    spotlight = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    grad = Image.radial_gradient("L").resize((w // 2, h // 2))
    grad = grad.point(lambda p: int((255 - p) * 0.35))
    glow = Image.new("RGBA", grad.size, (90, 110, 255, 0))
    glow.putalpha(grad)

    spotlight.alpha_composite(glow, (w // 8, h // 5))
    spotlight.alpha_composite(glow, (w // 2, h // 4))

    spotlight = spotlight.filter(ImageFilter.GaussianBlur(24))
    return Image.alpha_composite(base, spotlight)

def _render_bracket(
    rounds: list,
    title: str = "Tournament Bracket",
    bg_image: Image.Image | None = None,
    players: list[dict] | None = None,
) -> io.BytesIO:
    num_rounds = len(rounds)
    max_matches = len(rounds[0])

    slot_h = MATCH_BOX_H * 2 + MATCH_PADDING * 3
    img_w = SIDE_MARGIN * 2 + num_rounds * (MATCH_BOX_W + ROUND_GAP) - ROUND_GAP
    img_h = TOP_MARGIN + max_matches * slot_h + BOTTOM_MARGIN

    render_w = img_w * RENDER_SCALE
    render_h = img_h * RENDER_SCALE

    # ---------------- BACKGROUND ----------------
    if bg_image:
        canvas = bg_image.resize((render_w, render_h), Image.LANCZOS).convert("RGBA")
        dark_overlay = Image.new("RGBA", (render_w, render_h), (5, 8, 18, 205))
        canvas = Image.alpha_composite(canvas, dark_overlay)
    else:
        canvas = Image.new("RGBA", (render_w, render_h), (*BRACKET_BG, 255))

    canvas = _add_spotlights(canvas)
    noise = _make_noise_overlay((render_w, render_h), alpha=14)
    canvas = Image.alpha_composite(canvas, noise)

    draw = ImageDraw.Draw(canvas)
    glow_layer = Image.new("RGBA", (render_w, render_h), (0, 0, 0, 0))

    # ---------------- FONTS ----------------
    font_title = _load_font(TITLE_SIZE * RENDER_SCALE)
    font = _load_font(PLAYER_FONT_SIZE * RENDER_SCALE)
    font_small = _load_font(ROUND_FONT_SIZE * RENDER_SCALE)

    title_pos = (render_w // 2, int(34 * RENDER_SCALE))
    _draw_title_glow(canvas, title_pos, title, font_title)
    draw.text(title_pos, title, fill=TITLE_GOLD, font=font_title, anchor="mm")

    # ---------------- PLAYER LOOKUP MAP ----------------
    player_map = {}
    if players:
        player_map = {p["name"]: p for p in players}

    # ---------------- POSITION HELPERS ----------------
    def _box_top(round_idx: int, match_idx: int) -> tuple[int, int]:
        spacing = slot_h * (2 ** round_idx)
        x = SIDE_MARGIN + round_idx * (MATCH_BOX_W + ROUND_GAP)
        y = TOP_MARGIN + match_idx * spacing + (spacing - slot_h) // 2
        return x * RENDER_SCALE, y * RENDER_SCALE

    # ---------------- DRAW ----------------
    for r_idx, round_matches in enumerate(rounds):

        round_label = (
            "FINAL SHOWDOWN" if r_idx == num_rounds - 1
            else "SEMI-FINALS" if r_idx == num_rounds - 2
            else f"ROUND {r_idx + 1}"
        )

        x0 = (SIDE_MARGIN + r_idx * (MATCH_BOX_W + ROUND_GAP)) * RENDER_SCALE

        draw.text(
            (x0 + (MATCH_BOX_W * RENDER_SCALE) // 2, int((TOP_MARGIN - 28) * RENDER_SCALE)),
            round_label,
            fill=(190, 200, 255, 230),
            font=font_small,
            anchor="mm"
        )

        for m_idx, (p1, p2) in enumerate(round_matches):

            x, y = _box_top(r_idx, m_idx)

            for slot, player in enumerate((p1, p2)):

                sy = y + slot * ((MATCH_BOX_H + MATCH_PADDING) * RENDER_SCALE)

                x1, y1 = x, sy
                x2, y2 = x + MATCH_BOX_W * RENDER_SCALE, sy + MATCH_BOX_H * RENDER_SCALE

                is_winner = player and player == _slot_winner(rounds, r_idx, m_idx)
                fill = WIN_BOX if is_winner else (BOX_FILL if player else TBD_FILL)

                _draw_box_with_glow(
                    canvas,
                    draw,
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=fill,
                    outline=BOX_BORDER,
                    winner=bool(is_winner),
                )

                # ---------------- PLAYER RENDER (FIXED) ----------------
                if player:
                    data = player_map.get(player)

                    AV_SIZE = int(MATCH_BOX_H * RENDER_SCALE * 0.75)

                    # avatar
                    if data and data.get("avatar"):
                        try:
                            import requests
                            r = requests.get(data["avatar"])
                            avatar = Image.open(io.BytesIO(r.content)).convert("RGBA")
                            avatar = avatar.resize((AV_SIZE, AV_SIZE))

                            mask = Image.new("L", (AV_SIZE, AV_SIZE), 0)
                            md = ImageDraw.Draw(mask)
                            md.ellipse((0, 0, AV_SIZE, AV_SIZE), fill=255)

                            avatar.putalpha(mask)

                            canvas.paste(
                                avatar,
                                (
                                    int(x1 + 10),
                                    int(y1 + (MATCH_BOX_H * RENDER_SCALE - AV_SIZE) // 2),
                                ),
                                avatar,
                            )
                        except:
                            pass

                    # name
                    text_x = x1 + AV_SIZE + 20
                    text_y = y1 + (MATCH_BOX_H * RENDER_SCALE) // 2

                    draw.text(
                        (text_x, text_y),
                        player,
                        fill=BRACKET_FG,
                        font=font,
                        anchor="lm",
                    )

                else:
                    draw.text(
                        (x1 + 16 * RENDER_SCALE, y1 + (MATCH_BOX_H * RENDER_SCALE) // 2),
                        "TBD",
                        fill=(115, 120, 150),
                        font=font,
                        anchor="lm",
                    )

            # ---------------- CONNECTION LINES ----------------
            if r_idx + 1 < num_rounds:
                mid_y = y + (MATCH_BOX_H * RENDER_SCALE) + (MATCH_PADDING * RENDER_SCALE) // 2
                nx, ny = _box_top(r_idx + 1, m_idx // 2)

                target_slot = m_idx % 2
                ty = ny + target_slot * ((MATCH_BOX_H + MATCH_PADDING) * RENDER_SCALE) + (MATCH_BOX_H * RENDER_SCALE) // 2

                lx = x + MATCH_BOX_W * RENDER_SCALE + 4

                points = [
                    (lx, mid_y),
                    (lx + (ROUND_GAP * RENDER_SCALE) // 2, mid_y),
                    (lx + (ROUND_GAP * RENDER_SCALE) // 2, ty),
                    (nx - 4, ty),
                ]

                _draw_glow_line(
                    draw,
                    glow_layer,
                    points,
                    glow_color=LINE_GLOW,
                    core_color=LINE_COLOR,
                )

    # ---------------- FINAL FX ----------------
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(10))
    canvas = Image.alpha_composite(canvas, glow_layer)
    canvas = _apply_vignette(canvas, strength=120)

    final_img = canvas.convert("RGB")
    final_img = _fit_output(final_img, MAX_OUTPUT_WIDTH)

    buf = io.BytesIO()
    final_img.save(buf, format="PNG", optimize=True, compress_level=1)
    buf.seek(0)
    return buf


def _slot_winner(rounds, r_idx, m_idx):
    """Return winner of a match if they advanced to next round."""
    if r_idx + 1 >= len(rounds):
        return None
    next_match = rounds[r_idx + 1][m_idx // 2]
    slot = m_idx % 2
    return next_match[slot]


def _overall_winner(rounds):
    last_round = rounds[-1]
    if len(last_round) == 1:
        p1, p2 = last_round[0]
        return None
    return None


# ---------------------------------------------------------------------------
# Utility: parse player list from a message (for fallback)
# ---------------------------------------------------------------------------

def _parse_players(text: str) -> list[str]:
    parts = re.split(r"[,\n;]+", text)
    return [p.strip() for p in parts if p.strip()]


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

class BracketConfirmView(discord.ui.View):
    def __init__(self, author_id: int):
        super().__init__(timeout=120)
        self.author_id = author_id
        self.value = None  # "confirm" | "reroll" | "cancel"

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Only the tournament creator can do this.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="✅ Confirm", style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "confirm"
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label="🔀 Re-roll", style=discord.ButtonStyle.primary)
    async def reroll(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "reroll"
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "cancel"
        self.stop()
        await interaction.response.defer()


class MatchUpdateView(discord.ui.View):
    def __init__(self, p1: str, p2: str, author_id: int):
        super().__init__(timeout=60)
        self.winner = None
        self.author_id = author_id

        options = []
        if p1:
            options.append(discord.SelectOption(label=p1, value=p1))
        if p2:
            options.append(discord.SelectOption(label=p2, value=p2))

        select = discord.ui.Select(placeholder="Select the winner…", options=options)
        select.callback = self._select_cb
        self.add_item(select)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Only the tournament creator or a mod can do this.", ephemeral=True)
            return False
        return True

    async def _select_cb(self, interaction: discord.Interaction):
        self.winner = interaction.data["values"][0]
        self.stop()
        await interaction.response.defer()


# ---------------------------------------------------------------------------
# The Cog
# ---------------------------------------------------------------------------

class Tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tournament-create", description="Create a new tournament bracket.")
    async def create(self, ctx, *, name: str):
        """
        Start an interactive tournament creation.
        The creator will mention all participants in one message.
        """
        if name.lower() in _tournaments[ctx.guild.id]:
            await ctx.send(f"⚠️ A tournament named **{name}** already exists in this server.")
            return

        await ctx.send(
            f"🏆 Creating tournament: **{name}**\n\n"
            "Please mention all participants in a single message.\n"
            "Example: @user1 @user2 @user3"
        )

        def check_author(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for("message", check=check_author, timeout=120)
        except asyncio.TimeoutError:
            await ctx.send("⏰ Timed out. Tournament creation cancelled.")
            return

        participants = _extract_participants_from_mentions(msg)
        if len(participants) < 2:
            await ctx.send("❌ You need to mention at least 2 valid members in one message.")
            return

        player_names = [p["name"] for p in participants]
        player_map = {p["name"]: p for p in participants}

        await ctx.send(
            "🖼️ Do you want a background image for the bracket? "
            "Send the image now, or type `skip` to continue without one."
        )

        bg_image = None
        try:
            img_msg = await self.bot.wait_for("message", check=check_author, timeout=60)
            if img_msg.content.strip().lower() != "skip":
                if img_msg.attachments:
                    img_data = await img_msg.attachments[0].read()
                    bg_image = Image.open(io.BytesIO(img_data)).convert("RGBA")
                else:
                    await ctx.send("No image found, proceeding without a background.")
        except asyncio.TimeoutError:
            await ctx.send("No image received, continuing without background.")

        rounds = _make_bracket(player_names)
        while True:
            buf = _render_bracket(rounds, title=name, bg_image=bg_image, players=participants)
            file = discord.File(fp=buf, filename="bracket.png")
            embed = discord.Embed(
                title=f"🏆 {name} — Preview",
                description=f"**{len(participants)} players** | Use the buttons below to confirm or re-roll.",
                color=0xf1c40f,
                timestamp=utc_now(),
            )
            embed.set_image(url="attachment://bracket.png")
            embed.set_footer(text=f"Created by {ctx.author.display_name}")

            view = BracketConfirmView(ctx.author.id)
            preview_msg = await ctx.send(file=file, embed=embed, view=view)

            await view.wait()

            if view.value == "confirm":
                break
            elif view.value == "reroll":
                await preview_msg.edit(view=None)
                rounds = _make_bracket(player_names)
                await ctx.send("🔀 Re-rolling bracket...")
                continue
            else:
                await preview_msg.edit(view=None)
                await ctx.send("❌ Tournament creation cancelled.")
                return

        _tournaments[ctx.guild.id][name.lower()] = {
            "name": name,
            "game": None,
            "players": participants,
            "player_map": player_map,
            "rounds": rounds,
            "current_round": 0,
            "bg_image": bg_image,
            "author_id": ctx.author.id,
            "channel_id": ctx.channel.id,
            "created_at": utc_now(),
            "finished": False,
            "winner": None,
            "winner_id": None,
        }

        buf = _render_bracket(rounds, title=name, bg_image=bg_image)
        file = discord.File(fp=buf, filename="bracket.png")
        embed = discord.Embed(
            title=f"🏆 {name} — Official Bracket",
            description="\n".join(f"• {p['mention']} ({p['name']})" for p in participants),
            color=0x2ecc71,
            timestamp=utc_now(),
        )
        embed.set_image(url="attachment://bracket.png")
        embed.set_footer(text=f"Use tournament-update {name} to report results")
        await ctx.send(file=file, embed=embed)

    @commands.command(name="tournament-update", description="Report a match result and advance the bracket.")
    async def update(self, ctx, *, name: str):

        t = _tournaments[ctx.guild.id].get(name.lower())
        if not t:
            await ctx.send(f"❌ No tournament named **{name}** found.")
            return
        if t["finished"]:
            await ctx.send(f"🏁 **{name}** is already finished!")
            return

        is_author = ctx.author.id == t["author_id"]
        is_mod = ctx.author.guild_permissions.manage_guild
        if not (is_author or is_mod):
            await ctx.send("❌ Only the tournament creator or a server moderator can update results.")
            return

        rounds = t["rounds"]

        # Auto-resolve all bye matches first
        _resolve_byes(rounds)

        # Recompute current round after bye propagation
        t["current_round"] = _find_current_round(rounds)
        r_idx = t["current_round"]

        # Finals
        if r_idx == len(rounds) - 1:
            final_match = rounds[r_idx][0]
            if not (final_match[0] and final_match[1]):
                await ctx.send("⏳ The final is not ready yet.")
                return

            if t["winner"]:
                await ctx.send(f"🏁 **{name}** is already finished!")
                return

            pending = [(0, final_match)]
        else:
            pending = [
                (i, m)
                for i, m in enumerate(rounds[r_idx])
                if m[0] and m[1] and _slot_winner(rounds, r_idx, i) is None
            ]

            if not pending:
                _resolve_byes(rounds, start_round=r_idx)
                t["current_round"] = _find_current_round(rounds)
                r_idx = t["current_round"]

                if r_idx == len(rounds) - 1:
                    final_match = rounds[r_idx][0]
                    if final_match[0] and final_match[1] and not t["winner"]:
                        pending = [(0, final_match)]
                    else:
                        await ctx.send("⏳ No playable matches are ready yet.")
                        return
                else:
                    pending = [
                        (i, m)
                        for i, m in enumerate(rounds[r_idx])
                        if m[0] and m[1] and _slot_winner(rounds, r_idx, i) is None
                    ]
                    if not pending:
                        await ctx.send("⏳ No playable matches are ready yet.")
                        return

        options_text = "\n".join(f"`{i}` — **{m[0]}** vs **{m[1]}**" for i, m in pending)
        await ctx.send(f"**Pending matches in Round {r_idx + 1}:**\n{options_text}\n\nType the match number to update:")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            pick_msg = await self.bot.wait_for("message", check=check, timeout=60)
            match_num = int(pick_msg.content.strip())
        except (asyncio.TimeoutError, ValueError):
            await ctx.send("❌ Cancelled or invalid input.")
            return

        match_indices = [i for i, _ in pending]
        if match_num not in match_indices:
            await ctx.send("❌ Invalid match number.")
            return

        match = rounds[r_idx][match_num]
        view = MatchUpdateView(match[0], match[1], ctx.author.id)
        await ctx.send(f"Who won: **{match[0]}** vs **{match[1]}**?", view=view)
        await view.wait()

        if not view.winner:
            await ctx.send("❌ No winner selected. Update cancelled.")
            return

        winner = view.winner
        winner_data = t["player_map"].get(winner)

        if r_idx == len(rounds) - 1:
            t["winner"] = winner
            t["winner_id"] = winner_data["id"] if winner_data else None
            t["finished"] = True
        else:
            _advance(rounds, r_idx, match_num, winner)
            _resolve_byes(rounds, start_round=r_idx + 1)
            t["current_round"] = _find_current_round(rounds)

        buf = _render_bracket(rounds, title=t["name"], bg_image=t["bg_image"])
        file = discord.File(fp=buf, filename="bracket.png")
        embed = discord.Embed(
            title=f"🏆 {t['name']} — Updated",
            description=f"✅ **{winner}** advances!",
            color=0x3498db,
            timestamp=utc_now(),
        )
        embed.set_image(url="attachment://bracket.png")
        await ctx.send(file=file, embed=embed)

        if t["finished"]:
            await self._post_winner(ctx, t)

        @commands.command(name="tournament-winner", description="Announce the winner of a finished tournament.")
        async def winner(self, ctx, *, name: str):
            t = _tournaments[ctx.guild.id].get(name.lower())
            if not t:
                await ctx.send(f"❌ No tournament named **{name}** found.")
                return
            if not t["finished"] or not t["winner"]:
                await ctx.send(f"⏳ **{name}** isn't finished yet.")
                return
            await self._post_winner(ctx, t)

        async def _post_winner(self, ctx, t: dict):
            winner = t["winner"]
            winner_id = t.get("winner_id")
            winner_mention = f"<@{winner_id}>" if winner_id else f"**{winner}**"
            name = t["name"]

            embed = discord.Embed(
                title="🎉 We have a Champion!",
                description=(
                    f"{winner_mention} has won the **{name}** tournament!\n\n"
                    "🥇 Congratulations to the champion!\n"
                    "Thanks to all participants for competing! 🎊"
                ),
                color=0xffd700,
                timestamp=utc_now(),
            )
            embed.set_footer(text=f"Tournament concluded • {name}")

            buf = _render_bracket(t["rounds"], title=f"🏆 {name} — FINAL", bg_image=t["bg_image"])
            file = discord.File(fp=buf, filename="final_bracket.png")
            embed.set_image(url="attachment://final_bracket.png")
            embed.add_field(name="🏆 Winner", value=f"**{winner}**", inline=False)

            await ctx.send(
                content=f"🎊 @everyone {winner_mention} is the champion of **{name}**! 🎊",
                file=file,
                embed=embed,
            )

        @commands.command(name="tournament-list", description="Show all ongoing tournaments in this server.")
        async def list_tournaments(self, ctx):
            guild_ts = _tournaments.get(ctx.guild.id, {})
            active = {k: v for k, v in guild_ts.items() if not v["finished"]}
            finished = {k: v for k, v in guild_ts.items() if v["finished"]}

            if not guild_ts:
                await ctx.send("📭 No tournaments have been created in this server yet.")
                return

            embed = discord.Embed(
                title=f"🏆 Tournaments in {ctx.guild.name}",
                color=0x9b59b6,
                timestamp=utc_now(),
            )

            if active:
                lines = []
                for t in active.values():
                    r_idx = t["current_round"]
                    total_rounds = len(t["rounds"])
                    lines.append(
                        f"**{t['name']}** — Round {r_idx + 1}/{total_rounds} "
                        f"| {len(t['players'])} players "
                        f"| Started <t:{int(t['created_at'].timestamp())}:R>"
                    )
                embed.add_field(name="🟢 Active", value="\n".join(lines), inline=False)

            if finished:
                lines = []
                for t in finished.values():
                    lines.append(f"**{t['name']}** — 🥇 Won by **{t['winner']}**")
                embed.add_field(name="✅ Finished", value="\n".join(lines), inline=False)

            embed.set_footer(text="Use tournament-update <name> to report results")
            await ctx.send(embed=embed)

        @commands.command(name="tournament-show", description="Display the current bracket for a tournament.")
        async def show(self, ctx, *, name: str):
            t = _tournaments[ctx.guild.id].get(name.lower())
            if not t:
                await ctx.send(f"❌ No tournament named **{name}** found.")
                return

            buf = _render_bracket(t["rounds"], title=t["name"], bg_image=t["bg_image"])
            file = discord.File(fp=buf, filename="bracket.png")
            status = "🏁 Finished" if t["finished"] else f"🟢 Round {t['current_round'] + 1}/{len(t['rounds'])}"
            embed = discord.Embed(
                title=f"🏆 {t['name']}",
                description=f"**Status:** {status}",
                color=0xe74c3c if t["finished"] else 0x1abc9c,
                timestamp=utc_now(),
            )
            if t["finished"]:
                embed.add_field(name="🥇 Champion", value=f"**{t['winner']}**")
            embed.set_image(url="attachment://bracket.png")
            await ctx.send(file=file, embed=embed)

        @commands.command(name="tournament-delete", description="Delete a tournament (author or mod only).")
        async def delete(self, ctx, *, name: str):
            t = _tournaments[ctx.guild.id].get(name.lower())
            if not t:
                await ctx.send(f"❌ No tournament named **{name}** found.")
                return
            is_author = ctx.author.id == t["author_id"]
            is_mod = ctx.author.guild_permissions.manage_guild
            if not (is_author or is_mod):
                await ctx.send("❌ Only the tournament creator or a server moderator can delete a tournament.")
                return
            del _tournaments[ctx.guild.id][name.lower()]
            await ctx.send(f"🗑️ Tournament **{name}** has been deleted.")

        def _match_bye_winner(match: list[str | None]) -> str | None:
            p1, p2 = match
            if p1 and not p2:
                return p1
            if p2 and not p1:
                return p2
            return None


        def _resolve_byes(rounds: list, start_round: int = 0):
            """
            Automatically advance players in bye matches (player vs None).
            This cascades forward, so later rounds get filled too if possible.
            """
            for r_idx in range(start_round, len(rounds) - 1):
                for m_idx, match in enumerate(rounds[r_idx]):
                    if _slot_winner(rounds, r_idx, m_idx) is not None:
                        continue

                    bye_winner = _match_bye_winner(match)
                    if bye_winner:
                        _advance(rounds, r_idx, m_idx, bye_winner)


        def _find_current_round(rounds: list) -> int:
            """
            Return the first round that still has a playable unresolved match.
            If none are left, return the final round index.
            """
            for r_idx, round_matches in enumerate(rounds):
                playable_unresolved = False

                for m_idx, match in enumerate(round_matches):
                    p1, p2 = match

                    if r_idx == len(rounds) - 1:
                        if p1 and p2:
                            playable_unresolved = True
                            break
                    else:
                        if p1 and p2 and _slot_winner(rounds, r_idx, m_idx) is None:
                            playable_unresolved = True
                            break

                if playable_unresolved:
                    return r_idx

            return len(rounds) - 1

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

async def setup(bot):
    await bot.add_cog(Tournament(bot))