from threading import Timer
import discord
from discord import embeds
from discord import user
from discord.client import Client
from discord.colour import Color #pip install discord
from discord.ext import commands, tasks
from discord.ext.commands import BucketType, Greedy
from discord.member import Member
import requests #requests
from discord.errors import DiscordServerError, Forbidden
import random, textwrap
import datetime
import json 
import os
from PIL import Image, ImageFont, ImageDraw  #pip install Pillow
from io import BytesIO
import typing
import asyncio
import numpy
import mal
from mal import *
import asyncio

from requests.api import delete
from lxml import html
#from waifu import waifupics, waifuname, waifuseries
import numpy as np
import urllib.parse, urllib.request, re
from asyncio import gather
from bs4 import BeautifulSoup
import math
import certifi
from pymongo import MongoClient, database
import aiohttp
import praw
from selenium import webdriver
#urban = UrbanClient()
os.chdir(r".vscode")#G:\bot\stella\.vscode

#prefix...................]
intents = discord.Intents.default()
intents.members = True
#client = commands.Bot(command_prefix='.', intents = intents)

client = commands.Bot(command_prefix = ('stela ','S.','s.','Stela '), intents = intents)
#@client.event 
#async def on_message(message):
    #if message.content.startswith(f'{client.user.mention}'):
       #await message.channel.send(f'The prefix is{client.command_prefix}')
    
#{} means its required
#() means its optional
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
#options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=r"chromedriver",options = options )#G:\bot\stella\chromedriver.exe
cluster = MongoClient("mongodb+srv://vivekprakash_db:passwordfordb@cluster0.4i3yj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=certifi.where()) 
client2 = MongoClient("mongodb+srv://vivekprakash_india:passwordfordb@cluster0.tf1px.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["discord"]  
mal_collect = db["mal"]             
animetriv_collect = db["anime-trivia"]
upd = db["anime-updates"]
listed = db["watchlist"]
chan = db['channels']
airingg = db['airing']
db2 = client2['Waifus']
girl = db2['images']
girl.create_index([('name','text'),('anime','text')])
redit = praw.Reddit(client_id = 'zSgZiWoFnzqqlA',
                    client_secret = 'eGzaxrgCrPj4DkuxKm21iFVxOHjq3g',
                    #username = 'ItzStela',
                    #password = 'password@10',
                    user_agent = "memes")
#error.................
@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You are too weak ;-; Work hard and get powers to do that :)")
    if isinstance(error,commands.MemberNotFound):
        await ctx.send("Member Not Found")    
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Pls use command properly! `S.help <command>`")    
    elif isinstance(error,Forbidden):
        await ctx.send("Give me powers to do that! I will not disappoint you ;-;")   
    elif isinstance(error,commands.CommandOnCooldown):
        await ctx.send(f" You have to wait {error.retry_after:,.2F} secs ¯\_(ツ)_/¯")     
    else:
        raise error       


    


# do stuff......
@client.event
async def on_ready():
    #status
    global owner
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Anime | S.help for commands"))
    owner  = client.get_user(745006368175423489)
    #welcome 
    general_channel = client.get_channel(772496570436419592)

    await general_channel.send('Hello Master')
    print("bot is online")
    await checkNewLoop.start()
     
#@client.event
#async def on_message(message):
   # if not message.author.bot:
    #    mention = f'<@{client.user.id}>'
        
    #    if mention == message.content:
    #        await message.reply("My prefixes are `S.` and `Stela`")
    #        await message.reply("You mentioned me :)")   
     #   await client.process_commands(message)         
#commands...................................................


@client.command(name='version')
async def version(context):
    myembed = discord.Embed(title='Current Version', description='The Bot is in version 1.4.3',color=0x00ebff)
    myid = '<@!745006368175423489>'
    
    myembed.add_field(name= "**Developer**", value= myid )
    
    await context.message.channel.send(embed=myembed)

@client.command(name='Bot')   
async def Bot(context):
    helpembed = discord.Embed (title='Hi', description='Its me, Stela',color=0x00ebff) 
    await context.author.send(embed=helpembed) 

#moderation.................................................................................... 
#kick...............
@client.command(name='kick',pass_context = True,aliases=["Kick"])    
@commands.has_permissions(kick_members=True)
async def kick(context, member : discord.Member, *,reason = None):
    if member != context.author:
        message = discord.Embed(color=0x00ebff)
        kickgif = ('https://cdn.discordapp.com/attachments/782562061812891648/782714161560944670/kicked1.gif','https://cdn.discordapp.com/attachments/782562061812891648/782714161560944670/kicked1.gif')
        rndkick = random.choice(kickgif)
        message.add_field(name='Kicked',value=f"You have been **kicked** from {context.guild.name} for {reason}")
        message.set_image(url=rndkick)
        kicked= discord.Embed(color=0x00ebff)
        kicked.add_field(name='Kicked',value=f"{member.mention} has been kicked from the server!! Hehe:)")
        await member.kick(reason=reason)
        await context.send(embed=kicked)
        await member.send(embed=message)
    else:
        await context.send("Want to kick yourself? :(")


    
   
    
    

#ban.....................    
@client.command(name='ban',pass_context = True,aliases=["Ban"])    
@commands.has_permissions(ban_members=True)
async def ban(context, member : discord.Member, *,reason=None):
    
    if member != context.author:
        await member.ban(reason=reason)
        banned= discord.Embed(color=0x00ebff)
        banned.add_field(name='Banned',value=f"{member.mention} has been **Banned** from the server!! Hehe:)")
        await context.send(embed=banned)
        message = discord.Embed(color=0x00ebff)
        bangif = ('https://cdn.discordapp.com/attachments/782562061812891648/782722014829084672/ban1.gif','https://cdn.discordapp.com/attachments/782562061812891648/782722005044691014/ban_2.gif')
        rndban = random.choice(bangif)
        message.add_field(name='Banned',value=f"You have been banned from {context.guild.name} for {reason}")
        message.set_image(url=rndban)

        await member.send(embed=message)
    else:
        await context.send("Want to ban yourself? :(")



#clear.....
@client.command(name="clear",aliases=["Clear",'Clean','clean','delete','Delete','purge','Purge'])    
@commands.has_permissions(manage_messages = True)
async def clear(context,amount=2):
    await context.channel.purge(limit = (amount+1))
    await context.send(f"`{amount} messages has been Deleted... 👍`",delete_after = 10)

#mute
#addrole
@client.command(name="addrole",aliases=["Addrole"])       
async def addrole(ctx,member :discord.Member,role: typing.Optional[discord.Role], *,rolename = None):
    if ctx.author == owner:
        try:
            
            if role != None:
                
                await member.add_roles(role)
                await ctx.reply(f"`{role.name}` role has been given to {member.mention}")
            else:   
                roless = discord.utils.get(ctx.guild.roles, name = rolename)
            
                await member.add_roles(roless)
                await ctx.reply(f"`{rolename}` role has been given to {member.mention}")
        except:
            await ctx.reply("Type `S.addrole <member> <ROLE NAME OR MENTION ROLE>`")
 
@client.command(name="removerole",aliases=["Removerole"])        
async def removerole(ctx,member :discord.Member,role: typing.Optional[discord.Role], *,rolename = None):
    if ctx.author == owner:
        try:
            
            if role != None:
                
                await member.remove_roles(role)
                await ctx.reply(f"`{role.name}` role has been removed from {member.mention}")
            else:   
                roless = discord.utils.get(ctx.guild.roles, name = rolename)
            
                await member.remove_roles(roless)
                await ctx.reply(f"`{rolename}` role has been removed from {member.mention}")
        except:
                await ctx.reply("Type `S.removerole <member> <ROLE NAME OR MENTION ROLE>`") 

@client.command(name='Steal',aliases=["steal"])
@commands.has_permissions(manage_emojis = True) 
async def steal(ctx, emoji:discord.Emoji, *, name):
    guild = ctx.guild   
    url = str(emoji.url)    
    
    if name == None:
        name = "not given"
    async with aiohttp.ClientSession() as ses:
        async with ses.get(url) as r:
                    
                try:
                    img_or_gif = BytesIO(await r.read())
                    b_value = img_or_gif.getvalue()
                    if r.status in range(200, 299):
                        emoji = await guild.create_custom_emoji(image=b_value, name=name)
                        await ctx.send(f'Successfully created emoji: <:{name}:{emoji.id}>')
                        await ses.close()
                    else:
                        
                        await ctx.send(f'something went wrong| Try another emoji')
                        await ses.close()

                except discord.HTTPException:
                   
                    await ctx.send('File size is too big!')
    #for emo in emojiss:
  
     #   print(emo)
@client.command(name='addemoji',aliases=["Addemoji"])
@commands.has_permissions(manage_emojis = True) 
async def addemoji(ctx, url: str, *, name):
    guild = ctx.guild   
    if name == None:
        name = "not given"
    
    async with aiohttp.ClientSession() as ses:
        async with ses.get(url) as r:
                    
                try:
                    img_or_gif = BytesIO(await r.read())
                    b_value = img_or_gif.getvalue()
                    if r.status in range(200, 299):
                        emoji = await guild.create_custom_emoji(image=b_value, name=name)
                        await ctx.send(f'Successfully created emoji: <:{name}:{emoji.id}>')
                        await ses.close()
                    else:
                        
                        await ctx.send(f'something went wrong| Try another emoji')
                        await ses.close()

                except discord.HTTPException:
                   
                    await ctx.send('File size is too big!')    

                
                
                  
#EMOTES................................................................
#blush......
@client.command(name='blush')    
async def blush(context,member: typing.Optional[discord.Member], *,gifmsg=None):
    blushes = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow(),color=0x00ebff)
    if member == None:
        blushes.set_author(name = f"{context.message.author.display_name}  is Blushing >///<",icon_url=f"{context.message.author.avatar_url}") 
    else:
        blushes.set_author(name = f"{context.message.author.display_name}  turned red because of {member.display_name}!! kawaiiii......",icon_url=f"{context.message.author.avatar_url}") 
     
    blushgif = ('https://cdn.discordapp.com/attachments/782562061812891648/795239281932238848/blush_1.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239291092598794/blush_3.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239298751660032/blush_2.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239306557784074/blush_5.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239308096307221/blush_6.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239308520325140/blush_4.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239309674151936/blush_7.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239319702994974/blush_8.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239322269909002/blush_12.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239324622782464/blush_10.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239326103371797/blush_11.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239327743475712/blush_9.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239334386991104/blush_13.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239337335455764/blush_14.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239338048618496/blush_15.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239340460343326/blush_16.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239341227114507/blush_17.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239351067082793/blush_18.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239350405169152/blush_19.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239369669476362/blush_21.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239371762434048/blush_20.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239375315009546/blush_22.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239378586566716/blush_23.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239381744353320/blush_24.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239389273260042/blush_26.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239393987395604/blush_25.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239397515722762/blush_27.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239399268810763/blush_28.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239400082505728/blush_29.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239412262502420/blush_31.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239411964182528/blush_32.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239417538150400/blush_30.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239420525674536/blush_34.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239423783731200/blush_33.gif','https://cdn.discordapp.com/attachments/782562061812891648/795239435745624124/blush_35.gif')
    rnd_blush = random.choice(blushgif)
    #blushes.add_field(name="kawaaiii",value=(f"{context.author.mention} is Blushing >///<"))
    blushes.set_image(url=rnd_blush)
   
    await context.send(embed=blushes)
    await context.message.delete()

#smile......
@client.command(name='smile',aliases = ["Smile"])    
async def smile(context,member: typing.Optional[discord.Member], *,gifmsg=None):
    smiles = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow(),color=0x00ebff) 
    if member == None:
        smiles.set_author(name = f"{context.message.author.display_name}  is Smiling ｡◕‿◕｡",icon_url=f"{context.message.author.avatar_url}") 
    else:
        smiles.set_author(name = f"{context.message.author.display_name}  is Smiling with {member.display_name}｡◕‿◕｡",icon_url=f"{context.message.author.avatar_url}")   
    smilegif = ('https://cdn.discordapp.com/attachments/782562061812891648/794511199814287390/smile_1.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511215182741524/smile_2.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511219536953344/smile_5.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511220690124810/smile_3.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511226754957322/smile_4.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511228176695306/smile_6.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511232006750248/smile_9.jpg','https://cdn.discordapp.com/attachments/782562061812891648/794511235541368872/smile_8.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511234480209920/smile_7.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511238038028308/smile_11.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511243905204244/smile_12.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511251383255040/smile_13.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511271110246400/smile_14.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511274511564830/smile_10.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511285210447872/smile_16.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511288075943937/smile_15.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511292790603776/smile_18.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511293566550016/smile_17.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511296942833674/smile_19.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511301907972096/smile_20.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511306573086761/smile_21.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511307424006174/smile_22.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511306128228352/smile_23.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511316575846410/smile_25.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511318245441536/smile_24.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511332610539530/smile_28.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511333902647296/smile_27.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511340579455046/smile_26.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511346771165234/smile_29.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511348548632576/smile_30.gif','https://cdn.discordapp.com/attachments/782562061812891648/794511353657688074/smile_31.gif','https://cdn.discordapp.com/attachments/782562061812891648/794512158335172619/smile_32.gif')   
    rnd_smile = random.choice(smilegif)
    #smiles.add_field(name="Happy",value=(f"{context.author.mention} is Smiling ｡◕‿◕｡"))
    smiles.set_image(url=rnd_smile)

    await context.send(embed=smiles)
    await context.message.delete()


#stare
@client.command(name='stare',aliases = ["Stare"])    
async def stare(context,member: typing.Optional[discord.Member], *,gifmsg=None):
    stares = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow(),color=0x00ebff) 
    if member == None:
        stares.set_author(name = f"{context.message.author.display_name}  is Staring O_o",icon_url=f"{context.message.author.avatar_url}") 
    else:
        stares.set_author(name = f"{context.message.author.display_name}  is Staring {member.display_name} O_o",icon_url=f"{context.message.author.avatar_url}")   
    staregif = ('https://cdn.discordapp.com/attachments/782562061812891648/789443912103755776/stare_2.gif','https://cdn.discordapp.com/attachments/782562061812891648/789443993212813332/stare_1.gif','https://cdn.discordapp.com/attachments/782562061812891648/789445620208500736/stare_3.gif','https://cdn.discordapp.com/attachments/782562061812891648/789445636226547722/stare_4.gif','https://cdn.discordapp.com/attachments/782562061812891648/789445650386518026/stare_5.gif','https://cdn.discordapp.com/attachments/782562061812891648/789445687497981972/stare_6.gif','https://cdn.discordapp.com/attachments/782562061812891648/789445747531186196/stare_7.gif','https://cdn.discordapp.com/attachments/782562061812891648/789445768111980614/stare_8.gif','https://cdn.discordapp.com/attachments/782562061812891648/789445802275504128/stare_9.gif','https://cdn.discordapp.com/attachments/782562061812891648/789445820398174238/stare_10.gif','https://cdn.discordapp.com/attachments/782562061812891648/789445870402666497/stare_11.gif','https://cdn.discordapp.com/attachments/782562061812891648/789445918264655942/stare_12.gif','https://cdn.discordapp.com/attachments/782562061812891648/789446040427823104/stare_13.gif','https://cdn.discordapp.com/attachments/782562061812891648/789446107759509514/stare_14.gif','https://cdn.discordapp.com/attachments/782562061812891648/789446241955479552/stare_15.gif','https://cdn.discordapp.com/attachments/782562061812891648/789446261379170344/stare_16.gif','https://cdn.discordapp.com/attachments/782562061812891648/789446388420968458/stare_17.gif','https://cdn.discordapp.com/attachments/782562061812891648/789446419786104862/stare_18.gif','https://cdn.discordapp.com/attachments/782562061812891648/789446493534289920/stare_19.gif','https://cdn.discordapp.com/attachments/782562061812891648/789446622169661460/stare_20.gif','https://cdn.discordapp.com/attachments/782562061812891648/789446750108123166/stare_21.gif','https://cdn.discordapp.com/attachments/782562061812891648/789446777958957066/stare_22.gif','https://cdn.discordapp.com/attachments/782562061812891648/789446817716240434/stare_23.gif','https://cdn.discordapp.com/attachments/782562061812891648/789446896560111656/stare_24.gif','https://cdn.discordapp.com/attachments/782562061812891648/789446991095922688/stare_25.gif','https://cdn.discordapp.com/attachments/782562061812891648/789447044862836746/stare_26.gif','https://cdn.discordapp.com/attachments/782562061812891648/789447104065175572/stare_27.gif','https://cdn.discordapp.com/attachments/782562061812891648/789447242821795870/stare_28.gif','https://cdn.discordapp.com/attachments/782562061812891648/789447268893851678/stare_29.gif','https://cdn.discordapp.com/attachments/782562061812891648/789447607981572146/stare_30.gif','https://cdn.discordapp.com/attachments/782562061812891648/789447700235812874/stare_31.gif')   
    rnd_stare = random.choice(staregif)
    #smiles.add_field(name="Happy",value=(f"{context.author.mention} is Smiling ｡◕‿◕｡"))
    stares.set_image(url=rnd_stare)

    await context.send(embed=stares)
    await context.message.delete()

#laugh
@client.command(name='laugh',aliases = ["Laugh"])    
async def laugh(context,member: typing.Optional[discord.Member], *,gifmsg=None):
    laughs = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow(),color=0x00ebff) 
    if member == None:
        laughs.set_author(name = f"{context.message.author.display_name}  is laughing",icon_url=f"{context.message.author.avatar_url}") 
    else:
        laughs.set_author(name = f"{context.message.author.display_name}  is laughing on {member.display_name} ",icon_url=f"{context.message.author.avatar_url}")   
    laughgif = ('https://cdn.discordapp.com/attachments/782562061812891648/789435933350428682/laugh_1.gif','https://cdn.discordapp.com/attachments/782562061812891648/789435946047242240/laugh_3.gif','https://cdn.discordapp.com/attachments/782562061812891648/789435945753640960/laugh_2.gif','https://cdn.discordapp.com/attachments/782562061812891648/789435950320058368/laugh_4.gif','https://cdn.discordapp.com/attachments/782562061812891648/789435953848647700/laugh_5.gif','https://cdn.discordapp.com/attachments/782562061812891648/789435957735587870/laugh_7.gif','https://cdn.discordapp.com/attachments/782562061812891648/789435961943130132/laugh_6.gif','https://cdn.discordapp.com/attachments/782562061812891648/789435964212117514/laugh_9.gif','https://cdn.discordapp.com/attachments/782562061812891648/789435968183599124/laugh_10.gif','https://cdn.discordapp.com/attachments/782562061812891648/789435973796757504/laugh_8.gif','https://cdn.discordapp.com/attachments/782562061812891648/789435978901094420/laugh_12.gif','https://cdn.discordapp.com/attachments/782562061812891648/789435982000422942/laugh_13.gif','https://cdn.discordapp.com/attachments/782562061812891648/789435980238290974/laugh_11.gif','https://cdn.discordapp.com/attachments/782562061812891648/789435991504322570/laugh_14.gif','https://cdn.discordapp.com/attachments/782562061812891648/789435993698730024/laugh_16.gif','https://cdn.discordapp.com/attachments/782562061812891648/789435993102614548/laugh_15.gif','https://cdn.discordapp.com/attachments/782562061812891648/789435996843409419/laugh_17.gif','https://cdn.discordapp.com/attachments/782562061812891648/789436004238753812/laugh_19.gif','https://cdn.discordapp.com/attachments/782562061812891648/789436005136465950/laugh_18.gif','https://cdn.discordapp.com/attachments/782562061812891648/789436007300726844/laugh_20.gif','https://cdn.discordapp.com/attachments/782562061812891648/789436026615365642/laugh_21.gif','https://cdn.discordapp.com/attachments/782562061812891648/789436040381333524/laugh_23.gif','https://cdn.discordapp.com/attachments/782562061812891648/789436045430358016/laugh_24.gif','https://cdn.discordapp.com/attachments/782562061812891648/789436050514509864/laugh_25.gif','https://cdn.discordapp.com/attachments/782562061812891648/789436059167490077/laugh_26.gif','https://cdn.discordapp.com/attachments/782562061812891648/789436065425129472/laugh_27.gif','https://cdn.discordapp.com/attachments/782562061812891648/789436068189569044/laugh_28.gif','https://cdn.discordapp.com/attachments/782562061812891648/789436074854055946/laugh_29.gif','https://cdn.discordapp.com/attachments/782562061812891648/789436082122129428/laugh_30.gif','https://cdn.discordapp.com/attachments/782562061812891648/789436090477707284/laugh_31.gif','https://cdn.discordapp.com/attachments/782562061812891648/789436097792442368/laugh_32.gif','https://cdn.discordapp.com/attachments/782562061812891648/789436101789483008/laugh_33.gif','https://cdn.discordapp.com/attachments/782562061812891648/789436107284545536/laugh_34.gif')   
    rnd_laugh = random.choice(laughgif)
    #smiles.add_field(name="Happy",value=(f"{context.author.mention} is Smiling ｡◕‿◕｡"))
    laughs.set_image(url=rnd_laugh)

    await context.send(embed=laughs)
    await context.message.delete()    
#dance

       # await context.message.delete() 
@client.command(name='dance')    
async def dance(context, *,gifmsg=None):
    dances = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow(),color=0x00ebff) 
    dances.set_author(name = f"{context.message.author.display_name}  is Dancing ƪ(‾.‾“)┐",icon_url=f"{context.message.author.avatar_url}") 
    dancegif = ('https://cdn.discordapp.com/attachments/782562061812891648/783588914845712445/dance_32.gif','https://cdn.discordapp.com/attachments/782562061812891648/783588908256460830/dance_31.gif','https://cdn.discordapp.com/attachments/782562061812891648/783367053120897024/dance_30.gif','https://cdn.discordapp.com/attachments/782562061812891648/783367040429195304/dance_28.gif','https://cdn.discordapp.com/attachments/782562061812891648/783367042485059614/dance_29.gif','https://cdn.discordapp.com/attachments/782562061812891648/783367034427277342/dance_27.gif','https://cdn.discordapp.com/attachments/782562061812891648/783367010843099156/dance_26.gif','https://cdn.discordapp.com/attachments/782562061812891648/783367006023450694/dance_25.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366998456533062/dance_24.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366987798937620/dance_22.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366990193491998/dance_23.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366984175452200/dance_21.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366962431655996/dance_20.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366955133698108/dance_19.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366932325859388/dance_18.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366920493072415/dance_17.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366920694530058/dance_16.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366907029356564/dance_15.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366900256079902/dance_14.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366873633914910/dance_12.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366869020704798/dance_13.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366823449854012/dance_10.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366852662788136/dance_11.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366816352567296/dance_9.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366809696600074/dance_8.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366800284975134/dance_3.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366797033472050/dance_7.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366793015590942/dance_6.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366789958074418/dance_4.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366782760648744/dance_2.gif','https://cdn.discordapp.com/attachments/782562061812891648/783366753131429940/dance_1.gif') 
    rnd_dance = random.choice(dancegif)
    #dances.add_field(name="Dance",value=(f"{context.author.mention} is Dancing ƪ(‾.‾“)┐"))
    dances.set_image(url=rnd_dance)

    await context.send(embed=dances)
    await context.message.delete()

