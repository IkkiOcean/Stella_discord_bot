from threading import Timer
import discord
from discord import Forbidden, app_commands
from discord.ext import commands, tasks
from discord.ext.commands import BucketType, Greedy, CommandInvokeError
import requests
import random
import textwrap
import datetime
import json
import os
import sys
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw, UnidentifiedImageError
from io import BytesIO
import typing
import asyncio
import mal
from mal import *
from lxml import html
import numpy as np
import urllib.parse
import urllib.request
import re
from asyncio import gather
from bs4 import BeautifulSoup
import math
import certifi
from pymongo import MongoClient
import aiohttp
import praw
from selenium import webdriver
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / ".vscode"
GENERATED_DIR = BASE_DIR / "generated"
GENERATED_DIR.mkdir(exist_ok=True)

user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def asset_font(name: str, size: int):
    return ImageFont.truetype(str(ASSETS_DIR / name), size)


def output_path(name: str) -> str:
    return str(GENERATED_DIR / name)


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc)


def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def _is_image_bytes(data: bytes) -> bool:
    if not data:
        return False
    signatures = (
        b"\x89PNG\r\n\x1a\n",
        b"\xff\xd8\xff",
        b"GIF87a",
        b"GIF89a",
        b"RIFF",
    )
    return data.startswith(signatures)


def open_template(filename: str, fallback_url: str | None = None) -> Image.Image:
    """Load a meme template from bundled assets, with optional URL fallback."""
    local_path = ASSETS_DIR / filename
    if fallback_url:
        url = fallback_url.strip()
        headers = {"User-Agent": user_agent, "Accept": "image/*,*/*"}
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        if not _is_image_bytes(resp.content):
            raise ValueError(
                f"Could not download image template '{filename}' from {url}. "
                "The remote host returned a non-image response."
            )
        return Image.open(BytesIO(resp.content))

    else:
        if local_path.exists():
            with Image.open(local_path) as img:
                return img.copy()
        raise FileNotFoundError(
            f"Template '{filename}' not found in {ASSETS_DIR} and no fallback URL was provided."
        )

    


def env_flag(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default).lower()).strip().lower() in ("1", "true", "yes", "on")


load_dotenv()

BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID", "745006368175423489"))
STARTUP_CHANNEL_ID = os.getenv("STARTUP_CHANNEL_ID", "772496570436419592")
ENABLE_ANIME_UPDATES = env_flag("ENABLE_ANIME_UPDATES", False)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(
    command_prefix=commands.when_mentioned_or("stela ", "S.", "s.", "Stela "),
    intents=intents,
)

_driver = None
_driver_init_failed = False
_driver_init_error = None


class DriverUnavailableError(Exception):
    """Raised when headless Chrome cannot be started."""


def find_chrome_binary():
    configured = os.getenv("CHROME_BINARY_PATH", "").strip()
    if configured and Path(configured).exists():
        return configured

    if sys.platform == "darwin":
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
        ]
    elif sys.platform.startswith("linux"):
        # Raspberry Pi / ARM Debian/Raspberry Pi OS common paths
        candidates = [
            # Google Chrome
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            # Chromium variants
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
            "/snap/bin/chromium",
            # Raspberry Pi OS often installs chromium under these names
            "/usr/bin/chromium-browser-wayland",
            "/usr/bin/chromium-wayland",
        ]
    else:
        candidates = []

    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    return None


def get_driver():
    """Lazy Chrome driver — avoids crashing at import on servers without Chrome."""
    global _driver, _driver_init_failed, _driver_init_error
    if _driver is not None:
        return _driver
    if _driver_init_failed:
        raise DriverUnavailableError(_driver_init_error)

    from selenium.webdriver.chrome.service import Service

    chrome_binary = find_chrome_binary()
    if chrome_binary is None:
        _driver_init_failed = True
        _driver_init_error = (
            "Chrome/Chromium not found. Install Google Chrome, or set "
            "CHROME_BINARY_PATH in .env to your browser executable."
        )
        raise DriverUnavailableError(_driver_init_error)

    options = webdriver.ChromeOptions()
    options.binary_location = chrome_binary
    options.add_argument("--headless=new")
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server=direct://")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    # Common stability flags for ARM/Raspberry Pi
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")

    try:
        chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "").strip()
        if chromedriver_path and Path(chromedriver_path).exists():
            service = Service(chromedriver_path)
        else:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())

        _driver = webdriver.Chrome(service=service, options=options)
        return _driver
    except Exception as exc:
        _driver_init_failed = True
        _driver_init_error = str(exc)
        raise DriverUnavailableError(
            f"Could not start headless Chrome ({exc}). "
            "Install Chrome/Chromium or set CHROME_BINARY_PATH and CHROMEDRIVER_PATH."
        ) from exc


