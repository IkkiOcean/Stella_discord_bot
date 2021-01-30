import discord #pip install discord
from discord.ext import commands
from discord.ext.commands import BucketType, Greedy
import requests #requests
from discord.errors import Forbidden
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
from waifu import waifupics, waifuname, waifuseries

os.chdir(r".vscode")
# client (our bot)
#prefix...................]
intents = discord.Intents.all()
#client = commands.Bot(command_prefix='.', intents = intents)

client = commands.Bot(command_prefix = ('stela ','S.','Stela '), intents = intents)
#@client.event 
#async def on_message(message):
    #if message.content.startswith(f'{client.user.mention}'):
       #await message.channel.send(f'The prefix is{client.command_prefix}')
    
#{} means its required
#() means its optional
 
               


#error.................
@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You are too weak!;-; Work hard and get powers to do that :)")
    elif isinstance(error,Forbidden):
        await ctx.send("Give me powers to do that! I will not disappoint you")   
    elif isinstance(error,commands.CommandOnCooldown):
        await ctx.send(f" You have to wait {error.retry_after:,.2F} secs ¯\_(ツ)_/¯")     
    else:
        raise error       


    


# do stuff......
@client.event
async def on_ready():
    #status
    await client.change_presence(activity=discord.Streaming(name=' in Anime Ocean | use S. or Stela ',url=('https://discord.gg/H7MDM37')))

    #welcome 
    general_channel = client.get_channel(772496570436419592)

    await general_channel.send('Hello Master')
    print("bot is online")
    

#commands...................................................


@client.command(name='version')
async def version(context):
    myembed = discord.Embed(title='Current Version', description='The Bot is in version 1.0.0',color=0x00ebff)
    myid = '<@!745006368175423489>'
    helper1 = '<@!741967836422996008>'
    
    myembed.add_field(name= "**Developer**", value= myid )
    myembed.add_field(name= "**Helpers**",value= helper1)
    
    await context.message.channel.send(embed=myembed)

@client.command(name='Bot')   
async def Bot(context):
    helpembed = discord.Embed (title='Hi', description='Aur bhai kaisa laga bot',color=0x00ebff) 
    await context.author.send(embed=helpembed) 

#moderation.................................................................................... 
#kick...............
@client.command(name='kick',pass_context = True)    
@commands.has_permissions(kick_members=True)
async def kick(context, member : discord.Member, *,reason = None):
    
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
    
    

#ban.....................    
@client.command(name='ban',pass_context = True)    
@commands.has_permissions(ban_members=True)
async def ban(context, member : discord.Member, *,reason=None):
    
    
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


#clear.....
@client.command(name="clear",aliases=["Clear",'Clean','clean','delete','Delete'])    
@commands.has_permissions(manage_messages = True)
async def clear(context,amount=2):
    await context.channel.purge(limit = (amount+1))
    await context.send(f"`{amount} messages has been Deleted... 👍`",delete_after = 10)

#mute
    
 
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
    resp=requests.get("https://cdn.discordapp.com/attachments/782562061812891648/784300226537324564/Wanted.png") 
    
    wanted = Image.open(BytesIO(resp.content))
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())   
    pfp = Image.open(data)
    pfp = pfp.resize((385,261))
    wanted.paste(pfp,(57,153))
    font = ImageFont.truetype(font=BytesIO(open(".vscode/luffyfont.ttf", "rb").read())), 60)        
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
    font = ImageFont.truetype(font=BytesIO(open(".vscode/luffyfont.ttf", "rb").read())), 70)
    draw.text((102,534),bount,(93,63,51),font=font)
    wanted.save("wanted.png")
    
    if len(text1)>19:
        await ctx.send("Hey! Your name is longer than 19 Characters \n**Tip**: Keep it shorter :) ")
    await ctx.send(file=discord.File("wanted.png"))

@client.command(name='instagram', aliases=['insta','Insta','Instagram'])
async def instagram(ctx,user:typing.Optional[discord.Member]=None, *,caption= None):
    if user==None:
        user = ctx.author
    resp=requests.get("https://cdn.discordapp.com/attachments/782562061812891648/798163684589305916/instagramtemplate.png") 
    
    post = Image.open(BytesIO(resp.content))
    asset = user.avatar_url
    data = BytesIO(await asset.read())   
    pfp = Image.open(data)
    pfp = pfp.resize((322,313))
    post.paste(pfp,(19,54))
    font = ImageFont.truetype(font=BytesIO(open(".vscode/ARIAL.TTF", "rb").read())), 15)        
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

        

