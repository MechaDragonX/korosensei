#!/usr/bin/env python

from sys import prefix
import hikari
import game

class CommandHandler:
    # Command Prefix (ex: "!start")
    __prefix = '&'
    # Color of main embeds; Korosensei's color
    __koro_color = hikari.Color(0xfff46c)
    # Success color
    __success_color = hikari.Color(0x00ff7f)
    # Color of error embeds
    __error_color = hikari.Color(0xff4040)
    # A dictionary of command name to their help message
    __commands = {
        'init': 'Initialize the game by deciding what set of words to use. The sets are: English, JLPT N5 (just type N5), JLPT N4 (just type N4), JLPT N3 (just type N3), JLPT N2 (just type N2), JLPT N1 (just type N1). Usage: `{}init <set name>`. If a set name is not provided, English will selected.'.format(__prefix),
        'start': 'Play a game of hangman with Korosensei with English or Japanese words! Save someone from being killed by him! Are you faster than a Mach 20 Monster!? Usage: `{}start`'.format(__prefix),
        'help': 'This very command! Usage: `{}help`'.format(__prefix)
    }
    __sets = [ 'english', 'n5', 'n4', 'n3', 'n2', 'n1' ]
    # The game
    __robespierre = None

    def get_prefix(self) -> 'str':
        return self.__prefix
    def set_prefix(self, prefix) -> None:
        self.__prefix = prefix
    def get_commands(self) -> 'dict':
        return self.__commands

    # Check if the message starts with a command and then execute that command
    async def handle(self, bot, message) -> None:
        if message.content.startswith('{0}init'.format(self.__prefix)):
            if message.content.lower() == '{0}init help'.format(self.__prefix):
                await message.respond(hikari.Embed(title='{0}init'.format(self.__prefix), description=self.__commands['init'], color=self.__koro_color))
            elif len(message.content.split()) != 1:
                await self.__inititalize(message, message.content.split()[1])
            else:
                await self.__inititalize(message)
        elif message.content.startswith('{0}start'.format(self.__prefix)):
            if message.content.lower() == '{0}start help'.format(self.__prefix):
                await message.respond(hikari.Embed(title='{0}start'.format(self.__prefix), description=self.__commands['start'], color=self.__koro_color))
            else:
                await self.__start(bot, message)
        elif message.content.startswith(self.__prefix + 'help'):
            await self.__help(message)
    async def __inititalize(self, message, set = 'english') -> None:
        if self.__sets.count(set.lower()) == 0:
            # TODO: Add help/description for error mesage
            return await message.respond(hikari.Embed(title='No set called "{}" exists!'.format(set), color=self.__error_color))
        self.__robespierre = game.Game(set)
        return await message.respond(hikari.Embed(title='Game Initialized successfully!', description='Now you can run the `{}start` command to start it!'.format(self.__prefix), color=self.__success_color))
    async def __start(self, bot, message) -> None:
        if self.__robespierre == None:
            await message.respond(hikari.Embed(title='No words have been added to the word pool!', description='Please use the `{}init` command to do so! Type `help` after it for help!'.format(self.__prefix), color=self.__error_color))
        else:
            await self.__robespierre.game_loop(bot, message)
    async def __help(self, message) -> None:
        await message.respond(hikari.Embed(title='How to Start a Game', description='1. Initialize the game with a set. See the info on `{0}init` for more details.\n2. Start the game with `{0}start`\n3. Have fun!'.format(self.__prefix), color=self.__koro_color))
        command_description = ''
        for item in self.__commands.items():
            command_description += '{0}{1}: {2}\n\n'.format(self.__prefix, item[0], item[1])
        # Remove the extraneous new line character
        command_description.removesuffix('\n')
        await message.respond(hikari.Embed(title="Command List", description=command_description, color=self.__koro_color))
