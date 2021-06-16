import discord
import command_handler

client = discord.Client()
handler = command_handler.CommandHandler()
# Read info file to get any special information
info_file = open('info.txt', 'r').readlines()
# Read the first line to get the client token
token = info_file[0]

@client.event
async def on_ready() -> None:
    print('Agents are go!')
@client.event
async def on_message(message) -> None:
    # Prevent bot from messaging himself
    if message.author == client.user:
        return

    # Use CommandHandler class to handle all other messages
    await handler.handle(message)

# Run bot
client.run(token)