#sleepy
@client.command(name='sleep')
async def sleep(context, *,gifmsg=None):
    sleeps = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow(),color=0x00ebff) 
    sleeps.set_author(name = f"{context.message.author.display_name}  is Sleeping ",icon_url=f"{context.message.author.avatar_url}") 
    sleepgif = ('https://media.discordapp.net/attachments/782562061812891648/782574466886270976/sleep_30.gif','https://media.discordapp.net/attachments/782562061812891648/782574457469927424/sleep_29.gif','https://media.discordapp.net/attachments/782562061812891648/782574445281673216/sleep_28.gif','https://media.discordapp.net/attachments/782562061812891648/782574439824883732/sleep_27.gif','https://media.discordapp.net/attachments/782562061812891648/782573053677666324/sleep_26.gif','https://media.discordapp.net/attachments/782562061812891648/782572448583385098/sleep_25.gif','https://media.discordapp.net/attachments/782562061812891648/782572446833442816/sleep_21.gif','https://media.discordapp.net/attachments/782562061812891648/782572439733141504/sleep_22.gif','https://media.discordapp.net/attachments/782562061812891648/782572424934981632/sleep_24.gif','https://media.discordapp.net/attachments/782562061812891648/782572418782199808/sleep_23.gif','https://media.discordapp.net/attachments/782562061812891648/782572407574626324/sleep_20.gif','https://media.discordapp.net/attachments/782562061812891648/782572397660078080/sleep_18.gif','https://media.discordapp.net/attachments/782562061812891648/782572391300726784/sleep_16.gif','https://media.discordapp.net/attachments/782562061812891648/782572390910656512/sleep_17.gif','https://media.discordapp.net/attachments/782562061812891648/782572388021305345/sleep_15.gif','https://media.discordapp.net/attachments/782562061812891648/782572384557203466/sleep_14.gif','https://media.discordapp.net/attachments/782562061812891648/782572382081515520/sleep_13.gif','https://media.discordapp.net/attachments/782562061812891648/782572376398233600/sleep_12.gif','https://media.discordapp.net/attachments/782562061812891648/782572371923435560/sleep_11.gif','https://media.discordapp.net/attachments/782562061812891648/782568151132012594/sleep_4.gif','https://media.discordapp.net/attachments/782562061812891648/782568155464990730/sleep_5.gif','https://media.discordapp.net/attachments/782562061812891648/782568162814066698/sleep_6.gif?width=379&height=468','https://media.discordapp.net/attachments/782562061812891648/782568171952406578/sleep_7.gif','https://media.discordapp.net/attachments/782562061812891648/782568176386572308/sleep_8.gif','https://media.discordapp.net/attachments/782562061812891648/782568177112186920/sleep_9.gif','https://media.discordapp.net/attachments/782562061812891648/782568180094074930/sleep_10.gif','https://media.discordapp.net/attachments/782562061812891648/782564354733506631/sleep_2.gif','https://media.discordapp.net/attachments/782562061812891648/782564072130215966/sleep_3.gif','https://media.discordapp.net/attachments/782562061812891648/782564014781628416/sleep_1.gif')
    rnd_sleep = random.choice(sleepgif)
    #sleeps.add_field(name="Sleepy",value=(f"{context.author.mention} is Sleeping"))
    sleeps.set_image(url=rnd_sleep)

    await context.send(embed=sleeps)
    await context.message.delete()

#thinking..
@client.command(name='think')
async def think(context, *,gifmsg=None):
    thinks = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow(),color=0x00ebff)   
    thinks.set_author(name = f"{context.message.author.display_name}  is Thinking ",icon_url=f"{context.message.author.avatar_url}") 
    thinkgif = ('https://cdn.discordapp.com/attachments/782562061812891648/782647107529343016/thinking_30.gif','https://cdn.discordapp.com/attachments/782562061812891648/782647075372269658/thinking_29.gif','https://cdn.discordapp.com/attachments/782562061812891648/782647062038052864/thinking_28.gif','https://cdn.discordapp.com/attachments/782562061812891648/782647054299037696/thinking_26.gif','https://cdn.discordapp.com/attachments/782562061812891648/782647048319139840/thinking_25.gif','https://cdn.discordapp.com/attachments/782562061812891648/782647041158545439/thinking_24.gif','https://cdn.discordapp.com/attachments/782562061812891648/782647028530151454/thinking_22.gif','https://cdn.discordapp.com/attachments/782562061812891648/782647029812822016/thinking_23.gif','https://cdn.discordapp.com/attachments/782562061812891648/782647017297281096/thinking_20.gif','https://media.discordapp.net/attachments/782562061812891648/782647022641217556/thinking_21.gif','https://cdn.discordapp.com/attachments/782562061812891648/782647005217554472/thinking_19.gif','https://cdn.discordapp.com/attachments/782562061812891648/782647000532516864/thinking_18.gif','https://cdn.discordapp.com/attachments/782562061812891648/782646966542532628/thinking_15.gif','https://media.discordapp.net/attachments/782562061812891648/782646967074947102/thinking_17.gif','https://media.discordapp.net/attachments/782562061812891648/782646955788337184/thinking_14.gif','https://media.discordapp.net/attachments/782562061812891648/782646945239400559/thinking_13.gif','https://media.discordapp.net/attachments/782562061812891648/782646943104892958/thinking_12.gif','https://media.discordapp.net/attachments/782562061812891648/782646925798408212/thinking_11.gif','https://media.discordapp.net/attachments/782562061812891648/782646919809728593/thinking_10.gif','https://media.discordapp.net/attachments/782562061812891648/782646908371861514/thinking_9.gif','https://media.discordapp.net/attachments/782562061812891648/782646905972588584/thinking_8.gif','https://media.discordapp.net/attachments/782562061812891648/782646893024641034/thinking_6.gif','https://media.discordapp.net/attachments/782562061812891648/782646894118830100/thinking_7.gif','https://media.discordapp.net/attachments/782562061812891648/782646884417273926/thinking_5.gif','https://media.discordapp.net/attachments/782562061812891648/782646880323895316/thinking_4.gif','https://media.discordapp.net/attachments/782562061812891648/782646867682263040/thinking_3.gif','https://media.discordapp.net/attachments/782562061812891648/782646862334132264/thinking_1.gif?width=468&height=468','https://media.discordapp.net/attachments/782562061812891648/782646857284976640/thinking_2.gif')
    rnd_think = random.choice(thinkgif)
    #thinks.add_field(name="Think",value=(f"{context.author.mention} is Thinking"))
    thinks.set_image(url=rnd_think)

    await context.send(embed=thinks)
    await context.message.delete() 

#cry.......
@client.command(name='cry')
async def cry(context, *,gifmsg=None):
    crys = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow() ,color=0x00ebff)  
    crys.set_author(name = f"{context.message.author.display_name}  is Crying   ༎ຶ‿༎ຶ ",icon_url=f"{context.message.author.avatar_url}") 
    crygif = ('https://cdn.discordapp.com/attachments/782562061812891648/782897297645371393/crying_30.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897287285702656/crying_29.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897284648140800/crying_28.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897280738918410/crying_27.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897274073513994/crying_26.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897261637140480/crying_25.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897255660912650/crying_24.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897247641010256/crying_23.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897242272694272/crying_22.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897237734326282/crying_21.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897226539859988/crying_19.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897225856581642/crying_20.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897217315799100/crying_18.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897207413702666/crying_17.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897200412885002/crying_16.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897195678302238/crying_15.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897190921306112/crying_14.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897180260302858/crying_12.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897174265724949/crying_13.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897162378805268/crying_11.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897156650041394/crying_10.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897148580593664/crying_9.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897143060365332/crying_8.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897140950761502/crying_7.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897136194027560/crying_5.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897132394905650/crying_6.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897125591351296/crying_1.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897123070443540/crying_4.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897121648312320/crying_3.gif','https://cdn.discordapp.com/attachments/782562061812891648/782897119953420309/crying_2.gif')
    rnd_cry = random.choice(crygif)
    #crys.add_field(name="Cry",value=(f"{context.message.author.display_name} is Crying ༎ຶ‿༎ຶ"))
    crys.set_image(url=rnd_cry)

    await context.send(embed=crys) 
    await context.message.delete()    

#triggered..
@client.command(name='rage',aliases= ["angry","Rage","Angry","Anger","anger","Triggered","triggered"])
async def rage(context,member: typing.Optional[discord.Member] = None , *,gifmsg=None):
    triggereds = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow() ,color=0x00ebff)
    if member == None:
        triggereds.set_author(name = f"{context.message.author.display_name} is Triggered.... ",icon_url=f"{context.message.author.avatar_url}")
    else:
        triggereds.set_author(name = f"{context.message.author.display_name} is angry with {member.display_name}  ",icon_url=f"{context.message.author.avatar_url}")
      
    triggeredgif = ('https://cdn.discordapp.com/attachments/782562061812891648/789078382172307456/anger_5.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078390527098890/anger_6.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078400215810058/anger_7.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078405923602453/anger_8.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078427444969522/anger_10.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078427495038996/anger_9.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078449155211314/anger_11.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078460215459850/anger_12.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078469593923584/anger_13.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078486630793226/anger_14.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078507916361778/anger_15.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078517186560000/anger_16.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078526241275924/anger_17.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078531954049034/anger_18.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078544277700678/anger_19.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078559918129212/anger_20.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078584077058048/anger_21.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078586766000138/anger_22.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078596315512832/anger_23.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078606671380510/anger_24.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078612942258206/anger_25.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078629383536640/anger_27.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078629032263720/anger_26.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078645012168714/anger_28.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078674414370856/anger_30.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078686770528256/anger_31.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078691946299422/anger_32.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078701949190174/anger_33.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078992748937246/anger_34.gif','https://cdn.discordapp.com/attachments/782562061812891648/789080174150680586/anger_35.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078375959363604/anger_4.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078371363323924/anger_3.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078365574266900/anger_1.gif','https://cdn.discordapp.com/attachments/782562061812891648/789078365733650454/anger_2.gif')
    rnd_triggered = random.choice(triggeredgif)
    #triggereds.add_field(name="Triggered",value=(f"{context.author.mention} is Triggered ༎ຶ‿༎ຶ"))
    triggereds.set_image(url=rnd_triggered)

    await context.send(embed=triggereds) 
    await context.message.delete() 

@client.command(name='pout',aliases= ["Pout"])
async def pout(context,member: typing.Optional[discord.Member] = None , *,gifmsg=None):
    pouts = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow() ,color=0x00ebff)
    if member == None:
        pouts.set_author(name = f"{context.message.author.display_name} is pouting.... ",icon_url=f"{context.message.author.avatar_url}")
    else:
        pouts.set_author(name = f"{context.message.author.display_name} is pouting at {member.display_name}  ",icon_url=f"{context.message.author.avatar_url}")
      
    poutgif = ('https://cdn.discordapp.com/attachments/782562061812891648/783725881507184650/pout_1.gif','https://cdn.discordapp.com/attachments/782562061812891648/783725888403144764/pout_10.gif','https://cdn.discordapp.com/attachments/782562061812891648/783725908832813116/pout_2.gif','https://cdn.discordapp.com/attachments/782562061812891648/783725948641345536/pout_3.gif','https://cdn.discordapp.com/attachments/782562061812891648/783725952353042462/pout_4.gif','https://cdn.discordapp.com/attachments/782562061812891648/783725971378405396/pout_5.gif','https://cdn.discordapp.com/attachments/782562061812891648/783725977531449364/pout_6.gif','https://cdn.discordapp.com/attachments/782562061812891648/783725998734442547/pout_7.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726042388889610/pout_9.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726046448713738/pout_8.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726048335364096/pout_10.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726067466109019/pout_11.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726083777757234/pout_12.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726093390708806/pout_14.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726095043133450/pout_13.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726100244463667/pout_15.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726119186202674/pout_16.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726141252042834/pout_17.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726165868281856/pout_18.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726173032546314/pout_19.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726185929900042/pout_20.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726195438780456/pout_21.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726221368098907/pout_22.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726244474257428/pout_23.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726263902404608/pout_24.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726283514970202/pout_25.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726309086855178/pout_26.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726328398086184/pout_27.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726328398086184/pout_27.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726346852499466/pout_28.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726373041864735/pout_29.gif','https://cdn.discordapp.com/attachments/782562061812891648/783726400423198720/pout_30.gif')
    rnd_pout = random.choice(poutgif)
    #triggereds.add_field(name="Triggered",value=(f"{context.author.mention} is Triggered ༎ຶ‿༎ຶ"))
    pouts.set_image(url=rnd_pout)

    await context.send(embed=pouts) 
    await context.message.delete()    

#smug.....
@client.command(name='smug')
async def smug(context, *,gifmsg=None):
    smugs = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow() ,color=0x00ebff)
     
    smugs.set_author(name = f"{context.message.author.display_name}  is Smirking ",icon_url=f"{context.message.author.avatar_url}")   
    smuggif = ('https://images-ext-1.discordapp.net/external/DQkHEFdPW2-ZlXC0_UVHWTQIoQ440fbL2vl_u5wWBbs/https/cdn.weeb.sh/images/HJD-IJtw-.gif','https://images-ext-2.discordapp.net/external/XgG5PzlOGQ095Df4fU-h-x1CsT5lSLBbJ-jDV8mmtFQ/https/cdn.weeb.sh/images/H1xgWUktPW.gif')
    rnd_smug = random.choice(smuggif)
    #smugs.add_field(name="Smug",value=(f"{context.author.mention} is Smirking on {member.mention}"))
    # smugs.add_field(name="Smug",value=(f"{context.message.author.display_name} is Smirking on {member.display_name}"))
    smugs.set_image(url=rnd_smug)

    await context.send(embed=smugs)
    await context.message.delete()  
#action...............................................................
#kill...

@client.command(name='kill')
async def kill(context,member: discord.Member, *,gifmsg=None):
    if  member == context.author:
        kills = discord.Embed(timestamp=datetime.datetime.utcnow() ,color=0x00ebff) 
        kills.set_author(name = f"{context.message.author.display_name} don't die!! I'm with you..... ",icon_url=f"{context.message.author.avatar_url}")   
        killgif = ('https://cdn.discordapp.com/attachments/782562061812891648/785465632409649162/hug_15.gif','https://cdn.discordapp.com/attachments/782562061812891648/785465589740601344/hug_17.gif','https://cdn.discordapp.com/attachments/782562061812891648/785423760203317268/hug_18.gif','https://cdn.discordapp.com/attachments/782562061812891648/785423760034627594/hug_14.gif','https://cdn.discordapp.com/attachments/782562061812891648/785423757320912926/hug_16.gif','https://cdn.discordapp.com/attachments/782562061812891648/785423755077353522/hug_11.gif','https://cdn.discordapp.com/attachments/782562061812891648/785423753143648296/hug_12.gif','https://cdn.discordapp.com/attachments/782562061812891648/785423752204779540/hug_13.gif','https://cdn.discordapp.com/attachments/782562061812891648/785423751080312862/hug_10.gif','https://cdn.discordapp.com/attachments/782562061812891648/785420708792631296/hug_9.gif','https://cdn.discordapp.com/attachments/782562061812891648/785420707612852264/hug_8.gif','https://cdn.discordapp.com/attachments/782562061812891648/785420700059172894/hug_6.gif','https://cdn.discordapp.com/attachments/782562061812891648/785420699904245790/hug_5.gif','https://cdn.discordapp.com/attachments/782562061812891648/785420699056734279/hug_7.gif','https://cdn.discordapp.com/attachments/782562061812891648/785420695969464340/hug_4.gif','https://cdn.discordapp.com/attachments/782562061812891648/785420694002335764/hug_3.gif','https://cdn.discordapp.com/attachments/782562061812891648/785420688486826014/hug_2.gif','https://cdn.discordapp.com/attachments/782562061812891648/785420687942483978/hug_1.gif')
        rnd_kill = random.choice(killgif)
        kills.set_image(url=rnd_kill)
        await context.send(embed=kills) 

    else:
        kills = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow() ,color=0x00ebff) 
        kills.set_author(name = f"{context.message.author.display_name} is Murdering {member.display_name} ! Oh my... ",icon_url=f"{context.message.author.avatar_url}")   
        killgif = ('https://cdn.discordapp.com/attachments/782562061812891648/782990569441198151/kill_18.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990626551496704/kill_19.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990641461592084/kill_21.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990640786964500/kill_20.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990712387534859/kill_22.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990717860970586/kill_23.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990726862602280/kill_24.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990880973258762/kill_25.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990900740751392/kill_28.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990906424688650/kill_29.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990911591284746/kill_30.gif','https://cdn.discordapp.com/attachments/782562061812891648/782992926191517756/kill_26.gif','https://cdn.discordapp.com/attachments/782562061812891648/782994591178555442/kill_27.gif','https://cdn.discordapp.com/attachments/782562061812891648/783259161512116244/kill_31.gif','https://cdn.discordapp.com/attachments/782562061812891648/782989842656264222/kill_4.gif','https://cdn.discordapp.com/attachments/782562061812891648/782989850994802693/kill_3.gif','https://cdn.discordapp.com/attachments/782562061812891648/782989850994802693/kill_3.gif','https://cdn.discordapp.com/attachments/782562061812891648/782989851288535061/kill_2.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990058684153856/kill_5.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990191861301248/kill_7.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990191588802620/kill_8.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990254788837386/kill_9.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990256429465610/kill_10.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990387077447700/kill_11.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990390546268170/kill_12.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990430873714728/kill_13.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990439351058452/kill_14.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990512368910346/kill_15.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990516950007848/kill_16.gif','https://cdn.discordapp.com/attachments/782562061812891648/782990563628548136/kill_17.gif','https://cdn.discordapp.com/attachments/782562061812891648/782989841431920666/kill_1.gif')
        rnd_kill = random.choice(killgif)
    #smugs.add_field(name="Smug",value=(f"{context.author.mention} is Smirking on {member.mention}"))
    # smugs.add_field(name="Smug",value=(f"{context.message.author.display_name} is Smirking on {member.display_name}"))
        kills.set_image(url=rnd_kill)

        await context.send(embed=kills)
        await context.message.delete()      
#bonk

@client.command(name='bonk',aliases=["Bonk"])
async def bonk(context,member: discord.Member, *,gifmsg=None):
    bonks = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow() ,color=0x00ebff)

    bonks.set_author(name = f"{context.message.author.display_name} bonks {member.display_name} on the head.... ",icon_url=f"{context.message.author.avatar_url}")   
    bonkgif = ('https://cdn.discordapp.com/attachments/782562061812891648/802402148021174282/bonk_22.gif','https://cdn.discordapp.com/attachments/782562061812891648/802402147772661770/bonk_21.gif','https://cdn.discordapp.com/attachments/782562061812891648/802402147383509023/bonk_20.gif','https://cdn.discordapp.com/attachments/782562061812891648/802401983503007764/bonk_18.gif','https://cdn.discordapp.com/attachments/782562061812891648/802401983280840705/bonk_17.gif','https://cdn.discordapp.com/attachments/782562061812891648/802401982983438336/bonk_16.gif','https://cdn.discordapp.com/attachments/782562061812891648/802401982726799400/bonk_15.gif','https://cdn.discordapp.com/attachments/782562061812891648/802399252894056498/bonk_1.gif','https://cdn.discordapp.com/attachments/782562061812891648/802399252466106388/bonk_2.gif','https://cdn.discordapp.com/attachments/782562061812891648/802399197944217641/bonk_3.gif','https://cdn.discordapp.com/attachments/782562061812891648/802399197701079070/bonk_4.gif','https://cdn.discordapp.com/attachments/782562061812891648/802399197487562762/bonk_5.gif','https://cdn.discordapp.com/attachments/782562061812891648/802399197256089630/bonk_6.gif','https://cdn.discordapp.com/attachments/782562061812891648/802399196950560778/bonk_7.gif','https://cdn.discordapp.com/attachments/782562061812891648/802399196736258098/bonk_8.gif','https://cdn.discordapp.com/attachments/782562061812891648/802399105246167040/bonk_9.gif','https://cdn.discordapp.com/attachments/782562061812891648/802399104990052372/bonk_10.gif','https://cdn.discordapp.com/attachments/782562061812891648/802399104780730378/bonk_11.gif','https://cdn.discordapp.com/attachments/782562061812891648/802399104462356520/bonk_12.gif','https://cdn.discordapp.com/attachments/782562061812891648/802399104268763146/bonk_13.gif','https://cdn.discordapp.com/attachments/782562061812891648/802399103891800114/bonk_14.gif')
    rnd_bonk = random.choice(bonkgif)
    bonks.set_image(url=rnd_bonk) 
    await context.send(embed=bonks) 
    await context.message.delete() 

@client.command(name='punch',aliases=["Punch"])
async def punch(context,member: discord.Member, *,gifmsg=None):
    punchs = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow() ,color=0x00ebff)

    punchs.set_author(name = f"{context.message.author.display_name} punchs {member.display_name} Ha! ",icon_url=f"{context.message.author.avatar_url}")   
    punchgif = ('https://i.imgur.com/YJrX0hC.gif','https://i.imgur.com/vS2rUES.gif','https://i.imgur.com/Pm8fekf.gif','https://i.imgur.com/dpDqbXN.gif','https://i.imgur.com/wZKzFsk.gif','https://i.imgur.com/eDKXP7h.gif','https://i.imgur.com/wOj0iuK.gif','https://i.imgur.com/vstkI9k.gif','https://i.imgur.com/BR43afH.gif','https://i.imgur.com/Xr6Yzzw.gif','https://i.imgur.com/zv92jMR.gif','https://i.imgur.com/94BzVNx.gif','https://i.imgur.com/mOxZMps.gif','https://i.imgur.com/yTs6ioC.gif','https://i.imgur.com/JJNVkVy.gif','https://i.imgur.com/O20xM2k.gif','https://i.imgur.com/A9jhWJu.gif','https://i.imgur.com/iQ7HQED.gif','https://i.imgur.com/4wCSoTd.gif','https://i.imgur.com/YvEYrDj.gif','https://i.imgur.com/4eHqGR7.gif','https://i.imgur.com/S7d8z4J.gif','https://i.imgur.com/E9qS559.gif','https://i.imgur.com/fgsPMli.gif')
    print(len(punchgif))
    rnd_punch = random.choice(punchgif)
    punchs.set_image(url=rnd_punch) 
    await context.send(embed=punchs) 
    await context.message.delete()       
