import sys
from urllib.parse import quote_plus
from asyncio import sleep
from PIL.Image import core as _imaging
import disnake
from disnake.ext import commands
import os
import typing as typ
from typing import Union, Optional, List
import json
import _json
import random
import datetime
import asyncio
import aiohttp
import time
from dotenv import load_dotenv
import io
from io import BytesIO
from petpetgif import petpet as petpetgif

load_dotenv()

intents = disnake.Intents.all()
intents.members = True
bot = commands.Bot(intents=intents, command_prefix='.')
bot.remove_command('help')

afk_users = []
afk_users_reason = []

ping_users = []
ping_users_reply = []

requested_economy_users = []
coined_economy_users = []
rob_economy_users = []
daily_collect = []

@bot.listen()
async def on_message(msg):
  if msg.author.id == 963478861872496702 or msg.author.id == 952885946267889674:
    return
  for x in range(len(afk_users)):
      y = afk_users[x]
      bruho = await bot.fetch_user(y)
      if str(y) in msg.content:
          await msg.channel.send(f"{bruho.name}, is currently afk- {afk_users_reason[x]}")

      elif msg.author.id == y:
          await msg.channel.send(f"Welcom back {bruho.name}, I've removed your AFK :)")
          afk_users.pop(x)
          afk_users_reason.pop(x)
                    
  for a in range(len(ping_users)):
              b = ping_users[a]
              bruho = await bot.fetch_user(b)
              if str(b) in msg.content:
                  await msg.channel.send(f"{bruho.name} has set an autoreply for you- {ping_users_reply[a]}")
                
@bot.event
async def on_ready():
  print(f'The bot({bot.user}) is now ready to rock')
  
def convert(time):
    pos = ["s", "m", "h", "d", ]

    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[: -1])
    except:
        return -2

    return val * time_dict[unit]
  
@bot.event
async def on_message_delete(message):
    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content
    if message.guild.id == 952882695413858334:
        log_channel = mod.get_channel(955460713168642058)
        loge = disnake.Embed(title="Mesage Deleted", description="", colour=message.author.colour)
        loge.add_field(name="The Message", value=snipe_message_content[message.channel.id])
        loge.set_footer(text=f"Message deleted by {snipe_message_author[message.channel.id]}")
        await log_channel.send(embed=loge)
    await sleep(21600)
    del snipe_message_author[message.channel.id]
    del snipe_message_content[message.channel.id]
  
@bot.slash_command(name="afk", description="Set your afk")
async def afk(ctx, reason=None):
    if reason == None:
        reason = "No reason Provided"

    if ctx.author.id in afk_users:
        for x in range(len(afk_users)):
            thingy = afk_users.index(ctx.author.id)
            await ctx.send(f"Hi {ctx.author.mention}, welcome back!\n\nI've removed your afk for the reason : {afk_users_reason[thingy]}")
            if int(afk_users[x]) == ctx.author.id:
                afk_users.pop(x)
        #e = afk_users_reason.index(afk_users(ctx..id))
                afk_users_reason.pop(x)

    elif ctx.author.id not in afk_users:
        await ctx.send(f"{ctx.author.mention} I've set your afk\n\nReason: {reason}")
        afk_users.append(ctx.author.id)
        afk_users_reason.append(reason)
        
@bot.slash_command(name="ping_reply", description="Set your reply for ping")
async def ping_reply(ctx, reply=None):
    if reply == None:
        reply = f"He didn't set a message, but its simple, they don't want to get pinged, right?"
    
    if ctx.author.id in ping_users:
        for x in range(len(ping_users)):
            thingy = ping_users.index(ctx.author.id)
            await ctx.send(f"Hi {ctx.author.mention}, welcome back!\n\nI've removed your reply: {ping_users_reply[thingy]}")
            if int(ping_users[x]) == ctx.author.id:
                ping_users.pop(x)
                ping_users_reply.pop(x)

    elif ctx.author.id not in ping_users:
        await ctx.send(f"{ctx.author.mention} I've set your reply: {reply}")
        ping_users.append(ctx.author.id)
        ping_users_reply.append(reply)
        
