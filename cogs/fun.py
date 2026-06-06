import discord
from discord.ext import commands
from discord.ext.commands import BucketType, Greedy
from PIL import Image, ImageDraw
import numpy as np
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import textwrap
import random
import typing
import asyncio
import re
import math
from bot_utils import (
    open_template,
    output_path,
    text_size,
    girl,
    redit,
    utc_now,
    BOT_OWNER_ID
)

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='waifu', aliases=["Waifu"]) 
    @commands.cooldown(3, 120, BucketType.user)  
    async def waifu(self, ctx):
        count = girl.count_documents({})
        if count == 0:
            await ctx.send("No waifus found in database.")
            return
        ct = count - 1
        im = random.randint(0, ct)
        doc = girl.find_one({'_id' : im})     
        name = doc['name']
        anime = doc['anime']
        image = doc['image']
        byt = BytesIO(image)
        file = discord.File(fp=byt, filename='waifu.png')
        emb = discord.Embed(title=name, description=f"{anime}", color=0xdc143c)
        emb.set_image(url='attachment://waifu.png')
        message = await ctx.send(file=file, embed=emb)
        await message.add_reaction("💗")
        
        def check(reaction, user):
            return str(reaction.emoji) == "💗" and user != self.bot.user and reaction.message.id == message.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)
            await ctx.send(f"{user.name} wanna make {name}, waifu! 💝") 
            
            answer = random.randint(0, 9)    
            if answer <= 4:
                await asyncio.sleep(5)
                await ctx.send(f"{user.name}\nAwww... {name} said **Yes** for the marraige!! Congrats💝\nLet me make a wedding card for you >///<")
                bg = Image.new("RGBA", (1479, 600), (0, 0, 0, 0))
                marraige = open_template("marraige.png", "https://i.imgur.com/gxsD8hr.png").convert('RGBA')
                mrg = marraige.resize((250, 250))
                frm = open_template("marraige_frame.png", "https://i.imgur.com/Rs9YYjN.png").convert('RGBA')
                frm = frm.resize((580, 580))
                asset = user.display_avatar.replace(size=128)
                
                data = BytesIO(await asset.read())  
                 
                pfp = Image.open(data).convert('RGB')
                waifu0 = Image.open(byt).convert('RGB')
       
                pfp = pfp.resize((435, 435))
                waifu1 = waifu0.resize((435, 435))
                height, width = pfp.size
                lum_img = Image.new('L', [height, width], 0)
      
                draw = ImageDraw.Draw(lum_img)
                draw.pieslice([(0, 0), (height, width)], 0, 360, fill=255, outline="white")
                img_arr = np.array(pfp)
                lum_img_arr = np.array(lum_img)
                final_img_arr = np.dstack((img_arr, lum_img_arr))
                fll1 = Image.fromarray(final_img_arr)
                height, width = pfp.size
                lu_img = Image.new('L', [height, width], 0)
      
                draw = ImageDraw.Draw(lu_img)
                draw.pieslice([(0, 0), (height, width)], 0, 360, fill=255, outline="white")
                img_arrwa = np.array(waifu1)
                lu_img_arr = np.array(lu_img)
                final_img_arrwa = np.dstack((img_arrwa, lu_img_arr))
                fll = Image.fromarray(final_img_arrwa)
            
                bg.paste(fll1, (77, 80))
                bg.paste(fll, (886, 80))
                bg.paste(mrg, (570, 150))
                bg.paste(frm, (0, 0), mask=frm)
                bg.paste(frm, (809, 0), mask=frm)
                 
                bg.save(output_path("marraige.png"), format="png")    
                
                wed = discord.Embed(description=f"{user.name} and {name} are **married** now!!💝", timestamp=utc_now(), color=0x00ebff)
                file_msg = discord.File(output_path("marraige.png"))
                wed.set_image(url="attachment://marraige.png")
                await ctx.send(file=file_msg, embed=wed)
            if answer > 4:
                await asyncio.sleep(5)
                await ctx.send(f"{user.name}\n{name} said **No** to you.... ;-;")
                
        except asyncio.TimeoutError:
            return    

    @commands.hybrid_command(name='lookup', aliases=['lu','Lookup'])
    async def lookup(self, ctx, name):
        cursor = girl.find({"$text": {"$search": name}}, {'score': {'$meta': 'textScore'}})
        cursor.sort([('score', {'$meta': 'textScore'})])
        name_list = []
        title_list = []
        for nam in cursor:
            name_list.append(nam['name'])
            title_list.append(nam['anime'])
        total = len(name_list)  
        pages = math.ceil(total / 10)
        if total == 0:
            await ctx.reply('that character could not be found. It may not exist, or you may have misspelled their name.')
            return
        if pages > 1:      
            cur_page = 1
            x = 0
            y = 10
            show = ''
            count = 0

            for char, anime in zip(name_list[x:y], title_list[x:y]):
                count += 1
                show += f'{count}. {anime} . **{char}**\n'   
                 
            embb = discord.Embed(title="Waifu Results:", description=f"please type the number beside the character you are looking for.\n\n{show}", color=0xdc143c)
            embb.set_footer(text=f"{cur_page}/{pages}")
            message = await ctx.send(embed=embb) 
            
            await message.add_reaction("◀️")
            await message.add_reaction("▶️")
            def check_react(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
            def check_msg(msg):
                return msg.author == ctx.author and ctx.channel == msg.channel and msg.content.isdigit()   
            work = 'True'     
            while work == 'True':
                finished, unfinished = await asyncio.wait([
                    self.bot.wait_for('message', timeout=30, check=check_msg),
                    self.bot.wait_for('reaction_add', timeout=30, check=check_react)
                ], return_when=asyncio.FIRST_COMPLETED)
                for task in finished:
                    result = task.result() 
                try:  
                    if str(result[0].emoji) == "▶️" and cur_page != pages:
                        show = ""
                        cur_page += 1
                        x += 10
                        y += 10
                        num = x
                        for char, anime in zip(name_list[x:y], title_list[x:y]):
                            num += 1
                            show += f'{num}. {anime} . **{char}**\n'     
                        
                        if show != "":    
                            em = discord.Embed(title="Waifu Results:", description=f"please type the number beside the character you are looking for.\n\n{show}", color=0xdc143c)
                            em.set_footer(text=f"{cur_page}/{pages}")
                            await message.edit(embed=em)
                    elif str(result[0].emoji) == "◀️" and cur_page > 1:
                        show = ""
                        cur_page -= 1    
                        x -= 10
                        y -= 10
                        num = x
                        for char, anime in zip(name_list[x:y], title_list[x:y]):
                            num += 1
                            show += f'{num}. {anime} . **{char}**\n' 
                        emb = discord.Embed(title="Waifu Results:", description=f"please type the number beside the character you are looking for.\n\n{show}", color=0xdc143c)
                        emb.set_footer(text=f"{cur_page}/{pages}")
                        await message.edit(embed=emb)
                except Exception:            
                    if int(result.content) <= y and int(result.content) > x:
                        try:
                            msg3 = int(result.content)
                            index = msg3 - 1
                            chosen_name = name_list[index]
                            chosen_anime = title_list[index]
                            doc = girl.find_one({'name' : chosen_name, 'anime' : chosen_anime})
                            emmb = discord.Embed(title='Waifu Lookup', description=f"Name : **{doc['name']}**\n\nFrom : {doc['anime']}", color=0xdc143c)
                            image = doc['image']
                            byt = BytesIO(image)
                            file = discord.File(fp=byt, filename='waifu.png')
                            emmb.set_image(url='attachment://waifu.png')
                            await ctx.reply(file=file, embed=emmb)
                            work = 'False'
                            await message.delete()
                        except Exception:
                            await ctx.reply('Something went wrong, Please report this bug in support server!')
                           
        elif pages == 1:
            count = 0
            show = ""
            for char, anime in zip(name_list, title_list):
                count += 1
                show += f'{count}. {anime} . **{char}**\n'   
                 
            embb = discord.Embed(title="Waifu Results:", description=f"please type the number beside the character you are looking for.\n\n{show}", color=0xdc143c)
            msssg = await ctx.send(embed=embb)
            def check_msg(msg):
                return msg.author == ctx.author and ctx.channel == msg.channel and msg.content.isdigit()
            rest = 'true'    
            while rest == 'true':    
                try:
                    msg2 = await self.bot.wait_for('message', check=check_msg, timeout=30)
                    try:
                        msg3 = int(msg2.content)
                        if msg3 <= count and msg3 > 0:
                            index = msg3 - 1
                            chosen_name = name_list[index]
                            chosen_anime = title_list[index]
                            doc = girl.find_one({'name' : chosen_name, 'anime' : chosen_anime})
                            emmb = discord.Embed(title='Waifu Lookup', description=f"Name : **{doc['name']}**\n\nFrom : {doc['anime']}", color=0xdc143c)
                            image = doc['image']
                            byt = BytesIO(image)
                            file = discord.File(fp=byt, filename='waifu.png')
                            emmb.set_image(url='attachment://waifu.png')
                            await ctx.reply(file=file, embed=emmb)
                            rest = 'false'
                            await msssg.delete()
                    except Exception:
                        await ctx.reply('Something went wrong, Please report this bug in support server!')     
                except asyncio.TimeoutError:
                    return  

    @commands.hybrid_command(name='say', aliases=["Say", "Type", "type"])
    @commands.cooldown(2, 120, BucketType.user)
    async def say(self, ctx, *, msg: commands.clean_content):
        await ctx.send(msg + f"\n\n           -{ctx.author}")
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

    @commands.hybrid_command(name='spoiler', aliases=["Spoil", "spoil", "Spoiler"])
    @commands.cooldown(2, 120, BucketType.user)
    async def spoiler(self, ctx, *, msg: commands.clean_content):
        await ctx.send("||" + msg + f"||\n\n           -{ctx.author}")
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

    @commands.hybrid_command(name='match')
    async def match(self, ctx, member1: discord.Member, member2: discord.Member = None):  
        if member2 is None:
            mem2 = member1
            asset2 = mem2.display_avatar.replace(size=128)
            mem1 = ctx.author
            asset = mem1.display_avatar.replace(size=128)
        else:
            mem1 = member1
            mem2 = member2
            asset = member1.display_avatar.replace(size=128) 
            asset2 = mem2.display_avatar.replace(size=128)   
        data = BytesIO(await asset.read()) 
        data2 = BytesIO(await asset2.read())  
        pfp = Image.open(data)
        pfp = pfp.resize((400, 400))
        pfp2 = Image.open(data2)
        pfp2 = pfp2.resize((400, 400))
        image = Image.new('RGBA', (800, 400))
        image.paste(pfp, (0, 0))
        image.paste(pfp2, (400, 0))
        image.save(output_path("match.png"))    
        wed = discord.Embed(description=f"{mem1.name} and {mem2.name} are matching their pfp!", timestamp=utc_now(), color=0x00ebff)
        file = discord.File(output_path("match.png"))
        wed.set_image(url="attachment://match.png")
        await ctx.send(file=file, embed=wed)        

    @commands.hybrid_command(name="propose", aliases=["Propose"])
    async def propose(self, ctx, member: discord.Member, *, msg=None):
        if ctx.interaction is not None:
            await ctx.defer()
        if ctx.author != member:
            await ctx.send(f"{member.mention}\n{ctx.author.mention} proposed you for the marraige!! Do you accept?? \nType accept or reject")
            def check(response):
                return response.content.lower() in ["accept", "reject"] and response.author == member and response.channel == ctx.channel
        
            try:
                response = await self.bot.wait_for('message', check=check, timeout=40)
            
                if "accept" in response.content.lower():
                    bg = Image.new("RGBA", (1479, 600), (0, 0, 0, 0))
                    marraige = open_template("marraige.png", "https://i.imgur.com/gxsD8hr.png").convert('RGBA')
                    mrg = marraige.resize((250, 250))
                    frm = open_template("marraige_frame.png", "https://i.imgur.com/Rs9YYjN.png").convert('RGBA')
                    frm = frm.resize((580, 580))
                    asset = ctx.author.display_avatar.replace(size=128)
                    asset2 = member.display_avatar.replace(size=128)
                    data = BytesIO(await asset.read())  
                    data2 = BytesIO(await asset2.read())  
                    pfp = Image.open(data).convert('RGB')
                    waifu0 = Image.open(data2).convert('RGB')
       
                    pfp = pfp.resize((435, 435))
                    waifu1 = waifu0.resize((435, 435))
                    height, width = pfp.size
                    lum_img = Image.new('L', [height, width], 0)
      
                    draw = ImageDraw.Draw(lum_img)
                    draw.pieslice([(0, 0), (height, width)], 0, 360, fill=255, outline="white")
                    img_arr = np.array(pfp)
                    lum_img_arr = np.array(lum_img)
                    final_img_arr = np.dstack((img_arr, lum_img_arr))
                    fll1 = Image.fromarray(final_img_arr)
                    height, width = pfp.size
                    lu_img = Image.new('L', [height, width], 0)
      
                    draw = ImageDraw.Draw(lu_img)
                    draw.pieslice([(0, 0), (height, width)], 0, 360, fill=255, outline="white")
                    img_arrwa = np.array(waifu1)
                    lu_img_arr = np.array(lu_img)
                    final_img_arrwa = np.dstack((img_arrwa, lu_img_arr))
                    fll = Image.fromarray(final_img_arrwa)
                
                    bg.paste(fll1, (77, 80))
                    bg.paste(fll, (886, 80))
                    bg.paste(mrg, (570, 150))
                    bg.paste(frm, (0, 0), mask=frm)
                    bg.paste(frm, (809, 0), mask=frm)
                 
                    bg.save(output_path("marraige.png"), format="png")
                    wed = discord.Embed(description=f"{ctx.author.name} and {member.name} are **married** now!!💝", timestamp=utc_now(), color=0x00ebff)
                    file_msg = discord.File(output_path("marraige.png"))
                    wed.set_image(url="attachment://marraige.png")
                    await ctx.send(file=file_msg, embed=wed)
    
                if "reject" in response.content.lower():
                    await ctx.send(f"{ctx.author.mention} You got rejected... ;-;")   
    
            except asyncio.TimeoutError:
                await ctx.send(f"{ctx.author.mention} {member.name} didn't reply. ;-;")     
        else:
            await ctx.send(f"{ctx.author.mention} You really want to marry yourself ??!!\n||are you lonely? ;-;||")          

    @commands.hybrid_command(name='roast', aliases=["Roast"])
    async def roast(self, ctx, member: discord.Member = None):    
        if member is None:
            member = ctx.author
        try:
            data = requests.get("https://evilinsult.com/generate_insult.php").text
            await ctx.send(f"{member.mention} {data}")
        except Exception:
            await ctx.send("Couldn't think of a roast right now...")

    @commands.hybrid_command(name='insult', aliases=["Insult"])
    async def insult(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        try:
            data = requests.get('http://autoinsult.datahamster.com/index.php?style=3').text
            site = BeautifulSoup(data, "lxml")
            await ctx.send(f"{member.mention} " + "{}!".format(site.select("div.insult")[0].text))
        except Exception:
            await ctx.send("Couldn't think of an insult right now...")

    @commands.hybrid_command(name='df', aliases=["define", "Define", "Df"])
    async def define(self, ctx, *, word): 
        try: 
            r = requests.get("http://www.urbandictionary.com/define.php?term={}".format(word))
            soup = BeautifulSoup(r.content, features="lxml")
        
            mean = (soup.find("div", attrs={"class":"meaning"}).text)
            exp = (soup.find("div", attrs={"class":"example"}).text)
            up = (soup.find("a", attrs={"class":"up"}).text)
            down = (soup.find("a", attrs={"class":"down"}).text)
            em = discord.Embed(title=f"Word: {word}", colour=ctx.author.color, timestamp=ctx.message.created_at)
            em.add_field(name="Meaning:", value=mean)
            em.add_field(name="Example:", value=f"{exp}\n\n{up} 👍\n{down} 👎")
            await ctx.send(embed=em)
        except Exception:
            em = discord.Embed(title="Not found")
            await ctx.send(embed=em)

    @commands.hybrid_command(name='meme', aliases=['Meme','Memes','memes'])
    @commands.cooldown(5, 60, BucketType.user)  
    async def meme(self, ctx):
        try:
            subred = redit.subreddit("Animemes")
            subs = subred.top("day", limit=50)
            top = []
            for tops in subs:
                if "https://v.redd" not in tops.url and tops.over_18 == False:
                    top.append(tops)
            topp = random.choice(top)   
            em = discord.Embed(description=topp.title, color=ctx.author.color)
            em.set_image(url=topp.url)
            await ctx.send(embed=em)
        except Exception:
            await ctx.reply("`something went wrong ;-;`")    

    @commands.hybrid_command(name='reddit', aliases=['Reddit','red','Red'])
    @commands.cooldown(5, 60, BucketType.user)
    async def reddit(self, ctx, name):
        try:
            subred = redit.subreddit(name)
            subs = subred.top("day", limit=60)
            top = []
            for tops in subs:
                if "https://v.redd" not in tops.url and tops.over_18 == False:
                    top.append(tops)
            topp = random.choice(top)   
            em = discord.Embed(description=topp.title, color=ctx.author.color)
            em.set_image(url=topp.url)
            await ctx.send(embed=em)
        except Exception:
            await ctx.reply("`something went wrong ;-;`")    

    @commands.hybrid_command(name="f", aliases=["F"])
    async def f(self, ctx, *, msg: commands.clean_content):
        message = await ctx.send(f"Press 🇫 to pay respects to **{msg}**")  
        await message.add_reaction("🇫")
        count = 0
        uss = []
        def check(reaction, user):
            return str(reaction.emoji) == "🇫" and user != self.bot.user and reaction.message.id == message.id and user.id not in uss
        while True:     
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=25)
                uss.append(user.id)
                await ctx.send(f"**{user.display_name}** has paid their respects.")
                count += 1
            except asyncio.TimeoutError:
                if count == 0:
                    await message.reply(f"nobody paid their respects to **{msg}**....")
                elif count == 1:
                    await message.reply(f"**1** person paid their respects to **{msg}**") 
                else:
                    await message.reply(f"**{count}** people paid their respects to **{msg}**")       
                return 

    @commands.hybrid_command(name='imposter', aliases=['whoisimposter','Imposter'])
    async def imposter(self, ctx, member: Greedy[discord.Member]):
        imp = random.choice(member)
        imps = discord.Embed(timestamp=utc_now(), color=0x00ebff)
        imps.set_author(name=f'{self.bot.user.display_name}', icon_url=f'{self.bot.user.display_avatar.url}')
        line1 = f'{imp}  is the **Imposter**!! I saw {imp} killing blue..'
        line2 = f'{imp}  is the **Imposter**!! {imp} vented infront of me...'
        line3 = f'{imp}  is the **Imposter**!! {imp} was doing fake task! Lol noob...'
        linelist = (line1, line2, line3)
        line = random.choice(linelist)

        imps.add_field(name='Who is the Imposter!!', value=f'{line}')
        imps.set_image(url='https://i.imgur.com/m2EfMwb.jpg')
        await ctx.send(embed=imps)

    @commands.hybrid_command(name="hall", aliases=["Hall"])
    async def hall(self, ctx, *, text):
        hall_point = self.bot.get_channel(837605170330337310)
        if ctx.channel == hall_point:
            x, msg = text.split("|")
            colorhex = 0xff0000
            em = discord.Embed(description=msg, color=colorhex, timestamp=utc_now())
            em.set_author(name=f"Hall Of Fame {x}", icon_url=ctx.guild.icon_url)
            await ctx.send(embed=em)
            try:
                await ctx.message.delete()
            except discord.HTTPException:
                pass
        else:
            return

    @commands.hybrid_command(name="post", aliases=["Post"])  
    @commands.has_permissions(manage_messages=True)  
    async def post(self, ctx, *, id): 
        id1, id2 = id.split("|")  
        post_point = self.bot.get_channel(837609315572383755)
        if ctx.channel == post_point: 
            channel = self.bot.get_channel(837610754298478643) 
            msg1 = await channel.fetch_message(id1)
            msg2 = await channel.fetch_message(id2)
            message1 = await ctx.send("**Vote for the following Submissions!!**", embed=msg1.embeds[0])
            message2 = await ctx.send(embed=msg2.embeds[0])
            await message1.add_reaction("<a:Stela_up:838153046537535549>")
            await message2.add_reaction("<a:Stela_up:838153046537535549>")
        else:
            return    
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

    @commands.hybrid_command(name="poll", aliases=["Poll"])
    async def poll(self, ctx, ques, *, msg: commands.clean_content):
        if ctx.author.id == BOT_OWNER_ID:
            data = re.split(pattern=r"\|+", string=msg)
            await ctx.send("❔" + ques)
            for options in data:
                message = await ctx.send(options)
                await message.add_reaction("⏫")

    async def dm_helper(self, player: discord.User, question, answer, option, options):
        embedd = discord.Embed(title="Chase the Runner", description=f"**Type the Answer of the Question!**\n{question}\n\n{option}\n`Type cancel to cancel the game`") 
        msg = await player.send(embed=embedd)
        def check(res):
            return res.content.lower() in options and res.author == player 
            
        try:
            res = await self.bot.wait_for('message', check=check, timeout=30)
            if res.content.lower() == "cancel":
                emmb = discord.Embed(title="Chase the Runner", description=f"`Cancelling the game!`", color=0xFF0000) 
                await msg.edit(embed=emmb, delete_after=20)
                return ["cancel"]
                
            if res.content.lower() == answer.lower():
                embed4 = discord.Embed(title="Chase the Runner", description=f"**Answer the Question!**\n{question}\n`{res.content}` - **Correct Answer: +1**", color=0x00FF00) 
                await msg.edit(embed=embed4, delete_after=20)
                return [1]   
            else:    
                embed2 = discord.Embed(title="Chase the Runner", description=f"**Answer the Question!**\n{question}\n**Wrong Answer: +0**", color=0xFF0000) 
                await msg.edit(embed=embed2, delete_after=20)
                return [0]
                
        except asyncio.TimeoutError:
            embed3 = discord.Embed(title="Chase the Runner", description="timeout....", color=0xFF0000) 
            await msg.edit(embed=embed3, delete_after=10)
            return [0, 1]

    @commands.hybrid_command(name='challenge', aliases=["Challenge"])    
    async def challenge(self, ctx, member: discord.Member):
        if ctx.author != member:
            mem1 = ctx.author
            mem2 = member
            htmlcodes = (("'", '&#039;'), ('"', '&quot;'), (">", '&GT;'), ('<', '&lt;'), ('&', '&amp;'))
            
            em = discord.Embed(title="Chase the Runner", description=f"You have been challenged by {mem1.mention}\nYou have to answer as many questions as you can, time for each question is 40 sec\n`Do you accept the challenge?`")
            msg = await ctx.send(mem2.mention, embed=em)
            await msg.add_reaction("❌")
            await msg.add_reaction("✅")
            emoji_numbers = ["✅", "❌"]
            def check1(reaction, user):
                return str(reaction.emoji) in ["✅", "❌"] and user != self.bot.user and reaction.message.id == msg.id and user.id == mem2.id
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check1, timeout=40) 
                await msg.remove_reaction(reaction, mem2)
                i = 0
                while i < 2:
                    await msg.remove_reaction(emoji_numbers[i], self.bot.user)
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
                        api = random.choice([api1, api2, api3])
                        r = requests.get(api).json()
                        leng = (len(r['results']) - 1)
                        
                        choose = random.randint(0, leng)
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
                            option = option.replace(code[1], code[0])
                            options[0] = options[0].replace(code[1], code[0])
                            options[1] = options[1].replace(code[1], code[0])
                            options[2] = options[2].replace(code[1], code[0])
                            options[3] = options[3].replace(code[1], code[0])
                            qu = qu.replace(code[1], code[0]) 
                            ans = ans.replace(code[1], code[0])
                        for i in range(len(options)):
                            options[i] = options[i].lower() 
                        
                        def check_res(response):
                            return response.content.lower() in options and response.author == mem2 and response.channel == ctx.channel
                        embe = discord.Embed(title="Chase the Runner", description=f"{qu}\n\n{option}", color=0x00FF00)    
                        await msg.edit(embed=embe)
                        try:
                            response = await self.bot.wait_for('message', check=check_res, timeout=45)
                            if response.content.lower() == ans.lower():
                                money += 1
                                count += 1
                                if count > 8:
                                    name = "False"
                            else:
                                name = "False"        
                        except asyncio.TimeoutError:
                            name = "False"
                        
                    embed = discord.Embed(title="Chase the Runner", description=f"**Robbery ended**\nYou robbed {money*100}+ Respect", color=0x00FF00) 
                    await msg.edit(embed=embed)        
                    await ctx.send(f"{mem1.mention}|{mem2.mention}`Come in Dm \nChase will start in 30 sec`")
                    
                    TPA = 0
                    TPB = 2
                    
                    api1 = "https://opentdb.com/api.php?amount=45&category=31&difficulty=easy&type=multiple"
                    api2 = "https://opentdb.com/api.php?amount=50&category=31&difficulty=medium&type=multiple"
                    api3 = "https://opentdb.com/api.php?amount=37&category=31&difficulty=hard&type=multiple"
                    api = random.choice([api1, api2, api3])
                    r = requests.get(api).json()
                    lengg = (len(r['results']) - 1)
                    choice = random.randint(0, lengg)
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
                        optio = optio.replace(code[1], code[0])
                        optionss[0] = optionss[0].replace(code[1], code[0])
                        optionss[1] = optionss[1].replace(code[1], code[0])
                        optionss[2] = optionss[2].replace(code[1], code[0])
                        optionss[3] = optionss[3].replace(code[1], code[0])
                        q = q.replace(code[1], code[0]) 
                        anss = anss.replace(code[1], code[0])
                    for i in range(len(optionss)):
                        optionss[i] = optionss[i].lower() 
                        
                    dead = 1    
                    await asyncio.sleep(20)
                    await mem1.send("`Chase is starting Now!!`")
                    await mem2.send("`Chase is starting Now!!`") 
                    while work == "True":
                        point1 = self.dm_helper(mem1, q, anss, optio, optionss)
                        point2 = self.dm_helper(mem2, q, anss, optio, optionss)
                        pointA, pointB = await gather(point1, point2)
                        if pointA[0] != "cancel" and pointB[0] != "cancel":
                            TPA += pointA[0]
                            TPB += pointB[0]
                            
                            api1 = "https://opentdb.com/api.php?amount=45&category=31&difficulty=easy&type=multiple"
                            api2 = "https://opentdb.com/api.php?amount=50&category=31&difficulty=medium&type=multiple"
                            api3 = "https://opentdb.com/api.php?amount=37&category=31&difficulty=hard&type=multiple"
                            api = random.choice([api1, api2, api3])
                            r = requests.get(api).json()
                            lengg = (len(r['results']) - 1)
                            choice = random.randint(0, lengg)
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
                                optio = optio.replace(code[1], code[0])
                                optionss[0] = optionss[0].replace(code[1], code[0])
                                optionss[1] = optionss[1].replace(code[1], code[0])
                                optionss[2] = optionss[2].replace(code[1], code[0])
                                optionss[3] = optionss[3].replace(code[1], code[0])
                                q = q.replace(code[1], code[0]) 
                                anss = anss.replace(code[1], code[0])
                            for i in range(len(optionss)):
                                optionss[i] = optionss[i].lower()
                            
                            rd = "<a:Stela_road:865251683927719947> "
                            run = "<a:Stela_runner:865251935901057034>"
                            chase = "<a:Stela_chaser:865245652345946132>"
                            scene = f'{(8 - (TPB + 1)) * rd}{run}{((TPB - TPA) - 1) * rd}{chase}{TPA * rd}'
                            
                            if len(pointA) == 2 and len(pointB) == 2:
                                if pointA[1] == 1 and pointB[1] == 1:
                                    dead += 1
                                    
                            if len(pointA) != 2 or len(pointB) != 2:
                                dead = 1 
                                    
                            if dead > 3:
                                await mem1.send("`Game has been terminated because of inactivity`")
                                await mem2.send("`Game has been terminated because of inactivity`") 
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
                                await mem1.send(scene, delete_after=10)
                                await mem2.send(scene, delete_after=10)   
                        else:
                            await mem1.send("Game has been cancelled")
                            await mem2.send("Game has been cancelled")   
                            work = "False"       
                if str(reaction.emoji) == "❌":
                    emb = discord.Embed(title="Chase the Runner", description=f"{mem2.mention} declined the Challenge!", color=0xFF0000)
                    await msg.edit(embed=emb)  
            except asyncio.TimeoutError:
                embbb = discord.Embed(title="Chase the Runner", description=f"You have been challenged by {mem1.mention}\nYou have to answer as many questions as you can, time for each question is 45 sec\n`Timeout`", color=0xFF0000)
                await msg.edit(embed=embbb)
        else:
            await ctx.reply("How can you play with yourself.. Dummy")        

    @commands.hybrid_command(name="gcreate")
    async def giveaway(self, ctx):
        if ctx.author.id == BOT_OWNER_ID:
            await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")
            questions = [
                "Which channel should it be hosted in?", 
                "What should be the duration of the giveaway? (s|m|h|d)",
                "What is the prize of the giveaway?",
                "Enter the requirements If None then Type 'None'"
            ]
            answers = []
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel 

            for q in questions:
                await ctx.send(q)
                try:
                    msg = await self.bot.wait_for('message', timeout=30, check=check)
                except asyncio.TimeoutError:
                    await ctx.send('You didn\'t answer in time, please be quicker next time!')
                    return
                else:
                    answers.append(msg.content)
            try:
                c_id = int(answers[0][2:-1])
            except Exception:
                await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
                return

            channel = self.bot.get_channel(c_id)
            time_val = self.convert_time(answers[1])
            if time_val == -1:
                await ctx.send("You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
                return
            elif time_val == -2:
                await ctx.send("The time must be an integer. Please enter an integer next time")
                return            

            prize = answers[2]
            rqmt = answers[3]
            await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")

            embed = discord.Embed(title="Giveaway!", description=f"{prize}", color=ctx.author.color)
            if rqmt != "None":
                embed.add_field(name="Requirements:", value=rqmt)
            embed.add_field(name="Hosted by:", value=ctx.author.mention)
            embed.set_footer(text=f"Ends {answers[1]} from now!")

            my_msg = await channel.send(embed=embed)
            await my_msg.add_reaction("🎉")

            await asyncio.sleep(time_val)
            new_msg = await channel.fetch_message(my_msg.id)
            
            # Extract users from reaction
            users = []
            async for u in new_msg.reactions[0].users():
                users.append(u)
            if self.bot.user in users:
                users.remove(self.bot.user)
            if not users:
                await my_msg.reply("No one Participated ;-;")
            else:    
                winner = random.choice(users)
                await my_msg.reply(f"Congratulations! {winner.mention} won {prize}!")

    @commands.hybrid_command(name="reroll")
    @commands.has_permissions(manage_messages=True)
    async def reroll(self, ctx, id_: int):
        try:
            new_msg = await ctx.channel.fetch_message(id_)
        except Exception:
            await ctx.send("The id was entered incorrectly.")
            return
        
        users = []
        async for u in new_msg.reactions[0].users():
            users.append(u)
        if self.bot.user in users:
            users.remove(self.bot.user)

        if not users:
            await ctx.send("No users to reroll.")
            return

        winner = random.choice(users)
        await ctx.send(f"Congratulations! The new winner is {winner.mention}.!")

    def convert_time(self, time_str):
        pos = ["s", "m", "h", "d"]
        time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600 * 24}
        unit = time_str[-1]
        if unit not in pos:
            return -1
        try:
            val = int(time_str[:-1])
        except Exception:
            return -2
        return val * time_dict[unit]

async def setup(bot):
    await bot.add_cog(Fun(bot))
