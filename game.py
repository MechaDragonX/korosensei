#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import asyncio
import discord
import enum
import random

class Language(enum.Enum):
    English = 0,
    Japanese = 1
class KanaType(enum.Enum):
    English = -1,
    Hiragana = 0,
    Katakana = 1

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
    __language = Language.English
    __word_pool = []
    __word_pool_kanji = []
    __kana_type = KanaType.English
    # Dictionary of Hiragana to Katakana to allow for the input of either syllabic characcter in the game
    # This allows the game to be more fun and prvent loosing after inputting all the vowels and a couple other characcters all in one writing system
    __hira2kata = {
        # Gojuon (main 50 characters/syllables)
        'あ': 'ア', 'い': 'イ', 'う': 'ウ', 'え': 'エ', 'お': 'オ',
        'か': 'カ', 'き': 'キ', 'く': 'ク', 'け': 'ケ', 'こ': 'コ',
        'さ': 'サ', 'し': 'シ', 'す': 'ス', 'せ': 'セ', 'そ': 'ソ',
        'た': 'タ', 'ち': 'チ', 'つ': 'ツ', 'て': 'テ', 'と': 'ト',
        'な': 'ナ', 'に': 'ニ', 'ぬ': 'ヌ', 'ね': 'ネ', 'の': 'ノ',
        'は': 'ハ', 'ひ': 'ヒ', 'ふ': 'フ', 'へ': 'ヘ', 'ほ': 'ホ',
        'ま': 'マ', 'み': 'ミ', 'む': 'ム', 'め': 'メ', 'も': 'モ',
        'や': 'ヤ', 'ゆ': 'ユ', 'よ': 'ヨ',
        'ら': 'ラ', 'り': 'リ', 'る': 'ル', 'れ': 'レ', 'ろ': 'ロ',
        'わ': 'ワ', 'を': 'ヲ', 'ん': 'ン',

        # (Han)dakuten (extra sounds with diacritics)
        'が': 'ガ', 'ぎ': 'ギ', 'ぐ': 'グ', 'げ': 'ゲ', 'ご': 'ゴ',
        'ざ': 'ザ', 'じ': 'ジ', 'ず': 'ズ', 'ぜ': 'ゼ', 'ぞ': 'ゾ',
        'だ': 'ダ', 'ぢ': 'ヂ', 'づ': 'ヅ', 'で': 'デ', 'ど': 'ド',
        'ば': 'バ', 'び': 'ビ', 'ぶ': 'ブ', 'べ': 'ベ', 'ぼ': 'ボ',
        'ぱ': 'パ', 'ぴ': 'ピ', 'ぷ': 'プ', 'ぺ': 'ペ', 'ぽ': 'ポ',
    }
    # A seperate dictionary for Sokuon/Yoon (extra sounds with smaller characters) and long tone mark
    __extra_hira2kata = {
        'っ': 'ッ', 'ゃ': 'ャ', 'ゅ': 'ュ', 'ょ': 'ョ', 'ー': 'ー'
    }

    def __init__(self, set) -> None:
        # Fill the word pool
        lines = []
        # If set's language is not English, fill the main word pool and Kanji word pools
        if set != 'english':
            self.__language = Language.Japanese
            lines = open(r'data/{}.txt'.format(set), encoding="utf-8").readlines()
            for line in lines:
                self.__word_pool.append(line.split()[0])
                self.__word_pool_kanji.append(line.split()[1])
        # Otherwise, just fill the main word pool
        else:
            self.__word_pool = open(r'data/{}.txt'.format(set), encoding="utf-8").readlines()

        # Each entry has a new line character end. Remove it.
        i = 0
        while i < len(self.__word_pool):
            self.__word_pool[i] = self.__word_pool[i].removesuffix('\n')
            i += 1
        # Do this to the Kanji pool if there elements in it.
        if len(self.__word_pool_kanji) != 0:
            i = 0
            while i < len(self.__word_pool_kanji):
                self.__word_pool_kanji[i] = self.__word_pool_kanji[i].removesuffix('\n') 
                i += 1

    def get_word_pool(self) -> 'list':
        return self.__word_pool

    def __setup_game(self) -> None:
        # Set the word to a random word from the word pool
        self.__word = self.__word_pool[random.randint(0, len(self.__word_pool) - 1)]

        # If the language is English, simply set up the guessed parts and exit
        if self.__language == Language.English:
            self.__gen_guessed_parts()
            return
        # Otherwise...
        else:
            # Set up guessed parts so that everything is blank prior to modification
            self.__gen_guessed_parts()

            # Check if the first character is Hiragana (writing systems never switch)
            if self.__word[0] in self.__hira2kata.keys():
                # If so, set Kana type to Hiragana
                self.__kana_type = KanaType.Hiragana
            else:
                # If not, set Kana type to Katakana
                self.__kana_type = KanaType.Katakana

            # Check to see if any character in the word has an extra Kana (smaller characters and long tone marks)
            for char in self.__word:
                # If so, fill them in at the start
                if (char in self.__extra_hira2kata.keys()) or (char in self.__extra_hira2kata.values()):
                    self.__gen_guessed_parts(char)
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
        message_connect = ''
        await message.channel.send('```\n{}```'.format(self.__gallow_states[self.__fail_count]))

        i = 0
        while i < len(self.__correct_guesses):
            if self.__correct_guesses[i] == ' ':
                message_connect += '\_'
            else:
                message_connect += self.__correct_guesses[i]
            if i != len(self.__correct_guesses) - 1:
                message_connect += ' '
            i += 1
        await message.channel.send(message_connect)

        if len(self.__wrong_guesses) != 0:
            message_connect = ''
            i = 0
            while i < len(self.__wrong_guesses):
                if i == len(self.__wrong_guesses) - 1:
                    message_connect += self.__wrong_guesses[i]
                else:
                    message_connect += '{} '.format(self.__wrong_guesses[i])
                i += 1
            await message.channel.send(message_connect)
    def __check(self, letter) -> 'int':
        # If the language is Japanese, change the guess to the kana type of the word if necessary
        if self.__language == Language.Japanese:
            letter = self.__convert_kana_type(letter)

        # If the letter is not in the word, add it to the wrong guesses and increment the fail count
        if letter not in self.__word:
            self.__wrong_guesses.append(letter)
            self.__fail_count = len(self.__wrong_guesses)
            return 1
        # If the letter was already guessed
        elif letter in self.__correct_guesses:
            return 2
        # Otherwise, simply generate guessed parts again with the newly guessed letter
        else:
            self.__gen_guessed_parts(letter)
            return 0
    def __convert_kana_type(self, letter) -> 'str':
        # Determine the kana type of the guess by searching the dictinoary
        guess_kana_type = KanaType.Hiragana if letter in self.__hira2kata.keys() else KanaType.Katakana

        # Create a separate variable for the same guess in the opposite kana type
        opposite_kana_guess = ''
        if guess_kana_type == KanaType.Hiragana:
            # Simple get value by key
            opposite_kana_guess = self.__hira2kata[letter]
        elif guess_kana_type == KanaType.Katakana:
            # Get key by value using the index() function on value list
            opposite_kana_guess = list(self.__hira2kata.keys())[list(self.__hira2kata.values()).index(letter)]

        # If the kana type of the guess and the word do not match...
        if guess_kana_type != self.__kana_type:
            # Make the guess the opposite version
            letter = opposite_kana_guess

        return letter
    async def __end_game(self, message) -> 'bool':
        if self.__fail_count == 6:
            await self.__print_game_field(message)
            if self.__language == Language.English:
                await message.channel.send('Game Over!\nThe correct word was: {}'.format(self.__word))
            else:
                # Find the Kanji of the word by the finding the index of the Kana in the word pool list, and then using that index to get the Kanji
                await message.channel.send('Game Over!\nThe correct word was: {}'.format(self.__word_pool_kanji[self.__word_pool.index(self.__word)]))
            return True
        elif self.__word == ''.join(map(str, self.__correct_guesses)):
            await self.__print_game_field(message)
            if self.__language == Language.English:
                await message.channel.send('You Win!\nIt took you {} guesses!'.format(len(self.__correct_guesses) + self.__fail_count))
            else:
                # Find the Kanji of the word by the finding the index of the Kana in the word pool list, and then using that index to get the Kanji
                await message.channel.send('You Win!\nThe word was: {0}. It took you {1} guesses!'.format(
                    self.__word_pool_kanji[self.__word_pool.index(self.__word)],
                    len(self.__correct_guesses) + self.__fail_count
                ))
            return True
        return False
    async def game_loop(self, client, message) -> None:
        input_message = ''
        can_exit_round = False
        guess_status = -1
        game_status = False

        self.__setup_game()

        while True:
            await self.__print_game_field(message)
            while not can_exit_round:
                await message.channel.send('Please type a letter:')

                try:
                    input_message = await client.wait_for('message')
                except Exception:   
                    return await message.channel.send('Sorry, something went wrong!')

                if len(input_message.content) != 1:
                    await message.channel.send('\nPlease type just a single letter!')
                else:
                    guess_status = self.__check(input_message.content[0])
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
