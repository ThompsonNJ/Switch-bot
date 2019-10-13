import discord
from discord.ext.commands import Bot
from discord.utils import get
from discord.ext import commands
import asyncio
import random
import os
import time
import sqlite3
import re

bot = commands.Bot(command_prefix='!')
bot_channel = "526962869628043264"
get_roles_channel = "526958491303411752"
switch_ids = {}

@bot.event
async def on_ready():
    with open("switch_ids.txt") as file:
        for line in file:
            splitted_line = line.strip().split(":")
            switch_ids[splitted_line[0]] = splitted_line[1]

    await bot.send_message(get_roles_channel, "!purge 1")
    message = await bot.send_message(get_roles_channel, "*React with the MOST relevant emote to set your region.*")
    await bot.add_reaction(message, ":nae:")
    await bot.add_reaction(message, ":naw:")
    await bot.add_reaction(message, ":eue:")
    await bot.add_reaction(message, ":euw:")
    await bot.add_reaction(message, ":sam:")
    await bot.add_reaction(message, ":oce:")

    print("Online")


@bot.command(pass_context=True)
async def link(ctx, msg = None):
    if ctx.message.channel.id == bot_channel:
        try:
            if str(ctx.message.author) in switch_ids:
                await bot.say("`User already linked!`")
                raise KeyError

            if re.search('-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]', msg) and msg.upper().startswith("SW"):
                if msg is not None:
                    msg = msg.upper()
                    with open("switch_ids.txt", 'a') as file:
                        file.write(str(ctx.message.author) + ":" + msg + "\n")

                    switch_ids[str(ctx.message.author)] = msg
                    await bot.add_reaction(ctx.message,"\U00002705")
                else:
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            await bot.say("`Must be in format: SW-####-####-####`")
            await bot.add_reaction(ctx.message, "\U0000274c")

        except KeyError:
            await bot.add_reaction(ctx.message, "\U0000274c")


@bot.command(pass_context=True)
async def unlink(ctx):
    if ctx.message.channel.id == bot_channel and str(ctx.message.author) in switch_ids:
        switch_ids.pop(str(ctx.message.author), None)
        with open("switch_ids.txt", 'w') as file:
            for i in switch_ids:
                file.write(i + ":" + switch_ids[i] + "\n")

        await bot.add_reaction(ctx.message, "\U00002705")

    elif ctx.message.channel.id == bot_channel and str(ctx.message.author) not in switch_ids:
        await bot.say("`User is not linked!`")
        await bot.add_reaction(ctx.message, "\U0000274c")

@bot.command(pass_context=True)
async def add(ctx, msg = None):
    if msg is None:
        try:
            await bot.say(switch_ids.get(str(ctx.message.author), None))
        except:
            await bot.say("`User not found!`")

    else:
        try:
            await bot.say(switch_ids[msg])
        except:
            await bot.say("`{} not found!`".format(msg))

@bot.command(pass_context=True)
async def purge(ctx, amount):
    role_names = [role.name.lower() for role in ctx.message.author.roles]
    if "admin" in role_names:
        await bot.purge_from(ctx.message.channel, limit=int(amount) + 1)