#slap
@client.command(name='slap',aliases=["Slap"])
async def slap(context,member: discord.Member, *,gifmsg=None):
    slaps = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow() ,color=0x00ebff)

    slaps.set_author(name = f"{context.message.author.display_name} is slapping {member.display_name}  ",icon_url=f"{context.message.author.avatar_url}")   
    slapgif = ('https://cdn.discordapp.com/attachments/782562061812891648/803176639969624074/Slap2.gif','https://cdn.discordapp.com/attachments/782562061812891648/803181679308963850/Slap2.gif','https://cdn.discordapp.com/attachments/782562061812891648/803183012103454760/Slap3.gif','https://cdn.discordapp.com/attachments/782562061812891648/803183450940506202/Slap4.gif','https://cdn.discordapp.com/attachments/782562061812891648/803183766829924372/Slap5.gif','https://cdn.discordapp.com/attachments/782562061812891648/803184358890537050/Slap6.gif','https://cdn.discordapp.com/attachments/782562061812891648/803184758724362260/Slap7.gif','https://cdn.discordapp.com/attachments/782562061812891648/803185254629376020/Slap8.gif','https://cdn.discordapp.com/attachments/782562061812891648/803187334371475466/Slap11.gif','https://cdn.discordapp.com/attachments/782562061812891648/803188847587360818/Slap12.gif','https://cdn.discordapp.com/attachments/782562061812891648/803221561846136832/Slap11.gif','https://cdn.discordapp.com/attachments/782562061812891648/803221702926532658/Slap12.gif','https://cdn.discordapp.com/attachments/782562061812891648/803221837622018058/Slap13.gif','https://cdn.discordapp.com/attachments/782562061812891648/803221929166241822/Slap14.gif','https://cdn.discordapp.com/attachments/782562061812891648/803222200915591188/Slap15.gif','https://cdn.discordapp.com/attachments/782562061812891648/803588564826324992/Slap17.gif','https://cdn.discordapp.com/attachments/782562061812891648/803590140588589076/Slap19.gif','https://cdn.discordapp.com/attachments/782562061812891648/803590320491200552/Slap20.gif','https://cdn.discordapp.com/attachments/782562061812891648/803590819860709396/Slap21.gif','https://cdn.discordapp.com/attachments/782562061812891648/803591010236104705/Slap22.gif','https://cdn.discordapp.com/attachments/782562061812891648/804253033545859082/Slap23.gif','https://cdn.discordapp.com/attachments/782562061812891648/804253287557627904/Slap24.gif','https://cdn.discordapp.com/attachments/782562061812891648/804253667766698025/Slap25.gif','https://cdn.discordapp.com/attachments/782562061812891648/804254414641692692/Slap26.gif','https://cdn.discordapp.com/attachments/782562061812891648/804254783455363082/Slap27.gif','https://cdn.discordapp.com/attachments/782562061812891648/804255835450638346/Slap28.gif','https://cdn.discordapp.com/attachments/782562061812891648/804256388263575552/Slap29.gif','https://cdn.discordapp.com/attachments/782562061812891648/804256899276341258/Slap30.gif')
    rnd_slap = random.choice(slapgif)
    slaps.set_image(url=rnd_slap) 
    await context.send(embed=slaps) 
    await context.message.delete() 

#poke
@client.command(name='poke',aliases=["Poke"])
async def poke(context,member: discord.Member, *,gifmsg=None):
    pokes = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow() ,color=0x00ebff)

    pokes.set_author(name = f"{context.message.author.display_name} pokes {member.display_name}  ",icon_url=f"{context.message.author.avatar_url}")   
    pokegif = ('https://cdn.discordapp.com/attachments/782562061812891648/803204770668085258/poke_6.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204746000859136/poke_1.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204747216683038/poke_2.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204747418664970/poke_3.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204747599151124/poke_4.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204770440544276/poke_5.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204770869149696/poke_7.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204771108356126/poke_8.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204809649684500/poke_9.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204809922052116/poke_10.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204810064134205/poke_11.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204810253926430/poke_12.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204841291382814/poke_13.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204841483927582/poke_14.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204841702686720/poke_15.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204841899425852/poke_16.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204871552761856/poke_17.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204872048214057/poke_18.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204872248754196/poke_22.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204872446935101/poke_23.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204919711629312/poke_24.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204920186241024/poke_25.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204920408801280/poke_21.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204920945147965/poke_20.gif','https://cdn.discordapp.com/attachments/782562061812891648/803204921427886090/poke_19.gif','https://cdn.discordapp.com/attachments/782562061812891648/803219135529091092/poke_26.gif','https://cdn.discordapp.com/attachments/782562061812891648/803219135857295391/poke_27.gif','https://cdn.discordapp.com/attachments/782562061812891648/803219587537698847/poke_25_remastered.gif','https://cdn.discordapp.com/attachments/782562061812891648/803220821421981716/poke_28.gif','https://cdn.discordapp.com/attachments/782562061812891648/803220821706801192/poke_29.gif','https://cdn.discordapp.com/attachments/782562061812891648/803220821937225798/poke_30.gif','https://cdn.discordapp.com/attachments/782562061812891648/804354541583597568/poke_31.gif')
    rnd_poke = random.choice(pokegif)
    pokes.set_image(url=rnd_poke) 
    await context.send(embed=pokes) 
    await context.message.delete()
#pat............................
@client.command(name='pat',aliases=["Pat"])
async def pat(context,member: discord.Member, *,gifmsg=None):
    pats = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow() ,color=0x00ebff)

    pats.set_author(name = f"{context.message.author.display_name} pets {member.display_name} ! There there... ",icon_url=f"{context.message.author.avatar_url}")   
    patgif = ('https://cdn.discordapp.com/attachments/782562061812891648/783001926999867422/pat_12.gif','https://cdn.discordapp.com/attachments/782562061812891648/783002079600836708/pat_30.gif','https://cdn.discordapp.com/attachments/782562061812891648/783002064392290314/pat_29.gif','https://cdn.discordapp.com/attachments/782562061812891648/783002054918012958/pat_28.gif','https://cdn.discordapp.com/attachments/782562061812891648/783002050614788126/pat_27.gif','https://cdn.discordapp.com/attachments/782562061812891648/783002038275014686/pat_26.gif','https://cdn.discordapp.com/attachments/782562061812891648/783002024568029212/pat_24.gif','https://cdn.discordapp.com/attachments/782562061812891648/783002026803331112/pat_23.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001996965838858/pat_22.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001993392160778/pat_21.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001990384451584/pat_20.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001985010892830/pat_19.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001971535249418/pat_18.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001958150701056/pat_17.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001949612146728/pat_15.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001946599456788/pat_16.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001936236511294/pat_14.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001935535407124/pat_13.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001924919492608/pat_10.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001921358135356/pat_11.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001911867473942/pat_8.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001904535044176/pat_9.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001889570684958/pat_7.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001883743617114/pat_6.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001872906190898/pat_5.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001862139805696/pat_3.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001861141299210/pat_4.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001857600782357/pat_2.gif','https://cdn.discordapp.com/attachments/782562061812891648/783001843994984458/pat_1.gif')
    rnd_pat = random.choice(patgif)
    pats.set_image(url=rnd_pat) 
    await context.send(embed=pats) 
    await context.message.delete()
#hi,hello...........................
@client.command(name='Hi',aliases=['Hello','hello','hi','Hey','hey','wave','Wave'])
async def Hi(context,member: typing.Optional[discord.Member] = None , *,gifmsg=None):
    His = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow() ,color=0x00ebff)
    if member == None:
        His.set_author(name = f"{context.message.author.display_name} is waving... ",icon_url=f"{context.message.author.avatar_url}")
    else:
        His.set_author(name = f"{context.message.author.display_name} is waving to {member.display_name}  ",icon_url=f"{context.message.author.avatar_url}")          
    Higif = ('https://cdn.discordapp.com/attachments/782562061812891648/783374436757274675/greeting_30.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374421212790804/greeting_29.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374413092880464/greeting_28.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374405891391548/greeting_27.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374399046156368/greeting_26.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374389013512232/greeting_25.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374383640346634/greeting_24.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374376274755684/greeting_23.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374370885206086/greeting_22.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374365873799208/greeting_21.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374354863751198/greeting_20.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374346483531826/greeting_19.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374336718929980/greeting_18.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374329634095154/greeting_17.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374325016952892/greeting_16.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374319668428840/greeting_15.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374312333508608/greeting_14.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374309933711380/greeting_13.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374305589329950/greeting_11.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374305202667520/greeting_12.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374293153087498/greeting_10.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374292024164362/greeting_7.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374291168919572/greeting_8.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374290531778620/greeting_9.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374277201362944/greeting_6.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374271607078962/greeting_5.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374269224321054/greeting_4.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374267965243432/greeting_2.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374264157732914/greeting_3.gif','https://cdn.discordapp.com/attachments/782562061812891648/783374255861399602/greeting_1.gif')
    rnd_Hi = random.choice(Higif)
    His.set_image(url=rnd_Hi)
    await context.send(embed=His) 
    await context.message.delete() 

#nom-nom............................ 
@client.command(name='Nom',aliases=['nom','eat','bite','Bite','Eat'])
async def Nom(context,member: discord.Member, *,gifmsg=None):
    Noms = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow() ,color=0x00ebff)
    nom1 = (f"{context.message.author.display_name} noms {member.display_name}! ")
    nom2 = (f"{context.message.author.display_name} noms {member.display_name} Yummy! ")
    nom3 = (f"{context.message.author.display_name} is nomming on {member.display_name}! ")
    nomlist= (nom1,nom2,nom3)
    nomline = random.choice(nomlist)
    Noms.set_author(name = nomline,icon_url=f"{context.message.author.avatar_url}" )          
    Nomgif = ('https://cdn.discordapp.com/attachments/782562061812891648/783719325869277224/nom_33.gif','https://cdn.discordapp.com/attachments/782562061812891648/783718654188584971/nom_32.gif','https://cdn.discordapp.com/attachments/782562061812891648/783717579583389696/nom_31.gif','https://cdn.discordapp.com/attachments/782562061812891648/783717569152024616/nom_27.gif','https://cdn.discordapp.com/attachments/782562061812891648/783717558301098004/nom_26.gif','https://cdn.discordapp.com/attachments/782562061812891648/783717551531229184/nom_24.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715936980959283/nom_17.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715925119074304/nom_21.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715925027192852/nom_20.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715923790004285/nom_23.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715917938163712/nom_22.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715886544322580/nom_15.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715886514831370/nom_16.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715885109477376/nom_12.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715881267888138/nom_13.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715880550006804/nom_14.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715875442130944/nom_9.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715871334989843/nom_10.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715873726660638/nom_8.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715872472170576/nom_11.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715864892932106/nom_6.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715860320878642/nom_3.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715859604307988/nom_2.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715861575761920/nom_7.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715861084110898/nom_4.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715859729219654/nom_5.gif','https://cdn.discordapp.com/attachments/782562061812891648/783715837277241354/nom_29.gif')
    rnd_Nom = random.choice(Nomgif)
    Noms.set_image(url=rnd_Nom)
    await context.send(embed=Noms) 
    await context.message.delete()

#hug.................................
@client.command(name='hug',aliases=['Hug'])
async def hug(context,member: discord.Member, *,gifmsg=None):
    hugs = discord.Embed(description=gifmsg,timestamp=datetime.datetime.utcnow() ,color=0x00ebff)
    hug1 = (f"{context.message.author.display_name} hugs {member.display_name}! ＼(^o^)／")
    hug2 = (f"{context.message.author.display_name} hugs {member.display_name}! Don't squeeze too hard!! ")
    hug3 = (f"{context.message.author.display_name} gives {member.display_name} a big hug!! ")
    huglist= (hug1,hug2,hug3)
    hugline = random.choice(huglist)
    hugs.set_author(name = hugline,icon_url=f"{context.message.author.avatar_url}" )          
    huggif = ('https://cdn.discordapp.com/attachments/782562061812891648/785420695969464340/hug_4.gif','https://cdn.discordapp.com/attachments/782562061812891648/785423760034627594/hug_14.gif','https://cdn.discordapp.com/attachments/782562061812891648/785465589740601344/hug_17.gif','https://cdn.discordapp.com/attachments/782562061812891648/785465632409649162/hug_15.gif','https://cdn.discordapp.com/attachments/782562061812891648/785465989491195944/hug_20.gif','https://cdn.discordapp.com/attachments/782562061812891648/785465991043350538/hug_19.gif','https://cdn.discordapp.com/attachments/782562061812891648/785465996924289054/hug_21.gif','https://cdn.discordapp.com/attachments/782562061812891648/785465999776284732/hug_23.gif','https://cdn.discordapp.com/attachments/782562061812891648/785466001948672020/hug_22.gif','https://cdn.discordapp.com/attachments/782562061812891648/785466002610978826/hug_24.gif','https://cdn.discordapp.com/attachments/782562061812891648/785466004187643944/hug_26.gif','https://cdn.discordapp.com/attachments/782562061812891648/785466007417520148/hug_25.gif','https://cdn.discordapp.com/attachments/782562061812891648/785466013160308767/hug_28.gif','https://cdn.discordapp.com/attachments/782562061812891648/785466015780700220/hug_27.gif','https://cdn.discordapp.com/attachments/782562061812891648/785466034563317760/hug_35.gif','https://cdn.discordapp.com/attachments/782562061812891648/785466035129810944/hug_37.gif','https://cdn.discordapp.com/attachments/782562061812891648/785466037893464084/hug_32.gif','https://cdn.discordapp.com/attachments/782562061812891648/785466039706189879/hug_33.gif','https://cdn.discordapp.com/attachments/782562061812891648/785466043741110272/hug_39.gif','https://cdn.discordapp.com/attachments/782562061812891648/785466048416710666/hug_36.gif','https://cdn.discordapp.com/attachments/782562061812891648/785466051542122536/hug_38.gif','https://cdn.discordapp.com/attachments/782562061812891648/785466051075899413/hug_31.gif','https://cdn.discordapp.com/attachments/782562061812891648/785466051772678144/hug_34.gif','https://cdn.discordapp.com/attachments/782562061812891648/785466057800286239/hug_30.gif','https://cdn.discordapp.com/attachments/782562061812891648/785467997800235038/hug_29.gif')
    rnd_hug = random.choice(huggif)
    hugs.set_image(url=rnd_hug)
    await context.send(embed=hugs)          
    await context.message.delete()
#image Manipulation................................................................................................
@client.command(name='wanted', aliases=['Bounty','Wanted','bounty'])
async def wanted(ctx,user:discord.Member=None):
    if user==None:
        user = ctx.author
    resp=requests.get("https://i.imgur.com/jNJBoeJ.png") 
    
    wanted = Image.open(BytesIO(resp.content))
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())   
    pfp = Image.open(data)
    pfp = pfp.resize((385,261))
    wanted.paste(pfp,(57,153))
    font = ImageFont.truetype("luffyfont.ttf", 60)        
    draw=ImageDraw.Draw(wanted)
    text1 = user.display_name
    text = textwrap.wrap(text1, 19)
    W, H = (251,500)
    w, h = draw.textsize(text[0],font=font)
    draw.text((W-w/2, H-h/2),text[0],(93,63,51),font=font,align="center")
    #W, H = (442,530)
    #w, h = draw.textsize(text,font=font)
    #draw.text((W-w/2, H-h/2),text,(93,63,51),font=font,align="center")
    num= random.randint(100000000,10000000000) 
    bount= str(num)
    draw=ImageDraw.Draw(wanted)
    font = ImageFont.truetype("luffyfont.ttf", 70)
    draw.text((102,534),bount,(93,63,51),font=font)
    wanted.save("wanted.png")
    
    if len(text1)>19:
        await ctx.send("Hey! Your name is longer than 19 Characters \n**Tip**: Keep it shorter :) ")
    await ctx.send(file=discord.File("wanted.png"))

@client.command(name='instagram', aliases=['insta','Insta','Instagram'])
async def instagram(ctx,user:typing.Optional[discord.Member]=None, *,caption= None):
    if user==None:
        user = ctx.author
    resp=requests.get("https://i.imgur.com/REDMT7r.png") 
    
    post = Image.open(BytesIO(resp.content))
    asset = user.avatar_url
    data = BytesIO(await asset.read())   
    pfp = Image.open(data)
    pfp = pfp.resize((322,313))
    post.paste(pfp,(19,54))
    font = ImageFont.truetype("ARIAL.TTF", 15)        
    draw=ImageDraw.Draw(post)
    text1 = user.display_name
    text = textwrap.wrap(text1, 19)
    draw.text((56,21),text[0],(0,0,0),font=font)
    #W, H = (442,530)
    #w, h = draw.textsize(text,font=font)
    #draw.text((W-w/2, H-h/2),text,(93,63,51),font=font,align="center")
    
    img=Image.open(data).convert("RGB")
    img = img.resize((36,36))
    npImage=numpy.array(img)
    
    
    
    alpha = Image.new('L', [36,36],0)
    draw1 = ImageDraw.Draw(alpha)
    draw1.pieslice([0,0,36,36],0,360,fill=255)
    npAlpha=numpy.array(alpha)
    npImage=numpy.dstack((npImage,npAlpha))
    pfp1 = Image.fromarray(npImage)
    post.paste(pfp1, (18, 15))
    
    
    #draw=ImageDraw.Draw(wanted)
    caption1 = f"@{user.display_name}  {caption}"
    caption2 = textwrap.wrap(caption1, 39)
    draw.text((21,420),caption2[0],(0,0,0),font=font)
    post.save("instagram.png")
    
    if len(caption)>28:
        await ctx.send("Hey! that too long for a Caption ")
    if len(text1)>18:
        await ctx.send("Hey! Your name is longer than 18 Characters \n**Tip**: Keep it shorter :) ")    
    await ctx.send(file=discord.File("instagram.png"))
#distract  
@client.command(name='distract', aliases=['Distract',"distracted","Distracted"])
async def distract(ctx, *,caption): 
    resp=requests.get("https://i.imgur.com/WE18XMM.jpg") #distract 
    post = Image.open(BytesIO(resp.content)) 
    font = ImageFont.truetype("ARIAL.TTF", 40)
    line1, line2, line3 = caption.split(",")
    draw = ImageDraw.Draw(post)
    lines1 = textwrap.wrap(line1,7)  
    lines2 = textwrap.wrap(line2,7)
    lines3 = textwrap.wrap(line3,7)
    W1 = 376
    H1 = 164
    W2 = 563
    H2 = 138
    W3 = 110
    H3 = 21
    for line1 in lines1:
        w1, h1 = font.getsize(line1)
        draw.text((W1-w1/2,H1),line1,(0,0,0),font=font)
        H1 += h1 
    for line2 in lines2:
        w2, h2 = font.getsize(line2)
        draw.text((W2-w2/2,H2),line2,(0,0,0),font=font)
        H2 += h2  
    for line3 in lines3:
        w3, h3 = font.getsize(line3)
        draw.text((W3-w3/2,H3),line3,(0,0,0),font=font)
        H3 += h3      
    post.save("distracted.jpg")#185
    await ctx.send(file=discord.File("distracted.jpg"))
#thisisshit
@client.command(name='thisisshit', aliases=['Thisisshit'])
async def thisisshit(ctx,user:discord.Member=None): 
    if user == None:
        user = ctx.author
    resp=requests.get("https://i.imgur.com/jtZqJ2u.jpg") #shit 
    post = Image.open(BytesIO(resp.content)) 
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())   
    pfp = Image.open(data)
    pfp = pfp.resize((265,141))
    post.paste(pfp,(9,159))   
    post.save("thisisshit.jpg")    
    await ctx.send(file=discord.File("thisisshit.jpg"))
#water
@client.command(name='water', aliases=['Water'])
async def water(ctx,user:typing.Optional[discord.Member]=None, *,caption): 
    if user==None:
        user = ctx.author
    resp=requests.get("https://i.imgur.com/wpN45qC.jpg") #water
    post = Image.open(BytesIO(resp.content))  
    font = ImageFont.truetype("ARIAL.TTF", 30)
    W = 282
    H1 = 36
    
    draw = ImageDraw.Draw(post)
    lines = textwrap.wrap(caption,12)   
    for line in lines:
        w1, h1 = font.getsize(line)
        draw.text((W-w1/2,H1),line,(0,0,0),font=font)
        H1 += h1 
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())   
    pfp = Image.open(data)
    pfp = pfp.resize((86,94))
    post.paste(pfp,(18,264))    
    post.save("water.png")    
    await ctx.send(file=discord.File("water.png"))
#chika    
@client.command(name='chika', aliases=['Chika'])
async def chika(ctx, *,caption): 
    resp=requests.get("https://i.imgur.com/ZlnspzF.png") #chika 
    post = Image.open(BytesIO(resp.content)) 
    #post = Image.open("chika.png") 
    font = ImageFont.truetype("ARIAL.TTF", 30)
    line1, line2, line3, line4 = caption.split("|") 
    W = 470
    H1 = 15
    H2 = 191
    H3 = 372
    H4 = 555
    
    draw = ImageDraw.Draw(post)
    line11 = textwrap.wrap(line1,17)
    line22 = textwrap.wrap(line2,17)
    line33 = textwrap.wrap(line3,17)
    line44 = textwrap.wrap(line4,17)
    
    
    
    
    for element in line11:
        w1, h1 = font.getsize(element)
        draw.text((W-w1/2,H1),element,(0,0,0),font=font)
        H1 += h1
            
    
    for element2 in line22:
        w2, h2 = font.getsize(element2)
        draw.text((W-w2/2,H2),element2,(0,0,0),font=font)
        H2 += h2

            
    for element3 in line33:
        w3, h3 = font.getsize(element3)
        draw.text((W-w3/2,H3),element3,(0,0,0),font=font)
        H3 += h3

        
    for element4 in line44:
        w4, h4 = font.getsize(element4)
        draw.text((W-w4/2,H4),element4,(0,0,0),font=font)
        H4 += h4

           
    
    
    post.save("chika.png")#185
    await ctx.send(file=discord.File("chika.png"))
#myboi 
@client.command(name='myboi', aliases=['myboy',"Myboi","Myboy"])
async def myboi(ctx,user:discord.Member): 
    
    resp=requests.get("https://i.imgur.com/QTIHrse.jpg") #boy 
    post = Image.open(BytesIO(resp.content)) 
    text1 = ctx.author.display_name
    text = textwrap.wrap(text1, 19)
    W, H = (585,420)
    draw = ImageDraw.Draw(post)
    font = ImageFont.truetype("ARIAL.TTF", 60)
    w, h = draw.textsize(text[0],font=font)
    draw.text((W-w/2, H-h/2),text[0],(93,63,51),font=font,align="center")
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())   
    pfp = Image.open(data)
    pfp = pfp.resize((385,279))
    post.paste(pfp,(1213,3))
    
    post.save("Myboi.png")    
    await ctx.send(file=discord.File("Myboi.png"))

     
@client.command(name='dumb', aliases=['Dumb'])
async def tyg(ctx, *,caption):
    resp=requests.get("https://i.imgur.com/pvkkups.jpg") #water
    post = Image.open(BytesIO(resp.content))  
    font = ImageFont.truetype("ARIAL.TTF", 30)
    W = 347
    H1 = 435
    
    draw = ImageDraw.Draw(post)
    lines = textwrap.wrap(caption,14)   
    for line in lines:
        w1, h1 = font.getsize(line)
        draw.text((W-w1/2,H1),line,(0,0,0),font=font)
        H1 += h1
    post.save("dumb.png")#185
    await ctx.send(file=discord.File("dumb.png"))