@bot.slash_command(name="meme", description="Shows a fun meme")
async def meme(ctx):
  embed = disnake.Embed(title="", description="", color=ctx.author.color)
  print(f"showing meme to {ctx.author}")
  async with aiohttp.ClientSession() as cs:
    async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
      res = await r.json()
      embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
      embed.set_footer(text=f"Meme requested by {ctx.author}")
      await ctx.send(embed=embed)
      
@bot.slash_command(name="ynpoll", description="Creates a yes/no poll")
async def ynpoll(ctx, *, content: str):
    if ctx.author.id in bot_ban_user or ctx.guild.id in bot_ban_server:
        print(f"{ctx.author.mention} is bot banned, but trying to use a command")

    elif ctx.author.id not in bot_ban_user and ctx.guild.id not in bot_ban_server:
        print(f"Creating yes/no poll... for {ctx.author}")
        embed = disnake.Embed(title=f"{content}", description="React to this message with ✅ for yes, ❌ for no.",
                              color=ctx.author.color)
        message = await ctx.channel.send(embed=embed)
        print(f"Creating Yesno Poll From {ctx.author}")
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        
@bot.slash_command(name="snipe", description="Snipe a messgae")
async def snipe(ctx):
  channel = ctx.channel
  try:
    snipeEmbed = disnake.Embed(title=f"Last deleted message in #{channel.name}", description=snipe_message_content[channel.id])
    snipeEmbed.set_footer(text=f"Deleted by {snipe_message_author[channel.id]}")
    await ctx.send(embed=snipeEmbed)
        
@bot.slash_command(name="say", description="says something for you!")
async def say(ctx, *, text):
  await ctx.send(f'Alright!', ephemeral=True)
  await ctx.channel.send(f'{text}')
  
@bot.slash_command(name="ban", description="ban someone")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: disnake.Member, *, reason=None):
    if reason == None:
        reason = "No reason Provided"
    if ctx.guild.name == member.guild.name:
        if member.id != ctx.author.id:
            await member.ban(reason=reason)
            await ctx.send(f'User {member} has been banned')
            
@bot.slash_command(name="kick", description="kick someone")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: disnake.Member, *, reason=None):
    if reason == None:
        reason = "No reason Provided"
    if ctx.guild.name == member.guild.name:
        if member.id != ctx.author.id:
            await member.kick(reason=reason)
            await ctx.send(f'User {member} has been kicked')
            
@bot.slash_command(name="balance", description="Balance")
async def balance(ctx, person: disnake.Member=None):
    if person == None:
        person = ctx.author
    await open_account(person)
    user = person
    users = await get_bank_data()
    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]


    em = disnake.Embed(title=f"{person.name}'s Balance", color=ctx.author.color)
    em.add_field(name="Wallet", value=f'{wallet_amt} :coin:', inline=False)
    em.add_field(name="Bank", value=f'{bank_amt} :coin:', inline=False)
    await ctx.send(embed=em)
    
@bot.slash_command(name="beg", description="Request your luck")
async def beg(ctx):
    if ctx.author.id in requested_economy_users:
        await ctx.send(f"{ctx.author.mention} Please wait a while before you can request again")

    elif ctx.author.id not in requested_economy_users:
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        earnings = random.randrange(101)
        final = [f"Look at you small people, here take {earnings} :coin:", f"Imagine requesting, you can have {earnings}"]
        final_stuff = random.choice(final)
        await ctx.send(final_stuff)

        users[str(user.id)]["wallet"] += earnings
        with open("mainbank.json", "w") as f:
            json.dump(users, f)

        requested_economy_users.append(ctx.author.id)
        await sleep(45)
        requested_economy_users.remove(ctx.author.id)
        
