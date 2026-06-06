import discord
from discord.ext import commands
from discord.ext.commands import BucketType, Greedy
from PIL import Image, ImageDraw
import numpy as np
import numpy
from io import BytesIO
import textwrap
import random
import typing
from bot_utils import (
    open_template,
    asset_font,
    output_path,
    text_size,
    redit,
    utc_now
)

class MemeGen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='wanted', aliases=['Bounty','Wanted','bounty'])
    async def wanted(self, ctx, user: discord.Member = None):
        if ctx.interaction is not None:
            await ctx.defer()
        if user is None:
            user = ctx.author
        wanted_img = open_template("wanted.png", "https://i.imgur.com/jNJBoeJ.png")
        asset = user.display_avatar.replace(size=128)
        data = BytesIO(await asset.read())   
        pfp = Image.open(data)
        pfp = pfp.resize((385, 261))
        wanted_img.paste(pfp, (57, 153))
        font = asset_font("luffyfont.ttf", 60)        
        draw = ImageDraw.Draw(wanted_img)
        text1 = user.display_name
        text = textwrap.wrap(text1, 19)
        W, H = (251, 500)
        w, h = text_size(draw, text[0], font)
        draw.text((W - w / 2, H - h / 2), text[0], (93, 63, 51), font=font, align="center")
        num = random.randint(100000000, 10000000000) 
        bount = str(num)
        font_bounty = asset_font("luffyfont.ttf", 70)
        draw.text((102, 534), bount, (93, 63, 51), font=font_bounty)
        wanted_img.save(output_path("wanted.png"))
        
        if len(text1) > 19:
            await ctx.send("Hey! Your name is longer than 19 Characters \n**Tip**: Keep it shorter :) ")
        await ctx.send(file=discord.File(output_path("wanted.png")))

    @commands.hybrid_command(name='instagram', aliases=['insta','Insta','Instagram'])
    async def instagram(self, ctx, user: typing.Optional[discord.Member] = None, *, caption=None):
        if ctx.interaction is not None:
            await ctx.defer()
        if user is None:
            user = ctx.author
        post = open_template("instagram.png", "https://i.imgur.com/REDMT7r.png")
        asset = user.display_avatar.replace(size=128)
        data = BytesIO(await asset.read())   
        pfp = Image.open(data)
        pfp = pfp.resize((322, 313))
        post.paste(pfp, (19, 54))
        font = asset_font("ARIAL.TTF", 15)        
        draw = ImageDraw.Draw(post)
        text1 = user.display_name
        text = textwrap.wrap(text1, 19)
        draw.text((56, 21), text[0], (0, 0, 0), font=font)
        
        img = Image.open(data).convert("RGB")
        img = img.resize((36, 36))
        npImage = numpy.array(img)
        
        alpha = Image.new('L', [36, 36], 0)
        draw1 = ImageDraw.Draw(alpha)
        draw1.pieslice([0, 0, 36, 36], 0, 360, fill=255)
        npAlpha = numpy.array(alpha)
        npImage = numpy.dstack((npImage, npAlpha))
        pfp1 = Image.fromarray(npImage)
        post.paste(pfp1, (18, 15))
        
        caption1 = f"@{user.display_name}  {caption}"
        caption2 = textwrap.wrap(caption1, 39)
        draw.text((21, 420), caption2[0], (0, 0, 0), font=font)
        post.save(output_path("instagram.png"))
        
        if caption and len(caption) > 28:
            await ctx.send("Hey! that too long for a Caption ")
        if len(text1) > 18:
            await ctx.send("Hey! Your name is longer than 18 Characters \n**Tip**: Keep it shorter :) ")    
        await ctx.send(file=discord.File(output_path("instagram.png")))

    @commands.hybrid_command(name='distract', aliases=['Distract',"distracted","Distracted"])
    async def distract(self, ctx, *, caption): 
        if ctx.interaction is not None:
            await ctx.defer()
        post = open_template("distracted.jpg", "https://i.imgur.com/WE18XMM.jpg") 
        font = asset_font("ARIAL.TTF", 40)
        line1, line2, line3 = caption.split(",")
        draw = ImageDraw.Draw(post)
        lines1 = textwrap.wrap(line1, 7)  
        lines2 = textwrap.wrap(line2, 7)
        lines3 = textwrap.wrap(line3, 7)
        W1 = 376
        H1 = 164
        W2 = 563
        H2 = 138
        W3 = 110
        H3 = 21
        for l1 in lines1:
            w1, h1 = text_size(draw, l1, font)
            draw.text((W1 - w1 / 2, H1), l1, (0, 0, 0), font=font)
            H1 += h1 
        for l2 in lines2:
            w2, h2 = text_size(draw, l2, font)
            draw.text((W2 - w2 / 2, H2), l2, (0, 0, 0), font=font)
            H2 += h2  
        for l3 in lines3:
            w3, h3 = text_size(draw, l3, font)
            draw.text((W3 - w3 / 2, H3), l3, (0, 0, 0), font=font)
            H3 += h3      
        post.save(output_path("distracted.jpg"))
        await ctx.send(file=discord.File(output_path("distracted.jpg")))

    @commands.hybrid_command(name='thisisshit', aliases=['Thisisshit'])
    async def thisisshit(self, ctx, user: discord.Member = None): 
        if ctx.interaction is not None:
            await ctx.defer()
        if user is None:
            user = ctx.author
        post = open_template("thisisshit.jpg", "https://i.imgur.com/jtZqJ2u.jpg") 
        asset = user.display_avatar.replace(size=128)
        data = BytesIO(await asset.read())   
        pfp = Image.open(data)
        pfp = pfp.resize((265, 141))
        post.paste(pfp, (9, 159))   
        post.save(output_path("thisisshit.jpg"))    
        await ctx.send(file=discord.File(output_path("thisisshit.jpg")))

    @commands.hybrid_command(name='water', aliases=['Water'])
    async def water(self, ctx, user: typing.Optional[discord.Member] = None, *, caption): 
        if ctx.interaction is not None:
            await ctx.defer()
        if user is None:
            user = ctx.author
        post = open_template("water.png", "https://i.imgur.com/wpN45qC.jpg")  
        font = asset_font("ARIAL.TTF", 30)
        W = 282
        H1 = 36
        
        draw = ImageDraw.Draw(post)
        lines = textwrap.wrap(caption, 12)   
        for line in lines:
            w1, h1 = text_size(draw, line, font)
            draw.text((W - w1 / 2, H1), line, (0, 0, 0), font=font)
            H1 += h1 
        asset = user.display_avatar.replace(size=128)
        data = BytesIO(await asset.read())   
        pfp = Image.open(data)
        pfp = pfp.resize((86, 94))
        post.paste(pfp, (18, 264))    
        post.save(output_path("water.png"))    
        await ctx.send(file=discord.File(output_path("water.png")))

    @commands.hybrid_command(name='chika', aliases=['Chika'])
    async def chika(self, ctx, *, caption): 
        if ctx.interaction is not None:
            await ctx.defer()
        post = open_template("chika.png", "https://i.imgur.com/ZlnspzF.png") 
        font = asset_font("ARIAL.TTF", 30)
        line1, line2, line3, line4 = caption.split("|") 
        W = 470
        H1 = 15
        H2 = 191
        H3 = 372
        H4 = 555
        
        draw = ImageDraw.Draw(post)
        line11 = textwrap.wrap(line1, 17)
        line22 = textwrap.wrap(line2, 17)
        line33 = textwrap.wrap(line3, 17)
        line44 = textwrap.wrap(line4, 17)
        
        for element in line11:
            w1, h1 = text_size(draw, element, font)
            draw.text((W - w1 / 2, H1), element, (0, 0, 0), font=font)
            H1 += h1
            
        for element2 in line22:
            w2, h2 = text_size(draw, element2, font)
            draw.text((W - w2 / 2, H2), element2, (0, 0, 0), font=font)
            H2 += h2
            
        for element3 in line33:
            w3, h3 = text_size(draw, element3, font)
            draw.text((W - w3 / 2, H3), element3, (0, 0, 0), font=font)
            H3 += h3
        
        for element4 in line44:
            w4, h4 = text_size(draw, element4, font)
            draw.text((W - w4 / 2, H4), element4, (0, 0, 0), font=font)
            H4 += h4
            
        post.save(output_path("chika.png"))
        await ctx.send(file=discord.File(output_path("chika.png")))

    @commands.hybrid_command(name='myboi', aliases=['myboy',"Myboi","Myboy"])
    async def myboi(self, ctx, user: discord.Member): 
        if ctx.interaction is not None:
            await ctx.defer()
        
        post = open_template("Myboi.png", "https://i.imgur.com/QTIHrse.jpg") 
        text1 = ctx.author.display_name
        text = textwrap.wrap(text1, 19)
        W, H = (585, 420)
        draw = ImageDraw.Draw(post)
        font = asset_font("ARIAL.TTF", 60)
        w, h = text_size(draw, text[0], font)
        draw.text((W - w / 2, H - h / 2), text[0], (93, 63, 51), font=font, align="center")
        asset = user.display_avatar.replace(size=128)
        data = BytesIO(await asset.read())   
        pfp = Image.open(data)
        pfp = pfp.resize((385, 279))
        post.paste(pfp, (1213, 3))
        
        post.save(output_path("Myboi.png"))    
        await ctx.send(file=discord.File(output_path("Myboi.png")))

    @commands.hybrid_command(name='dumb', aliases=['Dumb'])
    async def dumb(self, ctx, *, caption):
        if ctx.interaction is not None:
            await ctx.defer()
        post = open_template("dumb.png", "https://i.imgur.com/pvkkups.jpg")  
        font = asset_font("ARIAL.TTF", 30)
        W = 347
        H1 = 435
        
        draw = ImageDraw.Draw(post)
        lines = textwrap.wrap(caption, 14)   
        for line in lines:
            w1, h1 = text_size(draw, line, font)
            draw.text((W - w1 / 2, H1), line, (0, 0, 0), font=font)
            H1 += h1
        post.save(output_path("dumb.png"))
        await ctx.send(file=discord.File(output_path("dumb.png")))

    @commands.hybrid_command(name='wallpunch', aliases=['Wallpunch',"wallPunch"])
    async def wallpunch(self, ctx, *, caption):
        if ctx.interaction is not None:
            await ctx.defer()
        post = open_template("wallpunch.png", "https://i.imgur.com/qYBV6yl.png")  
        font = asset_font("ARIAL.TTF", 40)
        W = 6
        H1 = 4
        
        draw = ImageDraw.Draw(post)
        lines = textwrap.wrap(caption, 24)   
        for line in lines:
            w1, h1 = text_size(draw, line, font)
            draw.text((W, H1), line, (0, 0, 0), font=font)
            H1 += h1
        post.save(output_path("wallpunch.png"))
        await ctx.send(file=discord.File(output_path("wallpunch.png"))) 

    @commands.hybrid_command(name='worthless', aliases=['Worthless'])
    async def worthless(self, ctx, *, caption): 
        if ctx.interaction is not None:
            await ctx.defer()
        post = open_template("worthless.png", "https://i.imgur.com/7yQETI9.png") 
         
        font = asset_font("ARIAL.TTF", 25)
        W = 202
        H1 = 75
        
        draw = ImageDraw.Draw(post)
        lines = textwrap.wrap(caption, 17)   
        for line in lines:
            w1, h1 = text_size(draw, line, font)
            draw.text((W - w1 / 2, H1), line, (0, 0, 0), font=font)
            H1 += h1 
        post.save(output_path("worthless.png"))    
        await ctx.send(file=discord.File(output_path("worthless.png")))

    @commands.hybrid_command(name='fbi', aliases=['Fbi'])
    async def fbi(self, ctx, *, msg):
        if ctx.interaction is not None:
            await ctx.defer()
        post = open_template("fbi.jpg", "https://i.imgur.com/OkhouW4.jpg")
        font = asset_font("Product_Sans_Regular.ttf", 35)     
        msg2 = textwrap.wrap(msg, 33)
        draw = ImageDraw.Draw(post)
        draw.text((35, 256), msg2[0], (0, 0, 0), font=font)
        post.save(output_path("fbi.jpg"))
        await ctx.send(file=discord.File(output_path("fbi.jpg")))

    @commands.hybrid_command(name='news', aliases=['News'])
    async def news(self, ctx, user: typing.Optional[discord.Member] = None, *, msg):
        if ctx.interaction is not None:
            await ctx.defer()
        if user is None:
            user = ctx.author
        post = open_template("news.png", "https://i.imgur.com/dvP6ekG.png")
        font1 = asset_font("BebasNeue-Regular.ttf", 35)  
        font2 = asset_font("BebasNeue-Regular.ttf", 15)    
        msg1, msg2 = msg.split("|") 
        msg1 = textwrap.wrap(msg1, 34)
        msg2 = textwrap.wrap(msg2, 70)
        draw = ImageDraw.Draw(post)
        draw.text((6, 200), msg1[0], (0, 0, 0), font=font1)
        draw.text((44, 248), msg2[0], (0, 0, 0), font=font2)
        asset = user.display_avatar.replace(size=128)
        data = BytesIO(await asset.read())   
        pfp = Image.open(data)
        pfp = pfp.resize((482, 198)) 
        bg = Image.new("RGB", (480, 270), (255, 255, 255))
        bg.paste(pfp, (0, 0))
        bg.paste(post, (0, 0), mask=post)
        bg.save(output_path("news.png"))
        await ctx.send(file=discord.File(output_path("news.png")))

    @commands.hybrid_command(name='santa', aliases=['Santa'])
    async def santa(self, ctx, *, caption): 
        if ctx.interaction is not None:
            await ctx.defer()
        post = open_template("santa.png", "https://i.imgur.com/jCZwcR3.jpg") 
        font = asset_font("ARIAL.TTF", 25)
        W = 123
        H1 = 351
        
        draw = ImageDraw.Draw(post)
        lines = textwrap.wrap(caption, 10)   
        for line in lines:
            w1, h1 = text_size(draw, line, font)
            draw.text((W - w1 / 2, H1), line, (0, 0, 0), font=font)
            H1 += h1 
        post.save(output_path("santa.png"))    
        await ctx.send(file=discord.File(output_path("santa.png")))    

    @commands.hybrid_command(name='jojo', aliases=['Jojo'])
    async def jojo(self, ctx, user: discord.Member = None): 
        if ctx.interaction is not None:
            await ctx.defer()
        if user is None:
            user = ctx.author
        post = open_template("jojo.png", "https://i.imgur.com/fFzVj4u.png") 
        asset = user.display_avatar.replace(size=128)
        data = BytesIO(await asset.read())   
        pfp = Image.open(data)
        pfp = pfp.resize((177, 240)) 
        post.paste(pfp, (94, 96))
        post.save(output_path("jojo.png"))
        await ctx.send(file=discord.File(output_path("jojo.png")))

    @commands.hybrid_command(name='disability', aliases=['Disability'])
    async def disability(self, ctx, user: discord.Member = None): 
        if ctx.interaction is not None:
            await ctx.defer()
        if user is None:
            user = ctx.author
        post = open_template("disability.png", "https://i.imgur.com/4RsH5M4.png") 
        asset = user.display_avatar.replace(size=128)
        data = BytesIO(await asset.read())   
        pfp = Image.open(data)
        pfp = pfp.resize((207, 187)) 
        post.paste(pfp, (567, 408))
        post.save(output_path("disability.png"))
        await ctx.send(file=discord.File(output_path("disability.png")))

    @commands.hybrid_command(name='rip', aliases=['Rip'])
    async def rip(self, ctx, user: discord.Member = None): 
        if ctx.interaction is not None:
            await ctx.defer()
        if user is None:
            user = ctx.author
        post = open_template("rip.png", "https://i.imgur.com/c8mksIz.png") 
        asset = user.display_avatar.replace(size=128)
        data = BytesIO(await asset.read())   
        pfp = Image.open(data)
        pfp = pfp.resize((78, 78)) 
        post.paste(pfp, (59, 116))
        # Note: the original code saved rip image to output_path("jojo.png"), let's follow that or change it to "rip.png"?
        # Wait, the original code had: post.save(output_path("jojo.png")) then ctx.send(file=discord.File(output_path("jojo.png")))
        # It's better to preserve this behavior, or save to "rip.png" and send "rip.png" (cleaner). Let's use rip.png since it's cleaner.
        post.save(output_path("rip.png"))
        message = await ctx.send(file=discord.File(output_path("rip.png"))) 
        await message.add_reaction("🇫")

    @commands.hybrid_command(name='billy', aliases=['Billy'])
    async def billy(self, ctx, *, msg):
        if ctx.interaction is not None:
            await ctx.defer()
        post = open_template("billy.jpg", "https://i.imgur.com/qhlo7N1.jpg")
        font = asset_font("Product_Sans_Regular.ttf", 15)     
        msg2 = textwrap.wrap(msg, 39)
        draw = ImageDraw.Draw(post)
        draw.text((264, 177), msg2[0], (0, 0, 0), font=font)
        post.save(output_path("billy.jpg"))
        await ctx.send(file=discord.File(output_path("billy.jpg")))

    @commands.hybrid_command(name='fact', aliases=['Fact'])
    async def fact(self, ctx, *, caption): 
        if ctx.interaction is not None:
            await ctx.defer()
        post = open_template("fact.png", "https://i.imgur.com/aKADQfg.jpg") 
        font = asset_font("ARIAL.TTF", 25)
        W = 107
        H1 = 345
        
        draw = ImageDraw.Draw(post)
        lines = textwrap.wrap(caption, 12)   
        for line in lines:
            w1, h1 = text_size(draw, line, font)
            draw.text((W - w1 / 2, H1), line, (0, 0, 0), font=font)
            H1 += h1 
            
        post.save(output_path("fact.png"))    
        await ctx.send(file=discord.File(output_path("fact.png")))  

    @commands.hybrid_command(name='bitch', aliases=['Bitch'])
    async def bitch(self, ctx, *, caption): 
        if ctx.interaction is not None:
            await ctx.defer()
        post = open_template("bitch.png", "https://i.imgur.com/2i9cJvo.png") 
        font = asset_font("ARIAL.TTF", 32)
        W = 187
        H1 = 317
        
        draw = ImageDraw.Draw(post)
        lines = textwrap.wrap(caption, 12)   
        for line in lines:
            w1, h1 = text_size(draw, line, font)
            draw.text((W - w1 / 2, H1), line, (0, 0, 0), font=font)
            H1 += h1 
        post.save(output_path("bitch.png"))    
        await ctx.send(file=discord.File(output_path("bitch.png")))   

    @commands.hybrid_command(name='yugioh', aliases=['Yugioh'])
    async def yugioh(self, ctx, *, msg): 
        if ctx.interaction is not None:
            await ctx.defer()
        post = open_template("yugioh.png", "https://i.imgur.com/bPMhqIY.jpg") 
        font = asset_font("ARIAL.TTF", 25)
        line1, line2 = msg.split("|")
        W = 88
        H1 = 80
        
        draw = ImageDraw.Draw(post)
        lines = textwrap.wrap(line1, 10)   
        for line in lines:
            w1, h1 = text_size(draw, line, font)
            draw.text((W - w1 / 2, H1), line, (0, 0, 0), font=font)
            H1 += h1     
              
        W2 = 88
        H2 = 299
        lines2 = textwrap.wrap(line2, 10)   
        for line in lines2:
            w2, h2 = text_size(draw, line, font)
            draw.text((W2 - w2 / 2, H2), line, (0, 0, 0), font=font)
            H2 += h2 

        post.save(output_path("yugioh.png"))
        await ctx.send(file=discord.File(output_path("yugioh.png"))) 

    @commands.hybrid_command(name='yugiohpfp', aliases=['Yugiohpfp'])
    async def yugiohpfp(self, ctx, member: Greedy[discord.Member]): 
        post = open_template("yugioh.png", "https://i.imgur.com/bPMhqIY.jpg") 
        asset1 = member[0].display_avatar.replace(size=128)
        data1 = BytesIO(await asset1.read())   
        pfp1 = Image.open(data1)
        pfp1 = pfp1.resize((171, 180)) 
        post.paste(pfp1, (3, 71))     

        asset = member[1].display_avatar.replace(size=128)
        data = BytesIO(await asset.read())   
        pfp = Image.open(data)
        pfp = pfp.resize((168, 167)) 
        post.paste(pfp, (6, 286))
        post.save(output_path("yugiohpfp.jpg"))
        await ctx.send(file=discord.File(output_path("yugiohpfp.jpg")))  

    @commands.hybrid_command(name='imagify', aliases=["img","Img", "Imagify"])
    async def imagify(self, ctx, *, text):
        if ctx.interaction is not None:
            await ctx.defer()
        
        post = open_template("profile.png", "https://i.imgur.com/CFvwPZQ.jpg")
        font = asset_font("Product_Sans_Regular.ttf", 30) 
        W2 = 210
        H2 = 20
        
        draw = ImageDraw.Draw(post)
        lines = textwrap.wrap(text, 25)   
        for line in lines:
            w2, h2 = text_size(draw, line, font)
            draw.text((W2 - w2 / 2, H2), line, (255, 255, 255), font=font)
            H2 += h2
        post.save(output_path("img.jpg"))
        await ctx.send(file=discord.File(output_path("img.jpg")))     

    @commands.hybrid_command(name='pro', aliases=["Pro"])
    async def pro(self, ctx, member: discord.Member = None):
        if ctx.interaction is not None:
            await ctx.defer()
        if member is None:
            member = ctx.author
           
        post = open_template("pro.png", "https://i.imgur.com/fAkM4cd.png").convert('RGBA')     
        asset1 = member.display_avatar.replace(size=128)
        data1 = BytesIO(await asset1.read())   
        pfp1 = Image.open(data1)
        pfp1 = pfp1.resize((110, 110)) 
        
        drw = ImageDraw.Draw(post)
        drw.ellipse((100, 300, 100, 300), fill=(0, 0, 0, 0))
        ImageDraw.floodfill(post, xy=(14, 24), value=(0, 0, 0, 0), thresh=40)
        post.paste(pfp1, (30, 87))
        post.save(output_path("profile.png"))
        await ctx.send(file=discord.File(output_path("profile.png"))) 

async def setup(bot):
    await bot.add_cog(MemeGen(bot))
