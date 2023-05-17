import time
import discord
from discord.ext import commands
from dotenv import load_dotenv
import pyautogui as pg

discord_token = "MTA3Mjk4NjMzNDA3Mjk0Njc1OA.G8CWwv.5Mv4MjwX0tPQJ9zlkq_9UU9lVC9xvHa1hG5sDs"

# Using readlines()
prompt_file = open('prompts.txt', 'r')
prompts = prompt_file.readlines()

prompt_counter = 0

load_dotenv()
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