#REACTION_ROLES.....................................................................
reaction_title = ""
reactions = {}
#imagelink = ""
reaction_message_id= ""
@client.command(name='create_reactionroles',pass_context = True)    
@commands.has_permissions(manage_guild=True)
async def create_reactionroles(context):
    embed=discord.Embed(title="Create Reaction Post", color=0x00ebff)
    embed.set_author(name=f'{client.user}' ,icon_url=f'{client.user.avatar_url}')
    embed.add_field(name='Set Title', value= "`set_title [Title]`",inline=False)
    embed.add_field(name='Add Role', value='`add_role {@role} {Emoji}`',inline=False)
    embed.add_field(name='Remove Role', value='`remove_role {@role}`',inline=False)
    #embed.add_field(name='Add Image', value= "`add_image {link}`",inline=False)
    await context.send(embed=embed)
    await context.message.delete()

@client.command(name='set_title',pass_context = True)    
@commands.has_permissions(manage_guild=True)  
async def set_title(context, *,new_title):
    global reaction_title 
    reaction_title = new_title
    await context.send("The title for the Reaction Role Embed is `" + reaction_title + " `now!!")
    await context.message.delete()

@client.command(name='add_role',pass_context = True)    
@commands.has_permissions(manage_guild=True)
async def add_role(context, role: discord.Role, reaction ):
       
    if role != None:
        reactions[role.name] = reaction
        await context.send("Role `" + role.name + "` has been **added** with the emoji"+ reaction)
        await context.message.delete()
    else:
        await context.send("Please try again and add role")

@client.command(name='remove_role',pass_context = True)    
@commands.has_permissions(manage_guild=True)
async def remove_role(context, role: discord.Role):
    if role.name in reactions:
        del reactions[role.name]
        await context.send("Role `" + role.name + "` has been **removed**")
        await context.message.delete()
    else:
        await context.send("That role was not added")


#@client.command(name='add_image')
#async def add_image(context, image):
    #imagelink = image
    #await context.send('Image has been **added**')
    #await context.message.delete()

@client.command(name='send_post',pass_context = True)    
@commands.has_permissions(manage_guild=True)
async def send_post(context):
    
    description = 'React To get Roles!\n'

    for role in reactions:
        description += '`' + role + "`  -  " + reactions[role] + '\n'

    embed = discord.Embed(title=reaction_title, description=description, color=0x00ebff) 
    embed.set_author(name=f'{client.user}' ,icon_url=f'{client.user.avatar_url}')
    #embed.set_image(url=imagelink)


    message = await context.send(embed=embed)   

    global reaction_message_id
    reaction_message_id = str(message.id)

    for role in reactions:
        await message.add_reaction(reactions[role])

    await context.message.delete()  


@client.event
async def on_reaction_add(reaction, user):   

    if not user.bot:

        message = reaction.message

        if str(message.id) == reaction_message_id:

            #add roles to our userss...

            role_to_give = ""

            for role in reactions:

                if reactions[role] == reaction.emoji:
                    role_to_give = role

            role_for_reaction = discord.utils.get(user.guild.roles, name=role_to_give)
            await user.add_roles(role_for_reaction)

#message................

#dm
@client.command(name='dm',pass_context = True)    
@commands.has_permissions(manage_guild=True)
async def dm(context, member : discord.Member, *,msg):
    
    await member.send("**" + msg + "**")
    await context.message.delete()
#say
@client.command(name='say',aliases = ["Say","Type","type"])
@commands.cooldown(2, 120, BucketType.user)
async def say(context, *,msg = None):
    if msg == None:
        return
    else:
        await context.send(msg)
        await context.message.delete()
