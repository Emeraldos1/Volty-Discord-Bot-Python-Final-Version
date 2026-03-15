from __future__ import unicode_literals
import discord
from discord.ext import commands, tasks
import re
import time
import requests
import json
import sys
import youtube_dl
import os
import random
import asyncio
from photoCog import pictureCog
from musicCog import musicCog




client = commands.Bot(command_prefix = "v!")

@client.event

async def on_ready():
    print("Bot is ready!")

    game = discord.Game("You could have something like this in your server!")
    await client.change_presence(activity=game)

   
    

@client.command()

async def buyme(ctx):
    await ctx.send("Hello! You could have something like this in your server!")



@client.command()
@commands.has_guild_permissions(kick_members = True)
async def kick(ctx,member: discord.Member ,*, reason = "None"):
    await member.kick(reason=reason)
    await ctx.send(f"Successfully kicked {member}")


@client.command()
@commands.has_guild_permissions(ban_members=True)

async def ban(ctx, member:discord.Member ,*, reason = "None"):
              await member.ban(reason=reason)
              await ctx.send(f"Successfully banned {member}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("Insufficient permission to perform ban command")


@client.command()
@commands.has_guild_permissions(ban_members=True)
async def unban(ctx, member:discord.Member):
    guild = discord.Guild(ctx.Guild)

    await guild.unban(member)

    await ctx.send(f"{member} has been unbanned!")

@unban.error
async def unban_error(ctx, error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("Insufficient permission to perform unban command")

    

@client.command()
#@commands.has_guild_permissions(manage_messages = True)
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"Successfully cleared {amount} message(s)!")

@clear.error

async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have sufficient permission to execute the clear command")

@client.command()

async def kill(ctx, member:discord.Member):
    killImage = discord.Embed()

    killImage.set_image(url = "https://upload.wikimedia.org/wikipedia/commons/5/52/Skeet._William_H._Keever%2C_USA.JPEG")

    await ctx.send(f"PEW PEW PEW YOU'RE DEAD, @{member}", embed = killImage)
   

@client.command()
async def poll(ctx,*, question = "Undefined"):
    command = ctx.message
    await command.delete()
    botMessage = await ctx.send(question)
    await discord.Message.add_reaction(botMessage, emoji="\U0001F44D")
    await discord.Message.add_reaction(botMessage, emoji="\U0001F44E")




    



@client.command()

async def nick(ctx, member:discord.Member,*, name = "Undefined"):

    await member.edit(nick=name)

    await ctx.send(f"Changed nickname to {name}!")
    
@nick.error
async def nick_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Insufficient permissions to execute the nickname command")
   
@client.command()
@commands.has_guild_permissions(mute_members=True)
async def mute(ctx, member:discord.Member,*, reason="Undefined"):
    await ctx.send(f"{member} has been muted for reason: {reason}!")

    await member.edit(mute=True)

    server = ctx.guild

    serverRoles = server.roles

    itemBoolean = False

    print(itemBoolean)

    for item in serverRoles:
        if str(item) == "Muted":
            itemBoolean = True

            mutedRole = item

            print(item)
            print(itemBoolean)

            break
            
        else:
            itemBoolean = False
            
            print(item)
            print(itemBoolean)

    if itemBoolean == True:
        print("Muted Role already exists")

        mutedRoleList = [mutedRole]

        await member.edit(roles=mutedRoleList)

        listofChannels = server.text_channels

        for item in listofChannels:
            await item.set_permissions(mutedRole, send_messages = False)

        

    else:
        print("Create Muted Role!")
        mutedPermissions = discord.Permissions()

        mutedPermissions = mutedPermissions.none()

        mutedRole = await server.create_role(name="Muted", permissions = mutedPermissions)

        mutedRoleList = [mutedRole]

        await member.edit(roles=mutedRoleList)

        listofChannels = server.text_channels

        for item in listofChannels:
            await item.set_permissions(mutedRole, send_messages = False)



        
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("insufficient permissions to execute mute command")
    
   

@client.command()
@commands.has_guild_permissions(mute_members=True)
async def unmute(ctx, member:discord.Member):
    await member.edit(mute=False, roles = [])

   

    await ctx.send(f"{member} has been unmuted!")

@unmute.error
async def unmute_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("insufficient permissions to execute unmute command")


@client.command()
async def magicball(ctx,*,question):
    r = requests.get(url=f"https://8ball.delegator.com/magic/JSON/{question}")
    r = json.loads(r.content)
    r = r["magic"]

    await ctx.send(str(r["answer"]) + " \u2728")

@client.command()
async def gif(ctx,*, search):

    params = {}
    
    r = requests.get(url=f"https://api.giphy.com/v1/gifs/search?api_key=xEydZo9zuGvVA8cv1OrvUBLtrINtZbKL&q={search}&limit=25&offset=0&rating=G&lang=en")

    r = json.loads(r.content)

    r = r["data"]

    r = r[0]

    r = r["url"]


    print(r)

 

    await ctx.send("Here's your gif!")

    await ctx.send(r)

@client.command()

async def currency(ctx, fromcurrency, tocurrency, amount):
    fromcurrency = fromcurrency.upper()

    tocurrency = tocurrency.upper()



    r = requests.get(f"https://api.exchangeratesapi.io/latest?symbols={fromcurrency},{tocurrency}")


    r = json.loads(r.content)

    r = r["rates"]

    r = r[tocurrency]

    exchangeCurrency = float(amount) * float(r)

    await ctx.send(f"{amount} {fromcurrency} is equal to {exchangeCurrency} {tocurrency}")

@client.command()
async def stop(ctx):
    voiceConnection.stop()

    await ctx.send("Stopped playing!")

    game = discord.Game("Nikiera looks like Leshawna")
    await client.change_presence(activity=game)

@client.command()
async def pause(ctx):
    voiceConnection.pause()

    await ctx.send("\u23F8 Paused song!")

    game = discord.Game("Nikiera looks like Leshawna")
    await client.change_presence(activity=game)

@client.command()
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)

@client.command()
async def fiverr(ctx):
    await ctx.message.delete()
    await ctx.send("Hi I'm a bot Emeraldos made! It can do all sorts of things like play music, play games, mute people, send gifs, and many more!")
    await ctx.send("If you want something like this, request me to do one for you on fiverr - all for cheap prices!")


client.add_cog(pictureCog())

client.add_cog(musicCog())



client.run("NjYzNDE2NjgxNjMyMTA0NDY4.XwAd_g.3BjrtsuvjHrIE1nYcmIv2fF3N84")



























