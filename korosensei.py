import discord
import command_handler

class KoroClient(discord.Client):
    handler = command_handler.CommandHandler()
    # Read info file to get any special information
    info_file = open('info.txt', 'r').readlines()
    # Read the first line to get the client token
    token = info_file[0]

    async def on_ready(self) -> None:
        print('Agents are go!')
    async def on_message(self, message) -> None:
        # Prevent bot from messaging himself
        if message.author == self.user:
            return

        # Use CommandHandler class to handle all other messages
        await self.handler.handle(self, message)

# Run bot
client = KoroClient()
client.run(client.token)
