import discord
import random
import keep_alive
import os
import json
import praw
import asyncio
from discord.ext import commands
from random import choice
from discord import Member
from discord.ext.commands import Bot
from discord.ext.commands import has_permissions, MissingPermissions, is_owner
from discord.ext.commands import has_permissions, MissingPermissions

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)


import urllib

def get_prefix(client, message):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
  try:
    x = prefixes.get(str(message.guild.id), "?")
    client.prefix = x
    return x
  except:
    pass
client = commands.Bot(command_prefix = get_prefix, intents = intents)

token = os.environ.get('DISCORD_BOT_SECREAT')

@client.event
async def on_guild_join(guild):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
  prefixes[str(guild.id)] = "?"
  with open("prefixes.json", "w") as f:
    json.dump(prefixes, f, indent=4)

# token = os.environ.get('DISCORD_BOT_SECREAT')
@client.command()
@commands.has_permissions(administrator=True)
async def set_prefix(ctx, prefix):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
  prefixes[str(ctx.guild.id)] = prefix
  with open("prefixes.json", "w") as f:
    json.dump(prefixes, f, indent=4)
  await ctx.send(f"Server prefix changed to: `{prefix}`")
  client.prefix = prefix


cs = os.environ.get('CLIENT_SECREAT')
ci = os.environ.get('CLIENT_ID')
un = os.environ.get('USERNAME')
ps = os.environ.get('PASSWORD')
ua = os.environ.get('USER_AGENT')


reddit = praw.Reddit(client_id = ci,
                     client_secret= cs,
                     username=un,
                     password=ps,
                     user_agent=ua)

subreddit = reddit.subreddit("memes")

top = subreddit.top(limit = 5)

# for submission in top:
#     print(submission.title)
@client.remove_command('help')
# @client.remove_command('help_moderation')
@client.event
async def on_ready():
    print("Hello There")
    activity = discord.Game(name="Serving You 😊 || Cedits : Dhruv ", type=3)
    await client.change_presence(status=discord.Status.idle, activity=activity)
    print('i am running')
    while 1:
      urllib.request.urlopen("https://trbot.skp627.repl.co")
      await asyncio.sleep(500)
# @client.event
# async def on_member_join(member):
#    await client.get_channel(791279306562469889).send(f"{member.mention}, **Has Taken Efforts To Join The Server . Hope you Have A good Time here\n**")
    
@client.event
async def on_member_remove(member):
    print(f'{member} has thankfully left the server')
    

@client.command()
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')

# @client.command()
# async def play(ctx, url:str):
#     await ctx.send('Sorry The Bot Is Not available **UNDER CONSTRUCTION**')

@client.command(aliases=['8ball','test'])
async def _8ball(ctx, *, question):
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful." ]
    
    await ctx.send(f'Questions: {question}\nAnswer: {random.choice(responses)}')
    
@client.command()
async def dm(ctx):
    await ctx.author.send("help command coming soon")
    
#Send anonymous DM's
@client.command()
async def send_anonymous_dm(ctx, member: discord.Member, *, content):
    channel = await member.create_dm() # creates a DM channel for mentioned user
    await channel.send(f'**Somebody Sent Anonymous Message Saying:** ||  {content}  ||') # send whatever in the content to the mentioned user.
# Usage: !send_anonymous_dm @mention_user <your message here>
 
# THIS FUNCTION WILL SEND A DM WITH THE AUTHORS NAME.
@client.command()
async def sendDM(ctx, member: discord.Member, *, content):
    channel = await member.create_dm() # creates a DM channel for mentioned user
    await channel.send(f"**{ctx.message.author} said:** {content}") # send whatever in the content to the mentioned user along with the author's name.
 
# Usage: !send_anonymous_dm @mention_user <your message here>


@client.command()
async def meme(ctx,subred = "memes"):
    subreddit = reddit.subreddit(subred)
    all_subs = []
    
    top = subreddit.top(limit = 100)

    for submission in top:
        all_subs.append(submission)
        
    random_sub = random.choice(all_subs)
    
    name = random_sub.title
    url = random_sub.url
    
    em = discord.Embed(title = name)
    
    em.set_image(url = url)
     
    await ctx.send(embed = em)
    
@client.command()
async def avatar(ctx, *, member: discord.Member=None): # set the member object to None
    if not member: # if member is no mentioned
        member = ctx.message.author # set member as the author
    userAvatar = member.avatar_url
    await ctx.send(userAvatar)

# @client.command()
# @commands.has_role('moderator')
# async def clear(ctx, amount=0):
#     await ctx.channel.purge()
    
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clean(ctx, amount=2):
        await ctx.channel.purge(limit=amount)
        await ctx.send('Cleared by {}'.format(ctx.author.mention))
        await ctx.message.delete()

@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"**You cant do that!** \n ")

    
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} **Has Been Kicked** for Reason **{reason}**.')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"**You cant do that!**\n")

# @client.command(name="kick", pass_context=True)
# @has_permissions(manage_roles=True, ban_members=True)
# async def _kick(ctx, member: Member):
#     await client.kick(member)

# # @_kick.error
# # async def kick_error(error, ctx):
# #     if isinstance(error, MissingPermissions):
# #         text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
# #         await client.send_message(ctx.message.channel, text)


    
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention} **Has Been Banned** for Reason **{reason}**')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"**You cant do that!**\n")

  
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user
        
        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'`Unbanned` {user.mention} wc Back!')

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"**You cant do that!**\n")
            