@client.command(name='wallpunch', aliases=['Wallpunch',"wallPunch"])
async def dammit(ctx, *,caption):
    resp=requests.get("https://i.imgur.com/qYBV6yl.png ") #water
    post = Image.open(BytesIO(resp.content))  
    font = ImageFont.truetype("ARIAL.TTF", 40)
    W = 6
    H1 = 4
    
    draw = ImageDraw.Draw(post)
    lines = textwrap.wrap(caption,24)   
    for line in lines:
        w1, h1 = font.getsize(line)
        draw.text((W,H1),line,(0,0,0),font=font)
        H1 += h1
    post.save("wallpunch.png")#185
    await ctx.send(file=discord.File("wallpunch.png")) 
@client.command(name='match')
async def match(ctx,member1 : discord.Member, member2 : discord.Member = None ):  
    
    
    if member2 ==None:
        mem2 = member1
        asset2 = mem2.avatar_url
        mem1 = ctx.author
        asset = mem1.avatar_url
    else:
        mem1 = member1
        mem2 = member2
        asset = member1.avatar_url 
        asset2 = mem2.avatar_url   
    data = BytesIO(await asset.read()) 
    data2 = BytesIO(await asset2.read())  
    pfp = Image.open(data)
    pfp = pfp.resize((400,400))
    pfp2 = Image.open(data2)
    pfp2 = pfp2.resize((400,400))
    image = Image.new('RGBA',(800,400))
    image.paste(pfp,(0,0))
    image.paste(pfp2,(400,0))
    image.save("match.png")    
    wed = discord.Embed(description=f"{mem1.name} and {mem2.name} are matching their pfp!",timestamp=datetime.datetime.utcnow() ,color=0x00ebff)
    file = discord.File("match.png")
    wed.set_image(url="attachment://match.png")
    await ctx.send(file = file, embed=wed)        
#worthless
@client.command(name='worthless', aliases=['Worthless'])
async def worthless(ctx, *,caption): 
    resp=requests.get("https://i.imgur.com/7yQETI9.png") #worthless 
    post = Image.open(BytesIO(resp.content)) 
     
    font = ImageFont.truetype("ARIAL.TTF", 25)
    W = 202
    H1 = 75
    
    draw = ImageDraw.Draw(post)
    lines = textwrap.wrap(caption,17)   
    for line in lines:
        w1, h1 = font.getsize(line)
        draw.text((W-w1/2,H1),line,(0,0,0),font=font)
        H1 += h1 
    post.save("worthless.png")    
    await ctx.send(file=discord.File("worthless.png"))
#fbi    
   
@client.command(name='fbi', aliases=['Fbi'])
async def fbi(ctx, *,msg):
    resp=requests.get("https://i.imgur.com/OkhouW4.jpg")  
    post = Image.open(BytesIO(resp.content))
    font = ImageFont.truetype("Product_Sans_Regular.ttf", 35)     
    #msg1 = str(msg)   
    msg2 = textwrap.wrap(msg,33)
    draw=ImageDraw.Draw(post)
    draw.text((35,256),msg2[0],(0,0,0),font=font)
    post.save("fbi.jpg")
    await ctx.send(file=discord.File("fbi.jpg"))

#breaking news
@client.command(name='news', aliases=['News'])
async def news(ctx,user:typing.Optional[discord.Member]=None, *,msg):
    if user==None:
        user = ctx.author
    resp=requests.get("https://i.imgur.com/dvP6ekG.png")  
    #resp2=requests.get("https://i.imgur.com/apeZldc.png") #bg
    #bg = Image.open(BytesIO(resp2.content)).convert('RGB')
    post = Image.open(BytesIO(resp.content))
    font1 = ImageFont.truetype("BebasNeue-Regular.ttf", 35)  
    font2 = ImageFont.truetype("BebasNeue-Regular.ttf", 15)    
    msg1, msg2 = msg.split("|") 
    #msg1 = str(msg)   
    msg1 = textwrap.wrap(msg1,34)
    msg2 = textwrap.wrap(msg2,70)
    draw=ImageDraw.Draw(post)
    draw.text((6,200),msg1[0],(0,0,0),font=font1)
    draw.text((44,248),msg2[0],(0,0,0),font=font2)
    asset = user.avatar_url#_as(size=128)
    data = BytesIO(await asset.read())   
    pfp = Image.open(data)
    pfp = pfp.resize((482,198)) 
    bg = Image.new("RGB",(480,270),(255,255,255))
    bg.paste(pfp,(0,0))
    bg.paste(post,(0,0),mask=post)
    #pfp = pfp.rotate(10)
    #post.paste(pfp,(0,0))
    bg.save("news.png")
    await ctx.send(file=discord.File("news.png"))
#santa
@client.command(name='santa', aliases=['Santa'])
async def santa(ctx, *,caption): 
    resp=requests.get("https://i.imgur.com/jCZwcR3.jpg") #santa 
    post = Image.open(BytesIO(resp.content)) 
     
    font = ImageFont.truetype("ARIAL.TTF", 25)
    W = 123
    H1 = 351
    
    draw = ImageDraw.Draw(post)
    lines = textwrap.wrap(caption,10)   
    for line in lines:
        w1, h1 = font.getsize(line)
        draw.text((W-w1/2,H1),line,(0,0,0),font=font)
        H1 += h1 
    post.save("santa.png")    
    await ctx.send(file=discord.File("santa.png"))    
#jojo
@client.command(name='jojo', aliases=['Jojo'])
async def jojo(ctx,user:discord.Member=None ): 
    if user==None:
        user = ctx.author
    resp=requests.get("https://i.imgur.com/fFzVj4u.png")  
    post = Image.open(BytesIO(resp.content)) 
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())   
    pfp = Image.open(data)
    pfp = pfp.resize((177,240)) 
    #pfp = pfp.rotate(10)
    post.paste(pfp,(94,96))
    post.save("jojo.png")
    await ctx.send(file=discord.File("jojo.png"))

#disability
@client.command(name='disability', aliases=['Disability'])
async def disability(ctx,user:discord.Member=None ): 
    if user==None:
        user = ctx.author
    resp=requests.get("https://i.imgur.com/4RsH5M4.png")  
    post = Image.open(BytesIO(resp.content)) 
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())   
    pfp = Image.open(data)
    pfp = pfp.resize((207,187)) 
    #pfp = pfp.rotate(10)
    post.paste(pfp,(567,408))
    post.save("disability.png")
    await ctx.send(file=discord.File("disability.png"))
#rip
@client.command(name='rip', aliases=['Rip'])
async def rip(ctx,user:discord.Member=None ): 
    if user==None:
        user = ctx.author
    resp=requests.get("https://i.imgur.com/c8mksIz.png")  
    post = Image.open(BytesIO(resp.content)) 
    asset = user.avatar_url
    data = BytesIO(await asset.read())   
    pfp = Image.open(data)
    pfp = pfp.resize((78,78)) 
    #pfp = pfp.rotate(10)
    post.paste(pfp,(59,116))
    post.save("jojo.png")
    message=await ctx.send(file=discord.File("jojo.png")) 
    await message.add_reaction("🇫")

#billy
@client.command(name='billy', aliases=['Billy'])
async def billy(ctx, *,msg):
    resp=requests.get("https://i.imgur.com/qhlo7N1.jpg")  
    post = Image.open(BytesIO(resp.content))
    font = ImageFont.truetype("Product_Sans_Regular.ttf", 15)     
    #msg1 = str(msg)   
    msg2 = textwrap.wrap(msg,39)
    draw=ImageDraw.Draw(post)
    draw.text((264,177),msg2[0],(0,0,0),font=font)
    post.save("billy.jpg")
    await ctx.send(file=discord.File("billy.jpg"))

#facts
@client.command(name='fact', aliases=['Fact'])
async def fact(ctx, *,caption): 
    resp=requests.get("https://i.imgur.com/aKADQfg.jpg") #fact
    post = Image.open(BytesIO(resp.content)) 
     
    font = ImageFont.truetype("ARIAL.TTF", 25)
    W = 107
    H1 = 345
    
    draw = ImageDraw.Draw(post)
    lines = textwrap.wrap(caption,12)   
    for line in lines:
        w1, h1 = font.getsize(line)
        draw.text((W-w1/2,H1),line,(0,0,0),font=font)
        H1 += h1 
        
    post.save("fact.png")    
    await ctx.send(file=discord.File("fact.png"))  

#meme
@client.command(name='bitch', aliases=['Bitch'])
async def bitch(ctx, *,caption): 
    resp=requests.get("https://i.imgur.com/2i9cJvo.png") #meme
    post = Image.open(BytesIO(resp.content)) 
     
    font = ImageFont.truetype("ARIAL.TTF", 32)
    W = 187
    H1 = 317
    
    draw = ImageDraw.Draw(post)
    lines = textwrap.wrap(caption,12)   
    for line in lines:
        w1, h1 = font.getsize(line)
        draw.text((W-w1/2,H1),line,(0,0,0),font=font)
        H1 += h1 
    post.save("bitch.png")    
    await ctx.send(file=discord.File("bitch.png"))   

#yu-gi-oh
@client.command(name='yugioh', aliases=['Yugioh'])
async def yugioh(ctx,*,msg ): 
    resp=requests.get("https://i.imgur.com/bPMhqIY.jpg")  
    post = Image.open(BytesIO(resp.content)) 
    font = ImageFont.truetype("ARIAL.TTF", 25)
    line1, line2 = msg.split("|")
    W = 88
    H1 = 80
    
    draw = ImageDraw.Draw(post)
    lines = textwrap.wrap(line1,10)   
    for line in lines:
        w1, h1 = font.getsize(line)
        draw.text((W-w1/2,H1),line,(0,0,0),font=font)
        H1 += h1     
          
    
    W2 = 88
    H2 = 299
    
    draw = ImageDraw.Draw(post)
    lines = textwrap.wrap(line2,10)   
    for line in lines:
        w2, h2 = font.getsize(line)
        draw.text((W2-w2/2,H2),line,(0,0,0),font=font)
        H2 += h2 

    post.save("yugioh.png")
    await ctx.send(file=discord.File("yugioh.png")) 

@client.command(name='meme', aliases=['Meme','Memes','memes'])
@commands.cooldown(5, 60, BucketType.user)  
async def meme(ctx):

    subred = redit.subreddit("Animemes")
    subs = subred.top("day",limit = 50)
    top = []
    for tops in subs:
        if "https://v.redd" not in tops.url and tops.over_18 == False:
            top.append(tops)
            
            
      
    topp = random.choice(top)   
    try:

        em = discord.Embed(description = topp.title,color = ctx.author.color)
        em.set_image(url = topp.url)
        await ctx.send(embed = em)
    except:
        await ctx.reply("`something went wrong ;-;`")    



@client.command(name='reddit', aliases=['Reddit','red','Red'])
@commands.cooldown(5, 60, BucketType.user)
async def redd(ctx,name):
    subred = redit.subreddit(name)
    subs = subred.top("day",limit = 60)
    top = []
    for tops in subs:
        if "https://v.redd" not in tops.url and tops.over_18 == False:
            top.append(tops)
            
            
      
    topp = random.choice(top)   
    
    try:

        em = discord.Embed(description = topp.title ,color = ctx.author.color)
        em.set_image(url = topp.url)
        await ctx.send(embed = em)
    except:
        await ctx.reply("`something went wrong ;-;`")    

#yu-gi-oh pfp
@client.command(name='yugiohpfp', aliases=['Yugiohpfp'])
async def yugiohpfp(ctx,member: Greedy[discord.Member] ): 
    resp=requests.get("https://i.imgur.com/bPMhqIY.jpg")  
    post = Image.open(BytesIO(resp.content)) 
    asset1 = member[0].avatar_url
    data1 = BytesIO(await asset1.read())   
    pfp1 = Image.open(data1)
    pfp1 = pfp1.resize((171,180)) 
    
    post.paste(pfp1,(3,71))     

    asset = member[1].avatar_url
    data = BytesIO(await asset.read())   
    pfp = Image.open(data)
    pfp = pfp.resize((168,167)) 
    post.paste(pfp,(6,286))
    post.save("yugiohpfp.jpg")
    await ctx.send(file=discord.File("yugiohpfp.jpg"))  

@client.command(name='Imagify',aliases=["img","Img","imagify"])
async def imagify(ctx, *,text):
    
    resp=requests.get("https://i.imgur.com/CFvwPZQ.jpg") 
    post = Image.open(BytesIO(resp.content))
    font = ImageFont.truetype("Product_Sans_Regular.ttf", 30) 
    W2 = 210
    H2 = 20
    
    draw = ImageDraw.Draw(post)
    lines = textwrap.wrap(text,25)   
    for line in lines:
        w2, h2 = font.getsize(line)
        draw.text((W2-w2/2,H2),line,(255,255,255),font=font)
        H2 += h2
    post.save("img.jpg")
    await ctx.send(file=discord.File("img.jpg"))     