def mongo_uri(name: str, fallback: str = "") -> str:
    uri = os.getenv(name, fallback).strip()
    if not uri:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return uri


cluster = MongoClient(mongo_uri("MONGODB_URI"), tlsCAFile=certifi.where())
client2 = MongoClient(
    mongo_uri("MONGODB_URI_WAIFUS", os.getenv("MONGODB_URI", "")),
    tlsCAFile=certifi.where(),
)
db = cluster["discord"]
mal_collect = db["mal"]
animetriv_collect = db["anime-trivia"]
upd = db["anime-updates"]
listed = db["watchlist"]
chan = db["channels"]
airingg = db["airing"]
db2 = client2["Waifus"]
girl = db2["images"]

redit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID", "YOUR CLIENT ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET", "YOUR CLIENT SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT", "stella-discord-bot"),
)

#error.................
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You are too weak ;-; Work hard and get powers to do that :)")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Member Not Found")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Pls use command properly! `S.help <command>`")
    elif isinstance(error, Forbidden):
        await ctx.send("Give me powers to do that! I will not disappoint you ;-;")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f" You have to wait {error.retry_after:,.2F} secs")
    elif isinstance(error, CommandInvokeError):
        cause = error.original
        if isinstance(cause, (UnidentifiedImageError, ValueError, FileNotFoundError)):
            await ctx.send(
                "Could not load the image template for this command. "
                "Please try again later or contact the bot owner."
            )
            print(f"Image command error in {getattr(ctx.command, 'name', '?')}: {cause}")
        else:
            raise error
    else:
        raise error


@client.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandInvokeError):
        cause = error.original
        if isinstance(cause, (UnidentifiedImageError, ValueError, FileNotFoundError)):
            msg = (
                "Could not load the image template for this command. "
                "Please try again later or contact the bot owner."
            )
            if interaction.response.is_done():
                await interaction.followup.send(msg, ephemeral=True)
            else:
                await interaction.response.send_message(msg, ephemeral=True)
            print(f"Slash image error: {cause}")
            return
    print(f"Unhandled slash command error: {error}")
    msg = "Something went wrong running that command."
    if interaction.response.is_done():
        await interaction.followup.send(msg, ephemeral=True)
    else:
        await interaction.response.send_message(msg, ephemeral=True)


    


# do stuff......
owner = None
@client.event
async def setup_hook():
    global owner
    
    # 1. Fetch owner safely once
    try:
        owner = await client.fetch_user(BOT_OWNER_ID)
    except discord.HTTPException:
        owner = None

@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Anime | S.help for commands",
        )
    )

    if STARTUP_CHANNEL_ID:
        general_channel = client.get_channel(int(STARTUP_CHANNEL_ID))
        if general_channel is not None:
            await general_channel.send("Hello Master")

    print(f"Bot is online as {client.user} (ID: {client.user.id})")

    try:
        girl.create_index([("name", "text"), ("anime", "text")])
    except Exception as exc:
        print(f"Warning: could not create waifu search index: {exc}")

    if ENABLE_ANIME_UPDATES:
        if not checkNewLoop.is_running():
            checkNewLoop.start()
        print("Anime update checker enabled")
    else:
        print("Anime update checker disabled (set ENABLE_ANIME_UPDATES=true to enable)")



     
#@client.event
#async def on_message(message):
   # if not message.author.bot:
    #    mention = f'<@{client.user.id}>'
        
    #    if mention == message.content:
    #        await message.reply("My prefixes are `S.` and `Stela`")
    #        await message.reply("You mentioned me :)")   
     #   await client.process_commands(message)         
#commands...................................................



#moderation.................................................................................... 
#kick...............
# Kick command moved to cogs.moderation