@client.command()
async def moderation(ctx):
    embed = discord.Embed(
        title = 'All Moderation Command',
        description = 'Commands:-',
        colour = discord.Colour.gold()
    )
    embed.set_footer(text='⭐Credits Go To: Dhruv⭐')
    embed.set_author(name='?moderation')
    embed.set_footer(text='⭐Credits Go To: Dhruv⭐')
    embed.add_field(name='ban <user.mention>', value='`Bans the User`\n', inline=True)
    embed.add_field(name='unban <name + #1234>', value='`Revoke The ban of The user`', inline=True)
    embed.add_field(name='kick <user.mention>', value='`kicks The User`', inline=True)
    embed.add_field(name='clean <value>', value='`Clears the messgae in channel`', inline=True)
    embed.add_field(name='avatar <user.mention> ', value='`Brings the Users Avatar`', inline=True)
    embed.add_field(name='ping ', value='`ping of the BOT`', inline=True)
    
    embed.set_thumbnail(url='https://vignette.wikia.nocookie.net/drawception/images/8/85/ModeratorBadge.jpeg/revision/latest?cb=20190201180259')
    

    await ctx.send(embed=embed)
    
@client.command()
async def special(ctx):
    embed = discord.Embed(
        title = '*All Specials Command*',
        # description = 'Commands:-',
        colour = discord.Colour.lighter_gray()
    )
    embed.set_footer(text='⭐Credits Go To: Dhruv⭐')
    # embed.set_author(name='?Help_specials')
    embed.set_footer(text='⭐Credits Go To: Dhruv⭐')
    embed.add_field(name='sendDM  <user.mention> <message>', value="`Send's DM via bot Mentioning your name.`", inline=False)
    embed.add_field(name='send_anonymous_dm  <user.mention>  <message>', value="`Send's DM via bot NOT Mentioning your name.`", inline=False)
    embed.set_thumbnail(url='https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/9672dd15202123.5628e1d8e1e8c.jpg')

    await ctx.send(embed=embed)

    
@client.command()
async def fun(ctx):
    embed = discord.Embed(
        title = "*Let's Have Some Fun*",
        # description = 'Commands:-',
        colour = discord.Colour.lighter_gray()
    )
    embed.set_footer(text='⭐Credits Go To: Dhruv⭐')
    # embed.set_author(name='?Help_specials')
    embed.set_footer(text='⭐Credits Go To: Dhruv⭐')
    embed.add_field(name='8ball <question>', value="`Classic 8ball Game with Predection`", inline=False)
    embed.add_field(name='meme or meme <subreddit>', value="`Get's you the best Top 50 Subreddit.`", inline=False)
    embed.set_thumbnail(url='https://www.richardsonsholidayparks.co.uk/wp-content/uploads/2019/03/Entertainment.png')

    await ctx.send(embed=embed)



@client.command()
async def help(ctx):
    embed = discord.Embed(
        title = '*Here To your Help*',
        # description = 'Our capablities',
        colour = discord.Colour.orange()
    )
    embed.set_footer(text='⭐Credits Go To: Dhruv⭐')
    # embed.set_author(name='?Help')
    embed.set_footer(text='⭐Credits Go To: Dhruv⭐')
    embed.set_footer(text='⭐Credits Go To: Dhruv⭐')
    embed.add_field(name='moderation', value='`All The Moderation Command`', inline=True)
    embed.add_field(name='special', value="`All the Special features of OUR bot`", inline=True)
    embed.add_field(name='fun', value='`Get some Fun`', inline=True)
    embed.add_field(name='set_prefix', value='`Customizes The Prefix For The Server`', inline=True)
    embed.set_thumbnail(url='https://www.graphicsprings.com/filestorage/stencils/d619ef29297bf4a1d98fa4bb57ab8d7f.png?width=500&height=500')
    embed.add_field(name='bot_info', value='```css\n Invite Bot , Source Code.. ```', inline=False)
    
    
    
    await ctx.send(embed=embed)
@client.command()
async def sm(ctx):
    embed = discord.Embed(
        title = 'Social media',
        description = '**[Dhruv Nation ~~ YTB ](https://www.youtube.com/channel/UCb9kY0I01P23eOxbs3kNH0g)\n[Audio Nation ~~ YTB](https://www.youtube.com/channel/UC9KPOrSqEI1O4pPD0waDsaQ)\n[GitHub](https://github.com/DHRUV-CODER)**',
        colour = discord.Colour.blue()
    )
    await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'`To use This you Require Administrator Privileges `\n \n **Assign A role Having Administrator Enabled**')
        

@client.command()
async def bot_info(ctx):
    embed = discord.Embed(
        title = '__Info__',
        description = "**[Invite](https://discord.com/api/oauth2/authorize?client_id=790592850588336151&permissions=8&scope=bot)**\n\n **[Bot's Source Code](https://github.com/DHRUV-CODER/Discord-Bot)**\n\n **Btw I was Created On *21/12/2020***",
        colour = discord.Colour.gold()
    )
    await ctx.send(embed=embed)   

keep_alive.keep_alive()

client.run(token)
from replit import db