#message................
@client.command(name='pro',aliases=["Pro"])
async def pro(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
       
    resp=requests.get("https://i.imgur.com/fAkM4cd.png")  
    post = Image.open(BytesIO(resp.content)).convert('RGBA')     
    asset1 = member.avatar_url
    data1 = BytesIO(await asset1.read())   
    pfp1 = Image.open(data1)
    pfp1 = pfp1.resize((110,110)) 
    
    drw = ImageDraw.Draw(post)
    drw.ellipse((100,300,100,300),fill=(0,0,0,0))
    ImageDraw.floodfill(post, xy=(14,24),value=(0,0,0,0),thresh = 40)
    post.paste(pfp1,(30,87))
    post.save('profile.png')
 
     
    
    await ctx.send(file=discord.File("profile.png")) 

#announcement
@client.command(name="announcement",aliases=["announce","Announce","Announcement"])
@commands.has_permissions(manage_guild=True)
async def announce_everyone(ctx,mention,channel : discord.TextChannel, *,msg):
    if mention == "everyone":
        em = discord.Embed(description=msg,timestamp=datetime.datetime.utcnow(),color=0x00ebff)
        em.set_footer(text=f"announced by {ctx.author}")
        await channel.send("@everyone", embed=em)

    if mention == "here":
        em = discord.Embed(description=msg,timestamp=datetime.datetime.utcnow(),color=0x00ebff)
        em.set_footer(text=f"announced by {ctx.author}")
        await channel.send("@here", embed=em)
    

#dm
@client.command(name='dm',pass_context = True)    
#@commands.has_permissions(manage_guild=True)
async def dm(context, member : discord.Member, *,msg):
    if context.author == owner:
        await member.send(msg +f"\n\nsent by **{context.author}** from **{context.guild}** ")

#say
@client.command(name='say',aliases = ["Say","Type","type"])
@commands.cooldown(2, 120, BucketType.user)
async def say(context, *,msg: commands.clean_content):
    await context.send(msg+f"\n\n           -{context.author}")
    await context.message.delete()
#spoiler
@client.command(name='Spoiler',aliases = ["spoiler","Spoil","spoil"])
@commands.cooldown(2, 120, BucketType.user)
async def Spoiler(context, *,msg: commands.clean_content):
    await context.send("||"+msg+ f"||\n\n           -{context.author}")
    await context.message.delete() 

#emoji 
#@client.command(name='Emote',aliases = ["emote","emoji","Emoji"])
#async def Emote(context, *,msg : discord.Emoji = None):
    #if msg == None:
        #return
    #else:
        #await context.send(msg)
        #await context.message.delete()        

#avatar
@client.command(name='avatar',aliases=["pfp","Pfp","Avatar"])
async def avatar(context, *,member : discord.Member = None):
    if member == None:
        user = context.author
    else:
        user = member    
        
    avatars = discord.Embed(timestamp=datetime.datetime.utcnow() ,color=0x00ebff)  
    avatars.set_author(name = f"{user.name}'s avatar",icon_url=f"{user.avatar_url}")  
    #triggereds.add_field(name="Triggered",value=(f"{context.author.mention} is Triggered ༎ຶ‿༎ຶ"))
    avatars.set_image(url=user.avatar_url)

    await context.send(embed=avatars)         

#marraige
@client.command(name="propose",aliases= ["Propose"])
async def propose(context, member: discord.Member , *,msg= None):
    if context.author != member:
        await context.send(f"{member.mention}\n{context.author.mention} proposed you for the marraige!! Do you accept?? \nType accept or reject")
        def check(response):
            return response.content.lower() in ["accept","reject"] and response.author == member and response.channel == context.channel
    
        try:
        
            response= await client.wait_for('message', check= check, timeout= 40)
        
            if "accept" in response.content.lower():
                resp=requests.get("https://i.imgur.com/gxsD8hr.png") #marraige
            #resp2=requests.get("https://i.imgur.com/apeZldc.png") #bg
                resp2=requests.get("https://i.imgur.com/Rs9YYjN.png")
                bg = Image.new("RGBA",(1479,600), (0,0,0,0))
             
                marraige = Image.open(BytesIO(resp.content)).convert('RGBA')
                mrg =  marraige.resize((250,250))
                frm = Image.open(BytesIO(resp2.content)).convert('RGBA')
                frm = frm.resize((580,580))
                asset = context.author.avatar_url_as(size=128)
                asset2 = member.avatar_url
                data = BytesIO(await asset.read())  
                data2 = BytesIO(await asset2.read())  
                pfp = Image.open(data).convert('RGB')
                waifu0 = Image.open(data2).convert('RGB')
   
                pfp = pfp.resize((435,435))
                waifu1 =  waifu0.resize((435,435))
                height,width = pfp.size
                lum_img = Image.new('L', [height,width] , 0)
  
                draw = ImageDraw.Draw(lum_img)
                draw.pieslice([(0,0), (height,width)], 0, 360, fill = 255, outline = "white")
                img_arr =np.array(pfp)
                lum_img_arr =np.array(lum_img)
    #display(Image.fromarray(lum_img_arr))
                final_img_arr = np.dstack((img_arr,lum_img_arr))
                fll1 = Image.fromarray(final_img_arr)
                height,width = pfp.size
                lu_img = Image.new('L', [height,width] , 0)
  
                draw = ImageDraw.Draw(lu_img)
                draw.pieslice([(0,0), (height,width)], 0, 360, fill = 255, outline = "white")
                img_arrwa =np.array(waifu1)
                lu_img_arr =np.array(lu_img)
    #display(Image.fromarray(lum_img_arr))
                final_img_arrwa = np.dstack((img_arrwa,lu_img_arr))
                fll = Image.fromarray(final_img_arrwa)
            
                bg.paste(fll1,(77,80))
            
                bg.paste(fll,(886,80))
                bg.paste(mrg,(570,150))
                bg.paste(frm,(0,0),mask=frm)
                bg.paste(frm,(809,0),mask=frm)
             
                bg.save("marraige.png",format="png")
                wed = discord.Embed(description=f"{context.author.name} and {member.name} are **married** now!!💝",timestamp=datetime.datetime.utcnow() ,color=0x00ebff)
                file = discord.File("marraige.png")
                wed.set_image(url="attachment://marraige.png")
                await context.send(file = file, embed=wed)

            if "reject" in response.content.lower():
                await context.send(f"{context.message.author.mention} You got rejected... ;-;")   

        except asyncio.TimeoutError:
            await context.send(f"{context.author.mention} {member.name} didn't reply. ;-;")     
    else:
        await context.send(f"{context.author.mention} You really want to marry yourself ??!!\n||are you lonely? ;-;||")          



@client.command(name='imposter',aliases= ['whoisimposter','Imposter'])
async def imposter(context, member: Greedy[discord.Member]):#member1 : discord.Member, member2 : discord.Member, member3 : discord.Member):

    #player=(member1.display_name,member2.display_name,member3.display_name)
    imp=random.choice(member)
    imps=discord.Embed(timestamp=datetime.datetime.utcnow() ,color=0x00ebff)
    imps.set_author(name=f'{client.user.display_name}' ,icon_url=f'{client.user.avatar_url}')
    line1=f'{imp}  is the **Imposter**!! I saw {imp} killing blue..'
    line2=f'{imp}  is the **Imposter**!! {imp} vented infront of me...'
    line3=f'{imp}  is the **Imposter**!! {imp} was doing fake task! Lol noob...'
    linelist =(line1,line2,line3)
    line=random.choice(linelist)

    imps.add_field(name='Who is the Imposter!!',value=f'{line}')
    imps.set_image(url='https://i.imgur.com/m2EfMwb.jpg')
    await context.send(embed=imps)



 
#MyAnimeList
#animesearch
@client.command(name= "anime",aliases = ["Anime"])
async def anime(ctx, *, anime):
    try:
        id = findid(anime)   
        if id != None:
            link = f'https://myanimelist.net/anime/{id}' 
            r = requests.get(link)
            soup = BeautifulSoup(r.content,features="lxml")
            japanese = soup.find("h1", {"class" : "title-name h1_bold_none"})
            
            english = soup.find("p", {"class" : "title-english title-inherit"})
            jap = (japanese.text)
            
            synop = soup.find("p", {"itemprop" : "description"})
            if synop != None:
                synopsis = (synop.text)
            else:
                synopsis = "Synopsis Not Available"    
            if english != None:
                
                mal = discord.Embed(description=f'**[{jap}]({link})** \nalso known as {english.text}\n{synopsis}',timestamp=datetime.datetime.utcnow(),color=0xff0092)
            else:
                mal = discord.Embed(description=f'**[{jap}]({link})** \n{synopsis}',timestamp=datetime.datetime.utcnow(),color=0xff0092)   
            
            
            rate = soup.find("div", {"class" : "fl-l score"})
            print(rate)
            if rate != None:
                rating = (rate.div.text)
            else:
                rating = "Not Available"
            rank = soup.find("span", {"class" : "numbers ranked"})
            if rank != None:
                ranks = (rank.text)
            else:
                ranks = "Not Available"    
            
            imgstat = soup.find("td", {"class" : "borderClass"})
            try:
                image = (imgstat.div.div.a.img['data-src'])
            except:
                image = "https://www.indiaspora.org/wp-content/uploads/2018/10/image-not-available.jpg"    
            stats = soup.find_all("span", {"class" : "dark_text"})
            episode = ""
            status = ""
            air = ""

            tyype = ""
            for stat in stats:
                if 'Episodes:' in stat.text:
                    try:
                        episode += (stat.nextSibling )
                    except:
                        episode += "Not Available"    
                elif 'Type:' in stat.text:
                    if stat.parent.a != None:
                        tyype += stat.parent.a.text
                    elif stat.parent.a == None:
                        tyype +=  stat.nextSibling   
                    else:
                        tyype += "Not Available"    
                elif 'Status:' in stat.text:
                    status += (stat.nextSibling )
                elif 'Aired:' in stat.text: 
                    try: 
                        air += (stat.nextSibling ) 
                    except:
                        air += "Not Available"         
                if episode != "" and status != "" and air != "" and tyype != "":
                    break    
            genres = soup.find_all("span", {"itemprop" : "genre"}) 
            genre = ''
            length = len(genres)
            num = 0
            for gen in genres:
                num += 1
                if num == length:
                    genre += f"{gen.text}."
                else:
                    genre += f"{gen.text}, "     
            
            mal.add_field(name="**⌛ Status**",value= status,inline=False)
            mal.add_field(name="**📺 Total Episodes**",value= episode,inline=True)
            mal.add_field(name="**📡 Aired**",value= air,inline=True)
            mal.add_field(name="**💻 Type**",value= tyype,inline=True)
            mal.add_field(name="**🎬 Genre**",value= genre,inline=False)
            mal.add_field(name="**⭐ Rating**",value= f'{rating}/10',inline=True )
            mal.add_field(name="**🎖️ Rank**",value= f'**{ranks}**',inline=False)
            mal.set_footer(text= f'Requested by {ctx.author}' )
            mal.set_thumbnail(url=image)

            await ctx.send(embed = mal)
        else:
            await ctx.reply('that anime could not be found. It may not exist, or you may have misspelled its name.')
    except:
        await ctx.reply('Something went wrong! pls report this to support server!')                    
#manga search
@client.command(name= "manga",aliases = ["Manga"])
async def manga(ctx, *, manga):
    from mal import MangaSearch
    search = MangaSearch(manga) 
    AManga= Manga(search.results[0].mal_id)
    x = ","
    gen = ""
    for genre in AManga.genres:
        if genre == AManga.genres[-1]:
            x = "."
        gen += (f"{genre}{x} ")
    mal = discord.Embed(description=f'**[{search.results[0].title}]({search.results[0].url})** \n{AManga.synopsis}',timestamp=datetime.datetime.utcnow(),color=0xff0092)
    mal.add_field(name="**⌛ Status**",value= AManga.status)          
    mal.add_field(name="**📕 Total Chapters**",value= AManga.chapters)
    mal.add_field(name="**📚 Total Volumes**",value= AManga.volumes)
    mal.add_field(name="**🗓️ Published**",value= AManga.published,inline=True)
    mal.add_field(name="**🎨 Type**",value= AManga.type,inline=True)
    mal.add_field(name="**🎬 Genre**",value= gen,inline=False)
    mal.add_field(name="**⭐ Rating**",value= f'{AManga.score}/10',inline=True )
    mal.add_field(name="**🎖️ Rank**",value= f'**Top {AManga.rank}**',inline=False)
    mal.set_footer(text= f'Requested by {ctx.author}' )
    mal.set_thumbnail(url=AManga.image_url)

    await ctx.send(embed = mal)    
#search.results[0].synopsis
#AnimeSearchResult.mal_id
#AnimeSearchResult.url
#AnimeSearchResult.image_url
#AnimeSearchResult.title
#AnimeSearchResult.synopsis
#AnimeSearchResult.type
#AnimeSearchResult.score    
#@client.command(name= "char",aliases = ["Character","Char","character"])
#async def character(ctx, *, name):    
 #   link = ("https://myanimelist.net/character.php?q={}").format(name)
  #  print(link)
  #  r = requests.get(link)
  #  soup = BeautifulSoup(r.content,features="lxml")
  #  span = soup.find('td',attrs={"class":"borderClass bgColor1"},{"width":"175"})
  #  print(span)
  #  print({span[0].a.string})
  #  print({span[0].a['href']})
  #  img = soup.find('img',attrs={"class":"lazyload"})['data-src']
  #  anime = span.get_text(strip=True)
   # 
    #em = discord.Embed(description = "Character search result", color = ctx.author.color)
    #em.add_field(name="Characters:",value= [{span[0].a.string}]({span[0].a['href']}) )  
 #   em.add_field(name="Show",value=anime)  
  #  em.thumbnail(url = img )
   # msg = await ctx.reply(embed=em)
    #await msg.add_reaction("🔎")
    #def check(reaction, user):
            
    #        return str(reaction.emoji) in ["🔎","📋"] and user != client.user and reaction.message.id == msg.id and user == ctx.author
    #while True:
     #   reaction = await client.wait_for("reaction_add", check=check,timeout=30) 
      #  if str(reaction.emoji) == "🔎":
       #     emb =discord.embed(color=ctx.author.color) 
        #    emb.set_image(url=img) 
         #   await msg.edit(embed=emb)
          #  await msg.remove_reaction("🔎",client.user)
           # await msg.add_reaction("📋") 
                    
      #  if str(reaction.emoji) == "📋": 
       #     await msg.remove_reaction(reaction, user) 
        #    await msg.remove_reaction("📋",client.user)  
         #   await msg.edit(embed=em)
          #  await msg.add_reaction("🔎")
        
        
@client.command(name='waifu',aliases=["Waifu"]) 
@commands.cooldown(3, 120, BucketType.user)  
async def waifu_(ctx):
    count = girl.find().count()
    ct = count -1
    im = random.randint(0,ct)
    doc = girl.find_one({'_id' : im})     
    name = doc['name']
    anime = doc['anime']
    image = doc['image']
    byt  = BytesIO(image)
    file = discord.File(fp = byt, filename = 'waifu.png')
    emb = discord.Embed(title = name,description = f"{anime}",color=0xdc143c)
    emb.set_image(url = 'attachment://waifu.png')
    message= await ctx.send(file = file, embed=emb)
    await message.add_reaction("💗")
    
    def check(reaction, user):
        return str(reaction.emoji) == "💗" and user != client.user and reaction.message.id == message.id

    try:
        reaction, user = await client.wait_for('reaction_add',check=check,timeout=60)

        await ctx.send(f"{user.name} wanna make {name}, waifu! 💝") 
        
        answer = random.randint(0,9)    
        if answer <= 4:
            await asyncio.sleep(5)
            await ctx.send(f"{user.name}\nAwww... {name} said **Yes** for the marraige!! Congrats💝\nLet me make a wedding card for you >///<")
            resp=requests.get("https://i.imgur.com/gxsD8hr.png") #marraige
            #resp2=requests.get("https://i.imgur.com/apeZldc.png") #bg
            resp2=requests.get("https://i.imgur.com/Rs9YYjN.png")
            bg = Image.new("RGBA",(1479,600), (0,0,0,0))
             
            marraige = Image.open(BytesIO(resp.content)).convert('RGBA')
            mrg =  marraige.resize((250,250))
            frm = Image.open(BytesIO(resp2.content)).convert('RGBA')
            frm = frm.resize((580,580))
            asset = user.avatar_url_as(size=128)
            
            data = BytesIO(await asset.read())  
             
            pfp = Image.open(data).convert('RGB')
            waifu0 = Image.open(byt).convert('RGB')
   
            pfp = pfp.resize((435,435))
            waifu1 =  waifu0.resize((435,435))
            height,width = pfp.size
            lum_img = Image.new('L', [height,width] , 0)
  
            draw = ImageDraw.Draw(lum_img)
            draw.pieslice([(0,0), (height,width)], 0, 360, fill = 255, outline = "white")
            img_arr =np.array(pfp)
            lum_img_arr =np.array(lum_img)
    #diplay(Image.fromarray(lum_img_arr))
            final_img_arr = np.dstack((img_arr,lum_img_arr))
            fll1 = Image.fromarray(final_img_arr)
            height,width = pfp.size
            lu_img = Image.new('L', [height,width] , 0)
  
            draw = ImageDraw.Draw(lu_img)
            draw.pieslice([(0,0), (height,width)], 0, 360, fill = 255, outline = "white")
            img_arrwa =np.array(waifu1)
            lu_img_arr =np.array(lu_img)
    #display(Image.fromarray(lum_img_arr))
            final_img_arrwa = np.dstack((img_arrwa,lu_img_arr))
            fll = Image.fromarray(final_img_arrwa)
        
            bg.paste(fll1,(77,80))
            
            bg.paste(fll,(886,80))
            bg.paste(mrg,(570,150))
            bg.paste(frm,(0,0),mask=frm)
            bg.paste(frm,(809,0),mask=frm)
             
            bg.save("marraige.png",format="png")    
            
            wed = discord.Embed(description=f"{user.name} and {name} are **married** now!!💝",timestamp=datetime.datetime.utcnow() ,color=0x00ebff)
            file = discord.File("marraige.png")
            wed.set_image(url="attachment://marraige.png")
            await ctx.send(file = file, embed=wed)
        if answer > 4:
            await asyncio.sleep(5)
            await ctx.send(f"{user.name}\n{name} said **No** to you.... ;-;")
            
    except asyncio.TimeoutError:
        return    
@client.command(name='lookup',aliases = ['lu','Lookup'])
async def lookup(ctx, name):
    cursor = girl.find({"$text": {"$search": name}},{'score': {'$meta': 'textScore'}})
    cursor.sort([('score', {'$meta':'textScore'})])
    name = []
    title = []
    for nam in cursor:
        name.append(nam['name'])
        title.append(nam['anime'])
    total = (len(name))  
    pages = math.ceil(total/10)
    if total == 0:
        await ctx.reply('that character could not be found. It may not exist, or you may have misspelled their name.')
    if pages > 1:      
        x = -10
        y = 0
        cur_page = 1
        x = 0
        y = 10
        show = ''
        count = 0

        for char,anime in zip(name[x:y],title[x:y]):
            count += 1
            show += f'{count}. {anime} . **{char}**\n'   
             
        embb = discord.Embed(title = "Waifu Results:",description = f"please type the number beside the character you are looking for.\n\n{show}",color=0xdc143c)
        embb.set_footer(text = f"{cur_page}/{pages}")
        message = await ctx.send(embed = embb) 
        
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
        def check1(msg):
            return msg.author == ctx.author and ctx.channel == msg.channel and msg.content.isdigit()   
        work  = 'True'     
        while work == 'True':
            
            #try:
                finished, unfinished = await asyncio.wait([client.wait_for('message', timeout=30,check=check1),client.wait_for('reaction_add', timeout=30,check=check)], return_when=asyncio.FIRST_COMPLETED)
                for task in finished:
                    result = task.result() 
                try:  
                    if str(result[0].emoji) == "▶️" and cur_page != pages:
                        show = ""
                        cur_page += 1
                        x += 10
                        y += 10
                        num  = x
                        for char,anime in zip(name[x:y],title[x:y]):
                            num += 1
                            show += f'{num}. {anime} . **{char}**\n'     
                        
                        if show != "":    
                            em = discord.Embed(title = "Waifu Results:",description = f"please type the number beside the character you are looking for.\n\n{show}",color=0xdc143c)
                            em.set_footer(text = f"{cur_page}/{pages}")
                            await message.edit(embed = em)
                    elif str(result[0].emoji) == "◀️" and cur_page > 1:
                            show = ""
                            cur_page -= 1    
                            x -= 10
                            y -= 10
                            num = x
                            for char,anime in zip(name[x:y],title[x:y]):
                                num += 1
                                show += f'{num}. {anime} . **{char}**\n' 
                            emb = discord.Embed(title = "Waifu Results:",description = f"please type the number beside the character you are looking for.\n\n{show}",color=0xdc143c)
                            emb.set_footer(text = f"{cur_page}/{pages}")
                            await message.edit(embed = emb)
                except:            
                    if int(result.content) <= y and int(result.content) > x:
                        try:
                            msg3 = int(result.content)
                            index = msg3 - 1
                            name = name[index]
                            anime = title[index]
                            doc = girl.find_one({'name' : name,'anime' : anime})
                            emmb = discord.Embed(title = 'Waifu Lookup',description = f"Name : **{doc['name']}**\n\nFrom : {doc['anime']}",color=0xdc143c)
                            image = doc['image']
                            byt  = BytesIO(image)
                            file = discord.File(fp = byt, filename = 'waifu.png')
                            emmb.set_image(url = 'attachment://waifu.png')
                            await ctx.reply(file = file, embed=emmb)
                            work = 'False'
                            await message.delete()
                        except:
                            await ctx.reply('Something went wrong, Please report this bug in support server!')
                       
    elif pages  == 1:
        count = 0
        show = ""
        for char,anime in zip(name,title):
            count += 1
            show += f'{count}. {anime} . **{char}**\n'   
             
        embb = discord.Embed(title = "Waifu Results:",description = f"please type the number beside the character you are looking for.\n\n{show}",color=0xdc143c)
        msssg = await ctx.send(embed = embb)
        def check(msg):
            return msg.author == ctx.author and ctx.channel == msg.channel and msg.content.isdigit()
        rest = 'true'    
        while rest == 'true':    
            try:
                msg2 = await client.wait_for('message', check=check,timeout=30)
                try:
                    msg3 = int(msg2.content)
                    if msg3 <= count and msg3 > 0:
                        index = msg3 - 1
                        name = name[index]
                        anime = title[index]
                        doc = girl.find_one({'name' : name,'anime' : anime})
                        emmb = discord.Embed(title = 'Waifu Lookup',description = f"Name : **{doc['name']}**\n\nFrom : {doc['anime']}",color=0xdc143c)
                        image = doc['image']
                        byt  = BytesIO(image)
                        file = discord.File(fp = byt, filename = 'waifu.png')
                        emmb.set_image(url = 'attachment://waifu.png')
                        await ctx.reply(file = file, embed=emmb)
                        rest = 'false'
                        await msssg.delete()
                except:
                    await ctx.reply('Something went wrong, Please report this bug in support server!')     
            except asyncio.TimeoutError:
                return  
        
        
#gogoanime


@client.command(name='movie',aliases=["Movie","Series","series"])
async def movie(ctx, *,name):
    #try:

        name = name.replace(" ","+")  
        link = f"https://www.imdb.com/find?s=tt&q={name}&ref_=nv_sr_sm"
        
        r = requests.get(link)
        soup = BeautifulSoup(r.content,features="lxml")
        spans = soup.find_all("td", {"class" : "result_text"})
        
        result = ""
        count = 1
        linkk = []
        names = []
        for span in spans:
            result += f"{count}. [{span.text}](https://www.imdb.com{span.a['href']})\n"
            linkk.append(f"https://www.imdb.com{span.a['href']}")
            names.append(span.text)
            count += 1
            if count > 7:
                break
        em = discord.Embed(title = "Result:",description= result,color = ctx.author.color)
        message = await ctx.reply(embed = em)
        emoji_numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
        for i in range(count-1):
            await message.add_reaction(emoji_numbers[i])
        def check(reaction, user):
                return str(reaction.emoji) in emoji_numbers and user != client.user and reaction.message.id == message.id and user == ctx.author
            # This makes sure nobody except the command sender can interact with the "menu"
        while True:
            #try:
                reaction, user = await client.wait_for('reaction_add', check=check, timeout=30)
                index = emoji_numbers.index(reaction.emoji)
                rn = requests.get(f"{linkk[index]}plotsummary?ref_=tt_stry_pl#synopsis")
               # ry = requests.get(f"{linkk[index]}")
               # print(json.load(ry))
                soupp = BeautifulSoup(rn.content,features="lxml")
                #sou = BeautifulSoup(ry.content,features='html.parser')
                print(f"{linkk[index]}?ref_=tt_stry_pl")
                
                      
                synop = soupp.find("li",{"class" : "ipl-zebra-list__item"})
                poster = soupp.find("img",{"class" : "poster"})
                emb = discord.Embed(title = names[index],description= f"{synop.text}",color = ctx.author.color)
                try:
                    
                    img = f"{poster['src'][0:-24]}.jpg"
                    emb.set_image(url = img)
                except:
                    
                    emb.set_footer(text="No Image Found")
                       
                
                await message.edit(embed =emb)
                
                await message.remove_reaction(reaction, user)
                for i in range(count-1):
                    await message.remove_reaction(emoji_numbers[i],client.user) 
            #except asyncio.TimeoutError:
                    #return
                  
    #except:
        #em = discord.Embed(title="Not found")
        #await ctx.send(embed=em)            
                
#['airing', 'akas', 'alternate versions', 'awards', 'connections', 'crazy credits', 'critic reviews', 'episodes', 'external reviews', 'external sites', 'faqs', 'full credits', 'goofs', 'keywords', 'list', 'locations', 'main', 'misc sites', 'news', 'official sites', 'parents guide', 'photo sites', 'plot', 'quotes', 'recommendations', 'release dates', 'release info', 'reviews', 'sound clips', 'soundtrack', 'synopsis', 'taglines', 'technical', 'trivia', 'tv schedule', 'video clips', 'vote details']
insult_api_url = 'http://autoinsult.datahamster.com/index.php?style=3'
@client.command(name='insult',aliases=["Insult"])
async def insult(ctx, member : discord.Member = None):
    if member == None:
        member = ctx.author
    data = requests.get(insult_api_url).text
    
    site = BeautifulSoup(data, "lxml")
    await ctx.send(f"{member.mention} " + "{}!".format(site.select("div.insult")[0].text))
roast_api_url = 'https://evilinsult.com/generate_insult.php?lang=en&amp;type=json'    
@client.command(name='roast',aliases=["Roast"])
async def roast(ctx, member : discord.Member = None):    
    if member == None:
        member = ctx.author
    data = requests.get("https://evilinsult.com/generate_insult.php").text
    await ctx.send(f"{member.mention} {data}") 
@client.command(name='df',aliases=["define","Define","Df"])
async def define(ctx, *,word): 
    try: 
        r = requests.get("http://www.urbandictionary.com/define.php?term={}".format(word))

        soup = BeautifulSoup(r.content,features="lxml")
    
        mean = (soup.find("div",attrs={"class":"meaning"}).text)
        exp = (soup.find("div",attrs={"class":"example"}).text)
        up = (soup.find("a",attrs={"class":"up"}).text)
        down = (soup.find("a",attrs={"class":"down"}).text)
        em = discord.Embed(title=f"Word: {word}",colour=ctx.author.color, timestamp=ctx.message.created_at)
        em.add_field(name="Meaning:",value=mean)
        em.add_field(name="Example:",value=f"{exp}\n\n{up} 👍\n{down} 👎")
        await ctx.send(embed=em)
    except:
        em = discord.Embed(title="Not found")
        await ctx.send(embed=em)
@client.command(name='char',aliases=["Char","character","Character"])
async def char(ctx, *,word): 
    
        #link = f"https://anilist.co/search/characters?search={word}"

    link = f"https://myanimelist.net/character.php?cat=character&q={word}"
    r = requests.get(link)
    soup = BeautifulSoup(r.content,features="lxml")
    spans = soup.find("td", {"class" : "borderClass bgColor1"}, width="175")
    img = soup.find('img', {'class': 'lazyload'})
    
  #  <div class="picSurround"><a href="https://myanimelist.net/character/85/Kakashi_Hatake"><img class=" lazyloaded" data-src="https://cdn.myanimelist.net/r/42x62/images/characters/7/284129.webp?s=51cf4d5b54e20bbcb6be84750078aeeb" src="https://cdn.myanimelist.net/r/42x62/images/characters/7/284129.webp?s=51cf4d5b54e20bbcb6be84750078aeeb" width="42" height="62" border="0"></a></div>
    em = discord.Embed(title="Character Result",description = f"[{spans.a.string}]({spans.a['href']})")
    imgg = img['data-src']
    imgg = imgg.replace("r/42x62/","")
    
    em.set_image(url=imgg)
    await ctx.send(embed = em) 
    
           # <a href="https://myanimelist.net/character/17/Naruto_Uzumaki">Uzumaki, Naruto</a><br><small>(Nine-Tails Jinchuuriki)</small>
           # </td>

 
    
@client.command(name='eplist',aliases=["Eplist"])
async def eplist(ctx, *,word):  
    try:   
        filler_string = word.replace(" ","-")
        link = ("https://www.animefillerlist.com/shows/" + filler_string)
        r = requests.get(link)
        
        soup = BeautifulSoup(r.content,features="lxml")
        spans = soup.find_all('td',attrs={"class":"Type"})
        spanss = soup.find_all('td',attrs={"class":"Title"})
        numbers = ""
        count = 1
        ep = len(spans)
        
        for (span,spa) in zip(spans,spanss):
            
            numbers += (f"**EP {count}**. {span.get_text(strip=True)}:\n||[{spa.get_text(strip=True)}]||\n")
    
            count += 1
            if count > 10:
                break    
                     
        em = discord.Embed(description = f"**[{word} Episode List]({link})**",color=ctx.author.color)    
        em.add_field(name= f"Total Episodes : {ep}",value=numbers )
        em.set_footer(text=f"Reply with the episode number\nRequested by {ctx.author}")
        msg1 = await ctx.send(embed = em) 
        def check(msg):
            return msg.author == ctx.author and ctx.channel == msg.channel and msg.content.isdigit()
        try:
            msg2 = await client.wait_for('message', check=check,timeout=30)
            msg3 = int(msg2.content)
            no = msg3-1
            num = msg3
            lis = ""
            nom = 0
            for (span,spa) in zip(spans[no:],spanss[no:]):
                lis += (f"**EP {num}**. {span.get_text(strip=True)}:\n||[{spa.get_text(strip=True)}]||\n")
                num += 1
                nom += 1
                if nom > 10:
                    break 
            emb = discord.Embed(description = f"**[{word} Episode List]({link})**",color=ctx.author.color)    
            emb.add_field(name= f"Total Episodes : {ep}",value=lis)
            emb.set_footer(text= f'Requested by {ctx.author}' )
            id = msg1.id
            dellmsg = await ctx.channel.fetch_message(id)
            await dellmsg.delete()
            await ctx.send(embed = emb) 
        except asyncio.TimeoutError:
            em1 = discord.Embed(description="**Timeout**")   
            await ctx.send(embed=em1)  
    except:
        em = discord.Embed(title="Not found")
        msg = await ctx.send(embed=em,delete_after=30)
@client.command(name='filler',aliases=["Filler","Fill","fill"])
async def filler(ctx, *,word):  
    try:  
        filler_string = word.replace(" ","-")
        link = ("https://www.animefillerlist.com/shows/" + filler_string)
        r = requests.get(link)    
        soup = BeautifulSoup(r.content,features="lxml")
        spans = soup.find_all('div',attrs={"class":"filler"})
        
        numbers  = ""
        for span in spans:
            numbers += (f"{span.get_text(strip=True)}, ")
        emb = discord.Embed(description=f"**[{word} Filler List]({link})**",color=ctx.author.color)
        emb.add_field(name= "**Filler Episodes:**",value = numbers[16:])  
        emb.set_footer(text= f'Requested by {ctx.author}' )  
        await ctx.send(embed = emb)
    except:
        em = discord.Embed(title="Not found")
        msg = await ctx.send(embed=em,delete_after=30)

@client.command(name='setmal',aliases=["Setmal","setprofile","Setprofile"])
async def setmal(ctx, *,word): 
    userid = ctx.author.id
    
    
    doc = mal_collect.find_one({"_id": userid})
    if doc != None:
        await ctx.reply("You already have your id tagged!\nTry `S.resetmal <your myanimelist id>` to reset!")
    else:
        post = {"_id": userid,"mal_id":word}
        mal_collect.insert_one(post)
        await ctx.reply("done! Check your profile `S.profile`")
@client.command(name='resetmal',aliases=["Resetmal"])
async def resetmal(ctx, *,word): 
    userid = ctx.author.id
    doc = mal_collect.find_one({"_id": userid})
    if doc != None:
        mal_collect.update_one({"_id": userid},{"$set":{"mal_id":word}})
        await ctx.reply("done")
    else:
        await ctx.reply("Set your id using `S.set <your myanimelist id>`")

@client.command(name='removemal',aliases=["Removemal"])
async def removemal(ctx):
    userid = ctx.author.id
    doc = mal_collect.find_one({"_id": userid})
    if doc != None:
        mal_collect.delete_one({"_id": userid})
        await ctx.reply("done")
    else:
        await ctx.reply("You haven't tagged your account with your id yet...")




@client.command(name='profile',aliases=["Profile"])
async def profile(ctx, *, member: discord.Member =None): 
    try:
        if member == None:
            member = ctx.author
        userid = member.id
        doc = mal_collect.find_one({"_id": userid})
        if doc != None:
            id = doc["mal_id"]
            link = "https://myanimelist.net/profile/{}".format(id)
            linkanime = "https://myanimelist.net/animelist/{}".format(id)
            linkmanga = "https://myanimelist.net/mangalist/{}".format(id)
            r = requests.get(link)

            soup = BeautifulSoup(r.content,features="lxml")
            #<a href="https://myanimelist.net/animelist/ItsIkki?status=2" class="">Completed</a>
        #watch = (soup.find("span",attrs={"class":"di-ib fl-r lh10"}).text)
        
            spans = soup.find_all('span',attrs={"class":"di-ib fl-r lh10"})
            numbers = []
            for span in spans:
                numbers.append(span.string)
            numb = []    
        
            entries = soup.find_all('span',attrs={"class":"di-ib fl-r"})
            for entry in entries:
                numb.append(entry.string)    
        
            
            score = soup.find('div',attrs={"class":"di-tc ar pr8 fs12 fw-b"}).get_text(strip=True)
            #print(score)
            
            days = soup.find('div',attrs={"class":"di-tc al pl8 fs12 fw-b"}).get_text(strip=True)
            
            img = soup.find('img',attrs={"class":"lazyload"})['data-src']
            
            em = discord.Embed(description=f"**[{member.display_name}'s Anime List]({linkanime})**\nMal user: {id}",color = ctx.author.color)   
            em.add_field(name="Watching:",value=numbers[0])
            em.add_field(name="Completed:",value=numbers[1])
            em.add_field(name="On Hold:",value=numbers[2])
            em.add_field(name="Dropped:",value=numbers[3])
            em.add_field(name="Plan to Watch:",value=numbers[4])
            em.add_field(name="Total Entries:",value=numb[0])
            em.add_field(name="Rewatched:",value=numb[1])
            em.add_field(name="Total Episodes:",value=numb[2])
            em.add_field(name="Mean Score:",value=score[11:])
            em.add_field(name="Days:",value=days[5:])
            em.set_thumbnail(url=img)
            em.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
            em.set_footer(text= f'Requested by {ctx.author}' )
            
            msg = await ctx.send(embed = em)
            #await msg.add_reaction("⬅️")
            await msg.add_reaction("🌟")
            await msg.add_reaction("🖌️")
            def check(reaction, user):
                
                return str(reaction.emoji) in ["🌟","🔖","🖌️"] and user != client.user and reaction.message.id == msg.id and user == ctx.author
            # This makes sure nobody except the command sender can interact with the "menu"

            while True:
                try:
                    reaction, user = await client.wait_for('reaction_add', check=check, timeout=30)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example
                    
                    if str(reaction.emoji) == "🌟":
                        
                        #<div class="di-tc va-t pl8 data">
                        #<a href="https://myanimelist.net/anime/20507/Noragami">Noragami</a><br>
                        favs = soup.find_all('li',attrs={"class":"btn-fav"})
                        #(spanss[msg1].a['href'])
                    
                        favanime = ""
                        favmanga = ""
                        favcharacter = ""
                        for fav in favs:
                            if '/anime/' in (fav.a['href']):
                            
                                favanime += f"[{fav['title']}]({fav.a['href']})\n"
                            if '/manga/' in (fav.a['href']):
                            
                                favmanga += f"[{fav['title']}]({fav.a['href']})\n"
                            if '/character/' in (fav.a['href']):
                            
                                favcharacter += f"[{fav['title']}](https://myanimelist.net{fav.a['href']})\n"    
                        if favmanga == "":
                            favmanga = "None"
                        if favanime == "":
                            favanime = "None" 
                        if favcharacter == "":
                            favcharacter = "None"           
                        emb = discord.Embed(description=f"**[{member.display_name}'s Profile]({link})**\nMal user: {id}",color = ctx.author.color)   
                        emb.add_field(name="Favourite Anime:",value=favanime)  
                        emb.add_field(name="Favourite Manga:",value=favmanga)
                        emb.add_field(name="Favourite Character:",value=favcharacter)   
                        emb.set_thumbnail(url=img)    
                        await msg.edit(embed=emb)  
                        await msg.remove_reaction(reaction, user) 
                        await msg.remove_reaction("🌟",client.user)
                        await msg.add_reaction("🔖") 
                        await msg.add_reaction("🖌️")
                    if str(reaction.emoji) == "🔖":
                        await msg.edit(embed=em) 
                        await msg.remove_reaction(reaction, user)
                        await msg.remove_reaction("🔖",client.user)
                        await msg.add_reaction("🌟")  
                        await msg.add_reaction("🖌️")
                    if str(reaction.emoji) == "🖌️":
                        embb = discord.Embed(description=f"**[{member.display_name}'s Manga List]({linkmanga})**\nMal user: {id}",color = ctx.author.color)
                        
                        embb.add_field(name="Reading:",value=numbers[5])
                        embb.add_field(name="Completed:",value=numbers[6])
                        embb.add_field(name="On Hold:",value=numbers[7])
                        embb.add_field(name="Dropped:",value=numbers[8])
                        embb.add_field(name="Plan to Watch:",value=numbers[9])
                        embb.add_field(name="Total Entries:",value=numb[3])
                        embb.add_field(name="Reread:",value=numb[4])
                        embb.add_field(name="Chapters:",value=numb[5])
                        embb.add_field(name="Volumes:",value=numb[6])
                    
                        embb.set_thumbnail(url=img)
                        embb.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
                        embb.set_footer(text= f'Requested by {ctx.author}' )
                        await msg.edit(embed=embb) 
                        await msg.remove_reaction(reaction, user)
                        await msg.remove_reaction("🖌️",client.user)
                        await msg.add_reaction("🌟")
                        await msg.add_reaction("🔖")
                except asyncio.TimeoutError:
                    return
        else:
            await ctx.send("Set your mal id first")    
                
        
                  
    except:
        em = discord.Embed(title="Not found")
        await ctx.send("Not found! Check your mal id")
@client.command(name='Mal',aliases=["mal"])
async def mal(ctx, *,word): 
    try:
        link = "https://myanimelist.net/profile/{}".format(word)
        linkanime = "https://myanimelist.net/animelist/{}".format(word)
        linkmanga = "https://myanimelist.net/mangalist/{}".format(word)
        r = requests.get(link)

        soup = BeautifulSoup(r.content,features="lxml")
        #<a href="https://myanimelist.net/animelist/ItsIkki?status=2" class="">Completed</a>
    #watch = (soup.find("span",attrs={"class":"di-ib fl-r lh10"}).text)
    
        spans = soup.find_all('span',attrs={"class":"di-ib fl-r lh10"})
        numbers = []
        for span in spans:
            numbers.append(span.string)
        numb = []    
    
        entries = soup.find_all('span',attrs={"class":"di-ib fl-r"})
        for entry in entries:
            numb.append(entry.string)    
    #comp = (a.find("span",attrs={"class":"di-ib fl-r lh10"}).text) 
        #print(numbers)
        
        score = soup.find('div',attrs={"class":"di-tc ar pr8 fs12 fw-b"}).get_text(strip=True)
        #print(score)
        
        days = soup.find('div',attrs={"class":"di-tc al pl8 fs12 fw-b"}).get_text(strip=True)
        #print(days)
        #<img class="" data-src="https://cdn.myanimelist.net/images/userimages/10597508.jpg?t=1622063400" src="https://cdn.myanimelist.net/images/userimages/10597508.jpg?t=1622063400" 
        
        img = soup.find('img',attrs={"class":"lazyload"})['data-src']
        #print(img)
        #<img class="" data-src="https://cdn.myanimelist.net/images/userimages/10597508.jpg?t=1622063400" src="https://cdn.myanimelist.net/images/userimages/10597508.jpg?t=1622063400" data-gtm-vis-first-on-screen-13153650_151="297" data-gtm-vis-first-on-screen-13153650_147="329" data-gtm-vis-recent-on-screen-13153650_151="3350706" data-gtm-vis-total-visible-time-13153650_151="100" data-gtm-vis-has-fired-13153650_151="1" data-gtm-vis-recent-on-screen-13153650_147="3350825" data-gtm-vis-total-visible-time-13153650_147="100" data-gtm-vis-has-fired-13153650_147="1">
        em = discord.Embed(description=f"**[{word}'s Anime List]({linkanime})**",color = ctx.author.color)   
        em.add_field(name="Watching:",value=numbers[0])
        em.add_field(name="Completed:",value=numbers[1])
        em.add_field(name="On Hold:",value=numbers[2])
        em.add_field(name="Dropped:",value=numbers[3])
        em.add_field(name="Plan to Watch:",value=numbers[4])
        em.add_field(name="Total Entries:",value=numb[0])
        em.add_field(name="Rewatched:",value=numb[1])
        em.add_field(name="Total Episodes:",value=numb[2])
        em.add_field(name="Mean Score:",value=score[11:])
        em.add_field(name="Days:",value=days[5:])
        em.set_thumbnail(url=img)
        em.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
        em.set_footer(text= f'Requested by {ctx.author}' )
        
        msg = await ctx.send(embed = em)
        #await msg.add_reaction("⬅️")
        await msg.add_reaction("🌟")
        await msg.add_reaction("🖌️")
        def check(reaction, user):
            
            return str(reaction.emoji) in ["🌟","🔖","🖌️"] and user != client.user and reaction.message.id == msg.id and user == ctx.author
        # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', check=check, timeout=30)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example
                 
                if str(reaction.emoji) == "🌟":
                    
                    #<div class="di-tc va-t pl8 data">
                    #<a href="https://myanimelist.net/anime/20507/Noragami">Noragami</a><br>
                    favs = soup.find_all('li',attrs={"class":"btn-fav"})
                    #(spanss[msg1].a['href'])
                    print(favs)
                    favanime = ""
                    favmanga = ""
                    favcharacter = ""
                    for fav in favs:
                        print (fav)
                        if '/anime/' in (fav.a['href']):
                        
                            favanime += f"[{fav['title']}]({fav.a['href']})\n"
                        if '/manga/' in (fav.a['href']):
                        
                            favmanga += f"[{fav['title']}]({fav.a['href']})\n"
                        if '/character/' in (fav.a['href']):
                        
                            favcharacter += f"[{fav['title']}](https://myanimelist.net{fav.a['href']})\n"    
                    if favmanga == "":
                        favmanga = "None"
                    if favanime == "":
                        favanime = "None" 
                    if favcharacter == "":
                        favcharacter = "None"           
                    emb = discord.Embed(description=f"**[{word}'s Profile]({link})**",color = ctx.author.color)   
                    emb.add_field(name="Favourite Anime:",value=favanime)  
                    emb.add_field(name="Favourite Manga:",value=favmanga)
                    emb.add_field(name="Favourite Character:",value=favcharacter)   
                    emb.set_thumbnail(url=img)    
                    await msg.edit(embed=emb)  
                    await msg.remove_reaction(reaction, user) 
                    await msg.remove_reaction("🌟",client.user)
                    await msg.add_reaction("🔖") 
                    await msg.add_reaction("🖌️")
                if str(reaction.emoji) == "🔖":
                    await msg.edit(embed=em) 
                    await msg.remove_reaction(reaction, user)
                    await msg.remove_reaction("🔖",client.user)
                    await msg.add_reaction("🌟")  
                    await msg.add_reaction("🖌️")
                if str(reaction.emoji) == "🖌️":
                    embb = discord.Embed(description=f"**[{word}'s Manga List]({linkmanga})**",color = ctx.author.color)
                    
                    embb.add_field(name="Reading:",value=numbers[5])
                    embb.add_field(name="Completed:",value=numbers[6])
                    embb.add_field(name="On Hold:",value=numbers[7])
                    embb.add_field(name="Dropped:",value=numbers[8])
                    embb.add_field(name="Plan to Watch:",value=numbers[9])
                    embb.add_field(name="Total Entries:",value=numb[3])
                    embb.add_field(name="Reread:",value=numb[4])
                    embb.add_field(name="Chapters:",value=numb[5])
                    embb.add_field(name="Volumes:",value=numb[6])
                
                    embb.set_thumbnail(url=img)
                    embb.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
                    embb.set_footer(text= f'Requested by {ctx.author}' )
                    await msg.edit(embed=embb) 
                    await msg.remove_reaction(reaction, user)
                    await msg.remove_reaction("🖌️",client.user)
                    await msg.add_reaction("🌟")
                    await msg.add_reaction("🔖")
            except asyncio.TimeoutError:
                return
                  
    except:
        em = discord.Embed(title="Not found")
        await ctx.send(embed=em)
   
@client.command(name='recommend',aliases=["Recommend","recom","Recom"])
async def recommend(ctx): 
    
        link = "https://myanimelist.net/recommendations.php?s=recentrecs&t=anime"
        r = requests.get(link)
        
        soup = BeautifulSoup(r.content,features="lxml")
        spans = soup.find_all('a',attrs={"class":"hoverinfo_trigger"})
        anime = []
        animelink = []
   # animeimg = []
        count = 0
        x = 0
        y = 0
        for span in spans:
             #hoverinfo_trigger
            anime.append(span.img['alt'])
            animelink.append(span['href'])
            #animeimg.append(span.img['data-src'])
            count += 1
            if count >99:
                break
        txt = soup.find_all('div',attrs={"class":"spaceit recommendations-user-recs-text"})
     #   print(len(spans))
        
            
        em = discord.Embed(title = "Anime Recommendations:",description= f"If you like [{anime[x]}]({animelink[x]})\nThen try [{anime[x+1]}]({animelink[x+1]})",color = ctx.author.color)
        em.add_field(name="Why?",value = txt[y].string)
        msg = await ctx.reply(embed=em)
        await msg.add_reaction("➡️")
        def check(reaction, user):
            
            return str(reaction.emoji) in ["⬅️","➡️"] and user != client.user and reaction.message.id == msg.id and user == ctx.author
        # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', check=check, timeout=30)

                if str(reaction.emoji) == "➡️":
                    x += 2
                    y += 1
                    emb = discord.Embed(title = "Anime Recommendations:",description= f"If you like [{anime[x]}]({animelink[x]})\nThen try [{anime[x+1]}]({animelink[x+1]})",color = ctx.author.color)
                    emb.add_field(name="Why?",value = txt[y].string)
                    await msg.edit(embed=emb)
            except asyncio.TimeoutError:   
                return

@client.command(name='similar',aliases=["Similar"])
async def similar(ctx, *,name):
    #try:
        
        search = findid(name) 
        id = (search.results[0].mal_id)
        link = f"https://myanimelist.net/anime/{id}/"
        
        r = requests.get(link)
        recom = ""
        count = 1
        linkk = []
        namme = []
        try:
            
            print(1)
            soup = BeautifulSoup(r.content,features="lxml")
            spans = soup.find_all('li',attrs={"class":"btn-anime"})
            
            for span in spans:
                recom += f"{count}. [{span['title']}]({span.a['href']})\n"
                print(span)
                
                count += 1
                namme.append(f"{count}. [{span['title']}]({span.a['href']})")
                linkk.append(span.img['data-src'])
                if count > 7:
                    break
            print(3)    
        except:
            print(2)

            sou = BeautifulSoup(r.content,features="lxml")
            spas = sou.find_all('li',attrs={"class":"btn-anime auto"})
            for spa in spas:
                recom += f"{count}. [{spa['title']}]({spa.a['href']})\n"
                print(spa)
                namme.append(f"{count}. [{spa['title']}]({spa.a['href']})")
                linkk.append(spa.img['src'])
                count += 1
                if count > 7:
                    break
            print(4) 
              
            print(recom)
        em = discord.Embed(title = "Anime Recommendations:",description= recom,color = ctx.author.color)
        message = await ctx.reply(embed = em)
        emoji_numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
        for i in range(count-1):
            await message.add_reaction(emoji_numbers[i])
        def check(reaction, user):
                return str(reaction.emoji) in emoji_numbers and user != client.user and reaction.message.id == message.id and user == ctx.author
            # This makes sure nobody except the command sender can interact with the "menu"
        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', check=check, timeout=20)
                index = emoji_numbers.index(reaction.emoji)
                emb = discord.Embed(description = namme[index],color = ctx.author.color)
                try:
                    image = linkk[index].replace("/r/90x140","")
                    emb.set_image(url = image)
                except:
                    emb.set_footer(text="No Image Found")
                    
                
                await message.edit(embed =emb)
                await message.remove_reaction(reaction, user)
                for i in range(count-1):
                    await message.remove_reaction(emoji_numbers[i],client.user) 
            except asyncio.TimeoutError:
                    return    
        
            
    #except:
        
       # return

        



@client.command(name="wallpaper",aliases = ["Wallpaper","wall","Wall"])
@commands.cooldown(9, 120, BucketType.user)
async def wallpaper(ctx, *,word = None ):
    
    try:    
        if word == None:
            word = 'anime'
        word = word.replace(" ","+")
        link = f"https://www.wallpaperflare.com/search?wallpaper={word}"
        r = requests.get(link)
        
        
        walls = []
        soup = BeautifulSoup(r.content,features="lxml")
        spans = soup.find_all('img',attrs={"class":"lazy"})
        
        for span in spans:
            walls.append(span['data-src'])
            
        
        wall = random.choice(walls)
        resp = requests.get(wall)
        wallpap = Image.open(BytesIO(resp.content))  
        wallpap.save('WallpaperForYou.jpg')
        await ctx.send(file=discord.File("WallpaperForYou.jpg"))

    except:
        await ctx.reply("Not found")


@client.command(name="mwallpaper",aliases = ["Mwallpaper","mwall","Mwall"])
@commands.cooldown(9, 120, BucketType.user)
async def wallpaper_mobile(ctx, *,word = None ):

    try:
        
        if word == None:
            word = 'anime'
        word = word.replace(" ","+")
        link = f"https://www.wallpaperflare.com/search?wallpaper={word}&mobile=ok"
        r = requests.get(link)
        
       # <a ="" href="https://www.wallpaperflare.com/akira-fudo-devilman-crybaby-red-wallpaper-znlue" target="_blank">
#<img class="lazy loaded" itemprop="contentUrl" alt="Akira Fudo, devilman crybaby, red HD wallpaper" title="Akira Fudo, devilman crybaby, red HD wallpaper" data-src="https://c4.wallpaperflare.com/wallpaper/252/232/12/akira-fudo-devilman-crybaby-red-devil-hd-wallpaper-preview.jpg" src="https://c4.wallpaperflare.com/wallpaper/252/232/12/akira-fudo-devilman-crybaby-red-devil-hd-wallpaper-preview.jpg" data-was-processed="true" width="400" height="250">
#</a>   
        
        soup = BeautifulSoup(r.content,features="lxml")
        spans = soup.find_all('a',attrs={"itemprop":"url"})
        walls = []
        for span in spans:
            walls.append(span.img['data-src'])
            
        wall = random.choice(walls)
        resp = requests.get(wall)
        wallpap = Image.open(BytesIO(resp.content))  
        wallpap.save('WallpaperForYou.jpg')
        await ctx.send(file=discord.File("WallpaperForYou.jpg"))
    except:
        await ctx.reply("Not found")

@client.command(name='rand',aliases=["Random","Rand","random"])
async def rndm(ctx, number : int):
    try:
        result = random.randint(1,number)      
        await ctx.send(result)  
    except:
        await ctx.reply("I need a number")

@client.command(name='userinfo',aliases=["whois","Whois","Userinfo"])
async def userinfo(ctx, member: discord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    roles = [role for role in member.roles[1:]]
    role1 = roles[::-1]
    msg = ""
    perm_list = [perm[0] for perm in member.guild_permissions if perm[1]]
    
    
    if 'administrator' in perm_list:
        msg += f"__`Administrator`__  "
    if 'manage_guild' in perm_list:    
        msg += f" __`Manage Server`__ "
    if 'manage_roles' in perm_list:    
        msg += f" __`Manage Roles`__ "   
    if 'manage_channels' in perm_list:    
        msg += f" __`Manage Channels`__ "
    if 'manage_messages' in perm_list:    
        msg += f" __`Manage Messages`__ "           
    if 'manage_webhooks' in perm_list:    
        msg += f" __`Manage Webhooks`__ "
    if 'manage_nicknames' in perm_list:    
        msg += f" __`Manage Nicknames`__ "
    if 'manage_emojis' in perm_list:    
        msg += f" __`Manage Emojis`__ "   
    if 'kick_members' in perm_list:    
        msg += f" __`Kick Members`__ " 
    if 'ban_members' in perm_list:    
        msg += f" __`Ban Members`__ "   
    if 'mention_everyone' in perm_list:    
        msg += f" __`Mention Everyone`__ " 
    if 'mute_members' in perm_list:    
        msg += f" __`Mute Members`__ " 
    if 'deafen_members' in perm_list:    
        msg += f" __`Deafen Members`__ "           
         
    #perms = [perms for perms in perm_list]
    embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at,title=f"User : {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="ID:", value=member.id,inline=False)
    embed.add_field(name="Display Name:", value=member.display_name,inline=False)

    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
    if role1 != []:
        embed.add_field(name=f"Roles[{len(role1)}]:", value="".join([role.mention for role in role1]),inline=False)
    else:
        embed.add_field(name=f"Roles[{len(role1)}]:", value="None",inline=False) 
    if msg != "":
        embed.add_field(name="Permissions:", value=msg,inline=False)
    if member.bot:  
        embed.add_field(name="Discord Bot?", value="Yes",inline=False)  
       
    
    
    #print(role.mention for role in roles)
    #print(roles)
    #print(member.guild_permissions for perm in perm_list)
    await ctx.send(embed=embed)

@client.command(name="serverinfo",aliases=["Serverinfo","Sinfo","sinfo"])
async def serverinfo(ctx):
  name = str(ctx.guild.name)

  ownner = str(ctx.guild.owner)
  id = str(ctx.guild.id)
  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)
  txtchannel = str(len(ctx.guild.text_channels))
  vcchannel = str(len(ctx.guild.voice_channels))
  role = str(len(ctx.guild.roles))
  icon = str(ctx.guild.icon_url)
  create = ctx.guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")
  embed = discord.Embed(color=discord.Color.blue())
  embed.set_author(name=name,icon_url=icon)
  embed.set_footer(text=f"Requested by {ctx.author} | Server Created : {create}")
  embed.set_thumbnail(url=icon)
  embed.add_field(name="Owner", value=ownner, inline=True)
  embed.add_field(name="Region", value=region, inline=True)
  embed.add_field(name="Server ID", value=id, inline=True)
  embed.add_field(name="Text Channels", value=txtchannel, inline=True)
  embed.add_field(name="Voice Channels", value=vcchannel, inline=True)
  embed.add_field(name="Roles", value=role, inline=True)
  embed.add_field(name="Member Count", value=memberCount, inline=True)

  await ctx.send(embed=embed)

@client.command(name="yt",aliases=["Yt","Youtube","youtube"])
async def yt(ctx, *, search):

    query_string = urllib.parse.urlencode({'search_query': search})
    htm_content = urllib.request.urlopen(
        'http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r'/watch\?v=(.{11})',htm_content.read().decode())
    await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])

