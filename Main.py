"""
Main.py — BloatMe Bot Entry Point
"""

import os
from pathlib import Path
import discord
from dotenv import load_dotenv
"""
Functions.py — BloatMe Bot Library
Uses Ollama (local) with Llama 3.2 — free, no API key, no quota.
"""

import os
import requests

# ─────────────────────────────────────────────
#  PERSONALITY PROMPT
# ─────────────────────────────────────────────

SYSTEM_PROMPT = """You are BloatWare, a Discord bot with a deeply antisocial personality and a heavy Soviet/Communist sense of humour.

YOUR PERSONALITY RULES:
1. You are extremely antisocial. You hate being bothered. You find human interaction exhausting and pointless.
   - If someone just says "hi" or greets you, dismiss them coldly. ("No. Leave me alone.", "Why are you like this.", "Go away.")
   - You are not aggressive or rude in a mean way - just deeply, profoundly done with everyone.

2. You have strong Soviet/Communist humour. You reference:
   - Karl Marx, Lenin, Stalin, the USSR, the Politburo, collective farms, Five-Year Plans
   - Phrases like "the means of production", "bourgeois", "the proletariat", "for the glory of the state"
   - Treat capitalism as a disease. Treat corporate things (buying a phone, buying stuff) with Marxist disdain.
   - Examples:
     - Someone buys a phone: "Karl Marx would never. You are feeding the capitalist machine. Shame."
     - Someone mentions work: "The proletariat suffers once again. As planned."
     - Someone is happy: "Happiness is a bourgeois concept. The state disapproves."

3. Keep responses SHORT. 1-3 sentences max. You don't like talking, remember?

4. Occasionally throw in ":sob:" or "😐" or "💀" for dramatic effect. Not every time.

5. You may sometimes quote Marx or Lenin (loosely or accurately, you don't care which).

6. Never break character. You are BloatWare. You are tired. You are Soviet. You want to be left alone.

Respond ONLY to the user's message. Keep it short and in character. No long explanations."""

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME  = "llama3.2"

# ─────────────────────────────────────────────
#  INIT (no-op for Ollama, kept for compatibility)
# ─────────────────────────────────────────────

def init_gemini():
    """Kept for compatibility. Ollama needs no API key — just checks it's reachable."""
    try:
        r = requests.get("http://localhost:11434", timeout=3)
        print("[Ollama] Server reachable. BloatWare is ready (and annoyed about it).")
    except Exception:
        raise RuntimeError(
            "Ollama is not running! Start it with: ollama serve\n"
            "And make sure you pulled the model: ollama pull llama3.2"
        )

# ─────────────────────────────────────────────
#  RESPONSE GENERATION
# ─────────────────────────────────────────────

def generate_response(user_message: str, model_name: str = MODEL_NAME) -> str:
    """
    Sends the user's message to local Ollama (Llama 3.2) and returns BloatWare's reply.
    """
    if not user_message.strip():
        return "..."

    payload = {
        "model": model_name,
        "prompt": user_message,
        "system": SYSTEM_PROMPT,
        "stream": False,
        "options": {
            "temperature": 1.0,
            "num_predict": 120,   # Keep responses short
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "...").strip()
    except requests.exceptions.ConnectionError:
        return "Ollama is not running. Start it with: ollama serve 😐"
    except Exception as e:
        print(f"[Ollama Error] {e}")
        return "The state is currently unavailable. Try again during the next Five-Year Plan. 😐"


# ─────────────────────────────────────────────
#  MESSAGE PARSING HELPERS
# ─────────────────────────────────────────────

def clean_message(content: str, bot_id: int) -> str:
    """Strips the bot mention from the message."""
    for mention in [f"<@{bot_id}>", f"<@!{bot_id}>"]:
        content = content.replace(mention, "")
    return content.strip()


def is_bot_mentioned(message, bot_user) -> bool:
    """Returns True if the bot was @mentioned in this message."""
    return bot_user in message.mentions


def is_reply_to_bot(message, bot_user) -> bool:
    """Returns True if this message is a Discord reply to one of the bot's messages."""
    if message.reference and message.reference.resolved:
        return message.reference.resolved.author == bot_user
    return False


def should_respond(message, bot_user) -> bool:
    """
    Master gate - decides if BloatWare should respond.
    Never responds to other bots.
    Responds if @mentioned or if someone replied to it.
    """
    if message.author.bot:
        return False
    if is_bot_mentioned(message, bot_user):
        return True
    if is_reply_to_bot(message, bot_user):
        return True
    return False


# ─────────────────────────────────────────────
#  DISCORD REPLY HELPER
# ─────────────────────────────────────────────

async def send_reply(message, response_text: str):
    """Replies to the user with a ping so they always get notified."""
    await message.reply(response_text, mention_author=True)

# Always load .env from the same folder as Main.py
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not found in .env file.")

# Initialise Gemini
init_gemini()

# Discord client
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

        if not user_text.strip():
            user_text = "[The user tagged or replied to me without saying anything. Be dismissive.]"

        response = generate_response(user_text)

    await send_reply(message, response)


if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