# Moderation commands (kick, ban, clear, addrole, removerole, addemoji) have been moved to cogs/moderation.py

    
   
    
    
    

# Moderation commands (kick, ban, clear, addrole, removerole, addemoji) have been moved to cogs/moderation.py
    

# ===========================================================================
# All command implementations have been moved to cogs:
#   cogs/moderation.py   - kick, ban, clear, addrole, removerole, addemoji
#   cogs/roleplay.py     - wave, nom, blush, bonk, cry, dance, hug, kill, laugh,
#                          pat, poke, pout, punch, rage, slap, sleep, smile, smug,
#                          stare, think
#   cogs/memegen.py      - wanted, insta, jojo, chika, fbi, worthless, water, rip,
#                          disability, thisisshit, distract, myboi, santa, news,
#                          yugioh, yugiohpfp, bitch, billy, fact, wallpunch, dumb
#   cogs/fun.py          - waifu, lookup, say, match, spoiler, propose, roast,
#                          define, insult, meme, F, reddit, challenge
#   cogs/anime_reminder.py - remind, addwatchlist, removewatchlist, watchlist,
#                            airing, setchannel, removechannel
#   cogs/anime_manga.py  - anime, manga, eplist, filler, mal, setmal, removemal,
#                          profile, recommend, character, rndqoute
#   cogs/utility.py      - server, invite, vote, movie, version, avatar, userinfo,
#                          announce, serverinfo, yt, embed, submit, wallpaper, rand
# ===========================================================================

def findname(id):
    link = f"https://myanimelist.net/anime/{id}"
    r = requests.get(link)
    tree = html.fromstring(r.content)
    anime = tree.xpath('//*[@itemprop = "name"]/h1/strong')[0].text
    if anime != []:
        return anime
    else:
        return None    
def findid(anime):
    link = f"https://myanimelist.net/anime.php?cat=anime&q={anime}"
    r = requests.get(link)
    tree = html.fromstring(r.content)
    anime = tree.xpath('//*/td[@class = "borderClass bgColor0"]/div[1]/a[1]/@href')
    if anime != []:
        id = anime[0].split('/')
        animeid = id[4]
        return animeid
    else:
        return None

@tasks.loop(minutes=15)
async def checkNewLoop():
    try:
        anime = check_new()
    except DriverUnavailableError as exc:
        print(f"Anime update check skipped: {exc}")
        return
    except Exception as exc:
        print(f"Anime update check failed: {exc}")
        if owner is not None:
            try:
                await owner.send(f"Error in checkNewLoop: {exc}")
            except Exception:
                pass
        return

    if anime == []:
        print("nothing new")
    else:
        try:    
            for ani in anime:
                title = ani['titles']
                episode = ani['episodes']
                #watch = ani['watch']
                image = ani['image']
                id = ani['id']
                em = discord.Embed(title = title,description = f"{episode} just dropped",color=0x00ebff)#\n\n[Click Here to watch]({watch})
                em.set_image(url = image)
                #await channel.send(embed = em)
                
                if id != "None":
                    docs = listed.find({"watchlist": id, "toggle" : 1}) 
                    if docs != None:
                        users = []
                        for doc in docs: 
                            users.append(doc['_id'])
                            
                        for user in users:
                            member = await client.fetch_user(user)
                            try:
                                await member.send(embed = em)
                            except:    
                                print("can't dm")
                else:                
                    await owner.send(f"id issues in {title}")                
                posts = chan.find()
                channels = []
                for post in posts:
                    channels.append(post['chnl'])
                for channel in channels:
                    chnnl = client.get_channel(channel)
                    try:
                        if chnnl == None:
                            chan.delete_one({'chnl' : channel})
                            print(f'deleted {channel}')
                        elif chnnl != None:  
                            await chnnl.send(embed =em) 
                    except:
                        print("can't post")                   
        except: 
            await owner.send("Error in checknewLoop!")                   
    print(f'checked')


@checkNewLoop.before_loop
async def before_check_new():
    await client.wait_until_ready()