@client.command(name="embed",aliases=["Embed"])   
@commands.has_permissions(manage_messages=True) 
async def embed(ctx,color, *,text = None):
    #msg, color = text.split("|")
    if text == None:
        text = ""
    first_word = color[0]
    
    if first_word == "#" and len(color) == 7:
        hexcode = int(color.replace("#",""),16)
        colorhex = int(hex(hexcode),0)
        em = discord.Embed(description = text,color=colorhex,timestamp=datetime.datetime.utcnow())
    else:
        colorhex = 0x00ebff 
        text = color + " " + text
        em = discord.Embed(description = text,color=colorhex,timestamp=datetime.datetime.utcnow())
    ##if color == None:
        #colorhex = 0x00ebff
    
    #else:  
        #print(1)  
       ## hexcode = int(color.replace("#",""),16)
        #colorhex = int(hex(hexcode),0)
    #em = discord.Embed(description = text,color=colorhex,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.guild.name,icon_url=ctx.guild.icon_url)
    await ctx.send("```To add a Image into your embed, paste the link of the particular image below within 20 seconds.If you don't want to embed image the process will be executed in 20 seconds. You are requested not to send any message except the link in these 20 seconds or the process will be terminated.```")
    try: 
        def check(msg1):
            return msg1.author == ctx.author and ctx.channel == msg1.channel 
        
        msg1 = await client.wait_for("message", check=check,timeout=20)
        link = msg1.content
        #resp=requests.get(msg)
         
        em.set_image(url=link)
        await ctx.send(embed=em)
        
    except asyncio.TimeoutError:
        await ctx.send(embed=em)            
       