#spoiler
@client.command(name='Spoiler',aliases = ["spoiler","Spoil","spoil"])
@commands.cooldown(2, 120, BucketType.user)
async def Spoiler(context, *,msg = None):
    if msg == None:
        return
    else:
        await context.send("||"+msg+ "||")
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
    await context.send(f"{member.mention}, {context.author.mention} proposed you for the marraige!! Do you accept?? \nType accept or reject")
    def check(response):
        return response.content.lower() in ["accept","reject"] and response.author == member and response.channel == context.channel
    
    try:
        
        response= await client.wait_for('message', check= check, timeout= 40)
        
        if "accept" in response.content.lower():
            resp=requests.get("https://cdn.discordapp.com/attachments/754740569552715817/804413355543494726/shipbot-min.png") 
            resp2=requests.get("https://cdn.discordapp.com/attachments/754740569552715817/804416481814773820/background.png")
            
            
            marraige = Image.open(BytesIO(resp.content)).convert('RGBA')
            
            bg = Image.open(BytesIO(resp2.content)).convert('RGB')
            asset = context.author.avatar_url_as(size=128)
            asset2 = member.avatar_url_as(size=128)
            data = BytesIO(await asset.read())  
            data2 = BytesIO(await asset2.read())  
            pfp = Image.open(data)
            waifu0 = Image.open(data2)

            pfp = pfp.resize((493,483))
            waifu1 =  waifu0.resize((493,483))
            
            bg.paste(pfp,(85,71))
            
            bg.paste(waifu1,(1295,61))
            bg.paste(marraige,(0,0),mask=marraige)
             
            bg.save("marraige.png",format="png")
            wed = discord.Embed(description=f"{context.author.name} and {member.name} are **married** now!!💝",timestamp=datetime.datetime.utcnow() ,color=0x00ebff)
            file = discord.File("marraige.png")
            wed.set_image(url="attachment://marraige.png")
            await context.send(file = file, embed=wed)

        if "reject" in response.content.lower():
            await context.send(f"{context.message.author.mention} You got rejected... ;-;")   

    except asyncio.TimeoutError:
        await context.send(f"{context.author.mention} {member.name} didn't reply. ;-;")       



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
    imps.set_image(url='https://cdn.discordapp.com/attachments/782562061812891648/783657342691967026/amoung_us.jpg')
    await context.send(embed=imps)



#Economy.................................................

#currency = ""
#@client.command(name='set_symbol',pass_context = True)    
#@commands.has_permissions(manage_guild=True)
#async def set_symbol(context, currency ):
 #   em =discord.Embed(description = f"Currency has been set to {currency}", timestamp=datetime.datetime.utcnow(),color =0x00ebff)
  #  em.set_author(name = f"{context.author.name} ",icon_url=f"{context.guild.icon_url} ")
   # await context.send(embed =em)
mainshop = [{"name":"Death Note","price":1000,"description":"It's a Death Note\n"},
            {"name":"3D Maneuver Gear","price":10000,"description":"Swords and gear From Attack On Titan\n"},
            {"name":"Grimoire","price":10000,"description":"TBook of Magic"}]


@client.command(name='balance',aliases = ["Balance","Bal","bal"])
async def balance(ctx, *, member: discord.Member = None):
    if member == None:
        
        await open_account(ctx.author)

        user = ctx.author
    
        users = await get_bank_data()

        wallet_amt = users[str(user.id)] ["wallet"]
        bank_amt= users[str(user.id)] ["bank"]
        net_worth= wallet_amt + bank_amt

        em =discord.Embed(timestamp=datetime.datetime.utcnow(),color =0x00ebff)
        em.set_author(name = f"{ctx.author.name} ",icon_url=f"{ctx.message.author.avatar_url}")
        em.add_field(name="Cash", value = f"{wallet_amt} :money_with_wings:" )
        em.add_field(name="Bank", value = f"{bank_amt} :money_with_wings:")
        em.add_field(name="Net Worth", value = f"{net_worth} :money_with_wings:")
        await ctx.send(embed = em)

    else:
        await open_account(member)

        user = member
    
        users = await get_bank_data()

        wallet_amt = users[str(user.id)] ["wallet"]
        bank_amt= users[str(user.id)] ["bank"]
        net_worth= wallet_amt + bank_amt

        em =discord.Embed(timestamp=datetime.datetime.utcnow(),color = discord.Color(0xfa43ee))
        em.set_author(name = f"{member.name} ",icon_url=f"{member.avatar_url}")
        em.add_field(name="Cash", value = f"{wallet_amt} :money_with_wings:" )
        em.add_field(name="Bank", value = f"{bank_amt} :money_with_wings:")
        em.add_field(name="Net Worth", value = f"{net_worth} :money_with_wings:")
        await ctx.send(embed = em)