def check_new():
    link = "https://animixplay.to"
    
    
    get_driver().get(link)
    
    r = get_driver().page_source
    tree = html.fromstring(r)
    newanime = []
    
    anime = tree.xpath('//*[@id="resultplace"]/ul/li')
    
    for anim in anime:
        title = (anim.xpath('.//a/@title'))[0]
        episode = (anim.xpath('.//a/div[@class = "details"]/p[@class = "infotext"]')[0].text)
        posst = {'titles' : title,'episodes' : episode}
        ccc = upd.find_one(posst)
        #titlee = title.replace("(Dub)","")
        
        if ccc == None:
            watch = anim.xpath('.//a/@href')
            image = anim.xpath('.//a/div[@class = "searchimg"]/img/@src')
            url = link + watch[0]
            id = findmixid(url)
            upd.insert_one(posst)
            if id  != None:
                newanime.append({'titles' : title,'episodes' : episode,'image': image[0],'id' : id})
            elif id == None:
                newanime.append({'titles' : title,'episodes' : episode,'image': image[0],'id' : 'None'})
    return newanime
        
def findmixid(url):
    get_driver().get(url)
    
    r = get_driver().page_source
    tree = html.fromstring(r)
    anime = tree.xpath('//*/a[@id = "animebtn2"]/@href')
    if anime != []:
        id = anime[0].split('/')
        animeid = id[2]
        return animeid
    else:
        return None
@client.command(name= 'updateairing')
async def updateairing(ctx, season): 
    if ctx.author == owner:
        link = 'http://myanimelist.net/anime/season'
        r = requests.get(link)
        mall = html.fromstring(r.content)
        anime = mall.xpath('//*/h2[@class = "h2_anime_title"]')
        #anime2 = mall.xpath('//*/div[@class = "js-anime-category-producer seasonal-anime js-seasonal-anime js-anime-type-all js-anime-type-3"]')
        #anime = anime1 + anime2
        titles = []
        animelink = []
        animeid = []
        for ani in anime:
            name = ani.xpath('.//a')[0].text
            link =  ani.xpath('.//a/@href')[0]
            id = link.split('/')
            animelink.append(link)
            animeid.append(id[4])
            titles.append(name) 
        print(titles)    
        doc = airingg.find()
        count = 0
        for d in doc:
            count += 1
            airingg.delete_one({'_id' : d['_id']})  
        await ctx.send(f"deleted {count}")  
        num = 0  
        for title,idd,url in zip(titles,animeid,animelink):
            post = {'_id' : idd, 'name' : title, 'url' : url}
            airingg.insert_one(post)
            num += 1
        await ctx.send(f"added {num}")
        r2 = requests.get(f'http://myanimelist.net/anime/season/{season}')
        mall2 = html.fromstring(r2.content)
        anime2 = mall2.xpath('//*/h2[@class = "h2_anime_title"]')
        
        titles2 = []
        animelink2 = []
        animeid2 = []
        for ani2 in anime2:
            name2 = ani2.xpath('.//a')[0].text
            link2 =  ani2.xpath('.//a/@href')[0]
            id2 = link2.split('/')
            animelink2.append(link2)
            animeid2.append(id2[4])
            titles2.append(name2)
        num2 = 0 
        for title2,idd2,url2 in zip(titles2,animeid2,animelink2):
            if idd2 not in animeid:
                post2 = {'_id' : idd2, 'name' : title2, 'url' : url2}
                airingg.insert_one(post2)
                num2 += 1
                
        await ctx.send(f"added {num2}\nTotal {num + num2}") 

# Commands below are implemented in cogs/anime_reminder.py and cogs/utility.py