@client.command(name="Hall",aliases=["hall"])
@commands.has_permissions(manage_messages= True)    
async def hall(ctx,* ,text):
    hall_point = client.get_channel(837605170330337310)
    if ctx.channel == hall_point:
        x, msg = text.split("|")

    
    
        colorhex = 0xff0000 
    
        em = discord.Embed(description = msg,color=colorhex,timestamp=datetime.datetime.utcnow())
    ##if color == None:
        #colorhex = 0x00ebff
    
    #else:  
        #print(1)  
       ## hexcode = int(color.replace("#",""),16)
        #colorhex = int(hex(hexcode),0)
    #em = discord.Embed(description = text,color=colorhex,timestamp=datetime.datetime.utcnow())
        em.set_author(name=f"Hall Of Fame {x}" ,icon_url=ctx.guild.icon_url)
        await ctx.send(embed=em)
        await ctx.message.delete() 
    else:
        return       
             
       

@client.command(name="submit",aliases=["Submit"])    
async def submit(ctx,*,text):
    drop_point = client.get_channel(837610754298478643)
    if ctx.channel == drop_point:
        
        
        colorhex = 0x00ebff 
    
        em = discord.Embed(description = f"Submitted by {ctx.author}\nUser ID: {ctx.author.id}",color=colorhex,timestamp=datetime.datetime.utcnow())
    ##if color == None:
        #colorhex = 0x00ebff
    
    #else:  
        #print(1)  
       ## hexcode = int(color.replace("#",""),16)
        #colorhex = int(hex(hexcode),0)
    #em = discord.Embed(description = text,color=colorhex,timestamp=datetime.datetime.utcnow())
        em.set_author(name=f"{text}")
        await ctx.send("```Paste the link of the image below within 20 seconds to complete your submission.\nDon't Send any message between these 20 sec```",delete_after=20)
        try: 
            def check(msg1):
                return msg1.author == ctx.author and ctx.channel == msg1.channel 
            
            msg1 = await client.wait_for("message", check=check,timeout=20)
            link = msg1.content
            id = msg1.id
            delmsg = await drop_point.fetch_message(id)
            await delmsg.delete()

        #resp=requests.get(msg)
            try:
                if link == "":
                    await ctx.send("You need to send the Image Link! try again...",delete_after=15)
                else:
                    em.set_image(url=link)
                    em.set_footer(text= f"Tournament Submission")
                    await ctx.send(embed=em)
            except:
                await ctx.send("You need to send the Image Link! try again...",delete_after=15)    
        
        except asyncio.TimeoutError:
            await ctx.send("Timeout",delete_after=10)  
        await ctx.message.delete()      
    else:
        return                  

@client.command(name="post",aliases=["Post"])  
@commands.has_permissions(manage_messages=True)  
async def post(ctx, *,id): 
    id1, id2 = id.split("|")  
    post_point = client.get_channel(837609315572383755)
    if ctx.channel == post_point: 
        channel = client.get_channel(837610754298478643) 

        msg1 = await channel.fetch_message(id1)
        msg2 = await channel.fetch_message(id2) #<@&836631353117900902> 
        message1 = await ctx.send("**Vote for the following Submissions!!**",embed = msg1.embeds[0])
        message2 = await ctx.send(embed = msg2.embeds[0])
        await message1.add_reaction("<a:Stela_up:838153046537535549>")
        await message2.add_reaction("<a:Stela_up:838153046537535549>")
    else:
        return    
    await ctx.message.delete()    
             
@client.event
async def on_member_join(member):
    if member.guild.id == (754084144807673947):

        village = client.get_channel(754090618669629481)
        rules = client.get_channel(754749808476160112)
        role = client.get_channel(754089226030678128)
        em = discord.Embed(description= f"Welcome {member.mention}, Enjoy your stay🤗! Don't forget to read {rules.mention} and check {role.mention} ",timestamp=datetime.datetime.utcnow(),color=0x00ebff)   
        welcomegif = ("https://i.imgur.com/COTu9rN.gif","https://i.imgur.com/ZzvVprt.gif")  
        rndgif = random.choice(welcomegif)
        em.set_image(url=rndgif)
        await village.send(f"{member.mention}",embed = em)   

@client.command(name="server")
async def server(ctx):
    try:
        await ctx.author.send("Heres our support server!\nhttps://discord.gg/ZbemgbQuXa")
    except:
        await ctx.send("Maybe your dm is close....")    
@client.command(name="guild")
async def guild(ctx):
    
    if ctx.author == owner:
          
        servers = (client.guilds)
        guilds = []
        serverss = str(len(servers))
        for guild in servers:
            guilds.append(guild.name)

        
        
        await ctx.send(guilds[-50:])
        await ctx.send(f"total servers {serverss}")



@client.command(name="poll",aliases = ["Poll"])
async def poll(ctx,ques, *,msg: commands.clean_content):
    if ctx.author == owner:
        data = re.split(pattern = "\|+" , string = msg)
        await ctx.send("❔"+ ques)
        for options in data:
            message = await ctx.send(options)
            await message.add_reaction("⏫")

@client.command(name="f",aliases = ["F"])
async def f(ctx,*,msg: commands.clean_content):
    message = await ctx.send(f"Press 🇫 to pay respects to **{msg}**")  
    await message.add_reaction("🇫")
    count = 0
    uss = []
    def check(reaction, user):
        return str(reaction.emoji) == "🇫" and user != client.user and reaction.message.id == message.id and user.id not in uss
    while True:     
        try:
            reaction, user = await client.wait_for("reaction_add", check=check,timeout= 25)
            uss.append(user.id)
            await ctx.send(f"**{user.display_name}** has paid their respects.")
            count += 1
        except asyncio.TimeoutError:
            if count == 0:
                await message.reply(f"nobody paid their respects to **{msg}**....")
            if count == 1:
                await message.reply(f"**1** person paid their respects to **{msg}**") 
            if count > 1:
                await message.reply(f"**{count}** people paid their respects to **{msg}**")       
            return 
      
        

    #except:
        #await ctx.send("Nobody paid respects, how shameful.")    


        

@client.command(name="rndqoute",aliases = ["Rndqoute","Rq","rq"])
async def rndquote(ctx):
    qoute = requests.get("https://animechan.vercel.app/api/random").json()
    
    anime = qoute['anime']
    character = qoute['character']
    line = qoute['quote']
    q = discord.Embed(timestamp=datetime.datetime.utcnow(),color = discord.Color(0x00ff7d))
    q.set_author(name="Random Qoute",icon_url= ctx.author.avatar_url)
    q.add_field(name=f"Anime: {anime}",value=f'"{line}"\n   -said by {character}')
    msg = await ctx.send(embed = q)
    await msg.add_reaction("<:AO_stonksup:843516237962149958>")



#GIVEAWAY
def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]
@client.command(name="gcreate")
#@commands.has_permissions(manage_messages = True)
async def giveaway(ctx):
    if ctx.author == owner:
        await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")

        questions = ["Which channel should it be hosted in?", 
                    "What should be the duration of the giveaway? (s|m|h|d)",
                    "What is the prize of the giveaway?","Enter the requirements If None then Type 'None'"]

        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel 

        for i in questions:
            await ctx.send(i)

            try:
                msg = await client.wait_for('message', timeout=30, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You didn\'t answer in time, please be quicker next time!')
                return
            else:
                answers.append(msg.content)
        try:
            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
            return

        channel = client.get_channel(c_id)

        time = convert(answers[1])
        if time == -1:
            await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
            return
        elif time == -2:
            await ctx.send(f"The time must be an integer. Please enter an integer next time")
            return            

        prize = answers[2]
        rqmt = answers[3]
        
        await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")


        embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)
        if rqmt != "None":
            embed.add_field(name="Requirements:",value= rqmt)
        embed.add_field(name = "Hosted by:", value = ctx.author.mention)

        embed.set_footer(text = f"Ends {answers[1]} from now!")

        my_msg = await channel.send(embed = embed)
        

        await my_msg.add_reaction("🎉")
        

        await asyncio.sleep(time)


        new_msg = await channel.fetch_message(my_msg.id)


        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(client.user))
        if users == []:
            await my_msg.reply("No one Participated ;-;")
        else:    
            winner = random.choice(users)

            await my_msg.reply(f"Congratulations! {winner.mention} won {prize}!")
@client.command()
@commands.has_permissions(manage_messages = True)
async def reroll(ctx,id_ : int):
    try:
        new_msg = await ctx.channel.fetch_message(id_)
    except:
        await ctx.send("The id was entered incorrectly.")
        return
    
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await ctx.send(f"Congratulations! The new winner is {winner.mention}.!")
#@client.command(name="t")
#async def t(ctx):    
    
    #asset1 = ctx.author.avatar_url
    #data1 = BytesIO(await asset1.read())   
    #img = Image.open(data1)
  
    #height,width = img.size
    #lum_img = Image.new('L', [height,width] , 0)
  
    #draw = ImageDraw.Draw(lum_img)
    #draw.pieslice([(0,0), (height,width)], 0, 360, fill = 255, outline = "white")
    #img_arr =np.array(img)
    #lum_img_arr =np.array(lum_img)
    #display(Image.fromarray(lum_img_arr))
    #final_img_arr = np.dstack((img_arr,lum_img_arr))
    #fll = Image.fromarray(final_img_arr)
    #fll.save("test.png")
    #await ctx.send(file=discord.File("test.png"))
#@client.command(name='w',aliases=["W"]) 
#@commands.cooldown(2, 120, BucketType.user)  
#async def w(ctx):
 #   i = 1
 #   chosen_index = i
  #  while i < 39: 
   #     embed=  discord.Embed(title = f"**{waifuname[chosen_index]}**",description= waifuseries[chosen_index],color =0x00ebff)
  #      embed.set_image(url=waifupics[chosen_index])
   #     message=await ctx.send(embed=embed)
    #    i += 1
       # chosen_index = i


             

async def dm_helper(player: discord.User,question , answer , option , options):
    #if player.bot:
    #    return random.choice(emojis)
    
    
    embedd = discord.Embed(title = "Chase the Runner",description = f"**Type the Answer of the Question!**\n{question}\n\n{option}\n`Type cancel to cancel the game`") 
    msg = await player.send(embed = embedd)
    def check(res):
        return res.content.lower() in options and res.author == player 
        

    try:
        
        res = await client.wait_for('message',check=check,timeout=30)
        
        if res.content.lower() == "cancel":
            emmb = discord.Embed(title = "Chase the Runner",description = f"`Cancelling the game!`",color=0xFF0000) 
            await msg.edit(embed = emmb,delete_after = 20)
            return ["cancel"]
            
        if res.content.lower() == answer.lower():
            embed4 = discord.Embed(title = "Chase the Runner",description = f"**Answer the Question!**\n{question}\n`{res.content}` - **Correct Answer: +1**",color=0x00FF00) 
            await msg.edit(embed = embed4,delete_after = 20)
            return [1]   
        else:    
            embed2 = discord.Embed(title = "Chase the Runner",description = f"**Answer the Question!**\n{question}\n**Wrong Answer: +0**",color=0xFF0000) 
            await msg.edit(embed = embed2,delete_after = 20)
            return [0]
            
    except asyncio.TimeoutError:
        embed3 = discord.Embed(title = "Chase the Runner",description = f"timeout....",color=0xFF0000) 
        await msg.edit(embed = embed3,delete_after = 10)
        return [0,1]

    
    
@client.command(name='challenge',pass_context = True,aliases=["Challenge"])    
async def challenge(ctx, member : discord.Member):
    if ctx.author != member:
        mem1 = ctx.author
        mem2 = member
        htmlcodes = (("'",'&#039;'),('"','&quot;'),(">",'&GT;'),('<','&lt;'),('&','&amp;'))
        
        em = discord.Embed(title = "Chase the Runner",description = f"You have been challenged by {mem1.mention}\nYou have to answer as many questions as you can, time for each question is 40 sec\n`Do you accept the challenge?`")
        msg = await ctx.send(mem2.mention,embed = em)
        await msg.add_reaction("❌")
        await msg.add_reaction("✅")
        emoji_numbers = ["✅","❌"]
        def check1(reaction, user):
            return str(reaction.emoji) in ["✅","❌"] and user != client.user and reaction.message.id == msg.id and user.id == mem2.id
        try:
            reaction, user = await client.wait_for('reaction_add',check = check1,timeout = 40) 
            await msg.remove_reaction(reaction, mem2)
            i = 0
            while i < 2:
                await msg.remove_reaction(emoji_numbers[i],client.user)
                i += 1
            if str(reaction.emoji) == "✅":
                money = 0
                name = "True"
                work = "True"
                count = 0
                
                while name == "True":
                    api1 = "https://opentdb.com/api.php?amount=45&category=31&difficulty=easy&type=multiple"
                    api2 = "https://opentdb.com/api.php?amount=50&category=31&difficulty=medium&type=multiple"
                    api3 = "https://opentdb.com/api.php?amount=37&category=31&difficulty=hard&type=multiple"
                    api = random.choice([api1,api2,api3])
                    r = requests.get(api).json()
                    leng = (len(r['results'])-1)
                    
                    choose = random.randint(0,leng)
                    qu = (r['results'][choose]['question'])
                    
                    ans = (r['results'][choose]['correct_answer'])
                    wrong = r['results'][choose]['incorrect_answers']
                    options = []
                    options.append(wrong[0])
                    options.append(wrong[1])
                    options.append(ans)
                    options.append(wrong[2])
                    shuffled = random.sample(options, len(options))
                
                        
                    option = ""
                    nom = 1
                    for shuffle in shuffled:

                        option += f"{nom}. {shuffle}\n"  
                        nom += 1 
        
                    for code in htmlcodes:
                        option = option.replace(code[1],code[0])
                        options[0] = options[0].replace(code[1],code[0])
                        options[1] = options[1].replace(code[1],code[0])
                        options[2] = options[2].replace(code[1],code[0])
                        options[3] = options[3].replace(code[1],code[0])
                        qu = qu.replace(code[1],code[0]) 
                        ans = ans.replace(code[1],code[0])
                    for i in range(len(options)):
                        options[i] = options[i].lower() 
                    
                    def check(response):
                        return response.content.lower() in options and response.author == mem2 and response.channel == ctx.channel
                    embe = discord.Embed(title = "Chase the Runner",description = f"{qu}\n\n{option}",color=0x00FF00)    
                    await msg.edit(embed = embe)
                    try:
                        
                        
                        response= await client.wait_for('message', check= check, timeout= 45)
                        
                        if response.content.lower() == ans.lower():
                            money += 1
                            count += 1
                            if count > 8:
                                name = "False"
                                
                        else:
                            name = "False"        
                            
                    except asyncio.TimeoutError:
                        #ms = await ctx.send(f"**Timeout**",delete = 20)
                        
                        name = "False"
                    
                embed = discord.Embed(title = "Chase the Runner",description = f"**Robbery ended**\nYou robbed {money*100}+ Respect",color=0x00FF00) 
                await msg.edit(embed =embed)        
                await ctx.send(f"{mem1.mention}|{mem2.mention}`Come in Dm \nChase will start in 30 sec`")
                
                TPA = 0
                TPB = 2
                
                api1 = "https://opentdb.com/api.php?amount=45&category=31&difficulty=easy&type=multiple"
                api2 = "https://opentdb.com/api.php?amount=50&category=31&difficulty=medium&type=multiple"
                api3 = "https://opentdb.com/api.php?amount=37&category=31&difficulty=hard&type=multiple"
                api = random.choice([api1,api2,api3])
                r = requests.get(api).json()
                lengg = (len(r['results'])-1)
                choice = random.randint(0,lengg)
                q = (r['results'][choice]['question'])
                anss = (r['results'][choice]['correct_answer'])
                wrongg = r['results'][choice]['incorrect_answers']
                optionss = []
                optionss.append(wrongg[0])
                optionss.append(wrongg[1])
                optionss.append(anss)
                optionss.append(wrongg[2])
                shuffledd = random.sample(optionss, len(optionss))
                optionss.append("cancel")
                
                
                
                optio = ""
                no = 1
                for shuffles in shuffledd:
                    optio += f"{no}. {shuffles}\n"  
                    no += 1  
                
                for code in htmlcodes:
                        optio = optio.replace(code[1],code[0])
                        optionss[0] = optionss[0].replace(code[1],code[0])
                        optionss[1] = optionss[1].replace(code[1],code[0])
                        optionss[2] = optionss[2].replace(code[1],code[0])
                        optionss[3] = optionss[3].replace(code[1],code[0])
                        q = q.replace(code[1],code[0]) 
                        anss = anss.replace(code[1],code[0])
                for i in range(len(optionss)):
                    optionss[i] = optionss[i].lower() 
                    
                dead = 1    
                await asyncio.sleep(20)
                await mem1.send("`Chase is starting Now!!`")
                await mem2.send("`Chase is starting Now!!`") 
                while work == "True":
                    point1 = dm_helper(mem1, q, anss,optio,optionss )  # Note no "await"
                    point2 = dm_helper(mem2, q, anss,optio,optionss)
                    pointA, pointB = await gather(point1, point2)
                    if pointA[0] != "cancel" and pointB[0] != "cancel" :
                        TPA += pointA[0]
                        TPB += pointB[0]
                        
                        api1 = "https://opentdb.com/api.php?amount=45&category=31&difficulty=easy&type=multiple"
                        api2 = "https://opentdb.com/api.php?amount=50&category=31&difficulty=medium&type=multiple"
                        api3 = "https://opentdb.com/api.php?amount=37&category=31&difficulty=hard&type=multiple"
                        api = random.choice([api1,api2,api3])
                        r = requests.get(api).json()
                        lengg = (len(r['results'])-1)
                        choice = random.randint(0,lengg)
                        q = (r['results'][choice]['question'])

                        anss = (r['results'][choice]['correct_answer'])
                        wrongg = r['results'][choice]['incorrect_answers']
                        optionss = []
                        optionss.append(wrongg[0])
                        optionss.append(wrongg[1])
                        optionss.append(anss)
                        optionss.append(wrongg[2])
                        shuffledd = random.sample(optionss, len(optionss))
                        optionss.append("cancel")
                        
                        
                        optio = ""
                        no = 1
                        for shuffles in shuffledd:
                            optio += f"{no}. {shuffles}\n"  
                            no += 1  
                        
                        for code in htmlcodes:
                            optio = optio.replace(code[1],code[0])
                            optionss[0] = optionss[0].replace(code[1],code[0])
                            optionss[1] = optionss[1].replace(code[1],code[0])
                            optionss[2] = optionss[2].replace(code[1],code[0])
                            optionss[3] = optionss[3].replace(code[1],code[0])
                            q = q.replace(code[1],code[0]) 
                            anss = anss.replace(code[1],code[0])
                        for i in range(len(optionss)):
                            optionss[i] = optionss[i].lower()
                        
                        rd = "<a:Stela_road:865251683927719947> "
                        run = "<a:Stela_runner:865251935901057034>"
                        chase = "<a:Stela_chaser:865245652345946132>"
                        scene = f'{(8-(TPB+1))*rd}{run}{((TPB-TPA)-1)*rd}{chase}{TPA*rd}'
                        
                        if len(pointA) == 2 and len(pointB) == 2:
                            
                            if  pointA[1] == 1 and pointB[1] == 1:
                                
                                dead += 1
                                
                        if len(pointA) != 2 or len(pointB) != 2:
                            dead = 1 
                                
                        if dead > 3:
                            await mem1.send(f"`Game has been terminated because of inactivity`")
                            await mem2.send(f"`Game has been terminated because of inactivity`") 
                            work = "False"    

                        if TPA == TPB:
                            await mem1.send(f"**You Caught** {mem2} congrats!\n{scene}")
                            await mem2.send(f"**You Loose...**\n{mem1} Caught You!\n{scene}") 
                            work = "False"
                        if TPB == 7 and TPA < 7:
                            await mem1.send(f"**You Loose...**\n{mem2} ran away with {money*100}+ Respect  ;-;\n{scene}")
                            await mem2.send(f"**You Win**\nYou succefully ran away from {mem1} with {money*100}+ Respect \n{scene}") 
                            work = "False"
                        else:
                            #emb2 = discord.Embed(title = "Chase the Runner",description = chase)
                            await mem1.send(scene,delete_after = 10)
                            await mem2.send(scene,delete_after = 10)   
                    else:
                        print(1)
                        await mem1.send("Game has been cancelled")
                        await mem2.send("Game has been cancelled")   
                        work = "False"       
            if str(reaction.emoji) == "❌":
                emb = discord.Embed(title = "Chase the Runner",description = f"{mem2.mention} declined the Challenge!",color=0xFF0000)
                await msg.edit(embed = emb)  
        except asyncio.TimeoutError:
            embbb = discord.Embed(title = "Chase the Runner",description = f"You have been challenged by {mem1.mention}\nYou have to answer as many questions as you can, time for each question is 45 sec\n`Timeout`",color=0xFF0000)
            await msg.edit(embed = embbb)
            
    else:
        await ctx.reply("How can you play with yourself.. Dummy")        
