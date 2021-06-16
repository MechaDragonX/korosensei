import asyncio
import discord

class Game:
    __correct_guesses = []
    __wrong_guesses = []
    __word = ''
    __fail_count = 0
    __gallow_states = [
        '  ___\n |   |\n     |\n     |\n     |\n   __|__',
        '  ___\n |   |\n O   |\n     |\n     |\n   __|__',
        '  ___\n |   |\n O   |\n |   |\n     |\n   __|__',
        '  ___\n |   |\n O   |\n\\|   |\n     |\n   __|__',
        '  ___\n |   |\n O   |\n\\|/  |\n     |\n   __|__',
        '  ___\n |   |\n O   |\n\\|/  |\n/    |\n   __|__',
        '  ___\n |   |\n O   |\n\\|/  |\n/\\   |\n   __|__'
    ]

    def __init__(self, word) -> None:
        self.__word = word
        self.__gen_guessed_parts()

    def __gen_guessed_parts(self, guessed_letter = ' ') -> None:
        if len(self.__correct_guesses) == 0 and self.__fail_count == 0:
            i = 0
            while i < len(self.__word):
                self.__correct_guesses.append(' ')
                i += 1
        else:
            i = 0
            while i < len(self.__word):
                if self.__word[i] == guessed_letter:
                    self.__correct_guesses[i] = guessed_letter
                i += 1
    async def __print_game_field(self, message) -> None:
        message_to_send = ''
        await message.channel.send(self.__gallow_states[self.__fail_count])

        i = 0
        while i < len(self.__word):
            if i == len(self.__word) - 1:
                message_to_send += self.__correct_guesses[i]
            else:
                message_to_send += '{} '.format(self.__correct_guesses[i])
            i += 1
        await message.channel.send(message_to_send)

        message_to_send = ''
        i = 0
        while i < len(self.__word):
            if i == len(self.__word) - 1:
                message_to_send += '_'
            else:
                message_to_send += '_ '
            i += 1
        await message.channel.send(message_to_send)

        message_to_send = ''
        i = 0
        while i < len(self.__wrong_guesses):
            if i == len(self.__wrong_guesses) - 1:
                message_to_send += self.__wrong_guesses[i]
            else:
                message_to_send += '{} '.format(self.__wrong_guesses[i])
            i += 1
        await message.channel.send(message_to_send)
    def __check(self, letter) -> 'int':
        if letter not in self.__word:
            self.__wrong_guesses.append(letter)
            self.__fail_count = len(self.__wrong_guesses)
            return 1
        elif letter in self.__correct_guesses:
            return 2
        else:
            self.__gen_guessed_parts(letter)
            return 0
    async def __end_game(self, message) -> 'bool':
        self.__print_game_field()
        await message.channel.send()

        if self.__fail_count == 6:
            await message.channel.send('Game Over!\nThe correcct word was: {}'.format(self.__word))
            return True
        elif self.__word == ''.join(map(str, self.__correct_guesses)):
            await message.channel.send('You Win!\nIt took you {} guesses!'.format(len(self.__correct_guesses) + self.__fail_count))
            return True

        return False
    async def game_loop(self, message) -> None:
        input_letter = ''
        can_exit_round = False
        guess_status = -1
        game_status = False

        while True:
            await self.__print_game_field(message)
            await message.channel.send()
            while not can_exit_round:
                await message.channel.send('Please type a letter: ')

                try:
                    input_letter = await self.wait_for('message', check=is_correct, timeout=5.0)
                except Exception:
                    return await message.channel.send('Sorry, something went wrong!')
                
                if len(input_letter) != 1:
                    await message.channel.send('\nPlease type just a single letter!')
                else:
                    guess_status = self.__check(input_letter[0])
                    if guess_status == 0:
                        can_exit_round = True
                    elif guess_status == 1:
                        await message.channel.send('\nThat letter doesn\'t exist!')
                        can_exit_round = True
                    else:
                        await message.channel.send('\nYou already guessed that letter!')
            can_exit_round = False
            guess_status = -1

            game_status = await self.__end_game(message)
            if game_status:
                return