#help...............................
client.remove_command("help")
@client.group(invoke_without_command=True)#<> required [] optional
async def help(ctx):
    em = discord.Embed(description = "For more info on a specific command, use stela help <command>\nFor more help, join our [server](https://discord.gg/ZbemgbQuXa)\n \nFor arguments in commands:\n<> means it's required\n[] means it's optional\n||Do not actually include the <> and [] symbols in the command||\n\n**__PRIVACY POLICY__**\n1) We Do not share any kind of information provided by our users\n2) We do not store any kind of data which is mandatory, users can opt-out from using such commands if they dont want to\n3)Prior to collecting any data we notify it by specific explanation texts displayed prior to the Data collection.\n4)If any user wants to delete his/hers data from the bot then he/she can do it simply by using some commands or by asking help from server given in `S.server` command",timestamp=utc_now(),color = discord.Color(0x00ff7d))
    em.set_author(name = "Help/Command List",icon_url=f"{client.user.display_avatar.url}")
    em.add_field(name="🛡️ Moderation",value="`kick` `ban` `clear` `addemoji`",inline=False)
    em.add_field(name="🤗 Roleplay",value="`wave` `nom` `blush` `bonk` `cry` `dance` `hug` `kill` `laugh` `pat` `poke` `pout` `punch` `rage` `slap` `sleep` `smile` `smug` `stare` `think` ",inline=False)
    em.add_field(name="😆 Meme Generation",value="`wanted` `insta` `jojo` `chika` `fbi` `worthless` `water` `rip` `disability` `thisisshit` `distract` `myboi` `santa` `news` `yugioh` `yugiohpfp` `bitch` `billy` `fact` `wallpunch` `dumb`",inline=False)
    #em.add_field(name="💰 Economy",value="`withdraw` `slot` `shop` `sell` `rob` `leaderboard` `kira` `inventory` `give` `deposit` `buy` `beg` `balance` ",inline=False)
    em.add_field(name="🥳 Fun",value="`waifu` `lookup` `say` `match` `spoiler` `propose` `roast` `define` `insult` `meme` `F` `reddit` `challenge` ",inline=False)
    em.add_field(name="🕰️ Anime Reminder",value="`remind` `addwatchlist` `removewatchlist` `watchlist` `airing` `setchannel` `removechannel`",inline=False)
    em.add_field(name="📺 Anime-Manga",value="`anime` `manga` `eplist` `filler` `mal` `setmal` `removemal` `profile` `recommend` `character` `rndqoute`",inline=False)
    em.add_field(name="🔧 Utility",value="`server` `invite` `vote` `movie` `version` `avatar` `userinfo` `announce` `serverinfo` `yt` `embed` `submit` `wallpaper` `rand`",inline=False)
    em.set_footer(text= f'Requested by {ctx.author}' )
    await ctx.send(embed=em)

