from PIL import Image
import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import urllib.parse
import urllib.request
import re
import datetime
import random
import asyncio
from bot_utils import (
    get_driver,
    output_path,
    utc_now,
    BOT_OWNER_ID,
    chan,
    upd,
    animetriv_collect,
    girl
)

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='version')
    async def version(self, ctx):
        myembed = discord.Embed(title='Current Version', description='The Bot is in version 3.0.0', color=0x00ebff)
        myid = '<@!745006368175423489>'
        myembed.add_field(name="**Developer**", value=myid)
        await ctx.send(embed=myembed)

    @commands.command(name='bot', aliases=['Bot'])
    async def bot(self, ctx):
        helpembed = discord.Embed(title='Hi', description='Its me, Stela', color=0x00ebff) 
        try:
            await ctx.author.send(embed=helpembed) 
        except discord.Forbidden:
            await ctx.send("I can't DM you, please open your DMs.")

    @commands.command(name="sync")
    @commands.is_owner()
    async def sync_commands(self, ctx, scope: str = "guild"):
        if scope == "global":
            await ctx.send("Syncing 97 commands globally... This can take up to 1 hour.")
            await self.bot.tree.sync()
            await ctx.send("Global sync payload sent successfully!")
        elif scope == "guild":
            await ctx.send("Syncing commands locally to this server instantly...")
            await self.bot.tree.sync(guild=ctx.guild)
            await ctx.send("Guild sync complete!")

    @commands.hybrid_command(name="announcement", aliases=["announce", "Announce", "Announcement"])
    @commands.has_permissions(manage_guild=True)
    async def announce_everyone(self, ctx, mention, channel: discord.TextChannel, *, msg):
        if mention == "everyone":
            em = discord.Embed(description=msg, timestamp=utc_now(), color=0x00ebff)
            em.set_footer(text=f"announced by {ctx.author}")
            await channel.send("@everyone", embed=em)
        elif mention == "here":
            em = discord.Embed(description=msg, timestamp=utc_now(), color=0x00ebff)
            em.set_footer(text=f"announced by {ctx.author}")
            await channel.send("@here", embed=em)

    @commands.command(name='dm')    
    async def dm(self, ctx, member: discord.Member, *, msg):
        if ctx.author.id == BOT_OWNER_ID:
            await member.send(msg + f"\n\nsent by **{ctx.author}** from **{ctx.guild}** ")

    @commands.hybrid_command(name='avatar', aliases=["pfp", "Pfp", "Avatar"])
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member is None:
            user = ctx.author
        else:
            user = member    
        avatars = discord.Embed(timestamp=utc_now(), color=0x00ebff)  
        avatars.set_author(name=f"{user.name}'s avatar", icon_url=user.display_avatar.url)  
        avatars.set_image(url=user.display_avatar.url)
        await ctx.send(embed=avatars)         

    @commands.hybrid_command(name='movie', aliases=["Movie", "Series", "series"])
    async def movie(self, ctx, *, name):
        name = name.replace(" ", "+")  
        link = f"https://www.imdb.com/find?s=tt&q={name}&ref_=nv_sr_sm"
        r = requests.get(link)
        soup = BeautifulSoup(r.content, features="lxml")
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
        if count == 1:
            await ctx.send("No results found.")
            return

        em = discord.Embed(title="Result:", description=result, color=ctx.author.color)
        message = await ctx.reply(embed=em)
        emoji_numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
        for i in range(count - 1):
            await message.add_reaction(emoji_numbers[i])
        def check(reaction, user):
            return str(reaction.emoji) in emoji_numbers and user != self.bot.user and reaction.message.id == message.id and user == ctx.author
        
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
                index = emoji_numbers.index(reaction.emoji)
                rn = requests.get(f"{linkk[index]}plotsummary?ref_=tt_stry_pl#synopsis")
                soupp = BeautifulSoup(rn.content, features="lxml")
                synop = soupp.find("li", {"class" : "ipl-zebra-list__item"})
                poster = soupp.find("img", {"class" : "poster"})
                synop_text = synop.text if synop else "No plot summary available."
                emb = discord.Embed(title=names[index], description=f"{synop_text}", color=ctx.author.color)
                try:
                    img = f"{poster['src'][0:-24]}.jpg"
                    emb.set_image(url=img)
                except Exception:
                    emb.set_footer(text="No Image Found")
                
                await message.edit(embed=emb)
                try:
                    await message.remove_reaction(reaction, user)
                    for i in range(count - 1):
                        await message.remove_reaction(emoji_numbers[i], self.bot.user) 
                except Exception:
                    pass
            except asyncio.TimeoutError:
                return

    @commands.hybrid_command(name="wallpaper", aliases=["Wallpaper", "wall", "Wall"])
    @commands.cooldown(9, 120, BucketType.user)
    async def wallpaper(self, ctx, *, word = None):
        try:    
            if word is None:
                word = 'anime'
            word = word.replace(" ", "+")
            link = f"https://www.wallpaperflare.com/search?wallpaper={word}"
            r = requests.get(link)
            walls = []
            soup = BeautifulSoup(r.content, features="lxml")
            spans = soup.find_all('img', attrs={"class": "lazy"})
            for span in spans:
                walls.append(span['data-src'])
            if not walls:
                await ctx.reply("Not found")
                return
            wall = random.choice(walls)
            resp = requests.get(wall)
            wallpap = Image.open(BytesIO(resp.content))  
            wallpap.save(output_path('WallpaperForYou.jpg'))
            await ctx.send(file=discord.File(output_path("WallpaperForYou.jpg")))
        except Exception:
            await ctx.reply("Not found")

    @commands.hybrid_command(name="mwallpaper", aliases=["Mwallpaper", "mwall", "Mwall"])
    @commands.cooldown(9, 120, BucketType.user)
    async def wallpaper_mobile(self, ctx, *, word = None):
        try:
            if word is None:
                word = 'anime'
            word = word.replace(" ", "+")
            link = f"https://www.wallpaperflare.com/search?wallpaper={word}&mobile=ok"
            r = requests.get(link)
            soup = BeautifulSoup(r.content, features="lxml")
            spans = soup.find_all('a', attrs={"itemprop": "url"})
            walls = []
            for span in spans:
                walls.append(span.img['data-src'])
            if not walls:
                await ctx.reply("Not found")
                return
            wall = random.choice(walls)
            resp = requests.get(wall)
            wallpap = Image.open(BytesIO(resp.content))  
            wallpap.save(output_path('WallpaperForYou.jpg'))
            await ctx.send(file=discord.File(output_path("WallpaperForYou.jpg")))
        except Exception:
            await ctx.reply("Not found")

    @commands.hybrid_command(name='rand', aliases=["Random", "Rand", "random"])
    async def rndm(self, ctx, number: int):
        try:
            result = random.randint(1, number)      
            await ctx.send(result)  
        except Exception:
            await ctx.reply("I need a number")

    @commands.hybrid_command(name='userinfo', aliases=["whois", "Whois", "Userinfo"])
    async def userinfo(self, ctx, member: discord.Member = None):
        if not member:  
            member = ctx.author  
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
             
        embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at, title=f"User : {member}")
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}")
        embed.add_field(name="ID:", value=member.id, inline=False)
        embed.add_field(name="Display Name:", value=member.display_name, inline=False)
        embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
        embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
        if role1 != []:
            embed.add_field(name=f"Roles[{len(role1)}]:", value="".join([role.mention for role in role1]), inline=False)
        else:
            embed.add_field(name=f"Roles[{len(role1)}]:", value="None", inline=False) 
        if msg != "":
            embed.add_field(name="Permissions:", value=msg, inline=False)
        if member.bot:  
            embed.add_field(name="Discord Bot?", value="Yes", inline=False)  
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="serverinfo", aliases=["Serverinfo", "Sinfo", "sinfo"])
    async def serverinfo(self, ctx):
        name = str(ctx.guild.name)
        ownner = str(ctx.guild.owner)
        guild_id = str(ctx.guild.id)
        # guild.region was removed in discord.py v2.0+
        memberCount = str(ctx.guild.member_count)
        txtchannel = str(len(ctx.guild.text_channels))
        vcchannel = str(len(ctx.guild.voice_channels))
        role = str(len(ctx.guild.roles))
        icon = str(ctx.guild.icon.url) if ctx.guild.icon else ""
        create = ctx.guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_author(name=name, icon_url=icon if icon else None)
        embed.set_footer(text=f"Requested by {ctx.author} | Server Created : {create}")
        if icon:
            embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=ownner, inline=True)
        embed.add_field(name="Server ID", value=guild_id, inline=True)
        embed.add_field(name="Text Channels", value=txtchannel, inline=True)
        embed.add_field(name="Voice Channels", value=vcchannel, inline=True)
        embed.add_field(name="Roles", value=role, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="yt", aliases=["Yt", "Youtube", "youtube"])
    async def yt(self, ctx, *, search):
        query_string = urllib.parse.urlencode({'search_query': search})
        htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
        search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
        if search_results:
            await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])
        else:
            await ctx.send("No video found.")

    @commands.hybrid_command(name="embed", aliases=["Embed"])   
    @commands.has_permissions(manage_messages=True) 
    async def embed(self, ctx, color, *, text = None):
        if text is None:
            text = ""
        first_word = color[0]
        if first_word == "#" and len(color) == 7:
            hexcode = int(color.replace("#", ""), 16)
            colorhex = int(hex(hexcode), 0)
            em = discord.Embed(description=text, color=colorhex, timestamp=utc_now())
        else:
            colorhex = 0x00ebff 
            text = color + " " + text
            em = discord.Embed(description=text, color=colorhex, timestamp=utc_now())
        if ctx.guild.icon:
            em.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
        else:
            em.set_author(name=ctx.guild.name)
        await ctx.send("```To add a Image into your embed, paste the link of the particular image below within 20 seconds.If you don't want to embed image the process will be executed in 20 seconds. You are requested not to send any message except the link in these 20 seconds or the process will be terminated.```")
        try: 
            def check(msg1):
                return msg1.author == ctx.author and ctx.channel == msg1.channel 
            
            msg1 = await self.bot.wait_for("message", check=check, timeout=20)
            link = msg1.content
            em.set_image(url=link)
            await ctx.send(embed=em)
        except asyncio.TimeoutError:
            await ctx.send(embed=em)            

    @commands.hybrid_command(name="submit", aliases=["Submit"])    
    async def submit(self, ctx, *, text):
        drop_point = self.bot.get_channel(837610754298478643)
        if ctx.channel == drop_point:
            colorhex = 0x00ebff 
            em = discord.Embed(description=f"Submitted by {ctx.author}\nUser ID: {ctx.author.id}", color=colorhex, timestamp=utc_now())
            em.set_author(name=f"{text}")
            await ctx.send("```Paste the link of the image below within 20 seconds to complete your submission.\nDon't Send any message between these 20 sec```", delete_after=20)
            try: 
                def check(msg1):
                    return msg1.author == ctx.author and ctx.channel == msg1.channel 
                
                msg1 = await self.bot.wait_for("message", check=check, timeout=20)
                link = msg1.content
                msg_id = msg1.id
                delmsg = await drop_point.fetch_message(msg_id)
                try:
                    await delmsg.delete()
                except Exception:
                    pass
                try:
                    if link == "":
                        await ctx.send("You need to send the Image Link! try again...", delete_after=15)
                    else:
                        em.set_image(url=link)
                        em.set_footer(text="Tournament Submission")
                        await ctx.send(embed=em)
                except Exception:
                    await ctx.send("You need to send the Image Link! try again...", delete_after=15)    
            except asyncio.TimeoutError:
                await ctx.send("Timeout", delete_after=10)  
            try:
                await ctx.message.delete()
            except Exception:
                pass
        else:
            return                  

    @commands.hybrid_command(name="server")
    async def server(self, ctx):
        try:
            await ctx.author.send("Heres our support server!\nhttps://discord.gg/ZbemgbQuXa")
        except Exception:
            await ctx.send("Maybe your dm is close....")    

    @commands.hybrid_command(name="guild")
    async def guild(self, ctx):
        if ctx.author.id == BOT_OWNER_ID:
            servers = self.bot.guilds
            guilds = []
            serverss = str(len(servers))
            for g in servers:
                guilds.append(g.name)
            await ctx.send(guilds[-50:])
            await ctx.send(f"total servers {serverss}")

    @commands.command(name='upload')  
    @commands.is_owner()  
    async def upload(self, ctx, num: int, *, question):
        if ctx.author.id == BOT_OWNER_ID:
            def check(response):
                return response.author.id == ctx.author.id and response.channel == ctx.channel
            count = 1
            options = []
            num += 1
            while count < num:    
                await ctx.reply(f"Send the {count} option")
                try:
                    response = await self.bot.wait_for('message', check=check, timeout=60)
                    await ctx.send(response.content)
                    options.append(response.content)
                    count += 1
                except Exception:    
                    await ctx.send("smtg went wrong")

            await ctx.reply("Send the correct answer")     
            res = await self.bot.wait_for('message', check=check, timeout=60)  
            await ctx.send(res.content)
            answer = res.content
            result = ""
            for optio in options:
                result += f"{optio}\n"
            emb = discord.Embed(description=f"{question}\n\n{result}\n\nCorrect answer : {answer}")
            msg = await ctx.send(embed=emb)
            await msg.add_reaction("❌")
            await msg.add_reaction("✅")
            def check1(reaction, user):
                return str(reaction.emoji) in ["✅", "❌"] and user != self.bot.user and reaction.message.id == msg.id and user.id == ctx.author.id
            reaction, user = await self.bot.wait_for('reaction_add', check=check1, timeout=40) 
            if str(reaction.emoji) == "✅": 
                cnt = animetriv_collect.count_documents({})
                post = {"_id": cnt, "question": question, "options": options, "answer": answer}
                animetriv_collect.insert_one(post)
                emb = discord.Embed(description=f"{question}\n\n{result}\n\nCorrect answer : {answer}\n\n'Added Successfully")
                await msg.edit(embed=emb)
            if str(reaction.emoji) == "❌":    
                await ctx.send("cancelled")

    @commands.command(name='cleardb')
    @commands.is_owner()
    async def cleardb(self, ctx): 
        if ctx.author.id == BOT_OWNER_ID:
            docs = upd.count_documents({})
            lmt = docs - 40
            if lmt > 2:
                await ctx.send(f'total entries {docs}')
                doc = upd.find().limit(lmt)
                count = 0
                for d in doc:
                    count += 1
                    upd.delete_one({'_id': d['_id']})
                await ctx.send(f'deleted {count} enties') 
            else:
                await ctx.send(docs) 

    @commands.command(name='tyyy')
    async def tyy(self, ctx, link): 
        if ctx.author.id == BOT_OWNER_ID:
            get_driver().get(link)
            await asyncio.sleep(5)
            soup = BeautifulSoup(get_driver().page_source, features="lxml")
            url = soup.find_all('div', {"class": "md:my-0 my-6"})
            
            urll = []
            for u in url:
                urll.append(u.div.a['href'])
            print(urll)
            for ur in urll:
                url = f"https://mywaifulist.moe{ur}" 
                get_driver().get(url)
                await asyncio.sleep(5)
                soup = BeautifulSoup(get_driver().page_source, features="lxml")
                spans = soup.find("div", {"class": "col-span-4 sm:col-span-5"})
                images = soup.find("div", {"class": "md:w-1/3 lg:w-1/4 sm:mb-0 mb-4"})
                name = spans.h1.text
                animes = soup.find("a", {"class": "tooltip-target text-blue-500 font-semibold no-underline tracking-wide cursor-pointer text-xs"})
                anime = animes.text
                await ctx.send(f"name : {name}\nanime : {anime}") 
                img = images.div.img['src']
                await ctx.send(img)
                dc = girl.find_one({'name': name, 'anime': anime})
                if dc is None:
                    r = requests.get(img)  
                    byt = BytesIO(r.content)
                    msg = await ctx.send(file=discord.File(fp=byt, filename='waifu.png'))
                    await msg.add_reaction("❌")
                    await msg.add_reaction("✅")
                    def check1(reaction, user):
                        return str(reaction.emoji) in ["✅", "❌"] and user != self.bot.user and reaction.message.id == msg.id and user.id == ctx.author.id
                    reaction, user = await self.bot.wait_for('reaction_add', check=check1, timeout=40) 
                    if str(reaction.emoji) == "✅": 
                        cnt = girl.count_documents({})
                        post = {"_id": cnt, "name": name, "anime": anime, "image": r.content}
                        emb = discord.Embed(description=f"{name}\n\n{anime}")
                        emb.set_image(url='attachment://waifu.png')
                        await msg.edit(embed=emb)
                        girl.insert_one(post)
                    if str(reaction.emoji) == "❌":    
                        await ctx.send("cancelled")
                else:
                    await ctx.send('already exist')        
            print('done')        

    @commands.hybrid_command(name='invite', aliases=["Invite"])
    async def invite(self, ctx): 
        em = discord.Embed(description='[Click here to invite me :)](https://discord.com/oauth2/authorize?client_id=866129012576223272)', color=0x00ebff)
        em.set_thumbnail(url=self.bot.user.display_avatar.url)
        await ctx.reply(embed=em)           
            
    @commands.hybrid_command(name='vote', aliases=["Vote"])
    async def vote(self, ctx): 
        await ctx.reply('https://top.gg/bot/782005398269984819/vote')    


async def setup(bot):
    await bot.add_cog(Utility(bot))
