# Korosensei

## What is Korosensei?
Korosensei is a Discord bot written in Python (to practice it) that allows the user to play Hangman. While that would be interesting, if basic, in and of itself, this bot was created for the Japanese learning server "[日本語を学ぼう！](https://disboard.org/server/788996101206310912)" (にほんごを　まがぼう！, Nihongo wo Manabou!; Link goes to [Disboard](https://disboard.org/)) as another fun way of practicing vocabulary.

## Can I invite the bot to my server?
All Discord app info such as client ID information is naturally not hardcoded and present in a text file called in `info.text` in the root of the repo. This is to prevent hacking and API abuse. **Thus, it is impossible for anyone but those with access to these API keys run this program with my Discord app.** However it is possible to run it with some other Discord app.

## Running Instructions (Using Personal Discord App)
- Follow [these](https://discordpy.readthedocs.io/en/stable/discord.html) instructions on the [discord.py](https://discordpy.readthedocs.io/) documentation to create a new Bot application and then invite it to the server of your choice. While this bot no longer uses discord.py, these instructions are quite good. This code connects the instructions set forth with whatever bot specified and then allow it perform those actions.
- Run this command in the directory where the repo is saved to install the [hikari](https://hikari-py.github.io/hikari/) package:
```sh
python3 -m pip install -U hikari
```
This command works in Windows (Command Prompt and PowerShell), macOS, Linux.
The shorter command,
```sh
pip install hikari
```
also works if your system supports it (Windows generally doesn't).
- Run the program using
```sh
python3 korosensei.py
```
If your system doesn't use `python3` has the package, then replace it with `python` instead. This applies to Arch-based distributions as far as I know.
- Now go to the server where the bot is on Discord, and interact with it!

## Usage Instructions (In the Event an Invite Link is Provided)
- Click the link
- Follow its instructions
- Go to the server where the bot is
- Interact with it!

## Is it functional? What issues are present? What other new features will there be?
Check the [issues](https://github.com/MechaDragonX/korosensei/issues) tab for any issues and new features that have yet to be addressed, or are being addressed currently.

## What the hell is this name?
The manga and anime franchise *Assassination Classroom* (暗殺教室, Ansatsu Kyoushitsu) features a character by the name of Korosensei (殺せんせー) who's name roughly means "unkillable teacher". The students of the titular classroom are tasked with killing their teacher before the end of the year, and their gradutation from middle school, lest the Earth faces the same fate as the moon. Utterly destroyed. While the premise makes this sound like an utterly ridiculous action story, it is in fact a very heartfelt character-driven story focusing on the relationship between the students, the students and their teacher, and their growth as people until their symbolic growth into adults with their graduation from Japanese compulsory education.

You can think of the game as being Korosensei about to kill someone as a test of your ability to catch the Mach 20 being. ...Even though that doesn't make much sense.
