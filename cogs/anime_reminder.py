import discord
from discord.ext import commands, tasks
from discord.ext.commands import BucketType
import requests
from lxml import html
import asyncio
import math
from bot_utils import (
    get_driver,
    DriverUnavailableError,
    listed,
    chan,
    upd,
    airingg,
    BOT_OWNER_ID,
    ENABLE_ANIME_UPDATES,
    utc_now
)

class AnimeReminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if ENABLE_ANIME_UPDATES:
            self.checkNewLoop.start()

    def cog_unload(self):
        if ENABLE_ANIME_UPDATES:
            self.checkNewLoop.cancel()

    @tasks.loop(minutes=15)
    async def checkNewLoop(self):
        try:
            anime = self.check_new()
        except DriverUnavailableError as exc:
            print(f"Anime update check skipped: {exc}")
            return
        except Exception as exc:
            print(f"Anime update check failed: {exc}")
            owner = self.bot.get_user(BOT_OWNER_ID)
            if owner is None:
                try:
                    owner = await self.bot.fetch_user(BOT_OWNER_ID)
                except Exception:
                    owner = None
            if owner is not None:
                try:
                    await owner.send(f"Error in checkNewLoop: {exc}")
                except Exception:
                    pass
            return

        if not anime:
            print("nothing new")
        else:
            try:    
                for ani in anime:
                    title = ani['titles']
                    episode = ani['episodes']
                    image = ani['image']
                    anime_id = ani['id']
                    em = discord.Embed(title=title, description=f"{episode} just dropped", color=0x00ebff)
                    em.set_image(url=image)
                    
                    owner = self.bot.get_user(BOT_OWNER_ID)
                    if owner is None:
                        try:
                            owner = await self.bot.fetch_user(BOT_OWNER_ID)
                        except Exception:
                            owner = None

                    if anime_id != "None":
                        docs = listed.find({"watchlist": anime_id, "toggle": 1}) 
                        if docs is not None:
                            users = []
                            for doc in docs: 
                                users.append(doc['_id'])
                                
                            for user in users:
                                try:
                                    member = await self.bot.fetch_user(user)
                                    await member.send(embed=em)
                                except Exception:    
                                    print("can't dm")
                    else:                
                        if owner is not None:
                            await owner.send(f"id issues in {title}")                
                    
                    posts = chan.find()
                    channels = []
                    for post in posts:
                        channels.append(post['chnl'])
                    for channel in channels:
                        chnnl = self.bot.get_channel(channel)
                        try:
                            if chnnl is None:
                                chan.delete_one({'chnl': channel})
                                print(f'deleted {channel}')
                            else:  
                                await chnnl.send(embed=em) 
                        except Exception:
                            print("can't post")                   
            except Exception: 
                if owner is not None:
                    try:
                        await owner.send("Error in checknewLoop!")                   
                    except Exception:
                        pass
        print('checked')

    @checkNewLoop.before_loop
    async def before_check_new(self):
        await self.bot.wait_until_ready()

    def check_new(self):
        link = "https://animixplay.to"
        get_driver().get(link)
        r = get_driver().page_source
        tree = html.fromstring(r)
        newanime = []
        anime = tree.xpath('//*[@id="resultplace"]/ul/li')
        
        for anim in anime:
            title = (anim.xpath('.//a/@title'))[0]
            episode = (anim.xpath('.//a/div[@class = "details"]/p[@class = "infotext"]')[0].text)
            posst = {'titles': title, 'episodes': episode}
            ccc = upd.find_one(posst)
            
            if ccc is None:
                watch = anim.xpath('.//a/@href')
                image = anim.xpath('.//a/div[@class = "searchimg"]/img/@src')
                url = link + watch[0]
                mix_id = self.findmixid(url)
                upd.insert_one(posst)
                if mix_id is not None:
                    newanime.append({'titles': title, 'episodes': episode, 'image': image[0], 'id': mix_id})
                else:
                    newanime.append({'titles': title, 'episodes': episode, 'image': image[0], 'id': 'None'})
        return newanime

    def findmixid(self, url):
        get_driver().get(url)
        r = get_driver().page_source
        tree = html.fromstring(r)
        anime = tree.xpath('//*/a[@id = "animebtn2"]/@href')
        if anime != []:
            id_split = anime[0].split('/')
            animeid = id_split[2]
            return animeid
        else:
            return None

    def findmixid_search(self, url):
        # Helper function used by other command search
        get_driver().get(url)
        r = get_driver().page_source
        tree = html.fromstring(r)
        anime = tree.xpath('//*/td[@class = "borderClass bgColor0"]/div[1]/a[1]/@href')
        if anime != []:
            id_split = anime[0].split('/')
            animeid = id_split[4]
            return animeid
        else:
            return None

    @commands.command(name='updateairing')
    async def updateairing(self, ctx, season): 
        owner = self.bot.get_user(BOT_OWNER_ID)
        if owner is None:
            try:
                owner = await self.bot.fetch_user(BOT_OWNER_ID)
            except Exception:
                owner = None
        if ctx.author.id == BOT_OWNER_ID:
            link = 'http://myanimelist.net/anime/season'
            r = requests.get(link)
            mall = html.fromstring(r.content)
            anime = mall.xpath('//*/h2[@class = "h2_anime_title"]')
            titles = []
            animelink = []
            animeid = []
            for ani in anime:
                name = ani.xpath('.//a')[0].text
                link_url = ani.xpath('.//a/@href')[0]
                id_split = link_url.split('/')
                animelink.append(link_url)
                animeid.append(id_split[4])
                titles.append(name) 
            print(titles)    
            doc = airingg.find()
            count = 0
            for d in doc:
                count += 1
                airingg.delete_one({'_id': d['_id']})  
            await ctx.send(f"deleted {count}")  
            num = 0  
            for title, idd, url in zip(titles, animeid, animelink):
                post = {'_id': idd, 'name': title, 'url': url}
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
                link2 = ani2.xpath('.//a/@href')[0]
                id2 = link2.split('/')
                animelink2.append(link2)
                animeid2.append(id2[4])
                titles2.append(name2)
            num2 = 0 
            for title2, idd2, url2 in zip(titles2, animeid2, animelink2):
                if idd2 not in animeid:
                    post2 = {'_id': idd2, 'name': title2, 'url': url2}
                    airingg.insert_one(post2)
                    num2 += 1
                    
            await ctx.send(f"added {num2}\nTotal {num + num2}") 

    @commands.hybrid_command(name='airing', aliases=["Air", "Airing", "air"])
    @commands.cooldown(2, 80, BucketType.user) 
    async def air(self, ctx):
        docs = airingg.find()
        titles = []
        animeid = []
        for doc in docs:
            animeid.append(doc['_id'])
            titles.append(doc['name'])
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
        x = 0
        y = 10
        cur_page = 1
        namee = ""
        
        pages = math.ceil(len(titles) / 10)
        for name, idd in zip(titles[x:y], animeid[x:y]):
            namee += f'{titles.index(name) + 1}. {name} - `{idd}`\n\n'
        embb = discord.Embed(title="Airing Animes:", description=namee, color=0x00ebff)
        embb.set_footer(text=f"{cur_page}/{pages}")
        message = await ctx.send(embed=embb) 
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    namee = ""
                    cur_page += 1
                    x += 10
                    y += 10
                    for name, idd in zip(titles[x:y], animeid[x:y]):
                        namee += f'{titles.index(name) + 1}. {name} - `{idd}`\n\n'
                    if namee != "":    
                        em = discord.Embed(title="Airing Animes:", description=namee, color=0x00ebff)
                        em.set_footer(text=f"{cur_page}/{pages}")
                        await message.edit(embed=em)
                    
                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    namee = ""
                    cur_page -= 1    
                    x -= 10
                    y -= 10
                    
                    for name, idd in zip(titles[x:y], animeid[x:y]):
                        namee += f'{titles.index(name) + 1}. {name} - `{idd}`\n\n'
                    emb = discord.Embed(title="Airing Animes:", description=namee, color=0x00ebff)
                    emb.set_footer(text=f"{cur_page}/{pages}")
                    await message.edit(embed=emb)
            except asyncio.TimeoutError:
                return               

    @commands.command(name='awl', aliases=["addwatchlist"])
    async def addwatchlist(self, ctx, code):  
        userid = ctx.author.id
        docs = airingg.find_one({"_id": code})
        if docs is not None:
            doc = listed.find_one({"_id": userid})  
            if doc is None:
                listed.insert_one({"_id": userid, "watchlist": [], "toggle": 1})
                listed.update_one({"_id": userid}, {"$push": {"watchlist": code}})
                await ctx.reply(f"`{code} - {docs['name']} has been added in watchlist`")
            elif doc is not None and len(doc['watchlist']) < 10:
                listed.update_one({"_id": userid}, {"$push": {"watchlist": code}})
                await ctx.reply(f"`{code} - {docs['name']} has been added in watchlist`")
            else:
                await ctx.reply("`your watchlist is full, remove any anime to enter new one`")  
        else:
            await ctx.reply("`Cant find the anime, Maybe its not airing right now`\nCheck using `S.airing`")        

    @commands.command(name='rwl', aliases=["removewatchlist"])
    async def removewatchlist(self, ctx, code):  
        userid = ctx.author.id
        doc = listed.find_one({"_id": userid})  
        if doc is None:
            listed.insert_one({"_id": userid, "watchlist": [], "toggle": 1})
            await ctx.reply("`your watchlist is already empty`")
        elif doc is not None and len(doc['watchlist']) > 0 and code in doc['watchlist']:
            listed.update_one({"_id": userid}, {"$pull": {"watchlist": code}})
            await ctx.reply(f"`{code}` has been removed from your watchlist")
        elif doc is not None and len(doc['watchlist']) == 0:
            await ctx.reply("`your watchlist is already empty`")
        else:
            await ctx.reply("`Its not in your watchlist`")

    @commands.command(name='watchlist', aliases=["Watchlist", "wl", "Wl"])
    @commands.cooldown(2, 80, BucketType.user) 
    async def watchlist(self, ctx, member: discord.Member = None):   
        if member is None:
            member = ctx.author
        userid = member.id
        doc = listed.find_one({"_id": userid})
        if doc is not None:
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
                if docs is None:
                    listed.update_one({"_id": userid}, {"$pull": {"watchlist": ani}})
                else:    
                    name += f"[{docs['name']}]({docs['url']}) - `{ani}`  \n"
                    slot += 1        
            em = discord.Embed(title="Watchlist", description=f"User : {member.mention}\nAvailable Slots : {slot}/10\nReminder - {rem}\n\n{name}", color=0x00ebff) 
            await ctx.reply(embed=em)
        elif doc is None:
            em = discord.Embed(title="Watchlist", description=f"User : {member.mention}\nAvailable Slots : 10/10\nReminder - Off\n\nUse `S.awl [animeid]` to add", color=0x00ebff) 
            await ctx.reply(embed=em)     

    @commands.command(name='remind', aliases=["Remind"])
    async def remind(self, ctx):
        userid = ctx.author.id
        doc = listed.find_one({"_id": userid})
        if doc is None:
            listed.insert_one({"_id": userid, "watchlist": [], "toggle": 1})
            await ctx.reply("`Reminder Enabled`")
        elif doc is not None:
            if doc["toggle"] == 1:
                listed.update_one({"_id": userid}, {"$set": {"toggle": 0}})
                await ctx.reply("`Reminder Disabled`")
            elif doc["toggle"] == 0:  
                listed.update_one({"_id": userid}, {"$set": {"toggle": 1}})
                await ctx.reply("`Reminder Enabled`") 

    @commands.command(name='setchannel')
    @commands.has_permissions(manage_guild=True)
    async def setchannel(self, ctx, channel: discord.TextChannel): 
        try:   
            guildid = ctx.guild.id
            doc = chan.find_one({"_id": guildid})
            if doc is not None:
                chan.update_one({"_id": guildid}, {"$set": {"chnl": channel.id}})
                await ctx.reply(f'{channel.mention} has been set for anime episode reminders!\n`Make sure Stela has permissions to send message there`')
            elif doc is None:
                post = {'_id': guildid, 'chnl': channel.id}
                chan.insert_one(post)
                await ctx.reply(f'{channel.mention} has been set for anime episode reminders!\n`Make sure Stela has permissions to send message there`')
            else:
                await ctx.reply('Something went wrong... join support server for help')
        except Exception:
            return                    
               
    @commands.command(name='removechannel')
    @commands.has_permissions(manage_guild=True)
    async def removechannel(self, ctx): 
        try:   
            guildid = ctx.guild.id
            doc = chan.find_one({"_id": guildid})
            if doc is not None:
                chal = doc['chnl']
                channel = self.bot.get_channel(chal)
                chan.delete_one({"_id": guildid})
                if channel is not None:
                    await ctx.reply(f'{channel.mention} has been removed for anime episode reminders!')
                else:
                    await ctx.reply('Channel removed from database.')
            elif doc is None:
                await ctx.reply("This server doesn't have an anime reminder channel\n`Set it using `S.setchannel <mention channel>")
            else:
                await ctx.reply('Something went wrong... join support server for help')
        except Exception:
            return

async def setup(bot):
    await bot.add_cog(AnimeReminder(bot))
