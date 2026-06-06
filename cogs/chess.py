"""
chess_cog.py  —  Single-command interactive Discord chess
Usage:  /chess @opponent
        Everything else is button clicks.
"""

import discord
from discord.ext import commands
from discord import ui
import asyncio
import io
import copy
from PIL import Image, ImageDraw, ImageFont

# ─── Visual constants ────────────────────────────────────────────────────────
LIGHT       = (240, 217, 181)
DARK        = (181, 136,  99)
HI_SEL      = (100, 180, 100)   # selected piece
HI_MOVE     = (100, 160, 220)   # legal move dot
HI_LASTFROM = (205, 210,  85)
HI_LASTTO   = (170, 180,  60)
HI_CHECK    = (220,  50,  50)
SQ          = 80
BORDER      = 36

UNICODE = {
    'wK':'♔','wQ':'♕','wR':'♖','wB':'♗','wN':'♘','wP':'♙',
    'bK':'♚','bQ':'♛','bR':'♜','bB':'♝','bN':'♞','bP':'♟',
}
PIECE_FILL = {
    'w': (255, 255, 255),
    'b': ( 15,  15,  15),
}
PIECE_OUTLINE = {
    'w': ( 40,  40,  40),
    'b': (230, 230, 230),
}

FILES = 'abcdefgh'


def rc(s):
    return 8 - int(s[1]), FILES.index(s[0])

def sq(r, c):
    return FILES[c] + str(8 - r)


