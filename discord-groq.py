# Written by Ali Tobah based on code by
# Dr. Abel Sanchez at https://github.com/abelsan/bot

from dotenv import load_dotenv
from groq import Groq
import discord
import os

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_KEY")
DISCORD_TOKEN = os.getenv("TOKEN")

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)


def call_groq(question):
    completion = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": f"Respond like a university professor to the following question: {question}"
            }
        ],
        max_tokens=1500  # maximum number of output tokens
    )

    response = completion.choices[0].message.content
    print(response)
    return response




# Discord setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Good day!")

    if message.content.startswith("$question"):
        message_content = message.content.split("$question", 1)[1].strip()
        print(f"Question: {message_content}")

        response = call_groq(message_content)
        print("---")

        for i in range(0, len(response), 2000):
            await message.channel.send(response[i:i + 2000])

client.run(DISCORD_TOKEN)