#client.remove_command("help")
         
           
@client.command(name='upload')    
async def upload(ctx, num : int,*,question):
    print(ctx.author.id)
    if ctx.author.id == 745006368175423489:
        print(1)
        def check(response):
            return  response.author.id == ctx.author.id and response.channel == ctx.channel
        count = 1
        options = []
        num += 1
        while count < num:    
                
            await ctx.reply(f"Send the {count} option")
            try:
                response= await client.wait_for('message', check= check, timeout= 60)
                await ctx.send(response.content)
                options.append(response.content)
                count += 1
            except:    
                await ctx.send("smtg went wrong")

        await ctx.reply(f"Send the correct answer")     
        res= await client.wait_for('message', check= check, timeout= 60)  
        await ctx.send(res.content)
        answer =  res.content
        result = ""
        for optio in options:
            result += f"{optio}\n"
        emb = discord.Embed(description = f"{question}\n\n{result}\n\nCorrect answer : {answer}")
        msg =await ctx.send(embed = emb)
        await msg.add_reaction("❌")
        await msg.add_reaction("✅")
        def check1(reaction, user):
                return str(reaction.emoji) in ["✅","❌"] and user != client.user and reaction.message.id == msg.id and user.id == ctx.author.id
        reaction, user = await client.wait_for('reaction_add',check = check1,timeout = 40) 
        if str(reaction.emoji) == "✅": 
            count = animetriv_collect.find().count()
            post = {"_id": count,"question": question, "options" : options,"answer" : answer }
            animetriv_collect.insert_one(post)
            emb = discord.Embed(description = f"{question}\n\n{result}\n\nCorrect answer : {answer}\n\n'Added Successfully")
            await msg.edit(embed = emb)
        if str(reaction.emoji) == "❌":    
            await ctx.send("cancelled")
    else:
        return




@client.command(name='cleardb')
async def cleardb(ctx): 
    if ctx.author.id  == 745006368175423489:
        docs = upd.find().count()
        lmt = docs - 40
        if lmt > 2:
            await ctx.send(f'total entries {docs}')
            doc = upd.find().limit(lmt)
            count = 0
            for d in doc:
                count += 1
                upd.delete_one({'_id' : d['_id']})

            await ctx.send(f'deleted {count} enties') 
        else:
            await ctx.send(docs) 
    else:
        print('error')
@client.command(name='tyyy')
async def tyy(ctx, link): 
    if ctx.author == owner:
           #https://mywaifulist.moe/popular
        driver.get(link)
        await asyncio.sleep(5)
        
        soup = BeautifulSoup(driver.page_source,features="lxml")
        url = soup.find_all('div', {"class" : "md:my-0 my-6"})
        
        urll = []
        for u in url:
            urll.append(u.div.a['href'])
        print(urll)
        for ur in urll:
            url = f"https://mywaifulist.moe{ur}" 
            driver.get(url)
            await asyncio.sleep(5)
            soup = BeautifulSoup(driver.page_source,features="lxml")
            spans = soup.find("div", {"class" : "col-span-4 sm:col-span-5"})
            images = soup.find("div", {"class" : "md:w-1/3 lg:w-1/4 sm:mb-0 mb-4"})
            print(images.div.img)
            name = spans.h1.text
            animes = soup.find("a", {"class" : "tooltip-target text-blue-500 font-semibold no-underline tracking-wide cursor-pointer text-xs"})
            anime = animes.text
            await ctx.send(f"name : {name}\nanime : {anime}") 
            img = images.div.img['src']
            await ctx.send(img)
            dc = girl.find_one({'name' : name, 'anime' : anime})
            if dc == None:
                r =  requests.get(img)  
                byt  = BytesIO(r.content)
                #print(byt)
                print(byt)
                #im.show()
                file = discord.File(fp = byt, filename = 'waifu.png')
                msg = await ctx.send(file = discord.File(fp = byt, filename = 'waifu.png'))
                await msg.add_reaction("❌")
                await msg.add_reaction("✅")
                def check1(reaction, user):
                        return str(reaction.emoji) in ["✅","❌"] and user != client.user and reaction.message.id == msg.id and user.id == ctx.author.id
                reaction, user = await client.wait_for('reaction_add',check = check1,timeout = 40) 
                if str(reaction.emoji) == "✅": 
                    count = girl.find().count()
                    print(count)
                    post = {"_id": count,"name": name, "anime" : anime,"image" : r.content }
                    emb = discord.Embed(description = f"{name}\n\n{anime}")
                    emb.set_image(url = 'attachment://waifu.png')
                    await msg.edit(embed = emb)
                    girl.insert_one(post)
                    print(1)
                    
                if str(reaction.emoji) == "❌":    
                    await ctx.send("cancelled")

            else:
                await ctx.send('already exist')        
        print('done')        
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

@tasks.loop(minutes= 15)
async def checkNewLoop():
    
    anime = check_new()
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
    

def check_new():
    link = "https://animixplay.to"
    
    
    driver.get(link)
    
    r = driver.page_source
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
    driver.get(url)
    
    r = driver.page_source
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
        link = 'http://myanimelist.net/anime/season/2022/spring'
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
@client.command(name='airing',aliases=["Air","Airing","air"])
@commands.cooldown(2, 80, BucketType.user) 
async def air(ctx):
            docs = airingg.find()
            titles = []
            animeid = []
            for doc in docs:
                animeid.append(doc['_id'])
                titles.append(doc['name'])
            
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
            x = -10
            y = 0
            cur_page = 1
            x = 0
            y = 10
            namee = ""
            
            pages = math.ceil(len(titles)/10)
            for name,idd in zip(titles[x:y],animeid[x:y]):
                namee += f'{titles.index(name)+1}. {name} - `{idd}`\n\n'
            embb = discord.Embed(title = "Airing Animes:",description = namee,color=0x00ebff)
            embb.set_footer(text = f"{cur_page}/{pages}")
            message = await ctx.send(embed = embb) 
            await message.add_reaction("◀️")
            await message.add_reaction("▶️")
            
            while True:
                try:
                    reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
                    if str(reaction.emoji) == "▶️" and cur_page != pages:
                        namee = ""
                        cur_page += 1
                        x += 10
                        y += 10
                        for name,idd in zip(titles[x:y],animeid[x:y]):
                            namee += f'{titles.index(name)+1}. {name} - `{idd}`\n\n'
                        if namee != None:    
                            em = discord.Embed(title = "Airing Animes:",description = namee,color=0x00ebff)
                            em.set_footer(text = f"{cur_page}/{pages}")
                            await message.edit(embed = em)
                        
                    elif str(reaction.emoji) == "◀️" and cur_page > 1:
                        namee = ""
                        cur_page -= 1    
                        x -= 10
                        y -= 10
                        
                        for name,idd in zip(titles[x:y],animeid[x:y]):
                            namee += f'{titles.index(name)+1}. {name} - `{idd}`\n\n'
                        emb = discord.Embed(title = "Airing Animes:",description = namee,color=0x00ebff)
                        emb.set_footer(text = f"{cur_page}/{pages}")
                        await message.edit(embed = emb)
                except asyncio.TimeoutError:
                    return               

@client.command(name='awl',aliases=["addwatchlist"])
async def addwatchlist(ctx, code):  
    userid = ctx.author.id
    
    docs = airingg.find_one({"_id": code})
    if docs != None:
        doc = listed.find_one({"_id": userid})  
        if doc == None:
            listed.insert_one({"_id": userid,"watchlist" : [],"toggle" : 1})
            listed.update_one({"_id": userid},{"$push":{"watchlist": code}})
            await ctx.reply(f"`{code} - {docs['name']} has been added in watchlist`")
        elif doc != None and len(doc['watchlist']) < 10:
            listed.update_one({"_id": userid},{"$push":{"watchlist": code}})
            await ctx.reply(f"`{code} - {docs['name']} has been added in watchlist`")
        else:
            await ctx.reply("`your watchlist is full, remove any anime to enter new one`")  
    else:
        await ctx.reply("`Cant find the anime, Maybe its not airing right now`\nCheck using `S.airing`")        

@client.command(name='rwl',aliases=["removewatchlist"])
async def removewatchlist(ctx, code):  
    userid = ctx.author.id
    doc = listed.find_one({"_id": userid})  
    if doc == None:
        listed.insert_one({"_id": userid,"watchlist" : [],"toggle" : 1})
        await ctx.reply(f"`your watchlist is already empty`")
    elif doc != None and len(doc['watchlist']) > 0 and code in (doc['watchlist']):
        listed.update_one({"_id": userid},{"$pull":{"watchlist": code}})
        await ctx.reply(f"`{code}` has been removed from your watchlist")
    elif doc != None and len(doc['watchlist']) == 0:
        await ctx.reply("`your watchlist is already empty`")
    else:
        await ctx.reply("`Its not in your watchlist`")

@client.command(name='watchlist',aliases=["Watchlist","wl","Wl"])
@commands.cooldown(2, 80, BucketType.user) 
async def watchlist(ctx,member: discord.Member = None):   
    if member == None:
        member = ctx.author
    userid = member.id
    doc = listed.find_one({"_id": userid})
    if doc != None:
        anime = doc['watchlist']
        rem = doc['toggle']
        if rem == 1:
            rem = 'On'
        elif rem == 0:
            rem = 'Off'    
        name = ""
        slot = 0
        for ani in anime:
            docs = airingg.find_one({"_id": ani})
            if docs == None:
                listed.update_one({"_id": userid},{"$pull":{"watchlist": ani}})
            else:    
                name += f"[{docs['name']}]({docs['url']}) - `{ani}`  \n"
                slot += 1        
        em = discord.Embed(title = "Watchlist",description = f"User : {member.mention}\nAvailable Slots : {slot}/10\nReminder - {rem}\n\n{name}",color=0x00ebff) 
        await ctx.reply(embed = em)
    elif doc == None:
        em = discord.Embed(title = "Watchlist",description = f"User : {member.mention}\nAvailable Slots : 10/10\nReminder - Off\n\nUse `S.awl [animeid]` to add",color=0x00ebff) 
        await ctx.reply(embed = em)     
@client.command(name='remind',aliases=["Remind"])
async def remind(ctx):
    userid = ctx.author.id
    doc = listed.find_one({"_id": userid})
    if doc == None:
        listed.insert_one({"_id": userid,"watchlist" : [],"toggle" : 1})
        await ctx.reply("`Reminder Enabled`")
    elif doc != None:
        if doc["toggle"] == 1:
            listed.update_one({"_id": userid},{"$set":{"toggle": 0}})
            await ctx.reply("`Reminder Disabled`")
        elif doc["toggle"] == 0:  
            listed.update_one({"_id": userid},{"$set":{"toggle": 1}})
            await ctx.reply("`Reminder Enabled`") 
@client.command(name='setchannel')
@commands.has_permissions(manage_guild = True)
async def setchannel(ctx, channel : discord.TextChannel): 
    try:   
        guildid = ctx.guild.id
        doc = chan.find_one({"_id": guildid})
        if doc != None:
            chan.update_one({"_id": guildid},{"$set":{"chnl": channel.id}})
            await ctx.reply(f'{channel.mention} has been set for anime episode reminders!\n`Make sure Stela has permissions to send message there`')
        elif doc == None:
            post = {'_id' : guildid, 'chnl' : channel.id}
            chan.insert_one(post)
            await ctx.reply(f'{channel.mention} has been set for anime episode reminders!\n`Make sure Stela has permissions to send message there`')
        else:
            await ctx.reply('Something went wrong... join support server for help')
    except:
        return                    
           
@client.command(name='removechannel')
@commands.has_permissions(manage_guild = True)
async def removechannel(ctx): 
    try:   
        guildid = ctx.guild.id
        doc = chan.find_one({"_id": guildid})
        if doc != None:
            chal = doc['chnl']
            channel = client.get_channel(chal)
            chan.delete_one({"_id": guildid})
            await ctx.reply(f'{channel.mention} has been removed for anime episode reminders!')
        elif doc == None:
            await ctx.reply(f"This server does'nt have a anime reminder channel\n`Set it using `S.setchannel <mention channel>")
        else:
            await ctx.reply('Something went wrong... join support server for help')
    except:
        return            
@client.command(name='invite',aliases=["Invite"])
async def invite(ctx): 
    em = discord.Embed(description = '[Click here to invite me :)](https://discord.com/api/oauth2/authorize?client_id=782005398269984819&permissions=1346890870&scope=bot)',color=0x00ebff)
    em.set_thumbnail(url = client.user.avatar_url )
    await ctx.reply(embed = em)           
        
@client.command(name='vote',aliases=["Vote"])
async def vote(ctx): 
    await ctx.reply('https://top.gg/bot/782005398269984819/vote')    


#help...............................
client.remove_command("help")
@client.group(invoke_without_command=True)#<> required [] optional
async def help(ctx):
    em = discord.Embed(description = "For more info on a specific command, use stela help <command>\nFor more help, join our [server](https://discord.gg/ZbemgbQuXa)\n \nFor arguments in commands:\n<> means it's required\n[] means it's optional\n||Do not actually include the <> and [] symbols in the command||",timestamp=datetime.datetime.utcnow(),color = discord.Color(0x00ff7d))
    em.set_author(name = "Help/Command List",icon_url=f"{client.user.avatar_url}")
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
    em = discord.Embed(description="Kicks a member from the Server",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.kick <member> [reason]`")
    em.add_field(name="**Permission required**",value="`Kick Member`")
    await ctx.send(embed=em)

@help.command()
async def submit(ctx):
    em = discord.Embed(description="Submits your contestant for the Tournament",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.submit <name>`\nafter that Send the link of the image within 20 sec\nThis command will only work in Tournament\nOnly works in support server")
    await ctx.send(embed=em)

@help.command()
async def ban(ctx):
    em = discord.Embed(description="Bans a member from the Server",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.ban <member> [reason]`")
    em.add_field(name="**Permission required**",value="`Ban Member`")
    await ctx.send(embed=em)

@help.command()
async def clear(ctx):
    em = discord.Embed(description="Deletes messages",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.clear <Number of Msgs>`")
    em.add_field(name="**Aliases**",value="`Clean` `delete` `purge`")
    em.add_field(name="**Permission required**",value="`Manage Messages`")
    await ctx.send(embed=em)

@help.command()
async def wanted(ctx):
    em = discord.Embed(description="Creates a Wanted poster from One Piece",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.wanted <member>`")
    em.add_field(name="**Aliases**",value="`bounty`")
    await ctx.send(embed=em)

@help.command()
async def jojo(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.jojo <member>`")
    await ctx.send(embed=em)   

@help.command()
async def chika(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.chika <message1>|<message2>|<message3>|<message4>`")
    await ctx.send(embed=em)

@help.command()
async def fbi(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.fbi <Text Message>`")
    await ctx.send(embed=em)
@help.command()
async def worthless(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.worthless <Text Message>`")
    await ctx.send(embed=em)

@help.command()
async def water(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.water [member] <Text Message>`")
    await ctx.send(embed=em)

@help.command()
async def rip(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.rip <member>`")
    await ctx.send(embed=em)

@help.command()
async def disability(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.disability <member>`")
    await ctx.send(embed=em)

@help.command()
async def thisisshit(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.thisisshit <member>`")
    await ctx.send(embed=em)

@help.command()
async def myboi(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.myboi <member>`")
    await ctx.send(embed=em)
 
@help.command()
async def santa(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.santa <Text Message>`")
    await ctx.send(embed=em) 

@help.command()
async def news(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.news <member> <message1>|<message2>`")
    await ctx.send(embed=em)

@help.command()
async def yugioh(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.yugioh <message1>|<message2>`")
    await ctx.send(embed=em)

@help.command()
async def yugiohpfp(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.yugiohpfp <member1> <member2>`")
    await ctx.send(embed=em)

@help.command()
async def bitch(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.bitch <Text message>`")
    await ctx.send(embed=em)

@help.command()
async def billy(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.bily <Text message>`")
    await ctx.send(embed=em)

@help.command()
async def fact(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.fact <Text message>`")
    await ctx.send(embed=em)

@help.command()
async def say(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.say <Text message>`")
    await ctx.send(embed=em)

@help.command()
async def spoiler(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.spoiler <Text message>`")
    em.add_field(name="**Aliases**",value="`spoil`")
    await ctx.send(embed=em)

@help.command()
async def propose(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.propose <member>`")
    await ctx.send(embed=em)


@help.command()
async def match(ctx):
    em = discord.Embed(description="Use it to match pfp with your friend",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.match <member>`")
    await ctx.send(embed=em)

@help.command()
async def dumb(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.dumb <text>`")
    await ctx.send(embed=em)  
@help.command()
async def wallpunch(ctx):
    em = discord.Embed(color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.wallpunch <text>`")
    await ctx.send(embed=em)      
@help.command()
async def anime(ctx):
    em = discord.Embed(description="Searches anime on Mal",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.anime <Name of anime>`")
    await ctx.send(embed=em)

@help.command()
async def manga(ctx):
    em = discord.Embed(description="Searches manga on Mal",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.manga <Number of Msgs>`")
    await ctx.send(embed=em)

#@help.command()
#async def dm(ctx):
 #   em = discord.Embed(description="Dms the message to the member",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
 #   em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
 #   em.set_footer(text= f'Requested by {ctx.author}' )
 #   em.add_field(name="**Usage**",value="`S.dm <member> <Text message`")
 #   em.add_field(name="**Permission required**",value="`Manage Server`")
 #   await ctx.send(embed=em)



@help.command()
async def announce(ctx):
    em = discord.Embed(description="Use it to do announcement",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.announce <everyone or here> <channel> <Text message>`")
    em.add_field(name="**Permission required**",value="`Manage Server`")
    await ctx.send(embed=em)

@help.command()
async def yt(ctx):
    em = discord.Embed(description="Searches video on Youtube",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.yt <search>`")
    await ctx.send(embed=em)

@help.command()
async def embed(ctx):
    em = discord.Embed(description="Use to create Embeds",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.embed [hexcode of color] <Text message>`")
    em.add_field(name="**Permission required**",value="`Manage Messages`")
    await ctx.send(embed=em)

@help.command()
async def rndqoute(ctx):
    em = discord.Embed(description="Sends a random anime qoute",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.rndqoute`")
    em.add_field(name="**Aliases**",value="`rq`")
    await ctx.send(embed=em)
@help.command()
async def rand(ctx):
    em = discord.Embed(description="Choose random number between the limits",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.rand <number>`")
    em.add_field(name="**Aliases**",value="`random`")
    await ctx.send(embed=em)
@help.command()
async def filler(ctx):
    em = discord.Embed(description="Sends filler episodes of anime, if any",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.filler <Anime>`")
    em.add_field(name="**Aliases**",value="`fill`")
    await ctx.send(embed=em)    

@help.command()
async def mal(ctx):
    em = discord.Embed(description="Use to check mal profile",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.mal <mal id>`")
    em.add_field(name="**Aliases**",value="`profile`")
    await ctx.send(embed=em)  

@help.command()
async def profile(ctx):
    em = discord.Embed(description="Use to see mal profile",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.profile`\nUse `S.set <mal-id>` to register")
    await ctx.send(embed=em)  

@help.command()
async def read(ctx):
    em = discord.Embed(description="Get link to read manga",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.read <Manga>`")
    await ctx.send(embed=em)

@help.command()
async def char(ctx):
    em = discord.Embed(description="Search Characters",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.char <Character Name>`")
    await ctx.send(embed=em)

@help.command()
async def eplist(ctx):
    em = discord.Embed(description="Sends the episode list of anime",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.eplist <Anime>`")
    
    await ctx.send(embed=em)  

@help.command()
async def wallpaper(ctx):
    em = discord.Embed(description="Sends Wallpapers",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.wallpaper [topic]` \n`S.mwallpaper [topic]` for mobile")
    em.add_field(name="**Aliases**",value="`wall`\n`mwall` for mobile")
    await ctx.send(embed=em)    

@help.command()
async def character(ctx):
    em = discord.Embed(description="Searchs Anime Characters",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.character <name>`")
    em.add_field(name="**Aliases**",value="`char`")
    await ctx.send(embed=em)
@help.command()
async def reddit(ctx):
    em = discord.Embed(description="Sends Sub-reddit posts",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.reddit <sub-reddit>`")
    em.add_field(name="**Aliases**",value="`red`")
    await ctx.send(embed=em)
@help.command()
async def addemoji(ctx):
    em = discord.Embed(description="Adds emoji in the server",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.addemoji <emoji link> [emoji name]`")
    em.add_field(name="**Permission required**",value="`Manage Emojis`")
    await ctx.send(embed=em)
@help.command()
async def challenge(ctx):
    em = discord.Embed(description="A trivia based chase game",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.challenge <mention>`")
    
    await ctx.send(embed=em)  
@help.command()
async def movie(ctx):
    em = discord.Embed(description="Searches movies/web series",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.movie <name>`")
    
    await ctx.send(embed=em)        

@help.command()
async def remind(ctx):
    em = discord.Embed(description="Toggles anime reminder",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.remind`")
    
    await ctx.send(embed=em)
@help.command()
async def addwatchlist(ctx):
    em = discord.Embed(description="Adds anime in your watchlist for reminder",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.addwatchlist <anime id>`")
    em.add_field(name="**Aliases**",value="`awl`")
    await ctx.send(embed=em) 
@help.command()
async def removewatchlist(ctx):
    em = discord.Embed(description="Removes anime from your watchlist for reminder",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.removewatchlist <anime id>`")
    em.add_field(name="**Aliases**",value="`rwl`")
    await ctx.send(embed=em) 

@help.command()
async def watchlist(ctx):
    em = discord.Embed(description="Shows anime in your watchlist for reminder",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.watchlist`")
    em.add_field(name="**Aliases**",value="`wl`")
    await ctx.send(embed=em)
@help.command()
async def airing(ctx):
    em = discord.Embed(description="Shows airing anime to add in your Watchlist",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.airing`")
    em.add_field(name="**Aliases**",value="`air`")
    await ctx.send(embed=em)   
@help.command()
async def setmal(ctx):
    em = discord.Embed(description="Tags your myanimelist account with your discord id",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.setmal <myanimelist id>`")
    await ctx.send(embed=em) 
@help.command()
async def removemal(ctx):
    em = discord.Embed(description="Removes your mal id from stela",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.removemal`")
    await ctx.send(embed=em)   

@help.command()
async def lookup(ctx):
    em = discord.Embed(description="Search waifus for waifu command",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.Lookup <name>`")
    em.add_field(name="**Aliases**",value="`lu`")
    await ctx.send(embed=em)        
@help.command()
async def setchannel(ctx):
    em = discord.Embed(description="Set a channel for anime updates in your server",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.setchannel <mention channel>`")
    em.add_field(name="**Permission required**",value="`Manage Server`")
    await ctx.send(embed=em)
@help.command()
async def removechannel(ctx):
    em = discord.Embed(description="Removes the channel from anime updates in your server",color=0x00ff7d,timestamp=datetime.datetime.utcnow())
    em.set_author(name=ctx.author.name,icon_url=f"{ctx.author.avatar_url}")
    em.set_footer(text= f'Requested by {ctx.author}' )
    em.add_field(name="**Usage**",value="`S.removechannel`")
    em.add_field(name="**Permission required**",value="`Manage Server`")
    await ctx.send(embed=em)                     
# run the client on the server
client.run('NzgyMDA1Mzk4MjY5OTg0ODE5.X8F5Rw.1sl5xrh9uoyW-uUZHo3kYpk-4pM')