# @bot.command(pass_context=True)
# async def roles(ctx):
#     role_names = [role.name.lower() for role in ctx.message.author.roles]
#     if "admin" in role_names:
#         embed = discord.Embed(color=0xff0000)
#         embed.add_field(name = "React with the relevant emote(s) to set your preferred character(s). You may choose up to three.",
#                         value = "__ __")
#         embed.set_image(url = "https://i.imgur.com/7N57zuc.jpg")
#         message = await bot.say(embed=embed)
#
#         for i in range(74):
#             emoji = get(bot.get_all_emojis(), name=reactions[0])
#             await bot.add_reaction(message, emoji)
#
#
#         # for emoji_name in reactions:
#         #     emoji = get(bot.get_all_emojis(), name=emoji_name)
#         #     await bot.add_reaction(message, emoji)
#

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.id != get_roles_channel:
        return

    role_names = [role.name for role in user.roles]
    if "NA-East" not in role_names and "NA-West" not in role_names and "EU-East" not in role_names and\
            "EU-West" not in role_names and "South America" not in role_names and "Oceania" not in role_names:

        if reaction.emoji.name == "nae":
            role = discord.utils.get(user.server.roles, name="NA-East")
            await bot.change_nickname(user, "[NAE] " + user.display_name)
            await bot.add_roles(user, role)

        elif reaction.emoji.name == "naw":
            role = discord.utils.get(user.server.roles, name="NA-West")
            await bot.change_nickname(user, "[NAW] " + user.display_name)
            await bot.add_roles(user, role)

        elif reaction.emoji.name == "euw":
            role = discord.utils.get(user.server.roles, name="EU-East")
            await bot.change_nickname(user, "[EUE] " + user.display_name)
            await bot.add_roles(user, role)

        elif reaction.emoji.name == "eue":
            role = discord.utils.get(user.server.roles, name="EU-West")
            await bot.change_nickname(user, "[EUW] " + user.display_name)
            await bot.add_roles(user, role)

        elif reaction.emoji.name == "sam":
            role = discord.utils.get(user.server.roles, name="South America")
            await bot.change_nickname(user, "[SAM] " + user.display_name)
            await bot.add_roles(user, role)

        elif reaction.emoji.name == "oce":
            role = discord.utils.get(user.server.roles, name="Oceania")
            await bot.change_nickname(user, "[OCE] " + user.display_name)
            await bot.add_roles(user, role)


@bot.event
async def on_reaction_remove(reaction, user):
    if reaction.message.channel.id != get_roles_channel:
        return

    role_names = [role.name for role in user.roles]
    if reaction.emoji.name == "nae":
        role = discord.utils.get(user.server.roles, name="NA-East")
        await bot.change_nickname(user, user.display_name[6:])
        await bot.remove_roles(user, role)

    elif reaction.emoji.name == "naw":
        role = discord.utils.get(user.server.roles, name="NA-West")
        await bot.change_nickname(user, user.display_name[6:])
        await bot.remove_roles(user, role)

    elif reaction.emoji.name == "euw":
        role = discord.utils.get(user.server.roles, name="EU-East")
        await bot.change_nickname(user, user.display_name[6:])
        await bot.remove_roles(user, role)

    elif reaction.emoji.name == "eue":
        role = discord.utils.get(user.server.roles, name="EU-West")
        await bot.change_nickname(user, user.display_name[6:])
        await bot.remove_roles(user, role)

    elif reaction.emoji.name == "sam":
        role = discord.utils.get(user.server.roles, name="South America")
        await bot.change_nickname(user, user.display_name[6:])
        await bot.remove_roles(user, role)

    elif reaction.emoji.name == "oce":
        role = discord.utils.get(user.server.roles, name="Oceania")
        await bot.change_nickname(user, user.display_name[6:])
        await bot.remove_roles(user, role)


# @bot.command(pass_context=True)
# async def emb(ctx):
#     embed = discord.Embed(title="Bot Commands", color=0xff0000)
#     embed.set_thumbnail(url = "https://i.gyazo.com/d701299bf4d97566ed8a8691126883a7.png")
#     embed.add_field(name="!link", value="Link your Switch account to your Discord account in the format: `SW-####-####-####`.", inline=False)
#     embed.add_field(name="!unlink", value="Unlink your Switch account from your Discord account.", inline=False)
#     embed.add_field(name="!add", value="Send your linked Switch account to the current channel.", inline=False)
#     embed.add_field(name="!add <username#1234>", value="Send the specified user's linked Switch account to the current channel.", inline=False)
#     await bot.say(embed=embed)


bot.run("TOKEN")