@bot.slash_command(name="deposit", description="Deposit some money in your bank")
async def deposit(ctx, amount):
    await open_account(ctx.author)

    bal = await update_bank(ctx.author)
    if amount == "all":
        amount = bal[0]
    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("You don't have that much money bro...\n**TIP: EARN/WITHDRAW THE MONEY**")
        return

    elif amount<0:
        await ctx.send("Please have some common sense, how can you deposit negative money? :joy:")
        return

    await update_bank(ctx.author, -1*amount)
    await update_bank(ctx.author, amount, "bank")
    await ctx.send(f"You gave {amount} :coin: to your bank!")

@bot.slash_command(name="withdraw", description="Withdraw some money from your bank")
async def withdraw(ctx, amount):
    await open_account(ctx.author)

    bal = await update_bank(ctx.author)
    if amount == "all":
        amount = bal[1]
    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("You don't have that much money bro...\n**TIP: DEPOSIT THE MONEY**")
        return

    elif amount<0:
        await ctx.send("Please have some common sense, how can you withdraw negative money? :joy:")
        return

    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1*amount, "bank")
    await ctx.send(f"You took {amount} :coin: from your bank!")
    

@bot.slash_command(name="gift", description="Withdraw some money from your bank")
async def gift(ctx, person: disnake.Member, amount):
    if ctx.author == person:
        await ctx.send("You can't transfer money to yourself...")
        return
    await open_account(ctx.author)
    await open_account(person)

    bal = await update_bank(ctx.author)
    if amount == "all":
        amount = bal[1]
    amount = int(amount)

    if ctx.author.id == 704640724490256384:
        await update_bank(person, amount, "bank")
        await ctx.send(f"{ctx.author.mention}, You gave {amount} :coin: from your bank to {person.mention}")
        return
    else:

        if amount>bal[1]:
            await ctx.send("You don't have that much money bro...")
            return

        elif amount<0:
            await ctx.send("Please have some common sense, how can you transfer negative money? :joy:")
            return


        await update_bank(ctx.author, -1*amount, "bank")
        await update_bank(person, amount, "bank")
        await ctx.send(f"{ctx.author.mention}, You gave {amount} :coin: from your bank to {person.mention}")
        
@bot.slash_command(name="rob", description="Rob Someone")
async def rob(ctx, person: disnake.Member):
    if person.id in making_staff_steal_proof:
        await ctx.send("You can't rob a staff")
        return
    if ctx.author.id in rob_economy_users:
        await ctx.send("Please wait a while before robbing again")
        return
    if person.id == 704640724490256384:
        return
    if ctx.author == person:
        await ctx.send(f"XD, you are robbing yourself -_-")
        return
    await open_account(ctx.author)
    await open_account(person)
    oof = [0,0,0,0,0,1,1,1,1,1]
    oops = random.choice(oof)
    if oops == 0:
        bal = await update_bank(ctx.author)
        if bal[0]<2500:
            earning = bal[0]/2
            await ctx.send(f"HAHA, {person} caught you, and you had to pay him {earning} as a penalty")

        else:
            earning = 2500
            await ctx.send(f"HAHA, {person} caught you, and you had to pay him {earning} as a penalty")

        await update_bank(person, earning)
        await update_bank(ctx.author, -1*earning)

    else:
        bal = await update_bank(person)
        if bal[0]<=500:
            await ctx.send(f"{person.mention} is currently poor, so you can't rob him.\nInstead donate him some money.")
            return

        elif bal[0]>500:
            real = int(bal[0])
            realme = real/2
            earning = random.randrange(0, int(bal[0]))
            await ctx.send(f"You took {earning} from {person.mention}")
            await update_bank(person, -1*earning)
            await update_bank(ctx.author, earning)

    rob_economy_users.append(ctx.author.id)
    await sleep(45)
    rob_economy_users.remove(ctx.author.id)
    
@bot.slash_command(name="daily", description="daily rewards")
async def daily(ctx):
    await open_account(ctx.author)
    bal = await update_bank(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    if user.id in daily_collect:
        await ctx.send("You already collected it within 24 hours, please try again later")
        return
    daily_collect.append(user.id)
    await update_bank(user, 500)
    await ctx.send("500 :coin: debited in your account :D")
    await sleep(86400)
    await daily_collect.remove(user.id)
    
bot.run('TOKEN')
