import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import requests
from bs4 import BeautifulSoup
from lxml import html
import asyncio
import math
from io import BytesIO
from mal import Manga, MangaSearch, AnimeSearch
from bot_utils import (
    mal_collect,
    girl,
    airingg,
    utc_now
)

def findid(anime):
    link = f"https://myanimelist.net/anime.php?cat=anime&q={anime}"
    r = requests.get(link)
    tree = html.fromstring(r.content)
    anime_list = tree.xpath('//*/td[@class = "borderClass bgColor0"]/div[1]/a[1]/@href')
    if anime_list != []:
        id_split = anime_list[0].split('/')
        animeid = id_split[4]
        return animeid
    else:
        return None

def findname(id_val):
    link = f"https://myanimelist.net/anime/{id_val}"
    r = requests.get(link)
    tree = html.fromstring(r.content)
    anime = tree.xpath('//*[@itemprop = "name"]/h1/strong')[0].text
    if anime != []:
        return anime
    else:
        return None

class AnimeManga(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="anime", aliases=["Anime"])
    async def anime(self, ctx, *, anime_name):
        try:
            anime_id = findid(anime_name)   
            if anime_id is not None:
                link = f'https://myanimelist.net/anime/{anime_id}' 
                r = requests.get(link)
                soup = BeautifulSoup(r.content, features="lxml")
                japanese = soup.find("h1", {"class" : "title-name h1_bold_none"})
                english = soup.find("p", {"class" : "title-english title-inherit"})
                jap = japanese.text if japanese else anime_name
                
                synop = soup.find("p", {"itemprop" : "description"})
                synopsis = synop.text if synop else "Synopsis Not Available"
                
                if english is not None:
                    embed = discord.Embed(description=f'**[{jap}]({link})** \nalso known as {english.text}\n{synopsis}', timestamp=utc_now(), color=0xff0092)
                else:
                    embed = discord.Embed(description=f'**[{jap}]({link})** \n{synopsis}', timestamp=utc_now(), color=0xff0092)   
                
                rate = soup.find("div", {"class" : "fl-l score"})
                rating = rate.div.text if rate and rate.div else "Not Available"
                
                rank = soup.find("span", {"class" : "numbers ranked"})
                ranks = rank.text if rank else "Not Available"    
                
                imgstat = soup.find("td", {"class" : "borderClass"})
                try:
                    image = imgstat.div.div.a.img['data-src']
                except Exception:
                    image = "https://www.indiaspora.org/wp-content/uploads/2018/10/image-not-available.jpg"    
                
                stats = soup.find_all("span", {"class" : "dark_text"})
                episode = ""
                status = ""
                air = ""
                tyype = ""
                for stat in stats:
                    if 'Episodes:' in stat.text:
                        try:
                            episode += stat.nextSibling
                        except Exception:
                            episode += "Not Available"    
                    elif 'Type:' in stat.text:
                        if stat.parent.a is not None:
                            tyype += stat.parent.a.text
                        elif stat.nextSibling is not None:
                            tyype += stat.nextSibling   
                        else:
                            tyype += "Not Available"    
                    elif 'Status:' in stat.text:
                        status += stat.nextSibling
                    elif 'Aired:' in stat.text: 
                        try: 
                            air += stat.nextSibling 
                        except Exception:
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
                
                embed.add_field(name="**⌛ Status**", value=status, inline=False)
                embed.add_field(name="**📺 Total Episodes**", value=episode, inline=True)
                embed.add_field(name="**📡 Aired**", value=air, inline=True)
                embed.add_field(name="**💻 Type**", value=tyype, inline=True)
                embed.add_field(name="**🎬 Genre**", value=genre, inline=False)
                embed.add_field(name="**⭐ Rating**", value=f'{rating}/10', inline=True)
                embed.add_field(name="**🎖️ Rank**", value=f'**{ranks}**', inline=False)
                embed.set_footer(text=f'Requested by {ctx.author}')
                embed.set_thumbnail(url=image)
                await ctx.send(embed=embed)
            else:
                await ctx.reply('that anime could not be found. It may not exist, or you may have misspelled its name.')
        except Exception:
            await ctx.reply('Something went wrong! pls report this to support server!')                    

    @commands.hybrid_command(name="manga", aliases=["Manga"])
    async def manga(self, ctx, *, manga_name):
        try:
            search = MangaSearch(manga_name) 
            AManga = Manga(search.results[0].mal_id)
            x = ","
            gen = ""
            for genre in AManga.genres:
                if genre == AManga.genres[-1]:
                    x = "."
                gen += f"{genre}{x} "
            embed = discord.Embed(description=f'**[{search.results[0].title}]({search.results[0].url})** \n{AManga.synopsis}', timestamp=utc_now(), color=0xff0092)
            embed.add_field(name="**⌛ Status**", value=AManga.status)          
            embed.add_field(name="**📕 Total Chapters**", value=AManga.chapters)
            embed.add_field(name="**📚 Total Volumes**", value=AManga.volumes)
            embed.add_field(name="**🗓️ Published**", value=AManga.published, inline=True)
            embed.add_field(name="**🎨 Type**", value=AManga.type, inline=True)
            embed.add_field(name="**🎬 Genre**", value=gen, inline=False)
            embed.add_field(name="**⭐ Rating**", value=f'{AManga.score}/10', inline=True)
            embed.add_field(name="**🎖️ Rank**", value=f'**Top {AManga.rank}**', inline=False)
            embed.set_footer(text=f'Requested by {ctx.author}')
            embed.set_thumbnail(url=AManga.image_url)
            await ctx.send(embed=embed)
        except Exception:
            await ctx.reply("Manga not found or error occurred.")

    @commands.hybrid_command(name='char', aliases=["Char", "character", "Character"])
    async def char(self, ctx, *, word): 
        try:
            link = f"https://myanimelist.net/character.php?cat=character&q={word}"
            r = requests.get(link)
            soup = BeautifulSoup(r.content, features="lxml")
            spans = soup.find("td", {"class" : "borderClass bgColor1"}, width="175")
            img = soup.find('img', {'class': 'lazyload'})
            
            embed = discord.Embed(title="Character Result", description=f"[{spans.a.string}]({spans.a['href']})")
            imgg = img['data-src']
            imgg = imgg.replace("r/42x62/", "")
            embed.set_image(url=imgg)
            await ctx.send(embed=embed) 
        except Exception:
            await ctx.send("Character not found.")

    @commands.command(name='eplist', aliases=["Eplist"])
    async def eplist(self, ctx, *, word):  
        try:   
            filler_string = word.replace(" ", "-")
            link = "https://www.animefillerlist.com/shows/" + filler_string
            r = requests.get(link)
            
            soup = BeautifulSoup(r.content, features="lxml")
            spans = soup.find_all('td', attrs={"class": "Type"})
            spanss = soup.find_all('td', attrs={"class": "Title"})
            numbers = ""
            count = 1
            ep = len(spans)
            
            for (span, spa) in zip(spans, spanss):
                numbers += f"**EP {count}**. {span.get_text(strip=True)}:\n||[{spa.get_text(strip=True)}]||\n"
                count += 1
                if count > 10:
                    break    
                         
            em = discord.Embed(description=f"**[{word} Episode List]({link})**", color=ctx.author.color)    
            em.add_field(name=f"Total Episodes : {ep}", value=numbers)
            em.set_footer(text=f"Reply with the episode number\nRequested by {ctx.author}")
            msg1 = await ctx.send(embed=em) 
            def check(msg):
                return msg.author == ctx.author and ctx.channel == msg.channel and msg.content.isdigit()
            try:
                msg2 = await self.bot.wait_for('message', check=check, timeout=30)
                msg3 = int(msg2.content)
                no = msg3 - 1
                num = msg3
                lis = ""
                nom = 0
                for (span, spa) in zip(spans[no:], spanss[no:]):
                    lis += f"**EP {num}**. {span.get_text(strip=True)}:\n||[{spa.get_text(strip=True)}]||\n"
                    num += 1
                    nom += 1
                    if nom > 10:
                        break 
                emb = discord.Embed(description=f"**[{word} Episode List]({link})**", color=ctx.author.color)    
                emb.add_field(name=f"Total Episodes : {ep}", value=lis)
                emb.set_footer(text=f'Requested by {ctx.author}')
                try:
                    await msg1.delete()
                except Exception:
                    pass
                await ctx.send(embed=emb) 
            except asyncio.TimeoutError:
                em1 = discord.Embed(description="**Timeout**")   
                await ctx.send(embed=em1)  
        except Exception:
            em = discord.Embed(title="Not found")
            await ctx.send(embed=em, delete_after=30)

    @commands.command(name='filler', aliases=["Filler", "Fill", "fill"])
    async def filler(self, ctx, *, word):  
        try:  
            filler_string = word.replace(" ", "-")
            link = "https://www.animefillerlist.com/shows/" + filler_string
            r = requests.get(link)    
            soup = BeautifulSoup(r.content, features="lxml")
            spans = soup.find_all('div', attrs={"class": "filler"})
            
            numbers = ""
            for span in spans:
                numbers += f"{span.get_text(strip=True)}, "
            emb = discord.Embed(description=f"**[{word} Filler List]({link})**", color=ctx.author.color)
            emb.add_field(name="**Filler Episodes:**", value=numbers[16:])  
            emb.set_footer(text=f'Requested by {ctx.author}')  
            await ctx.send(embed=emb)
        except Exception:
            em = discord.Embed(title="Not found")
            await ctx.send(embed=em, delete_after=30)

    @commands.command(name='setmal', aliases=["Setmal", "setprofile", "Setprofile"])
    async def setmal(self, ctx, *, word): 
        userid = ctx.author.id
        doc = mal_collect.find_one({"_id": userid})
        if doc is not None:
            await ctx.reply("You already have your id tagged!\nTry `S.resetmal <your myanimelist id>` to reset!")
        else:
            post = {"_id": userid, "mal_id": word}
            mal_collect.insert_one(post)
            await ctx.reply("done! Check your profile `S.profile`")

    @commands.command(name='resetmal', aliases=["Resetmal"])
    async def resetmal(self, ctx, *, word): 
        userid = ctx.author.id
        doc = mal_collect.find_one({"_id": userid})
        if doc is not None:
            mal_collect.update_one({"_id": userid}, {"$set": {"mal_id": word}})
            await ctx.reply("done")
        else:
            await ctx.reply("Set your id using `S.set <your myanimelist id>`")

    @commands.command(name='removemal', aliases=["Removemal"])
    async def removemal(self, ctx):
        userid = ctx.author.id
        doc = mal_collect.find_one({"_id": userid})
        if doc is not None:
            mal_collect.delete_one({"_id": userid})
            await ctx.reply("done")
        else:
            await ctx.reply("You haven't tagged your account with your id yet...")

    @commands.hybrid_command(name='profile', aliases=["Profile"])
    async def profile(self, ctx, *, member: discord.Member = None): 
        try:
            if member is None:
                member = ctx.author
            userid = member.id
            doc = mal_collect.find_one({"_id": userid})
            if doc is not None:
                mal_id = doc["mal_id"]
                link = f"https://myanimelist.net/profile/{mal_id}"
                linkanime = f"https://myanimelist.net/animelist/{mal_id}"
                linkmanga = f"https://myanimelist.net/mangalist/{mal_id}"
                r = requests.get(link)

                soup = BeautifulSoup(r.content, features="lxml")
                spans = soup.find_all('span', attrs={"class": "di-ib fl-r lh10"})
                numbers = []
                for span in spans:
                    numbers.append(span.string)
                numb = []    
            
                entries = soup.find_all('span', attrs={"class": "di-ib fl-r"})
                for entry in entries:
                    numb.append(entry.string)    
            
                score = soup.find('div', attrs={"class": "di-tc ar pr8 fs12 fw-b"}).get_text(strip=True)
                days = soup.find('div', attrs={"class": "di-tc al pl8 fs12 fw-b"}).get_text(strip=True)
                img = soup.find('img', attrs={"class": "lazyload"})['data-src']
                
                em = discord.Embed(description=f"**[{member.display_name}'s Anime List]({linkanime})**\nMal user: {mal_id}", color=ctx.author.color)   
                em.add_field(name="Watching:", value=numbers[0])
                em.add_field(name="Completed:", value=numbers[1])
                em.add_field(name="On Hold:", value=numbers[2])
                em.add_field(name="Dropped:", value=numbers[3])
                em.add_field(name="Plan to Watch:", value=numbers[4])
                em.add_field(name="Total Entries:", value=numb[0])
                em.add_field(name="Rewatched:", value=numb[1])
                em.add_field(name="Total Episodes:", value=numb[2])
                em.add_field(name="Mean Score:", value=score[11:])
                em.add_field(name="Days:", value=days[5:])
                em.set_thumbnail(url=img)
                em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
                em.set_footer(text=f'Requested by {ctx.author}')
                
                msg = await ctx.send(embed=em)
                await msg.add_reaction("🌟")
                await msg.add_reaction("🖌️")
                def check(reaction, user):
                    return str(reaction.emoji) in ["🌟", "🔖", "🖌️"] and user != self.bot.user and reaction.message.id == msg.id and user == ctx.author

                while True:
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
                        if str(reaction.emoji) == "🌟":
                            favs = soup.find_all('li', attrs={"class": "btn-fav"})
                            favanime = ""
                            favmanga = ""
                            favcharacter = ""
                            for fav in favs:
                                if '/anime/' in fav.a['href']:
                                    favanime += f"[{fav['title']}]({fav.a['href']})\n"
                                if '/manga/' in fav.a['href']:
                                    favmanga += f"[{fav['title']}]({fav.a['href']})\n"
                                if '/character/' in fav.a['href']:
                                    favcharacter += f"[{fav['title']}](https://myanimelist.net{fav.a['href']})\n"    
                            if favmanga == "":
                                favmanga = "None"
                            if favanime == "":
                                favanime = "None" 
                            if favcharacter == "":
                                favcharacter = "None"           
                            emb = discord.Embed(description=f"**[{member.display_name}'s Profile]({link})**\nMal user: {mal_id}", color=ctx.author.color)   
                            emb.add_field(name="Favourite Anime:", value=favanime)  
                            emb.add_field(name="Favourite Manga:", value=favmanga)
                            emb.add_field(name="Favourite Character:", value=favcharacter)   
                            emb.set_thumbnail(url=img)    
                            await msg.edit(embed=emb)  
                            try:
                                await msg.remove_reaction(reaction, user) 
                                await msg.remove_reaction("🌟", self.bot.user)
                            except Exception:
                                pass
                            await msg.add_reaction("🔖") 
                            await msg.add_reaction("🖌️")
                        if str(reaction.emoji) == "🔖":
                            await msg.edit(embed=em) 
                            try:
                                await msg.remove_reaction(reaction, user)
                                await msg.remove_reaction("🔖", self.bot.user)
                            except Exception:
                                pass
                            await msg.add_reaction("🌟")  
                            await msg.add_reaction("🖌️")
                        if str(reaction.emoji) == "🖌️":
                            embb = discord.Embed(description=f"**[{member.display_name}'s Manga List]({linkmanga})**\nMal user: {mal_id}", color=ctx.author.color)
                            embb.add_field(name="Reading:", value=numbers[5])
                            embb.add_field(name="Completed:", value=numbers[6])
                            embb.add_field(name="On Hold:", value=numbers[7])
                            embb.add_field(name="Dropped:", value=numbers[8])
                            embb.add_field(name="Plan to Watch:", value=numbers[9])
                            embb.add_field(name="Total Entries:", value=numb[3])
                            embb.add_field(name="Reread:", value=numb[4])
                            embb.add_field(name="Chapters:", value=numb[5])
                            embb.add_field(name="Volumes:", value=numb[6])
                        
                            embb.set_thumbnail(url=img)
                            embb.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
                            embb.set_footer(text=f'Requested by {ctx.author}')
                            await msg.edit(embed=embb) 
                            try:
                                await msg.remove_reaction(reaction, user)
                                await msg.remove_reaction("🖌️", self.bot.user)
                            except Exception:
                                pass
                            await msg.add_reaction("🌟")
                            await msg.add_reaction("🔖")
                    except asyncio.TimeoutError:
                        return
            else:
                await ctx.send("Set your mal id first")    
        except Exception:
            await ctx.send("Not found! Check your mal id")

    @commands.hybrid_command(name='mal', aliases=["Mal"])
    async def mal(self, ctx, *, word): 
        try:
            link = f"https://myanimelist.net/profile/{word}"
            linkanime = f"https://myanimelist.net/animelist/{word}"
            linkmanga = f"https://myanimelist.net/mangalist/{word}"
            r = requests.get(link)

            soup = BeautifulSoup(r.content, features="lxml")
            spans = soup.find_all('span', attrs={"class": "di-ib fl-r lh10"})
            numbers = []
            for span in spans:
                numbers.append(span.string)
            numb = []    
        
            entries = soup.find_all('span', attrs={"class": "di-ib fl-r"})
            for entry in entries:
                numb.append(entry.string)    
            
            score = soup.find('div', attrs={"class": "di-tc ar pr8 fs12 fw-b"}).get_text(strip=True)
            days = soup.find('div', attrs={"class": "di-tc al pl8 fs12 fw-b"}).get_text(strip=True)
            img = soup.find('img', attrs={"class": "lazyload"})['data-src']
            
            em = discord.Embed(description=f"**[{word}'s Anime List]({linkanime})**", color=ctx.author.color)   
            em.add_field(name="Watching:", value=numbers[0])
            em.add_field(name="Completed:", value=numbers[1])
            em.add_field(name="On Hold:", value=numbers[2])
            em.add_field(name="Dropped:", value=numbers[3])
            em.add_field(name="Plan to Watch:", value=numbers[4])
            em.add_field(name="Total Entries:", value=numb[0])
            em.add_field(name="Rewatched:", value=numb[1])
            em.add_field(name="Total Episodes:", value=numb[2])
            em.add_field(name="Mean Score:", value=score[11:])
            em.add_field(name="Days:", value=days[5:])
            em.set_thumbnail(url=img)
            em.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
            em.set_footer(text=f'Requested by {ctx.author}')
            
            msg = await ctx.send(embed=em)
            await msg.add_reaction("🌟")
            await msg.add_reaction("🖌️")
            def check(reaction, user):
                return str(reaction.emoji) in ["🌟", "🔖", "🖌️"] and user != self.bot.user and reaction.message.id == msg.id and user == ctx.author

            while True:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
                    if str(reaction.emoji) == "🌟":
                        favs = soup.find_all('li', attrs={"class": "btn-fav"})
                        favanime = ""
                        favmanga = ""
                        favcharacter = ""
                        for fav in favs:
                            if '/anime/' in fav.a['href']:
                                favanime += f"[{fav['title']}]({fav.a['href']})\n"
                            if '/manga/' in fav.a['href']:
                                favmanga += f"[{fav['title']}]({fav.a['href']})\n"
                            if '/character/' in fav.a['href']:
                                favcharacter += f"[{fav['title']}](https://myanimelist.net{fav.a['href']})\n"    
                        if favmanga == "":
                            favmanga = "None"
                        if favanime == "":
                            favanime = "None" 
                        if favcharacter == "":
                            favcharacter = "None"           
                        emb = discord.Embed(description=f"**[{word}'s Profile]({link})**", color=ctx.author.color)   
                        emb.add_field(name="Favourite Anime:", value=favanime)  
                        emb.add_field(name="Favourite Manga:", value=favmanga)
                        emb.add_field(name="Favourite Character:", value=favcharacter)   
                        emb.set_thumbnail(url=img)    
                        await msg.edit(embed=emb)  
                        try:
                            await msg.remove_reaction(reaction, user) 
                            await msg.remove_reaction("🌟", self.bot.user)
                        except Exception:
                            pass
                        await msg.add_reaction("🔖") 
                        await msg.add_reaction("🖌️")
                    if str(reaction.emoji) == "🔖":
                        await msg.edit(embed=em) 
                        try:
                            await msg.remove_reaction(reaction, user)
                            await msg.remove_reaction("🔖", self.bot.user)
                        except Exception:
                            pass
                        await msg.add_reaction("🌟")  
                        await msg.add_reaction("🖌️")
                    if str(reaction.emoji) == "🖌️":
                        embb = discord.Embed(description=f"**[{word}'s Manga List]({linkmanga})**", color=ctx.author.color)
                        embb.add_field(name="Reading:", value=numbers[5])
                        embb.add_field(name="Completed:", value=numbers[6])
                        embb.add_field(name="On Hold:", value=numbers[7])
                        embb.add_field(name="Dropped:", value=numbers[8])
                        embb.add_field(name="Plan to Watch:", value=numbers[9])
                        embb.add_field(name="Total Entries:", value=numb[3])
                        embb.add_field(name="Reread:", value=numb[4])
                        embb.add_field(name="Chapters:", value=numb[5])
                        embb.add_field(name="Volumes:", value=numb[6])
                    
                        embb.set_thumbnail(url=img)
                        embb.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
                        embb.set_footer(text=f'Requested by {ctx.author}')
                        await msg.edit(embed=embb) 
                        try:
                            await msg.remove_reaction(reaction, user)
                            await msg.remove_reaction("🖌️", self.bot.user)
                        except Exception:
                            pass
                        await msg.add_reaction("🌟")
                        await msg.add_reaction("🔖")
                except asyncio.TimeoutError:
                    return
        except Exception:
            em = discord.Embed(title="Not found")
            await ctx.send(embed=em)

    @commands.hybrid_command(name='recommend', aliases=["Recommend", "recom", "Recom"])
    async def recommend(self, ctx): 
        try:
            link = "https://myanimelist.net/recommendations.php?s=recentrecs&t=anime"
            r = requests.get(link)
            
            soup = BeautifulSoup(r.content, features="lxml")
            spans = soup.find_all('a', attrs={"class": "hoverinfo_trigger"})
            anime_list = []
            animelink = []
            count = 0
            x = 0
            y = 0
            for span in spans:
                anime_list.append(span.img['alt'])
                animelink.append(span['href'])
                count += 1
                if count > 99:
                    break
            txt = soup.find_all('div', attrs={"class": "spaceit recommendations-user-recs-text"})
            
            em = discord.Embed(title="Anime Recommendations:", description=f"If you like [{anime_list[x]}]({animelink[x]})\nThen try [{anime_list[x+1]}]({animelink[x+1]})", color=ctx.author.color)
            em.add_field(name="Why?", value=txt[y].string)
            msg = await ctx.reply(embed=em)
            await msg.add_reaction("➡️")
            def check(reaction, user):
                return str(reaction.emoji) in ["⬅️", "➡️"] and user != self.bot.user and reaction.message.id == msg.id and user == ctx.author

            while True:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
                    if str(reaction.emoji) == "➡️":
                        x += 2
                        y += 1
                        emb = discord.Embed(title="Anime Recommendations:", description=f"If you like [{anime_list[x]}]({animelink[x]})\nThen try [{anime_list[x+1]}]({animelink[x+1]})", color=ctx.author.color)
                        emb.add_field(name="Why?", value=txt[y].string)
                        await msg.edit(embed=emb)
                except asyncio.TimeoutError:   
                    return
        except Exception:
            await ctx.send("Could not load recommendations.")

    @commands.hybrid_command(name='similar', aliases=["Similar"])
    async def similar(self, ctx, *, name):
        try:
            # Robust extraction of anime ID
            anime_id = findid(name)
            if anime_id is None:
                try:
                    search = AnimeSearch(name)
                    anime_id = search.results[0].mal_id
                except Exception:
                    await ctx.send("Anime not found.")
                    return
            
            link = f"https://myanimelist.net/anime/{anime_id}/"
            r = requests.get(link)
            recom = ""
            count = 1
            linkk = []
            namme = []
            try:
                soup = BeautifulSoup(r.content, features="lxml")
                spans = soup.find_all('li', attrs={"class": "btn-anime"})
                for span in spans:
                    recom += f"{count}. [{span['title']}]({span.a['href']})\n"
                    count += 1
                    namme.append(f"{count}. [{span['title']}]({span.a['href']})")
                    linkk.append(span.img['data-src'])
                    if count > 7:
                        break
            except Exception:
                sou = BeautifulSoup(r.content, features="lxml")
                spas = sou.find_all('li', attrs={"class": "btn-anime auto"})
                for spa in spas:
                    recom += f"{count}. [{spa['title']}]({spa.a['href']})\n"
                    namme.append(f"{count}. [{spa['title']}]({spa.a['href']})")
                    linkk.append(spa.img['src'])
                    count += 1
                    if count > 7:
                        break
            
            em = discord.Embed(title="Anime Recommendations:", description=recom, color=ctx.author.color)
            message = await ctx.reply(embed=em)
            emoji_numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
            for i in range(count - 1):
                await message.add_reaction(emoji_numbers[i])
            def check(reaction, user):
                return str(reaction.emoji) in emoji_numbers and user != self.bot.user and reaction.message.id == message.id and user == ctx.author
            while True:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=20)
                    index = emoji_numbers.index(reaction.emoji)
                    emb = discord.Embed(description=namme[index], color=ctx.author.color)
                    try:
                        image = linkk[index].replace("/r/90x140", "")
                        emb.set_image(url=image)
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
        except Exception:
            await ctx.send("Could not retrieve similar anime.")

    @commands.hybrid_command(name="rndqoute", aliases=["Rndqoute", "Rq", "rq"])
    async def rndquote(self, ctx):
        try:
            qoute = requests.get("https://animechan.vercel.app/api/random").json()
            anime = qoute['anime']
            character = qoute['character']
            line = qoute['quote']
            q = discord.Embed(timestamp=utc_now(), color=discord.Color(0x00ff7d))
            q.set_author(name="Random Qoute", icon_url=ctx.author.display_avatar.url)
            q.add_field(name=f"Anime: {anime}", value=f'"{line}"\n   -said by {character}')
            msg = await ctx.send(embed=q)
            await msg.add_reaction("<:AO_stonksup:843516237962149958>")
        except Exception:
            await ctx.send("Could not fetch a quote.")

async def setup(bot):
    await bot.add_cog(AnimeManga(bot))
