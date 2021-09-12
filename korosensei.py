#!/usr/bin/env python

import hikari
import command_handler

# Read info file to get any special information
info_file = open('info.txt', 'r').readlines()
# Read the first line to get the client token
bot = hikari.GatewayBot(token=info_file[0].strip())

handler = command_handler.CommandHandler()

@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent) -> None:
    if event.is_bot or not event.content:
        return
    # use CommandHandler class to handle all other messages
    await handler.handle(bot, event.message)

bot.run()
