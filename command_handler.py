#!/usr/bin/env python

from sys import prefix
import discord
import game

class CommandHandler:
    # Command Prefix (ex: "!start")
    __prefix = '&'
    # A dictionary of command name to their help message
    __commands = {
        'init': 'Initialize the game by deciding what set of words to use. The sets are: English, JLPT N5 (just type N5), JLPT N4 (just type N4), JLPT N3 (just type N3), JLPT N2 (just type N2), JLPT N1 (just type N1). Usage: `{}init <set name>`. If a set name is not provided, English will selected.'.format(__prefix),
        'start': 'Play a game of hangman with Korosensei with English words! Save someone from being killed by him! Are you faster than a Mach 20 Monster!? Usage: `{}start`'.format(__prefix),
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
    async def handle(self, client, message) -> None:
        if message.content.startswith('{0}init'.format(self.__prefix)):
            if message.content.lower() == '{0}init help'.format(self.__prefix):
                await message.channel.send('{0}{1}: {2}'.format(self.__prefix, 'init', self.__commands['init']))
            elif len(message.content.split()) != 1:
                await self.__inititalize(message, message.content.split()[1])
            else:
                await self.__inititalize(message)
        elif message.content.startswith('{0}start'.format(self.__prefix)):
            if message.content.lower() == '{0}start help'.format(self.__prefix):
                await message.channel.send('{0}{1}: {2}'.format(self.__prefix, 'start', self.__commands['start']))
            else:
                await self.__start(client, message)
        elif message.content.startswith(self.__prefix + 'help'):
            await self.__help(message)
    async def __inititalize(self, message, set = 'english') -> None:
        if self.__sets.count(set.lower()) == 0:
            return await message.channel.send('No set called "{}" exists!'.format(set))
        self.__robespierre = game.Game(set)
        return await message.channel.send('Game initialized successfully! Now you can run the `{}start` command to start it!'.format(self.__prefix))
    async def __start(self, client, message) -> None:
        if len(self.__robespierre.get_word_pool()) == 0:
            await message.channel.send('No words have been added to the word pool!')
        else:
            await self.__robespierre.game_loop(client, message)
    async def __help(self, message) -> None:
        message_content = ''
        for item in self.__commands.items():
            message_content += '{0}{1}: {2}\n'.format(self.__prefix, item[0], item[1])
        # Remove the extraneous new line character
        message_content.removesuffix('\n')
        await message.channel.send(message_content)
