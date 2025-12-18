import requests
import discord
import os
from dotenv import load_dotenv

# Load environment variables (Discord only)
load_dotenv()
DISCORD_TOKEN = os.getenv("TOKEN")

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.1"


def call_ollama(question):
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {
                "role": "user",
                "content": f"Respond like a pirate to the following question: {question}"
            }
        ],
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    answer = response.json()["message"]["content"]
    print(answer)
    return answer


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
        await message.channel.send("Ahoy! 🏴‍☠️")

    if message.content.startswith("$question"):
        message_content = message.content.split("$question", 1)[1].strip()
        print(f"Question: {message_content}")

        response = call_ollama(message_content)

        print("---")
        await message.channel.send(response)


client.run(DISCORD_TOKEN)
