import discord
import game

class CommandHandler:
    # Command Prefix (ex: "!start")
    __prefix = '!'
    # A dictionary of command name to their help message
    __commands = {
        'start': 'Play a game of hangman with Korosensei with English words! Save someone from being killed by him! Are you faster than a Mach 20 Monster!?',
        'start-en': 'Play a game of hangman with Korosensei with English words! Save someone from being killed by him! Are you faster than a Mach 20 Monster!?',
        # 'start-enja': 'Play a game of hangman with Korosensei with Japanese words! Save someone from being killed by him! Are you faster than a Mach 20 Monster!?',
        # 'start-ja': '殺（ころ）せんせーとハングマンをやろう！ あいつから人（ひと）を助（たす）けろ！マッハ２０の怪物（かいぶつ）より速（はや）いのか！？',
        # 'スタート': '殺（ころ）せんせーとハングマンをやろう！ あいつから人（ひと）を助（たす）けろ！マッハ２０の怪物（かいぶつ）より速（はや）いのか！？'
        'help': 'This very command!'
    }

    def get_prefix(self) -> 'str':
        return self.__prefix
    def set_prefix(self, prefix) -> None:
        self.__prefix = prefix
    def get_commands(self) -> 'dict':
        return self.__commands

    # Check if the message starts with a command and then execute that command
    async def handle(self, client, message) -> None:
        if message.content.startswith('{0}start'.format(self.__prefix)) or message.content.startswith('{0}start-en'.format(self.__prefix)):
            if message.content.lower() == '{0}start help'.format(self.__prefix) or message.content.lower() == '{0}start-en help'.format(self.__prefix):
                await message.channel.send('{0}{1}: {2}'.format(self.__prefix, 'start', self.__commands['start']))
            else:
                await self.__start_en(client, message)
        # elif message.content.startswith(self.__prefix + 'start-enja'):
        #     await self.__start_enja(message)
        # elif message.content.startswith(self.__prefix  + 'start-ja') or message.content.startswith(self.__prefix + 'スタート'):
        #     await self.__start_ja(message)
        elif message.content.startswith(self.__prefix + 'help'):
            await self.__help(message)

    async def __start_en(self, client, message) -> None:
        robespierre = game.Game('disjointed')
        await robespierre.game_loop(client, message)
    # async def __start_enja(self, message) -> None:
    #     pass
    # async def __start_ja(self, message) -> None:
    #     pass
    async def __help(self, message) -> None:
        message_content = ''
        for item in self.__commands.items():
            message_content += '{0}{1}: {2}\n'.format(self.__prefix, item[0], item[1])
        # Remove the extraneous new line character
        message_content.removesuffix('\n')
        await message.channel.send(message_content)
