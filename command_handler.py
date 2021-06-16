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
    }

    def get_prefix(self) -> 'str':
        return self.__prefix
    def set_prefix(self, prefix) -> None:
        self.__prefix = prefix
    def get_commands(self) -> 'dict':
        return self.__commands

    # Check if the message starts with a command and then execute that command
    async def handle(self, message) -> None:
        if message.content.startswith(self.__prefix + 'start') or message.content.startswith(self.__prefix + 'start-en'):
            await self.__start_en(message)
        # elif message.content.startswith(self.__prefix + 'start-enja'):
        #     await self.__start_enja(message)
        # elif message.content.startswith(self.__prefix  + 'start-ja') or message.content.startswith(self.__prefix + 'スタート'):
        #     await self.__start_ja(message)


    async def __start_en(self, message) -> None:
        robespierre = game.Game('disjointed')
        await robespierre.game_loop(message)
    # async def __start_enja(self, message) -> None:
    #     pass
    # async def __start_ja(self, message) -> None:
    #     pass
