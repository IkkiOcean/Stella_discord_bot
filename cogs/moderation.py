import discord
from discord.ext import commands
import random
import aiohttp
from io import BytesIO
import typing
from bot_utils import BOT_OWNER_ID

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='kick', aliases=["Kick"])    
    @commands.has_permissions(kick_members=True)
    async def kick(self, context, member: discord.Member, *, reason=None):
        if member != context.author:
            message = discord.Embed(color=0x00ebff)
            kickgif = (
                'https://cdn.discordapp.com/attachments/782562061812891648/782714161560944670/kicked1.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782714161560944670/kicked1.gif'
            )
            rndkick = random.choice(kickgif)
            message.add_field(name='Kicked', value=f"You have been **kicked** from {context.guild.name} for {reason}")
            message.set_image(url=rndkick)
            kicked = discord.Embed(color=0x00ebff)
            kicked.add_field(name='Kicked', value=f"{member.mention} has been kicked from the server!! Hehe:)")
            await member.kick(reason=reason)
            await context.send(embed=kicked)
            await member.send(embed=message)
        else:
            await context.send("Want to kick yourself? :(")

    @commands.hybrid_command(name='ban', aliases=["Ban"])    
    @commands.has_permissions(ban_members=True)
    async def ban(self, context, member: discord.Member, *, reason=None):
        if member != context.author:
            await member.ban(reason=reason)
            banned = discord.Embed(color=0x00ebff)
            banned.add_field(name='Banned', value=f"{member.mention} has been **Banned** from the server!! Hehe:)")
            await context.send(embed=banned)
            message = discord.Embed(color=0x00ebff)
            bangif = (
                'https://cdn.discordapp.com/attachments/782562061812891648/782722014829084672/ban1.gif',
                'https://cdn.discordapp.com/attachments/782562061812891648/782722005044691014/ban_2.gif'
            )
            rndban = random.choice(bangif)
            message.add_field(name='Banned', value=f"You have been banned from {context.guild.name} for {reason}")
            message.set_image(url=rndban)
            await member.send(embed=message)
        else:
            await context.send("Want to ban yourself? :(")

    @commands.hybrid_command(name="clear", aliases=["Clear", 'Clean', 'clean', 'delete', 'Delete', 'purge', 'Purge'])    
    @commands.has_permissions(manage_messages=True)
    async def clear(self, context, amount: int = 2):
        await context.channel.purge(limit=(amount + 1))
        await context.send(f"`{amount} messages has been Deleted... 👍`", delete_after=10)

    @commands.hybrid_command(name="addrole", aliases=["Addrole"])       
    async def addrole(self, ctx, member: discord.Member, role: typing.Optional[discord.Role], *, rolename=None):
        if ctx.author.id == BOT_OWNER_ID:
            try:
                if role is not None:
                    await member.add_roles(role)
                    await ctx.reply(f"`{role.name}` role has been given to {member.mention}")
                else:   
                    roless = discord.utils.get(ctx.guild.roles, name=rolename)
                    await member.add_roles(roless)
                    await ctx.reply(f"`{rolename}` role has been given to {member.mention}")
            except Exception:
                await ctx.reply("Type `S.addrole <member> <ROLE NAME OR MENTION ROLE>`")
     
    @commands.hybrid_command(name="removerole", aliases=["Removerole"])        
    async def removerole(self, ctx, member: discord.Member, role: typing.Optional[discord.Role], *, rolename=None):
        if ctx.author.id == BOT_OWNER_ID:
            try:
                if role is not None:
                    await member.remove_roles(role)
                    await ctx.reply(f"`{role.name}` role has been removed from {member.mention}")
                else:   
                    roless = discord.utils.get(ctx.guild.roles, name=rolename)
                    await member.remove_roles(roless)
                    await ctx.reply(f"`{rolename}` role has been removed from {member.mention}")
            except Exception:
                await ctx.reply("Type `S.removerole <member> <ROLE NAME OR MENTION ROLE>`") 

    @commands.hybrid_command(name='steal', aliases=["Steal"])
    @commands.has_permissions(manage_emojis=True) 
    async def steal(self, ctx, emoji: discord.Emoji, *, name):
        guild = ctx.guild   
        url = str(emoji.url)    
        if name is None:
            name = "not given"
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as r:
                try:
                    img_or_gif = BytesIO(await r.read())
                    b_value = img_or_gif.getvalue()
                    if r.status in range(200, 299):
                        new_emoji = await guild.create_custom_emoji(image=b_value, name=name)
                        await ctx.send(f'Successfully created emoji: <:{name}:{new_emoji.id}>')
                        await ses.close()
                    else:
                        await ctx.send(f'something went wrong| Try another emoji')
                        await ses.close()
                except discord.HTTPException:
                    await ctx.send('File size is too big!')

    @commands.hybrid_command(name='addemoji', aliases=["Addemoji"])
    @commands.has_permissions(manage_emojis=True) 
    async def addemoji(self, ctx, url: str, *, name):
        guild = ctx.guild   
        if name is None:
            name = "not given"
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as r:
                try:
                    img_or_gif = BytesIO(await r.read())
                    b_value = img_or_gif.getvalue()
                    if r.status in range(200, 299):
                        new_emoji = await guild.create_custom_emoji(image=b_value, name=name)
                        await ctx.send(f'Successfully created emoji: <:{name}:{new_emoji.id}>')
                        await ses.close()
                    else:
                        await ctx.send(f'something went wrong| Try another emoji')
                        await ses.close()
                except discord.HTTPException:
                    await ctx.send('File size is too big!')

async def setup(bot):
    await bot.add_cog(Moderation(bot))
