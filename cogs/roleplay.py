import discord
from discord.ext import commands
import random
import typing
from bot_utils import utc_now

class Roleplay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='blush')    
    async def blush(self, context, member: typing.Optional[discord.Member] = None, *, gifmsg=None):
        blushes = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff)
        if member is None:
            blushes.set_author(name=f"{context.message.author.display_name}  is Blushing >///<", icon_url=f"{context.message.author.display_avatar.url}") 
        else:
            blushes.set_author(name=f"{context.message.author.display_name}  turned red because of {member.display_name}!! kawaiiii......", icon_url=f"{context.message.author.display_avatar.url}") 
         
        blushgif = (
            'https://cdn.discordapp.com/attachments/782562061812891648/795239281932238848/blush_1.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239291092598794/blush_3.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239298751660032/blush_2.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239306557784074/blush_5.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239308096307221/blush_6.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239308520325140/blush_4.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239309674151936/blush_7.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239319702994974/blush_8.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239322269909002/blush_12.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239324622782464/blush_10.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239326103371797/blush_11.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239327743475712/blush_9.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239334386991104/blush_13.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239337335455764/blush_14.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239338048618496/blush_15.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239340460343326/blush_16.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239341227114507/blush_17.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239351067082793/blush_18.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239350405169152/blush_19.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239369669476362/blush_21.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239371762434048/blush_20.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239375315009546/blush_22.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239378586566716/blush_23.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239381744353320/blush_24.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239389273260042/blush_26.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239393987395604/blush_25.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239397515722762/blush_27.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239399268810763/blush_28.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239400082505728/blush_29.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239412262502420/blush_31.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239411964182528/blush_32.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239417538150400/blush_30.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239420525674536/blush_34.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239423783731200/blush_33.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/795239435745624124/blush_35.gif'
        )
        rnd_blush = random.choice(blushgif)
        blushes.set_image(url=rnd_blush)
        await context.send(embed=blushes)
        await context.message.delete()

    @commands.hybrid_command(name='smile', aliases=["Smile"])    
    async def smile(self, context, member: typing.Optional[discord.Member] = None, *, gifmsg=None):
        smiles = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff) 
        if member is None:
            smiles.set_author(name=f"{context.message.author.display_name}  is Smiling ｡◕‿◕｡", icon_url=f"{context.message.author.display_avatar.url}") 
        else:
            smiles.set_author(name=f"{context.message.author.display_name}  is Smiling with {member.display_name}｡◕‿◕｡", icon_url=f"{context.message.author.display_avatar.url}")   
        smilegif = (
            'https://cdn.discordapp.com/attachments/782562061812891648/794511199814287390/smile_1.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511215182741524/smile_2.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511219536953344/smile_5.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511220690124810/smile_3.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511226754957322/smile_4.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511228176695306/smile_6.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511232006750248/smile_9.jpg',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511235541368872/smile_8.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511234480209920/smile_7.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511238038028308/smile_11.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511243905204244/smile_12.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511251383255040/smile_13.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511271110246400/smile_14.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511274511564830/smile_10.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511285210447872/smile_16.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511288075943937/smile_15.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511292790603776/smile_18.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511293566550016/smile_17.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511296942833674/smile_19.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511301907972096/smile_20.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511306573086761/smile_21.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511307424006174/smile_22.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511306128228352/smile_23.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511316575846410/smile_25.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511318245441536/smile_24.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511332610539530/smile_28.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511333902647296/smile_27.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511340579455046/smile_26.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511346771165234/smile_29.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511348548632576/smile_30.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794511353657688074/smile_31.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/794512158335172619/smile_32.gif'
        )   
        rnd_smile = random.choice(smilegif)
        smiles.set_image(url=rnd_smile)
        await context.send(embed=smiles)
        await context.message.delete()

    @commands.hybrid_command(name='stare', aliases=["Stare"])    
    async def stare(self, context, member: typing.Optional[discord.Member] = None, *, gifmsg=None):
        stares = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff) 
        if member is None:
            stares.set_author(name=f"{context.message.author.display_name}  is Staring O_o", icon_url=f"{context.message.author.display_avatar.url}") 
        else:
            stares.set_author(name=f"{context.message.author.display_name}  is Staring {member.display_name} O_o", icon_url=f"{context.message.author.display_avatar.url}")   
        staregif = (
            'https://cdn.discordapp.com/attachments/782562061812891648/789443912103755776/stare_2.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789443993212813332/stare_1.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789445620208500736/stare_3.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789445636226547722/stare_4.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789445650386518026/stare_5.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789445687497981972/stare_6.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789445747531186196/stare_7.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789445768111980614/stare_8.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789445802275504128/stare_9.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789445820398174238/stare_10.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789445870402666497/stare_11.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789445918264655942/stare_12.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789446040427823104/stare_13.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789446107759509514/stare_14.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789446241955479552/stare_15.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789446261379170344/stare_16.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789446388420968458/stare_17.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789446419786104862/stare_18.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789446493534289920/stare_19.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789446622169661460/stare_20.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789446750108123166/stare_21.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789446777958957066/stare_22.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789446817716240434/stare_23.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789446896560111656/stare_24.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789446991095922688/stare_25.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789447044862836746/stare_26.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789447104065175572/stare_27.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789447242821795870/stare_28.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789447268893851678/stare_29.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789447607981572146/stare_30.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789447700235812874/stare_31.gif'
        )   
        rnd_stare = random.choice(staregif)
        stares.set_image(url=rnd_stare)
        await context.send(embed=stares)
        await context.message.delete()

    @commands.hybrid_command(name='laugh', aliases=["Laugh"])    
    async def laugh(self, context, member: typing.Optional[discord.Member] = None, *, gifmsg=None):
        laughs = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff) 
        if member is None:
            laughs.set_author(name=f"{context.message.author.display_name}  is laughing", icon_url=f"{context.message.author.display_avatar.url}") 
        else:
            laughs.set_author(name=f"{context.message.author.display_name}  is laughing on {member.display_name} ", icon_url=f"{context.message.author.display_avatar.url}")   
        laughgif = (
            'https://cdn.discordapp.com/attachments/782562061812891648/789435933350428682/laugh_1.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789435946047242240/laugh_3.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789435945753640960/laugh_2.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789435950320058368/laugh_4.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789435953848647700/laugh_5.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789435957735587870/laugh_7.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789435961943130132/laugh_6.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789435964212117514/laugh_9.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789435968183599124/laugh_10.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789435973796757504/laugh_8.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789435978901094420/laugh_12.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789435982000422942/laugh_13.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789435980238290974/laugh_11.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789435991504322570/laugh_14.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789435993698730024/laugh_16.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789435993102614548/laugh_15.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789435996843409419/laugh_17.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789436004238753812/laugh_19.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789436005136465950/laugh_18.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789436007300726844/laugh_20.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789436026615365642/laugh_21.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789436040381333524/laugh_23.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789436045430358016/laugh_24.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789436050514509864/laugh_25.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789436059167490077/laugh_26.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789436065425129472/laugh_27.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789436068189569044/laugh_28.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789436074854055946/laugh_29.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789436082122129428/laugh_30.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789436090477707284/laugh_31.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789436097792442368/laugh_32.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789436101789483008/laugh_33.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789436107284545536/laugh_34.gif'
        )   
        rnd_laugh = random.choice(laughgif)
        laughs.set_image(url=rnd_laugh)
        await context.send(embed=laughs)
        await context.message.delete()    

    @commands.hybrid_command(name='dance')    
    async def dance(self, context, *, gifmsg=None):
        dances = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff) 
        dances.set_author(name=f"{context.message.author.display_name}  is Dancing ƪ(‾.‾“)┐", icon_url=f"{context.message.author.display_avatar.url}") 
        dancegif = (
            'https://cdn.discordapp.com/attachments/782562061812891648/783588914845712445/dance_32.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783588908256460830/dance_31.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783367053120897024/dance_30.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783367040429195304/dance_28.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783367042485059614/dance_29.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783367034427277342/dance_27.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783367010843099156/dance_26.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783367006023450694/dance_25.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366998456533062/dance_24.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366987798937620/dance_22.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366990193491998/dance_23.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366984175452200/dance_21.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366962431655996/dance_20.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366955133698108/dance_19.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366932325859388/dance_18.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366920493072415/dance_17.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366920694530058/dance_16.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366907029356564/dance_15.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366900256079902/dance_14.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366873633914910/dance_12.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366869020704798/dance_13.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366823449854012/dance_10.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366852662788136/dance_11.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366816352567296/dance_9.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366809696600074/dance_8.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366800284975134/dance_3.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366797033472050/dance_7.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366793015590942/dance_6.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366789958074418/dance_4.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366782760648744/dance_2.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783366753131429940/dance_1.gif'
        ) 
        rnd_dance = random.choice(dancegif)
        dances.set_image(url=rnd_dance)
        await context.send(embed=dances)
        await context.message.delete()

    @commands.hybrid_command(name='sleep')
    async def sleep(self, context, *, gifmsg=None):
        sleeps = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff) 
        sleeps.set_author(name=f"{context.message.author.display_name}  is Sleeping ", icon_url=f"{context.message.author.display_avatar.url}") 
        sleepgif = (
            'https://media.discordapp.net/attachments/782562061812891648/782574466886270976/sleep_30.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782574457469927424/sleep_29.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782574445281673216/sleep_28.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782574439824883732/sleep_27.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782573053677666324/sleep_26.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782572448583385098/sleep_25.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782572446833442816/sleep_21.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782572439733141504/sleep_22.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782572424934981632/sleep_24.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782572418782199808/sleep_23.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782572407574626324/sleep_20.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782572397660078080/sleep_18.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782572391300726784/sleep_16.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782572390910656512/sleep_17.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782572388021305345/sleep_15.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782572384557203466/sleep_14.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782572382081515520/sleep_13.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782572376398233600/sleep_12.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782572371923435560/sleep_11.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782568151132012594/sleep_4.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782568155464990730/sleep_5.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782568162814066698/sleep_6.gif?width=379&height=468',
            'https://media.discordapp.net/attachments/782562061812891648/782568171952406578/sleep_7.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782568176386572308/sleep_8.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782568177112186920/sleep_9.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782568180094074930/sleep_10.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782564354733506631/sleep_2.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782564072130215966/sleep_3.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782564014781628416/sleep_1.gif'
        )
        rnd_sleep = random.choice(sleepgif)
        sleeps.set_image(url=rnd_sleep)
        await context.send(embed=sleeps)
        await context.message.delete()

    @commands.hybrid_command(name='think')
    async def think(self, context, *, gifmsg=None):
        thinks = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff)   
        thinks.set_author(name=f"{context.message.author.display_name}  is Thinking ", icon_url=f"{context.message.author.display_avatar.url}") 
        thinkgif = (
            'https://cdn.discordapp.com/attachments/782562061812891648/782647107529343016/thinking_30.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782647075372269658/thinking_29.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782647062038052864/thinking_28.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782647054299037696/thinking_26.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782647048319139840/thinking_25.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782647041158545439/thinking_24.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782647028530151454/thinking_22.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782647029812822016/thinking_23.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782647017297281096/thinking_20.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782647022641217556/thinking_21.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782647005217554472/thinking_19.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782647000532516864/thinking_18.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782646966542532628/thinking_15.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782646967074947102/thinking_17.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782646955788337184/thinking_14.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782646945239400559/thinking_13.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782646943104892958/thinking_12.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782646925798408212/thinking_11.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782646919809728593/thinking_10.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782646908371861514/thinking_9.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782646905972588584/thinking_8.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782646893024641034/thinking_6.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782646894118830100/thinking_7.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782646884417273926/thinking_5.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782646880323895316/thinking_4.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782646867682263040/thinking_3.gif',
            'https://media.discordapp.net/attachments/782562061812891648/782646862334132264/thinking_1.gif?width=468&height=468',
            'https://media.discordapp.net/attachments/782562061812891648/782646857284976640/thinking_2.gif'
        )
        rnd_think = random.choice(thinkgif)
        thinks.set_image(url=rnd_think)
        await context.send(embed=thinks)
        await context.message.delete() 

    @commands.hybrid_command(name='cry')
    async def cry(self, context, *, gifmsg=None):
        crys = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff)  
        crys.set_author(name=f"{context.message.author.display_name}  is Crying   ༎ຶ‿༎ຶ ", icon_url=f"{context.message.author.display_avatar.url}") 
        crygif = (
            'https://cdn.discordapp.com/attachments/782562061812891648/782897297645371393/crying_30.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897287285702656/crying_29.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897284648140800/crying_28.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897280738918410/crying_27.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897274073513994/crying_26.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897261637140480/crying_25.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897255660912650/crying_24.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897247641010256/crying_23.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897242272694272/crying_22.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897237734326282/crying_21.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897226539859988/crying_19.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897225856581642/crying_20.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897217315799100/crying_18.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897207413702666/crying_17.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897200412885002/crying_16.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897195678302238/crying_15.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897190921306112/crying_14.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897180260302858/crying_12.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897174265724949/crying_13.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897162378805268/crying_11.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897156650041394/crying_10.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897148580593664/crying_9.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897143060365332/crying_8.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897140950761502/crying_7.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897136194027560/crying_5.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897132394905650/crying_6.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897125591351296/crying_1.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897123070443540/crying_4.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897121648312320/crying_3.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/782897119953420309/crying_2.gif'
        )
        rnd_cry = random.choice(crygif)
        crys.set_image(url=rnd_cry)
        await context.send(embed=crys) 
        await context.message.delete()    

    @commands.hybrid_command(name='rage', aliases=["angry", "Rage", "Angry", "Anger", "anger", "Triggered", "triggered"])
    async def rage(self, context, member: typing.Optional[discord.Member] = None, *, gifmsg=None):
        triggereds = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff)
        if member is None:
            triggereds.set_author(name=f"{context.message.author.display_name} is Triggered.... ", icon_url=f"{context.message.author.display_avatar.url}")
        else:
            triggereds.set_author(name=f"{context.message.author.display_name} is angry with {member.display_name}  ", icon_url=f"{context.message.author.display_avatar.url}")
          
        triggeredgif = (
            'https://cdn.discordapp.com/attachments/782562061812891648/789078382172307456/anger_5.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078390527098890/anger_6.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078400215810058/anger_7.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078405923602453/anger_8.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078427444969522/anger_10.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078427495038996/anger_9.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078449155211314/anger_11.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078460215459850/anger_12.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078469593923584/anger_13.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078486630793226/anger_14.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078507916361778/anger_15.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078517186560000/anger_16.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078526241275924/anger_17.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078531954049034/anger_18.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078544277700678/anger_19.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078559918129212/anger_20.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078584077058048/anger_21.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078586766000138/anger_22.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078596315512832/anger_23.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078606671380510/anger_24.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078612942258206/anger_25.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078629383536640/anger_27.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078629032263720/anger_26.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078645012168714/anger_28.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078674414370856/anger_30.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078686770528256/anger_31.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078691946299422/anger_32.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078701949190174/anger_33.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078992748937246/anger_34.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789080174150680586/anger_35.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078375959363604/anger_4.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078371363323924/anger_3.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078365574266900/anger_1.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/789078365733650454/anger_2.gif'
        )
        rnd_triggered = random.choice(triggeredgif)
        triggereds.set_image(url=rnd_triggered)
        await context.send(embed=triggereds) 
        await context.message.delete() 

    @commands.hybrid_command(name='pout', aliases=["Pout"])
    async def pout(self, context, member: typing.Optional[discord.Member] = None, *, gifmsg=None):
        pouts = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff)
        if member is None:
            pouts.set_author(name=f"{context.message.author.display_name} is pouting.... ", icon_url=f"{context.message.author.display_avatar.url}")
        else:
            pouts.set_author(name=f"{context.message.author.display_name} is pouting at {member.display_name}  ", icon_url=f"{context.message.author.display_avatar.url}")
          
        poutgif = (
            'https://cdn.discordapp.com/attachments/782562061812891648/783725881507184650/pout_1.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783725888403144764/pout_10.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783725908832813116/pout_2.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783725948641345536/pout_3.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783725952353042462/pout_4.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783725971378405396/pout_5.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783725977531449364/pout_6.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783725998734442547/pout_7.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726042388889610/pout_9.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726046448713738/pout_8.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726048335364096/pout_10.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726067466109019/pout_11.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726083777757234/pout_12.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726093390708806/pout_14.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726095043133450/pout_13.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726100244463667/pout_15.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726119186202674/pout_16.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726141252042834/pout_17.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726165868281856/pout_18.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726173032546314/pout_19.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726185929900042/pout_20.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726195438780456/pout_21.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726221368098907/pout_22.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726244474257428/pout_23.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726263902404608/pout_24.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726283514970202/pout_25.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726309086855178/pout_26.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726328398086184/pout_27.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726346852499466/pout_28.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726373041864735/pout_29.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783726400423198720/pout_30.gif'
        )
        rnd_pout = random.choice(poutgif)
        pouts.set_image(url=rnd_pout)
        await context.send(embed=pouts) 
        await context.message.delete()    

    @commands.hybrid_command(name='smug')
    async def smug(self, context, *, gifmsg=None):
        smugs = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff)
        smugs.set_author(name=f"{context.message.author.display_name}  is Smirking ", icon_url=f"{context.message.author.display_avatar.url}")   
        smuggif = (
            'https://images-ext-1.discordapp.net/external/DQkHEFdPW2-ZlXC0_UVHWTQIoQ440fbL2vl_u5wWBbs/https/cdn.weeb.sh/images/HJD-IJtw-.gif',
            'https://images-ext-2.discordapp.net/external/XgG5PzlOGQ095Df4fU-h-x1CsT5lSLBbJ-jDV8mmtFQ/https/cdn.weeb.sh/images/H1xgWUktPW.gif'
        )
        rnd_smug = random.choice(smuggif)
        smugs.set_image(url=rnd_smug)
        await context.send(embed=smugs)
        await context.message.delete()  

    @commands.hybrid_command(name='kill')
    async def kill(self, context, member: discord.Member, *, gifmsg=None):
        if member == context.author:
            kills = discord.Embed(timestamp=utc_now(), color=0x00ebff) 
            kills.set_author(name=f"{context.message.author.display_name} don't die!! I'm with you..... ", icon_url=f"{context.message.author.display_avatar.url}")   
            killgif = (
                'https://cdn.discordapp.com/attachments/782562061812891648/785465632409649162/hug_15.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/785465589740601344/hug_17.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/785423760203317268/hug_18.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/785423760034627594/hug_14.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/785423757320912926/hug_16.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/785423755077353522/hug_11.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/785423753143648296/hug_12.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/785423752204779540/hug_13.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/785423751080312862/hug_10.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/785420708792631296/hug_9.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/785420707612852264/hug_8.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/785420700059172894/hug_6.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/785420699904245790/hug_5.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/785420699056734279/hug_7.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/785420695969464340/hug_4.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/785420694002335764/hug_3.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/785420688486826014/hug_2.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/785420687942483978/hug_1.gif'
            )
            rnd_kill = random.choice(killgif)
            kills.set_image(url=rnd_kill)
            await context.send(embed=kills) 
        else:
            kills = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff) 
            kills.set_author(name=f"{context.message.author.display_name} is Murdering {member.display_name} ! Oh my... ", icon_url=f"{context.message.author.display_avatar.url}")   
            killgif = (
                'https://cdn.discordapp.com/attachments/782562061812891648/782990569441198151/kill_18.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990626551496704/kill_19.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990641461592084/kill_21.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990640786964500/kill_20.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990712387534859/kill_22.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990717860970586/kill_23.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990726862602280/kill_24.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990880973258762/kill_25.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990900740751392/kill_28.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990906424688650/kill_29.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990911591284746/kill_30.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782992926191517756/kill_26.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782994591178555442/kill_27.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/783259161512116244/kill_31.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782989842656264222/kill_4.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782989850994802693/kill_3.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782989851288535061/kill_2.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990058684153856/kill_5.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990191861301248/kill_7.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990191588802620/kill_8.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990254788837386/kill_9.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990256429465610/kill_10.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990387077447700/kill_11.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990390546268170/kill_12.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990430873714728/kill_13.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990439351058452/kill_14.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990512368910346/kill_15.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990516950007848/kill_16.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782990563628548136/kill_17.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782989841431920666/kill_1.gif'
            )
            rnd_kill = random.choice(killgif)
            kills.set_image(url=rnd_kill)
            await context.send(embed=kills)
            await context.message.delete()      

    @commands.hybrid_command(name='bonk', aliases=["Bonk"])
    async def bonk(self, context, member: discord.Member, *, gifmsg=None):
        bonks = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff)
        bonks.set_author(name=f"{context.message.author.display_name} bonks {member.display_name} on the head.... ", icon_url=f"{context.message.author.display_avatar.url}")   
        bonkgif = (
            'https://cdn.discordapp.com/attachments/782562061812891648/802402148021174282/bonk_22.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802402147772661770/bonk_21.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802402147383509023/bonk_20.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802401983503007764/bonk_18.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802401983280840705/bonk_17.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802401982983438336/bonk_16.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802401982726799400/bonk_15.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802399252894056498/bonk_1.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802399252466106388/bonk_2.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802399197944217641/bonk_3.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802399197701079070/bonk_4.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802399197487562762/bonk_5.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802399197256089630/bonk_6.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802399196950560778/bonk_7.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802399196736258098/bonk_8.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802399105246167040/bonk_9.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802399104990052372/bonk_10.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802399104780730378/bonk_11.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802399104462356520/bonk_12.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802399104268763146/bonk_13.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/802399103891800114/bonk_14.gif'
        )
        rnd_bonk = random.choice(bonkgif)
        bonks.set_image(url=rnd_bonk) 
        await context.send(embed=bonks) 
        await context.message.delete() 

    @commands.hybrid_command(name='punch', aliases=["Punch"])
    async def punch(self, context, member: discord.Member, *, gifmsg=None):
        punchs = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff)
        punchs.set_author(name=f"{context.message.author.display_name} punchs {member.display_name} Ha! ", icon_url=f"{context.message.author.display_avatar.url}")   
        punchgif = (
            'https://i.imgur.com/YJrX0hC.gif',
            'https://i.imgur.com/vS2rUES.gif',
            'https://i.imgur.com/Pm8fekf.gif',
            'https://i.imgur.com/dpDqbXN.gif',
            'https://i.imgur.com/wZKzFsk.gif',
            'https://i.imgur.com/eDKXP7h.gif',
            'https://i.imgur.com/wOj0iuK.gif',
            'https://i.imgur.com/vstkI9k.gif',
            'https://i.imgur.com/BR43afH.gif',
            'https://i.imgur.com/Xr6Yzzw.gif',
            'https://i.imgur.com/zv92jMR.gif',
            'https://i.imgur.com/94BzVNx.gif',
            'https://i.imgur.com/mOxZMps.gif',
            'https://i.imgur.com/yTs6ioC.gif',
            'https://i.imgur.com/JJNVkVy.gif',
            'https://i.imgur.com/O20xM2k.gif',
            'https://i.imgur.com/A9jhWJu.gif',
            'https://i.imgur.com/iQ7HQED.gif',
            'https://i.imgur.com/4wCSoTd.gif',
            'https://i.imgur.com/YvEYrDj.gif',
            'https://i.imgur.com/4eHqGR7.gif',
            'https://i.imgur.com/S7d8z4J.gif',
            'https://i.imgur.com/E9qS559.gif',
            'https://i.imgur.com/fgsPMli.gif'
        )
        rnd_punch = random.choice(punchgif)
        punchs.set_image(url=rnd_punch) 
        await context.send(embed=punchs) 
        await context.message.delete()       

    @commands.hybrid_command(name='slap', aliases=["Slap"])
    async def slap(self, context, member: discord.Member, *, gifmsg=None):
        slaps = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff)
        slaps.set_author(name=f"{context.message.author.display_name} is slapping {member.display_name}  ", icon_url=f"{context.message.author.display_avatar.url}")   
        slapgif = (
            'https://cdn.discordapp.com/attachments/782562061812891648/803176639969624074/Slap2.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803181679308963850/Slap2.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803183012103454760/Slap3.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803183450940506202/Slap4.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803183766829924372/Slap5.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803184358890537050/Slap6.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803184758724362260/Slap7.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803185254629376020/Slap8.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803187334371475466/Slap11.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803188847587360818/Slap12.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803221561846136832/Slap11.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803221702926532658/Slap12.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803221837622018058/Slap13.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803221929166241822/Slap14.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803222200915591188/Slap15.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803588564826324992/Slap17.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803590140588589076/Slap19.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803590320491200552/Slap20.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803590819860709396/Slap21.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803591010236104705/Slap22.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/804253033545859082/Slap23.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/804253287557627904/Slap24.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/804253667766698025/Slap25.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/804254414641692692/Slap26.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/804254783455363082/Slap27.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/804255835450638346/Slap28.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/804256388263575552/Slap29.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/804256899276341258/Slap30.gif'
        )
        rnd_slap = random.choice(slapgif)
        slaps.set_image(url=rnd_slap) 
        await context.send(embed=slaps) 
        await context.message.delete() 

    @commands.hybrid_command(name='poke', aliases=["Poke"])
    async def poke(self, context, member: discord.Member, *, gifmsg=None):
        pokes = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff)
        pokes.set_author(name=f"{context.message.author.display_name} pokes {member.display_name}  ", icon_url=f"{context.message.author.display_avatar.url}")   
        pokegif = (
            'https://cdn.discordapp.com/attachments/782562061812891648/803204770668085258/poke_6.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204746000859136/poke_1.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204747216683038/poke_2.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204747418664970/poke_3.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204747599151124/poke_4.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204770440544276/poke_5.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204770869149696/poke_7.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204771108356126/poke_8.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204809649684500/poke_9.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204809922052116/poke_10.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204810064134205/poke_11.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204810253926430/poke_12.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204841291382814/poke_13.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204841483927582/poke_14.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204841702686720/poke_15.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204841899425852/poke_16.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204871552761856/poke_17.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204872048214057/poke_18.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204872248754196/poke_22.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204872446935101/poke_23.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204919711629312/poke_24.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204920186241024/poke_25.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204920408801280/poke_21.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204920945147965/poke_20.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803204921427886090/poke_19.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803219135529091092/poke_26.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803219135857295391/poke_27.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803219587537698847/poke_25_remastered.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803220821421981716/poke_28.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803220821706801192/poke_29.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/803220821937225798/poke_30.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/804354541583597568/poke_31.gif'
        )
        rnd_poke = random.choice(pokegif)
        pokes.set_image(url=rnd_poke) 
        await context.send(embed=pokes) 
        await context.message.delete()

    @commands.hybrid_command(name='pat', aliases=["Pat"])
    async def pat(self, context, member: discord.Member, *, gifmsg=None):
        pats = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff)
        pats.set_author(name=f"{context.message.author.display_name} pets {member.display_name} ! There there... ", icon_url=f"{context.message.author.display_avatar.url}")   
        patgif = (
            'https://cdn.discordapp.com/attachments/782562061812891648/783001926999867422/pat_12.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783002079600836708/pat_30.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783002064392290314/pat_29.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783002054918012958/pat_28.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783002050614788126/pat_27.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783002038275014686/pat_26.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783002024568029212/pat_24.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783002026803331112/pat_23.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001996965838858/pat_22.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001993392160778/pat_21.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001990384451584/pat_20.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001985010892830/pat_19.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001971535249418/pat_18.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001958150701056/pat_17.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001949612146728/pat_15.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001946599456788/pat_16.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001936236511294/pat_14.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001935535407124/pat_13.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001924919492608/pat_10.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001921358135356/pat_11.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001911867473942/pat_8.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001904535044176/pat_9.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001889570684958/pat_7.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001883743617114/pat_6.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001872906190898/pat_5.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001862139805696/pat_3.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001861141299210/pat_4.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001857600782357/pat_2.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783001843994984458/pat_1.gif'
        )
        rnd_pat = random.choice(patgif)
        pats.set_image(url=rnd_pat) 
        await context.send(embed=pats) 
        await context.message.delete()

    @commands.hybrid_command(name='hi', aliases=['Hello', 'hello', 'Hey', 'hey', 'wave', 'Wave', 'Hi'])
    async def hi(self, context, member: typing.Optional[discord.Member] = None, *, gifmsg=None):
        His = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff)
        if member is None:
            His.set_author(name=f"{context.message.author.display_name} is waving... ", icon_url=f"{context.message.author.display_avatar.url}")
        else:
            His.set_author(name=f"{context.message.author.display_name} is waving to {member.display_name}  ", icon_url=f"{context.message.author.display_avatar.url}")          
        Higif = (
            'https://cdn.discordapp.com/attachments/782562061812891648/783374436757274675/greeting_30.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374421212790804/greeting_29.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374413092880464/greeting_28.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374405891391548/greeting_27.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374399046156368/greeting_26.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374389013512232/greeting_25.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374383640346634/greeting_24.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374376274755684/greeting_23.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374370885206086/greeting_22.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374365873799208/greeting_21.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374354863751198/greeting_20.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374346483531826/greeting_19.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374336718929980/greeting_18.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374329634095154/greeting_17.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374325016952892/greeting_16.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374319668428840/greeting_15.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374312333508608/greeting_14.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374309933711380/greeting_13.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374305589329950/greeting_11.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374305202667520/greeting_12.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374293153087498/greeting_10.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374292024164362/greeting_7.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374291168919572/greeting_8.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374290531778620/greeting_9.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374277201362944/greeting_6.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374271607078962/greeting_5.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374269224321054/greeting_4.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374267965243432/greeting_2.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374264157732914/greeting_3.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783374255861399602/greeting_1.gif'
        )
        rnd_Hi = random.choice(Higif)
        His.set_image(url=rnd_Hi)
        await context.send(embed=His) 
        await context.message.delete() 

    @commands.hybrid_command(name='nom', aliases=['eat', 'bite', 'Bite', 'Eat', 'Nom'])
    async def nom(self, context, member: discord.Member, *, gifmsg=None):
        Noms = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff)
        nom1 = f"{context.message.author.display_name} noms {member.display_name}! "
        nom2 = f"{context.message.author.display_name} noms {member.display_name} Yummy! "
        nom3 = f"{context.message.author.display_name} is nomming on {member.display_name}! "
        nomlist = (nom1, nom2, nom3)
        nomline = random.choice(nomlist)
        Noms.set_author(name=nomline, icon_url=f"{context.message.author.display_avatar.url}")          
        Nomgif = (
            'https://cdn.discordapp.com/attachments/782562061812891648/783719325869277224/nom_33.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783718654188584971/nom_32.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783717579583389696/nom_31.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783717569152024616/nom_27.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783717558301098004/nom_26.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783717551531229184/nom_24.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715936980959283/nom_17.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715925119074304/nom_21.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715925027192852/nom_20.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715923790004285/nom_23.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715917938163712/nom_22.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715886544322580/nom_15.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715886514831370/nom_16.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715885109477376/nom_12.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715881267888138/nom_13.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715880550006804/nom_14.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715875442130944/nom_9.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715871334989843/nom_10.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715873726660638/nom_8.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715872472170576/nom_11.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715864892932106/nom_6.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715860320878642/nom_3.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715859604307988/nom_2.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715861575761920/nom_7.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715861084110898/nom_4.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715859729219654/nom_5.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/783715837277241354/nom_29.gif'
        )
        rnd_Nom = random.choice(Nomgif)
        Noms.set_image(url=rnd_Nom)
        await context.send(embed=Noms) 
        await context.message.delete()

    @commands.hybrid_command(name='hug', aliases=['Hug'])
    async def hug(self, context, member: discord.Member, *, gifmsg=None):
        if context.interaction is not None:
            await context.defer()
        hugs = discord.Embed(description=gifmsg, timestamp=utc_now(), color=0x00ebff)
        hug1 = f"{context.message.author.display_name} hugs {member.display_name}! ＼(^o^)／"
        hug2 = f"{context.message.author.display_name} hugs {member.display_name}! Don't squeeze too hard!! "
        hug3 = f"{context.message.author.display_name} gives {member.display_name} a big hug!! "
        huglist = (hug1, hug2, hug3)
        hugline = random.choice(huglist)
        hugs.set_author(name=hugline, icon_url=f"{context.message.author.display_avatar.url}")          
        huggif = (
            'https://cdn.discordapp.com/attachments/782562061812891648/785420695969464340/hug_4.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785423760034627594/hug_14.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785465589740601344/hug_17.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785465632409649162/hug_15.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785465989491195944/hug_20.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785465991043350538/hug_19.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785465996924289054/hug_21.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785465999776284732/hug_23.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785466001948672020/hug_22.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785466002610978826/hug_24.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785466004187643944/hug_26.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785466007417520148/hug_25.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785466013160308767/hug_28.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785466015780700220/hug_27.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785466034563317760/hug_35.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785466035129810944/hug_37.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785466037893464084/hug_32.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785466039706189879/hug_33.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785466043741110272/hug_39.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785466048416710666/hug_36.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785466051542122536/hug_38.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785466051075899413/hug_31.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785466051772678144/hug_34.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785466057800286239/hug_30.gif',
            'https://cdn.discordapp.com/attachments/782562061812891648/785467997800235038/hug_29.gif'
        )
        rnd_hug = random.choice(huggif)
        hugs.set_image(url=rnd_hug)
        await context.send(embed=hugs)          
        await context.message.delete()

async def setup(bot):
    await bot.add_cog(Roleplay(bot))