@client.command(name= 'beg',aliases = ["Beg"])
@commands.cooldown(2, 120, BucketType.user)

async def beg(ctx):
    await open_account(ctx.author)

    user = ctx.author
    
    users = await get_bank_data()

    earnings = random.randrange(101)

    await ctx.send(f"Someone gave you {earnings} :money_with_wings:!!") #have to make emote system like reaction roles

    users[str(user.id)]['wallet'] += earnings

    with open('bank.json',"w") as f:
        json.dump(users,f) 

        

                
                

       

@client.command(name= 'withdraw', aliases= ['with','With','Withdraw'])
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send('Atleast , Tell me how much to withdraw!')
        return

    bal = await update_bank(ctx.author) 
    if amount == "all":
        amount = bal[1]
    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("You don't have that much **money** ;-;")   
        return
    if amount<0:
        await ctx.send("How can I withdraw something, which does'nt exist! dummyyy.....")  
        return  

    await update_bank(ctx.author,amount) 
    await update_bank(ctx.author,-1*amount,"bank") 
    em =discord.Embed(description = f"Withdrew {amount} :money_with_wings: from your bank! ",timestamp=datetime.datetime.utcnow(),color = discord.Color(0xfa43ee))
    em.set_author(name = f"{ctx.author.name} ",icon_url=f"{ctx.message.author.avatar_url}") 

    await ctx.send(embed = em) 