# ─── Chess engine ─────────────────────────────────────────────────────────────
class ChessGame:
    def __init__(self, white_id, black_id):
        self.white_id   = white_id
        self.black_id   = black_id
        self.turn       = 'w'
        self.board      = self._start()
        self.en_passant = None
        self.castling   = {'wK':True,'wQ':True,'bK':True,'bQ':True}
        self.last_move  = None
        self.status     = 'playing'   # playing|check|checkmate|stalemate
        self.result     = None        # 'white'|'black'|'draw'
        self.draw_offer = None        # user_id who offered draw
        self.selected   = None        # square currently selected by active player
        self.legal_cache= []          # legal moves for selected square

    def _start(self):
        b = [[None]*8 for _ in range(8)]
        order = ['R','N','B','Q','K','B','N','R']
        for i,p in enumerate(order):
            b[0][i]='b'+p; b[7][i]='w'+p
        for i in range(8):
            b[1][i]='bP'; b[6][i]='wP'
        return b

    def piece_at(self, s):
        r,c=rc(s); return self.board[r][c]

    def set_piece(self, s, p):
        r,c=rc(s); self.board[r][c]=p

    # ── pseudo-legal ──
    def pseudo(self, fs):
        p=self.piece_at(fs)
        if not p: return []
        color,kind=p[0],p[1]
        r,c=rc(fs)
        mv=[]

        def add(nr,nc):
            if 0<=nr<8 and 0<=nc<8:
                t=self.board[nr][nc]
                if not t or t[0]!=color: mv.append(sq(nr,nc))

        def slide(dr,dc):
            nr,nc=r+dr,c+dc
            while 0<=nr<8 and 0<=nc<8:
                t=self.board[nr][nc]
                if t:
                    if t[0]!=color: mv.append(sq(nr,nc))
                    break
                mv.append(sq(nr,nc)); nr+=dr; nc+=dc

        if kind=='P':
            d=-1 if color=='w' else 1
            nr=r+d
            if 0<=nr<8 and not self.board[nr][c]:
                mv.append(sq(nr,c))
                sr=6 if color=='w' else 1
                nr2=r+2*d
                if r==sr and not self.board[nr2][c]: mv.append(sq(nr2,c))
            for dc in [-1,1]:
                nc2=c+dc
                if 0<=nr<8 and 0<=nc2<8:
                    t=self.board[nr][nc2]
                    if t and t[0]!=color: mv.append(sq(nr,nc2))
                    if self.en_passant and sq(nr,nc2)==self.en_passant: mv.append(sq(nr,nc2))
        elif kind=='N':
            for dr,dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]: add(r+dr,c+dc)
        elif kind=='B':
            for d in [(-1,-1),(-1,1),(1,-1),(1,1)]: slide(*d)
        elif kind=='R':
            for d in [(-1,0),(1,0),(0,-1),(0,1)]: slide(*d)
        elif kind=='Q':
            for d in [(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)]: slide(*d)
        elif kind=='K':
            for dr,dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]: add(r+dr,c+dc)
            row=7 if color=='w' else 0
            if r==row and c==4:
                if self.castling[color+'K'] and not self.board[row][5] and not self.board[row][6] and self.board[row][7]==color+'R':
                    mv.append(sq(row,6))
                if self.castling[color+'Q'] and not self.board[row][3] and not self.board[row][2] and not self.board[row][1] and self.board[row][0]==color+'R':
                    mv.append(sq(row,2))
        return mv

    def _attacks(self, fs, board):
        p=board[rc(fs)[0]][rc(fs)[1]]
        if not p: return []
        color,kind=p[0],p[1]; r,c=rc(fs); at=[]
        def add(nr,nc):
            if 0<=nr<8 and 0<=nc<8:
                t=board[nr][nc]
                if not t or t[0]!=color: at.append(sq(nr,nc))
        def slide(dr,dc):
            nr,nc=r+dr,c+dc
            while 0<=nr<8 and 0<=nc<8:
                t=board[nr][nc]
                if t:
                    if t[0]!=color: at.append(sq(nr,nc)); break
                at.append(sq(nr,nc)); nr+=dr; nc+=dc
        if kind=='P':
            d=-1 if color=='w' else 1
            for dc in [-1,1]:
                nr,nc=r+d,c+dc
                if 0<=nr<8 and 0<=nc<8: at.append(sq(nr,nc))
        elif kind=='N':
            for dr,dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]: add(r+dr,c+dc)
        elif kind=='B':
            for d in [(-1,-1),(-1,1),(1,-1),(1,1)]: slide(*d)
        elif kind=='R':
            for d in [(-1,0),(1,0),(0,-1),(0,1)]: slide(*d)
        elif kind=='Q':
            for d in [(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)]: slide(*d)
        elif kind=='K':
            for dr,dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]: add(r+dr,c+dc)
        return at

    def is_attacked(self, tsq, by_color, board=None):
        if board is None: board=self.board
        for r in range(8):
            for c in range(8):
                p=board[r][c]
                if p and p[0]==by_color:
                    if tsq in self._attacks(sq(r,c), board): return True
        return False

    def apply(self, board, fs, ts, promo='Q'):
        b=[row[:] for row in board]
        fr,fc=rc(fs); tr,tc=rc(ts)
        piece=b[fr][fc]; color,kind=piece[0],piece[1]
        if kind=='P' and ts==self.en_passant:
            b[fr][tc]=None
        if kind=='K':
            row=fr
            if fc==4 and tc==6: b[row][5]=b[row][7]; b[row][7]=None
            elif fc==4 and tc==2: b[row][3]=b[row][0]; b[row][0]=None
        b[tr][tc]=piece; b[fr][fc]=None
        if kind=='P' and (tr==0 or tr==7):
            b[tr][tc]=color+(promo or 'Q')
        return b

    def find_king(self, color, board=None):
        if board is None: board=self.board
        for r in range(8):
            for c in range(8):
                if board[r][c]==color+'K': return sq(r,c)
        return None

    def in_check(self, color, board=None):
        if board is None: board=self.board
        ks=self.find_king(color,board)
        opp='b' if color=='w' else 'w'
        return self.is_attacked(ks, opp, board) if ks else False

    def legal_moves(self, fs):
        p=self.piece_at(fs)
        if not p or p[0]!=self.turn: return []
        color=p[0]; result=[]
        for ts in self.pseudo(fs):
            if p[1]=='K':
                fr,fc=rc(fs); tr,tc=rc(ts)
                if abs(fc-tc)==2:
                    if self.in_check(color): continue
                    mid=sq(fr,(fc+tc)//2)
                    nb=self.apply(self.board,fs,mid)
                    if self.in_check(color,nb): continue
            nb=self.apply(self.board,fs,ts)
            if not self.in_check(color,nb): result.append(ts)
        return result

    def all_legal(self, color=None):
        color=color or self.turn
        moves=[]
        for r in range(8):
            for c in range(8):
                p=self.board[r][c]
                if p and p[0]==color:
                    s=sq(r,c)
                    for t in self.legal_moves(s): moves.append((s,t))
        return moves

    def make_move(self, fs, ts, promo='Q'):
        if self.status not in ('playing','check'): return False,'Game over'
        p=self.piece_at(fs)
        if not p: return False,'No piece'
        if p[0]!=self.turn: return False,'Wrong turn'
        if ts not in self.legal_moves(fs): return False,'Illegal'
        color,kind=p[0],p[1]
        fr,fc=rc(fs); tr,tc=rc(ts)
        # en passant state
        if kind=='P' and abs(fr-tr)==2:
            self.en_passant=sq((fr+tr)//2,fc)
        else:
            self.en_passant=None
        # castling rights
        if kind=='K': self.castling[color+'K']=False; self.castling[color+'Q']=False
        if kind=='R':
            if fs=='a1': self.castling['wQ']=False
            if fs=='h1': self.castling['wK']=False
            if fs=='a8': self.castling['bQ']=False
            if fs=='h8': self.castling['bK']=False
        self.board=self.apply(self.board,fs,ts,promo)
        self.last_move=(fs,ts)
        self.selected=None; self.legal_cache=[]
        self.turn='b' if self.turn=='w' else 'w'
        # update status
        opp=self.turn
        ic=self.in_check(opp)
        legal=self.all_legal(opp)
        if not legal:
            self.status='checkmate' if ic else 'stalemate'
            self.result=('white' if opp=='b' else 'black') if ic else 'draw'
        elif ic:
            self.status='check'
        else:
            self.status='playing'
        self.draw_offer=None
        return True,None

    # ── rendering ──────────────────────────────────────────────────────────────
    def render(self, perspective='w'):
        size=SQ*8+BORDER*2
        img=Image.new('RGB',(size,size),(30,30,30))
        draw=ImageDraw.Draw(img)
        try:
            pf=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",54)
            lf=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",16)
        except Exception:
            pf=ImageFont.load_default()
            lf=ImageFont.load_default()

        ks_check=self.find_king(self.turn) if self.status in ('check','checkmate') else None
        sel=self.selected
        legal=set(self.legal_cache)

        for row in range(8):
            for col in range(8):
                if perspective == 'w':
                    br = row
                    bc = col
                else:
                    br = 7 - row
                    bc = 7 - col
                s=sq(br,bc)
                x=BORDER+col*SQ; y=BORDER+row*SQ
                base=LIGHT if (br+bc)%2==0 else DARK

                # layered highlights
                color=base
                if self.last_move:
                    if s==self.last_move[0]: color=_blend(base,HI_LASTFROM,0.55)
                    elif s==self.last_move[1]: color=_blend(base,HI_LASTTO,0.55)
                if s==ks_check: color=_blend(base,HI_CHECK,0.65)
                if s==sel: color=_blend(base,HI_SEL,0.6)

                draw.rectangle([x,y,x+SQ-1,y+SQ-1],fill=color)

                # legal move indicator
                if s in legal:
                    p=self.piece_at(s)
                    if p:  # capture — draw corner triangles
                        pts=[(x,y),(x+16,y),(x,y+16)]
                        draw.polygon(pts,fill=HI_MOVE)
                    else:  # empty — small dot
                        cx=x+SQ//2; cy=y+SQ//2; r=12
                        draw.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(*HI_MOVE,180))

                # piece (use bundled PNG assets from /pieces for better visuals)
                piece = self.board[br][bc]

                if piece:
                    try:
                        piece_path = f"pieces/{piece}.png"

                        piece_img = Image.open(piece_path).convert("RGBA")

                        pad = 4

                        piece_img = piece_img.resize(
                            (SQ - pad * 2, SQ - pad * 2),
                            Image.Resampling.LANCZOS
                        )

                        px = x + pad
                        py = y + pad

                        img.paste(
                            piece_img,
                            (px, py),
                            piece_img
                        )

                    except Exception as e:
                        print(f"[RENDER] Failed loading {piece}: {e}")
                    


        # border labels
        for i in range(8):
            files = FILES if perspective == 'w' else FILES[::-1]
            ranks = list(range(8, 0, -1)) if perspective == 'w' else list(range(1, 9))
            draw.text((BORDER//2, BORDER + i*SQ + SQ//2),str(ranks[i]),font=lf,fill=(160,160,160),anchor='mm')
            draw.text((BORDER + i*SQ + SQ//2, BORDER + 8*SQ + BORDER//2),
    files[i],
    font=lf,
    fill=(160,160,160),
    anchor='mm'
)

        buf=io.BytesIO(); img.save(buf,'PNG'); buf.seek(0)
        return buf


def _blend(a,b,t):
    return tuple(int(av*(1-t)+bv*t) for av,bv in zip(a,b))


# ─── Discord UI ───────────────────────────────────────────────────────────────
RANK_EMOJIS = ['8️⃣','7️⃣','6️⃣','5️⃣','4️⃣','3️⃣','2️⃣','1️⃣']
FILE_EMOJIS = ['🇦','🇧','🇨','🇩','🇪','🇫','🇬','🇭']
# Map emoji -> letter/rank for parsing
FILE_MAP = {e:FILES[i] for i,e in enumerate(FILE_EMOJIS)}
RANK_MAP = {e:str(8-i) for i,e in enumerate(RANK_EMOJIS)}


class SquareSelectView(ui.View):
    """Step 1: choose file, Step 2: choose rank (or deselect)."""
    def __init__(self, game: ChessGame, cog, message, phase='file', chosen_file=None, selecting_dest=False):
        super().__init__(timeout=120)
        self.game=game; self.cog=cog; self.message=message
        self.phase=phase; self.chosen_file=chosen_file
        self.selecting_dest=selecting_dest

        if phase=='file':
            # Show file buttons A-H
            for i,f in enumerate(FILES):
                btn=ui.Button(label=f.upper(), style=discord.ButtonStyle.secondary, row=i//4)
                btn.callback=self._make_file_cb(f)
                self.add_item(btn)
            # Cancel
            cancel=ui.Button(label='✕ Cancel',style=discord.ButtonStyle.danger,row=1)
            cancel.callback=self._cancel
            self.add_item(cancel)

        elif phase=='rank':
            # Show rank buttons 1-8
            for rank in range(1,9):
                s=chosen_file+str(rank)
                piece=game.piece_at(s)
                # If selecting destination, highlight if it's in legal moves
                is_legal=s in game.legal_cache
                if selecting_dest:
                    style=discord.ButtonStyle.success if is_legal else discord.ButtonStyle.secondary
                    disabled=not is_legal
                else:
                    has_piece=piece and piece[0]==game.turn
                    style=discord.ButtonStyle.primary if has_piece else discord.ButtonStyle.secondary
                    disabled=False
                label=f"{chosen_file.upper()}{rank}"
                if piece: label+=f" {UNICODE.get(piece,'')}"
                btn=ui.Button(label=label,style=style,disabled=disabled,row=(rank-1)//4)
                btn.callback=self._make_rank_cb(chosen_file+str(rank))
                self.add_item(btn)
            back=ui.Button(label='← Back',style=discord.ButtonStyle.secondary,row=1)
            back.callback=self._back
            self.add_item(back)

    def _make_file_cb(self, f):
        async def cb(interaction: discord.Interaction):
            print(f"[DEST_FILE] clicked file={f}")

            if not self._check_player(interaction):
                print("[DEST_FILE] wrong player")
                await interaction.response.send_message(
                    "It's not your turn!",
                    ephemeral=True
                )
                return

            print("[DEST_FILE] opening rank selector")

            view=SquareSelectView(
                self.game,
                self.cog,
                self.message,
                phase='rank',
                chosen_file=f,
                selecting_dest=self.selecting_dest
            )

            await interaction.response.edit_message(view=view)

            print("[DEST_FILE] rank selector displayed")

        return cb

    def _make_rank_cb(self, square):
        async def cb(interaction: discord.Interaction):

            print(
                f"[DEST_RANK] square={square} "
                f"selecting_dest={self.selecting_dest}"
            )

            if not self._check_player(interaction):
                print("[DEST_RANK] wrong player")
                await interaction.response.send_message(
                    "It's not your turn!",
                    ephemeral=True
                )
                return

            await interaction.response.defer()

            if self.selecting_dest:
                print("[DEST_RANK] executing move")
                await self.cog.execute_move(
                    interaction,
                    self.game,
                    square
                )
            else:
                print("[DEST_RANK] selecting piece")
                await self.cog.select_piece(
                    interaction,
                    self.game,
                    square,
                    self.message
                )

        return cb

    async def _back(self, interaction: discord.Interaction):
        view=SquareSelectView(self.game,self.cog,self.message,
                               selecting_dest=self.selecting_dest)
        await interaction.response.edit_message(view=view)

    async def _cancel(self, interaction: discord.Interaction):
        self.game.selected=None; self.game.legal_cache=[]
        await interaction.response.defer()
        await self.cog.refresh_board(interaction, self.game, self.message)

    def _check_player(self, interaction):
        uid=interaction.user.id
        expected=self.game.white_id if self.game.turn=='w' else self.game.black_id
        return uid==expected

    async def on_timeout(self):
        try:
            await self.message.edit(view=None)
        except Exception:
            pass


class GameView(ui.View):
    """Main game view — shown alongside the board."""
    def __init__(self, game: ChessGame, cog, message=None):
        super().__init__(timeout=None)
        self.game=game; self.cog=cog; self.message=message

    @ui.button(label='♟ Move',style=discord.ButtonStyle.primary,row=0)
    async def move_btn(self, interaction: discord.Interaction, button: ui.Button):
        uid=interaction.user.id
        expected=self.game.white_id if self.game.turn=='w' else self.game.black_id
        if uid!=expected:
            await interaction.response.send_message("It's not your turn!",ephemeral=True); return
        if self.game.status not in ('playing','check'):
            await interaction.response.send_message("Game is over.",ephemeral=True); return
        view=SquareSelectView(self.game,self.cog,self.message,selecting_dest=False)
        await interaction.response.send_message("**Select the piece to move — choose a file:**",
                                                 view=view,ephemeral=True)

    @ui.button(label='🏳 Resign',style=discord.ButtonStyle.danger,row=0)
    async def resign_btn(self, interaction: discord.Interaction, button: ui.Button):
        uid=interaction.user.id
        if uid not in (self.game.white_id,self.game.black_id):
            await interaction.response.send_message("You're not in this game.",ephemeral=True); return
        if self.game.status not in ('playing','check'):
            await interaction.response.send_message("Game already over.",ephemeral=True); return
        winner_id=self.game.black_id if uid==self.game.white_id else self.game.white_id
        guild=interaction.guild
        winner=guild.get_member(winner_id)
        resigner=interaction.user
        self.game.status='resigned'
        cid=interaction.channel_id
        if cid in self.cog.games: del self.cog.games[cid]
        self.stop()
        emb=discord.Embed(title="🏳️ Resignation",
            description=f"{resigner.mention} resigned.\n**{winner.mention} wins!**",
            color=0xc0392b)
        await interaction.response.edit_message(embed=emb,attachments=[],view=None)

    @ui.button(label='🤝 Draw',style=discord.ButtonStyle.secondary,row=0)
    async def draw_btn(self, interaction: discord.Interaction, button: ui.Button):
        uid=interaction.user.id
        if uid not in (self.game.white_id,self.game.black_id):
            await interaction.response.send_message("You're not in this game.",ephemeral=True); return
        if self.game.status not in ('playing','check'):
            await interaction.response.send_message("Game already over.",ephemeral=True); return
        if self.game.draw_offer is None:
            self.game.draw_offer=uid
            opp_id=self.game.black_id if uid==self.game.white_id else self.game.white_id
            opp=interaction.guild.get_member(opp_id)
            await interaction.response.send_message(
                f"Draw offered to {opp.mention}! They can accept by clicking **🤝 Draw**.",
                ephemeral=False)
        else:
            if self.game.draw_offer==uid:
                await interaction.response.send_message("You already offered a draw. Waiting for opponent.",ephemeral=True); return
            # Accept
            cid=interaction.channel_id
            if cid in self.cog.games: del self.cog.games[cid]
            self.stop()
            emb=discord.Embed(title="🤝 Draw Agreed",
                description="The game ended in a draw by mutual agreement.",color=0x95a5a6)
            await interaction.response.edit_message(embed=emb,attachments=[],view=None)


class PromotionView(ui.View):
    def __init__(self, cog, game, fs, ts, message):
        super().__init__(timeout=60)
        self.cog=cog; self.game=game; self.fs=fs; self.ts=ts; self.message=message
        pieces={'Queen':'Q','Rook':'R','Bishop':'B','Knight':'N'}
        emojis={'Queen':'♛','Rook':'♜','Bishop':'♝','Knight':'♞'}
        for name,code in pieces.items():
            btn=ui.Button(label=f"{emojis[name]} {name}",style=discord.ButtonStyle.primary)
            btn.callback=self._make_cb(code)
            self.add_item(btn)

    def _make_cb(self,code):
        async def cb(interaction: discord.Interaction):
            await interaction.response.defer()
            await self.cog.finalize_move(interaction,self.game,self.fs,self.ts,code,self.message)
        return cb


# ─── Cog ─────────────────────────────────────────────────────────────────────
class Chess(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.games={}          # channel_id -> ChessGame
        self.pending={}        # challenger_id -> (channel_id, target_id)

    # ── /chess ────────────────────────────────────────────────────────────────
    @commands.hybrid_command(name='chess', aliases=['Chess', 'ch'],
                             description='Start a chess game against another player.')
    async def chess(self, ctx, opponent: discord.Member):
        if opponent==ctx.author:
            await ctx.reply("You can't play against yourself!"); return
        if opponent.bot:
            await ctx.reply("You can't challenge a bot."); return
        cid=ctx.channel.id
        # if cid in self.games:
        #     await ctx.reply("A game is already running in this channel."); return
        if ctx.author.id in self.pending:
            await ctx.reply("You already have a pending challenge."); return

        self.pending[ctx.author.id]=(cid, opponent.id)

        class ChallengeView(ui.View):
            def __init__(cv):
                super().__init__(timeout=60)
            @ui.button(label='✅ Accept',style=discord.ButtonStyle.success)
            async def accept(cv,interaction,button):
                if interaction.user.id!=opponent.id:
                    await interaction.response.send_message("This challenge isn't for you.",ephemeral=True); return
                if ctx.author.id not in self.pending:
                    await interaction.response.send_message("Challenge expired.",ephemeral=True); return
                del self.pending[ctx.author.id]
                game=ChessGame(ctx.author.id, opponent.id)
                self.games[cid]=game
                cv.stop()
                await interaction.response.defer()
                await interaction.message.delete()
                await self._post_board(ctx,game,cid,channel=ctx.channel)
            @ui.button(label='❌ Decline',style=discord.ButtonStyle.danger)
            async def decline(cv,interaction,button):
                if interaction.user.id not in (ctx.author.id,opponent.id):
                    await interaction.response.send_message("Not your challenge.",ephemeral=True); return
                if ctx.author.id in self.pending: del self.pending[ctx.author.id]
                cv.stop()
                await interaction.response.edit_message(
                    content=f"Challenge declined by {interaction.user.mention}.",embed=None,view=None)

        emb=discord.Embed(
            title="♟️ Chess Challenge",
            description=f"{ctx.author.mention} challenges {opponent.mention} to chess!\n\n"
                        f"⬜ White: {ctx.author.mention}\n⬛ Black: {opponent.mention}",
            color=0xf0d9b5)
        await ctx.send(embed=emb, view=ChallengeView())

    # ── board posting ──────────────────────────────────────────────────────────
    async def _post_board(self, ctx_or_none, game, cid, channel=None, edit_msg=None):
        try:
            print("[BOARD] start")

            print("[BOARD] rendering image")
            perspective = 'w' if game.turn == 'w' else 'b'

            buf = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: game.render(perspective)
            )
            print("[BOARD] image rendered")

            file = discord.File(
                fp=buf,
                filename='board.png'
            )
            print("[BOARD] file object created")

            print("[BOARD] resolving guild")

            if channel:
                guild = channel.guild
            elif ctx_or_none:
                guild = ctx_or_none.guild
            elif hasattr(game, "board_message") and game.board_message:
                guild = game.board_message.guild
            else:
                print("[BOARD] ERROR: unable to resolve guild")
                return None

            print(f"[BOARD] guild={guild.name}")

            white = guild.get_member(game.white_id)
            black = guild.get_member(game.black_id)

            print(f"[BOARD] white={white}")
            print(f"[BOARD] black={black}")

            turn_m = white if game.turn == 'w' else black
            color_name = 'White' if game.turn == 'w' else 'Black'
            piece_icon = '⬜' if game.turn == 'w' else '⬛'

            print(
                f"[BOARD] turn={game.turn} "
                f"status={game.status}"
            )

            status_txt = {
                'playing': f"{piece_icon} **{color_name}** to move — {turn_m.mention}",
                'check': f"⚠️ **{color_name} is in CHECK!** — {turn_m.mention} must move",
                'checkmate': f"♟️ **Checkmate!** {'⬛ Black' if game.result=='black' else '⬜ White'} wins!",
                'stalemate': f"🤝 **Stalemate!** Draw.",
            }.get(game.status, game.status)

            print("[BOARD] creating embed")

            emb = discord.Embed(
                title="♟️ Chess",
                description=(
                    f"⬜ **White:** {white.mention if white else 'Unknown'}\n"
                    f"⬛ **Black:** {black.mention if black else 'Unknown'}\n\n"
                    f"{status_txt}"
                ),
                color=0xf0d9b5 if game.turn == 'w' else 0x2c2c2c
            )

            if game.last_move:
                emb.set_footer(
                    text=f"Last move: {game.last_move[0].upper()} → {game.last_move[1].upper()}"
                )

            emb.set_image(
                url='attachment://board.png'
            )

            print("[BOARD] embed created")

            game_over = game.status in (
                'checkmate',
                'stalemate'
            )

            view = None if game_over else GameView(
                game,
                self
            )

            print(
                f"[BOARD] game_over={game_over}"
            )

            if edit_msg:
                print("[BOARD] editing existing message")
                print(f"[BOARD] message_id={edit_msg.id}")

                await edit_msg.edit(
                    embed=emb,
                    attachments=[file],
                    view=view
                )

                print("[BOARD] edit completed")

                msg = edit_msg

            else:
                print("[BOARD] sending new message")

                ch = channel or (
                    ctx_or_none.channel
                    if ctx_or_none
                    else None
                )

                msg = await ch.send(
                    embed=emb,
                    file=file,
                    view=view
                )

                print(
                    f"[BOARD] new message id={msg.id}"
                )

            if view:
                view.message = msg

            game.board_message = msg

            print(
                "[BOARD] board_message updated"
            )

            if game_over and cid in self.games:
                print(
                    "[BOARD] removing game from registry"
                )
                del self.games[cid]

            print("[BOARD] done")

            return msg

        except Exception as e:
            import traceback

            print(
                f"[BOARD] EXCEPTION: {type(e).__name__}: {e}"
            )

            traceback.print_exc()

            raise


    # ── piece selection ────────────────────────────────────────────────────────
    async def select_piece(self, interaction, game, square, board_message):
        print(f"[SELECT_PIECE] square={square}")

        piece=game.piece_at(square)

        if not piece or piece[0]!=game.turn:
            print("[SELECT_PIECE] invalid piece")
            await interaction.followup.send("No piece of yours there.",ephemeral=True)
            return

        moves=game.legal_moves(square)

        print(f"[SELECT_PIECE] piece={piece}")
        print(f"[SELECT_PIECE] legal_moves={moves}")

        if not moves:
            print("[SELECT_PIECE] no legal moves")
            await interaction.followup.send("That piece has no legal moves.",ephemeral=True)
            return

        game.selected=square
        game.legal_cache=moves

        print("[SELECT_PIECE] refreshing board")

        await self.refresh_board(interaction, game, board_message)

        print("[SELECT_PIECE] sending destination selector")

        view=SquareSelectView(
            game,
            self,
            board_message,
            selecting_dest=True
        )

        await interaction.followup.send(
            f"**{UNICODE.get(piece,'')} {square.upper()} selected.** Now choose destination file:",
            view=view,
            ephemeral=True
        )

        print("[SELECT_PIECE] destination selector sent")

    async def execute_move(self, interaction, game, to_sq):
        print(f"[EXECUTE_MOVE] selected={game.selected}")
        print(f"[EXECUTE_MOVE] destination={to_sq}")

        fs=game.selected

        if not fs:
            print("[EXECUTE_MOVE] no selected piece")
            await interaction.followup.send(
                "No piece selected.",
                ephemeral=True
            )
            return

        piece=game.piece_at(fs)

        print(f"[EXECUTE_MOVE] piece={piece}")

        tr,_=rc(to_sq)

        if piece and piece[1]=='P' and (tr==0 or tr==7):
            print("[EXECUTE_MOVE] promotion required")

            view=PromotionView(
                self,
                game,
                fs,
                to_sq,
                game.board_message
            )

            await interaction.followup.send(
                "**Choose promotion piece:**",
                view=view,
                ephemeral=True
            )

            return

        print("[EXECUTE_MOVE] finalizing move")

        await self.finalize_move(
            interaction,
            game,
            fs,
            to_sq,
            'Q',
            game.board_message
        )
    async def finalize_move(self, interaction, game, fs, ts, promo, board_message):
        ok,err=game.make_move(fs,ts,promo)
        if not ok:
            await interaction.followup.send(f"Error: {err}",ephemeral=True); return
        cid=interaction.channel_id
        await self._post_board(None,game,cid,edit_msg=board_message)

    async def refresh_board(self, interaction, game, board_message):
        cid=interaction.channel_id
        await self._post_board(None,game,cid,edit_msg=board_message)


async def setup(bot):
    await bot.add_cog(Chess(bot))
    # Sync the slash command tree so /chess appears in Discord.
    # On first load this registers the command globally (may take ~1 hr to propagate)
    # or instantly for guild-specific sync — see notes below.
    try:
        # synced = await bot.tree.sync()
        print(f"[Chess] Synced slash command(s).")
    except Exception as e:
        print(f"[Chess] Tree sync failed: {e}")