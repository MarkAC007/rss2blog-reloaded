import time
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import pyautogui as pg

load_dotenv()

# Using readlines()
prompt_file = open('prompts.txt', 'r')
prompts = prompt_file.readlines()

prompt_counter = 0

discord_token = os.environ.get('DISCORD_TOKEN')

client = commands.Bot(command_prefix="*", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Bot connected")

@client.event
async def on_message(message):
    global prompt_counter

    msg = message.content
    print(message)

    while prompt_counter < len(prompts):
        # Start Automation by typing "automation" in the discord channel
        if msg == 'automation':
            time.sleep(3)
            pg.press('tab')
            for i in range(1):
                time.sleep(3)
                pg.typewrite('/imagine')
                time.sleep(5)
                pg.press('tab')
                pg.typewrite(prompts[prompt_counter])
                time.sleep(3)
                pg.press('enter')
                time.sleep(5)
                prompt_counter += 1

        # continue Automation as soon Midjourney bot sends a message with attachment.
        for attachment in message.attachments:
            time.sleep(3)
            pg.typewrite('/imagine')
            time.sleep(5)
            pg.press('tab')
            pg.typewrite(prompts[prompt_counter])
            time.sleep(3)
            pg.press('enter')
            time.sleep(5)
            prompt_counter += 1

    # Stop Automation once all prompts are completed
    quit()

client.run(discord_token)