@client.command(name= 'deposit', aliases= ['Deposit','Dep','dep'])
async def deposit(ctx, amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send('Atleast , Tell me how much to Deposit!')
        return

    bal = await update_bank(ctx.author) 
    if amount == "all":
        amount = bal[0]
    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("You don't have that much **money** ;-;")   
        return
    if amount<=0:
        await ctx.send("You need Cash for that... :-(")
        return
    await update_bank(ctx.author,-1*amount) 
    await update_bank(ctx.author,amount,"bank") 

    em =discord.Embed(description = f"Deposited  {amount} :money_with_wings: in your bank! ",timestamp=datetime.datetime.utcnow(),color = discord.Color(0xfa43ee))
    em.set_author(name = f"{ctx.author.name} ",icon_url=f"{ctx.message.author.avatar_url}") 

    await ctx.send(embed = em)  

    
     

    

#sendmoney...
@client.command(name= 'give', aliases= ['send','Give','Send'])
async def give(ctx, member: discord.Member, amount = None):
    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
        await ctx.send('Atleast , Tell me how much to Send!')
        return

    bal = await update_bank(ctx.author) 
    if amount == "all":
        amount = bal[0]
    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("You don't have that much **money** ;-;")   
        return
    if amount<0:
        return
    await update_bank(ctx.author,-1*amount,"wallet") 
    await update_bank(member,amount,"wallet") 

    em =discord.Embed(description = f"{member.display_name} recieved your {amount} :money_with_wings: ",timestamp=datetime.datetime.utcnow(),color = discord.Color(0xfa43ee))
    em.set_author(name = f"{ctx.author.name} ",icon_url=f"{ctx.message.author.avatar_url}") 

    await ctx.send(embed = em)    

#slots....
@client.command(name= 'slot', aliases= ['Slots','Slot','slots'])
async def slots(ctx, amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send('Hehe! Tell me how much to **bet**...')
        return

    bal = await update_bank(ctx.author) 
    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("You don't have that much **money** ;-;")   
        return
    if amount<0:
        return    
    upper = []
    final = []
    lower = []        
    for i in range(3):
        a = random.choice([":peach:",":star2:",":black_joker:"])
        b = random.choice([":peach:",":star2:",":black_joker:"])
        c = random.choice([":peach:",":star2:",":black_joker:"])
        final.append(a)
        upper.append(b)
        lower.append(c)
    
    if final[0] == final[1] and final[0] == final[2] and final[2] == final[1]:
        await update_bank(ctx.author,2*amount)
        em =discord.Embed(description = f"You won {amount} :money_with_wings: ",timestamp=datetime.datetime.utcnow(),color = discord.Color(0xfa43ee))
        em.add_field(name = "result:",value = f"{upper[0]} | {upper[1]} | {upper[2]}\n{final[0]} | {final[1]} | {final[2]}    :arrow_left:\n{lower[0]} | {lower[1]} | {lower[2]}")
        em.set_author(name = f"{ctx.author.name} ",icon_url=f"{ctx.message.author.avatar_url}")

        await ctx.send(embed= em)
    else:
        await update_bank(ctx.author,-1*amount)
        em =discord.Embed(description = f"You lost {amount} :money_with_wings: ",timestamp=datetime.datetime.utcnow(),color = discord.Color(0xfa43ee))
        em.add_field(name = "result:",value = f"{upper[0]} | {upper[1]} | {upper[2]}\n{final[0]} | {final[1]} | {final[2]}    :arrow_left:\n{lower[0]} | {lower[1]} | {lower[2]}")
        em.set_author(name = f"{ctx.author.name} ",icon_url=f"{ctx.message.author.avatar_url}")  
        await ctx.send(embed= em)

#rob.......
@client.command(name= 'rob', aliases= ['Rob','Snatch','snatch'])
async def rob(ctx, member: discord.Member):
    await open_account(ctx.author)
    await open_account(member)


    bal = await update_bank(member) 
    
    if bal[0]<100:
        await ctx.send("Hey! Don't rob a poor person ;-;")   
        return

    listd = ("a","b")   
    earnings = random.randrange(0,bal[0])
    robs = random.choice(listd)    
    if robs == "a":

        await update_bank(ctx.author,earnings,"wallet") 
        await update_bank(member,-1*earnings,"wallet") 

        em =discord.Embed(description = f"Hehe! You robbed {earnings} :money_with_wings: from {member.display_name}",timestamp=datetime.datetime.utcnow(),color = discord.Color(0xfa43ee))
        em.set_author(name = f"{ctx.author.name} ",icon_url=f"{ctx.message.author.avatar_url}") 

          

    else: 
        await update_bank(ctx.author,-1*earnings,"wallet") 
        

        em =discord.Embed(description = f"Shit! You were caught attempting to rob {member.display_name} and have been fined {earnings} :money_with_wings: ;-; ",timestamp=datetime.datetime.utcnow(),color = discord.Color(0xfa43ee))
        em.set_author(name = f"{ctx.author.name} ",icon_url=f"{ctx.message.author.avatar_url}") 

    await ctx.send(embed = em)

#shop.................



@client.command(name="shop")
async def shop(ctx):
    em = discord.Embed(title = "Shop",timestamp=datetime.datetime.utcnow(),color = discord.Color(0xfa43ee))

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f":money_with_wings:{price} \n {desc}")
        em.set_author(name= f"{ctx.guild.name}" , icon_url=f"{ctx.guild.icon_url}")

    await ctx.send(embed = em)

@client.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return


    await ctx.send(f"You just bought {amount} {item}")

#use deathnote
@client.command(name= 'kira',aliases = ["Kira"])
@commands.cooldown(2, 120, BucketType.user)

async def kira(ctx):
    await open_account(ctx.author)

    user = ctx.author
    
    users = await get_bank_data()
    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []
    try:
        for thing in bag:
            n = thing["item"]
            amt = thing["amount"]
            if n == "death note" and amt >=1:
                
                earnings = random.randrange(500)
                users[str(user.id)]['wallet'] += earnings
                kira = discord.Embed(timestamp=datetime.datetime.utcnow(),color= 0x990000)
                kira.set_author(name = f"{ctx.author.name} ",icon_url=f"{ctx.message.author.avatar_url}") 
                line1 = f"You killed your friend (if you have any🙃) with Death Note and Earned {earnings} :money_with_wings:!! **MONSTER**"
                line2 = f'You killed Naruto with Death Note because he was screaming "Datebbayo" and Earned {earnings} :money_with_wings:!! Believe it'
                line3 = f'You killed your neighbour with Death Note because he was staring your waifu and Earned {earnings} :money_with_wings:!!'
                line4 = f'You killed Ryuuk (but why? how? can you?🙃) with Death Note and Earned {earnings} :money_with_wings:!!'
                line5 = f'You killed someone with Death Note and Earned {earnings} :money_with_wings:!!'
                linelist = (line1,line2,line3,line4,line5)
                kiraline = random.choice(linelist)
                kira.add_field(name= "✍️ Kira", value=f"{kiraline}" )
                kiragif = ('https://cdn.discordapp.com/attachments/782562061812891648/792763328639533076/kira5.gif','https://cdn.discordapp.com/attachments/782562061812891648/792763323456028733/kira4.gif','https://cdn.discordapp.com/attachments/782562061812891648/792763320917819392/kira3.gif','https://cdn.discordapp.com/attachments/782562061812891648/792763318284189716/kira2.gif',"https://cdn.discordapp.com/attachments/782562061812891648/792763314992054282/kira1.gif")
                rndkira = random.choice(kiragif)
                kira.set_thumbnail(url=rndkira)
                await ctx.send(embed= kira)
                
            if n == "death note" and amt < 1:
                await ctx.send("Buy one Death Note")
            
    except:
        await ctx.send("Buy Death Note")            
        
                    
    with open('bank.json',"w") as f:
       json.dump(users,f)
    
#aot

@client.command(name="inventory",aliases=['bag','inv','Inv','Bag'])
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = "Bag",color = discord.Color(0xfa43ee))
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)
        
    
                
    if amount == None:
        await ctx.send("you have nothing")
    else:    
        await ctx.send(embed = em)    

