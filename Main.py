import os
from pathlib import Path
import discord
from dotenv import load_dotenv
import BloatMe.Functions as Functions

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not found in .env file.")

init_ollama()

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"[BloatWare] Logged in as {client.user} (ID: {client.user.id})")
    print("[BloatWare] Online. Deeply unhappy about it.")
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="the fall of capitalism 🚩"
        )
    )


@client.event
async def on_message(message: discord.Message):
    if not should_respond(message, client.user):
        return

    async with message.channel.typing():
        user_text = clean_message(message.content, client.user.id)
        if not user_text:
            user_text = "[User tagged or replied without saying anything. Be dismissive.]"
        response = await generate_response(user_text)

    await send_reply(message, response)


if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