@help.command()
async def kick(ctx):
    em = discord.Embed(description="Kicks a member from the Server",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.kick <member> [reason]`")
    em.add_field(name="**Permission required**",value="`Kick Member`")
    await ctx.send(embed=em)

@help.command()
async def submit(ctx):
    em = discord.Embed(description="Submits your contestant for the Tournament",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.submit <name>`\nafter that Send the link of the image within 20 sec\nThis command will only work in Tournament\nOnly works in support server")
    await ctx.send(embed=em)

@help.command()
async def ban(ctx):
    em = discord.Embed(description="Bans a member from the Server",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.ban <member> [reason]`")
    em.add_field(name="**Permission required**",value="`Ban Member`")
    await ctx.send(embed=em)

@help.command()
async def clear(ctx):
    em = discord.Embed(description="Deletes messages",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.clear <Number of Msgs>`")
    em.add_field(name="**Aliases**",value="`Clean` `delete` `purge`")
    em.add_field(name="**Permission required**",value="`Manage Messages`")
    await ctx.send(embed=em)

@help.command()
async def wanted(ctx):
    em = discord.Embed(description="Creates a Wanted poster from One Piece",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.wanted <member>`")
    em.add_field(name="**Aliases**",value="`bounty`")
    await ctx.send(embed=em)

@help.command()
async def jojo(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.jojo <member>`")
    await ctx.send(embed=em)   

@help.command()
async def chika(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.chika <message1>|<message2>|<message3>|<message4>`")
    await ctx.send(embed=em)

@help.command()
async def fbi(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.fbi <Text Message>`")
    await ctx.send(embed=em)
@help.command()
async def worthless(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.worthless <Text Message>`")
    await ctx.send(embed=em)

@help.command()
async def water(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.water [member] <Text Message>`")
    await ctx.send(embed=em)

@help.command()
async def rip(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.rip <member>`")
    await ctx.send(embed=em)

@help.command()
async def disability(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.disability <member>`")
    await ctx.send(embed=em)

@help.command()
async def thisisshit(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.thisisshit <member>`")
    await ctx.send(embed=em)

@help.command()
async def myboi(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.myboi <member>`")
    await ctx.send(embed=em)
 
@help.command()
async def santa(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.santa <Text Message>`")
    await ctx.send(embed=em) 

@help.command()
async def news(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.news <member> <message1>|<message2>`")
    await ctx.send(embed=em)

@help.command()
async def yugioh(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.yugioh <message1>|<message2>`")
    await ctx.send(embed=em)

@help.command()
async def yugiohpfp(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.yugiohpfp <member1> <member2>`")
    await ctx.send(embed=em)

@help.command()
async def bitch(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.bitch <Text message>`")
    await ctx.send(embed=em)

@help.command()
async def billy(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.bily <Text message>`")
    await ctx.send(embed=em)

@help.command()
async def fact(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.fact <Text message>`")
    await ctx.send(embed=em)

@help.command()
async def say(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.say <Text message>`")
    await ctx.send(embed=em)

@help.command()
async def spoiler(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.spoiler <Text message>`")
    em.add_field(name="**Aliases**",value="`spoil`")
    await ctx.send(embed=em)

@help.command()
async def propose(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.propose <member>`")
    await ctx.send(embed=em)


@help.command()
async def match(ctx):
    em = discord.Embed(description="Use it to match pfp with your friend",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.match <member>`")
    await ctx.send(embed=em)

@help.command()
async def dumb(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.dumb <text>`")
    await ctx.send(embed=em)  
@help.command()
async def wallpunch(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.wallpunch <text>`")
    await ctx.send(embed=em)      
@help.command()
async def anime(ctx):
    em = discord.Embed(description="Searches anime on Mal",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.anime <Name of anime>`")
    await ctx.send(embed=em)

@help.command()
async def manga(ctx):
    em = discord.Embed(description="Searches manga on Mal",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.manga <Number of Msgs>`")
    await ctx.send(embed=em)

#@help.command()
#async def dm(ctx):
 #   em = discord.Embed(description="Dms the message to the member",color=0x00ff7d,timestamp=utc_now())
 #   em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
 #   em.set_footer(text= f'Requested by {ctx.author}' )
 #   em.add_field(name="**Usage**",value="`S.dm <member> <Text message`")
 #   em.add_field(name="**Permission required**",value="`Manage Server`")
 #   await ctx.send(embed=em)



@help.command()
async def announce(ctx):
    em = discord.Embed(description="Use it to do announcement",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.announce <everyone or here> <channel> <Text message>`")
    em.add_field(name="**Permission required**",value="`Manage Server`")
    await ctx.send(embed=em)

@help.command()
async def yt(ctx):
    em = discord.Embed(description="Searches video on Youtube",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.yt <search>`")
    await ctx.send(embed=em)

@help.command()
async def embed(ctx):
    em = discord.Embed(description="Use to create Embeds",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.embed [hexcode of color] <Text message>`")
    em.add_field(name="**Permission required**",value="`Manage Messages`")
    await ctx.send(embed=em)

@help.command()
async def rndqoute(ctx):
    em = discord.Embed(description="Sends a random anime qoute",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.rndqoute`")
    em.add_field(name="**Aliases**",value="`rq`")
    await ctx.send(embed=em)
@help.command()
async def rand(ctx):
    em = discord.Embed(description="Choose random number between the limits",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.rand <number>`")
    em.add_field(name="**Aliases**",value="`random`")
    await ctx.send(embed=em)
@help.command()
async def filler(ctx):
    em = discord.Embed(description="Sends filler episodes of anime, if any",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.filler <Anime>`")
    em.add_field(name="**Aliases**",value="`fill`")
    await ctx.send(embed=em)    

@help.command()
async def mal(ctx):
    em = discord.Embed(description="Use to check mal profile",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.mal <mal id>`")
    em.add_field(name="**Aliases**",value="`profile`")
    await ctx.send(embed=em)  

@help.command()
async def profile(ctx):
    em = discord.Embed(description="Use to see mal profile",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.profile`\nUse `S.set <mal-id>` to register")
    await ctx.send(embed=em)  

@help.command()
async def read(ctx):
    em = discord.Embed(description="Get link to read manga",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.read <Manga>`")
    await ctx.send(embed=em)

@help.command()
async def char(ctx):
    em = discord.Embed(description="Search Characters",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.char <Character Name>`")
    await ctx.send(embed=em)

@help.command()
async def eplist(ctx):
    em = discord.Embed(description="Sends the episode list of anime",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.eplist <Anime>`")
    
    await ctx.send(embed=em)  

@help.command()
async def wallpaper(ctx):
    em = discord.Embed(description="Sends Wallpapers",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.wallpaper [topic]` \n`S.mwallpaper [topic]` for mobile")
    em.add_field(name="**Aliases**",value="`wall`\n`mwall` for mobile")
    await ctx.send(embed=em)    

@help.command()
async def character(ctx):
    em = discord.Embed(description="Searchs Anime Characters",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.character <name>`")
    em.add_field(name="**Aliases**",value="`char`")
    await ctx.send(embed=em)
@help.command()
async def reddit(ctx):
    em = discord.Embed(description="Sends Sub-reddit posts",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.reddit <sub-reddit>`")
    em.add_field(name="**Aliases**",value="`red`")
    await ctx.send(embed=em)
@help.command()
async def addemoji(ctx):
    em = discord.Embed(description="Adds emoji in the server",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.addemoji <emoji link> [emoji name]`")
    em.add_field(name="**Permission required**",value="`Manage Emojis`")
    await ctx.send(embed=em)
@help.command()
async def challenge(ctx):
    em = discord.Embed(description="A trivia based chase game",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.challenge <mention>`")
    
    await ctx.send(embed=em)  
@help.command()
async def movie(ctx):
    em = discord.Embed(description="Searches movies/web series",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.movie <name>`")
    
    await ctx.send(embed=em)        

@help.command()
async def remind(ctx):
    em = discord.Embed(description="Toggles anime reminder",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.remind`")
    
    await ctx.send(embed=em)
@help.command()
async def addwatchlist(ctx):
    em = discord.Embed(description="Adds anime in your watchlist for reminder",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.addwatchlist <anime id>`")
    em.add_field(name="**Aliases**",value="`awl`")
    await ctx.send(embed=em) 
@help.command()
async def removewatchlist(ctx):
    em = discord.Embed(description="Removes anime from your watchlist for reminder",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.removewatchlist <anime id>`")
    em.add_field(name="**Aliases**",value="`rwl`")
    await ctx.send(embed=em) 

@help.command()
async def watchlist(ctx):
    em = discord.Embed(description="Shows anime in your watchlist for reminder",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.watchlist`")
    em.add_field(name="**Aliases**",value="`wl`")
    await ctx.send(embed=em)
@help.command()
async def airing(ctx):
    em = discord.Embed(description="Shows airing anime to add in your Watchlist",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.airing`")
    em.add_field(name="**Aliases**",value="`air`")
    await ctx.send(embed=em)   
@help.command()
async def setmal(ctx):
    em = discord.Embed(description="Tags your myanimelist account with your discord id",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.setmal <myanimelist id>`")
    await ctx.send(embed=em) 
@help.command()
async def removemal(ctx):
    em = discord.Embed(description="Removes your mal id from stela",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.removemal`")
    await ctx.send(embed=em)   

@help.command()
async def lookup(ctx):
    em = discord.Embed(description="Search waifus for waifu command",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.Lookup <name>`")
    em.add_field(name="**Aliases**",value="`lu`")
    await ctx.send(embed=em)        
@help.command()
async def setchannel(ctx):
    em = discord.Embed(description="Set a channel for anime updates in your server",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.setchannel <mention channel>`")
    em.add_field(name="**Permission required**",value="`Manage Server`")
    await ctx.send(embed=em)
@help.command()
async def removechannel(ctx):
    em = discord.Embed(description="Removes the channel from anime updates in your server",color=0x00ff7d,timestamp=utc_now())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.display_avatar.url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.removechannel`")
    em.add_field(name="**Permission required**",value="`Manage Server`")
    await ctx.send(embed=em)                     
# run the client on the server
EXTENSIONS = [
    'cogs.moderation',
    'cogs.roleplay',
    'cogs.fun',
    'cogs.memegen',
    # 'cogs.anime_reminder',
    'cogs.tournament',
    'cogs.chess',
    'cogs.anime_manga',
    'cogs.utility',
]

async def main_async():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError(
            "DISCORD_TOKEN is not set. Copy .env.example to .env and add your bot token."
        )
    async with client:
        for ext in EXTENSIONS:
            try:
                await client.load_extension(ext)
                print(f"✅ Loaded {ext}")
            except Exception as exc:
                print(f"❌ Failed to load {ext}: {exc}")
        await client.start(token)

def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