async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("bank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]    

@client.command(name="sell")
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    await ctx.send(f"You just sold {amount} {item}.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("bank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]


#lb.......
@client.command(name="leaderboard",aliases = ["lb"])
async def leaderboard(ctx,x = 10):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = await client.fetch_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f":money_with_wings: {amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)    
        
async def open_account(user):
    
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)] ["wallet"] = 0
        users[str(user.id)] ["bank"] = 0

    with open('bank.json',"w") as f:
        json.dump(users,f)   
    return True  


async def get_bank_data():
    with open("bank.json","r") as f:
        users = json.load(f)    

    return users
    #withdraw....
async def update_bank(user,change = 0,mode = "wallet"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open('bank.json',"w") as f:
        json.dump(users,f)       
    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal  
#MyAnimeList
#animesearch
@client.command(name= "anime",aliases = ["Anime"])
async def anime(ctx, *, anime):
    from mal import AnimeSearch
    search = AnimeSearch(anime) 
    AAnime= Anime(search.results[0].mal_id)
    mal = discord.Embed(description=f'**[{search.results[0].title}]({search.results[0].url})** \n{AAnime.synopsis}',timestamp=datetime.datetime.utcnow(),color=0xff0092)
    mal.add_field(name="**⌛ Status**",value= AAnime.status,inline=False)
    mal.add_field(name="**📺 Total Episodes**",value= AAnime.episodes,inline=True)
    mal.add_field(name="**📡 Aired**",value= AAnime.aired,inline=True)
    mal.add_field(name="**💻 Type**",value= AAnime.type,inline=True)
    mal.add_field(name="**🎬 Genre**",value= AAnime.genres,inline=False)
    mal.add_field(name="**⭐ Rating**",value= f'{AAnime.score}/10',inline=True )
    mal.add_field(name="**🎖️ Rank**",value= f'**Top {AAnime.rank}**',inline=False)
    mal.set_footer(text= f'Requested by {ctx.author}' )
    mal.set_thumbnail(url=AAnime.image_url)

    await ctx.send(embed = mal)
#manga search
@client.command(name= "manga",aliases = ["Manga"])
async def manga(ctx, *, manga):
    from mal import MangaSearch
    search = MangaSearch(manga) 
    AManga= Manga(search.results[0].mal_id)
    mal = discord.Embed(description=f'**[{search.results[0].title}]({search.results[0].url})** \n{AManga.synopsis}',timestamp=datetime.datetime.utcnow(),color=0xff0092)
    mal.add_field(name="**⌛ Status**",value= AManga.status)          
    mal.add_field(name="**📕 Total Chapters**",value= AManga.chapters)
    mal.add_field(name="**📚 Total Volumes**",value= AManga.volumes)
    mal.add_field(name="**🗓️ Published**",value= AManga.published,inline=True)
    mal.add_field(name="**🎨 Type**",value= AManga.type,inline=True)
    mal.add_field(name="**🎬 Genre**",value= AManga.genres,inline=False)
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


#list.................
@client.command(name='Create_Team')
@commands.has_permissions(manage_guild = True)
async def Create_Team(context, Leader : discord.Member , *, team):
    em = discord.Embed(timestamp=datetime.datetime.utcnow(),color =0x00ebff)
    em.set_author(name= team , icon_url=f"{context.guild.icon_url}")
    em.add_field(name= f"Leader :  {Leader.display_name}",value= "Team has been Created!")

    await context.send( embed = em)

#async def make_team(user):
    
    #users = await get_bank_data()

    #if str(user.id) in users:
        #return False
    #else:
        #users[str(user.id)] = {}
        #users[str(user.id)] ["wallet"] = 0
        #users[str(user.id)] ["bank"] = 0

    #with open('bank.json',"w") as f:
       # json.dump(users,f)   
  #  return True  


#async def get_bank_data():
    #with open("bank.json","r") as f:
        #users = json.load(f)     















import asyncio


@client.command(name='waifu',aliases=["Waifu"]) 
@commands.cooldown(2, 120, BucketType.user)  
async def waifu_(ctx):
    chosen_index = random.randint(0,52) 
    embed=  discord.Embed(title = f"**{waifuname[chosen_index]}**",description= waifuseries[chosen_index],color =0x00ebff)
    embed.set_image(url=waifupics[chosen_index])
    message=await ctx.send(embed=embed)
    
    await message.add_reaction("💗")
    
    def check(reaction, user):
        return str(reaction.emoji) == "💗" and user != client.user and reaction.message.id == message.id

    try:
        reaction, user = await client.wait_for('reaction_add',check=check,timeout=60)

        await ctx.send(f"{user.name} wanna make {waifuname[chosen_index]}, waifu! 💝") 
        choice = ("Yes","No")
        answer = random.choice(choice)    
        if answer == "Yes":
            await asyncio.sleep(5)
            await ctx.send(f"{user.name}\nAwww... {waifuname[chosen_index]} said **Yes** for the marraige!! Congrats💝\nLet me make a wedding card for you >///<")
            resp=requests.get("https://cdn.discordapp.com/attachments/754740569552715817/804413355543494726/shipbot-min.png") 
            resp2=requests.get("https://cdn.discordapp.com/attachments/754740569552715817/804416481814773820/background.png")
            resp3=requests.get(waifupics[chosen_index])
            waifu0 = Image.open(BytesIO(resp3.content))
            marraige = Image.open(BytesIO(resp.content)).convert('RGBA')
            
            bg = Image.open(BytesIO(resp2.content)).convert('RGB')
            asset = user.avatar_url_as(size=128)
            data = BytesIO(await asset.read())   
            pfp = Image.open(data)
            pfp = pfp.resize((493,483))
            waifu1 =  waifu0.resize((493,483))
            
            bg.paste(pfp,(85,71))
            
            bg.paste(waifu1,(1295,61))
            bg.paste(marraige,(0,0),mask=marraige)
            
            bg.save("marraige.png",format="png")
            wed = discord.Embed(description=f"{user.name} and {waifuname[chosen_index]} are **married** now!!💝",timestamp=datetime.datetime.utcnow() ,color=0x00ebff)
            file = discord.File("marraige.png")
            wed.set_image(url="attachment://marraige.png")
            await ctx.send(file = file, embed=wed)
        if answer == "No":
            await asyncio.sleep(5)
            await ctx.send(f"{user.name}\n{waifuname[chosen_index]} said **No** to you.... ;-;")
            
    except asyncio.TimeoutError:
        await ctx.send(f"{user.name}{waifuname[chosen_index]} ran away with someone ;-;")    
         

# run the client on the server
client.run('NzgyMDA1Mzk4MjY5OTg0ODE5.X8F5Rw.RoKqLr0IWKoG20WKpW10g37OZk0')
