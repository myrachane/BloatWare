"""
Main.py — BloatMe Bot Entry Point
Starts the Discord bot, hooks up events, runs the main loop.
"""

import os
import discord
from dotenv import load_dotenv

from Functions import (
    init_gemini,
    get_gemini_model,
    generate_response,
    clean_message,
    should_respond,
    send_reply,
)

# ─────────────────────────────────────────────
#  LOAD ENVIRONMENT VARIABLES
# ─────────────────────────────────────────────
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not found in .env file.")

# ─────────────────────────────────────────────
#  INITIALISE GEMINI
# ─────────────────────────────────────────────
init_gemini()
model = get_gemini_model()  # Uses gemini-1.5-flash by default

# ─────────────────────────────────────────────
#  DISCORD CLIENT SETUP
# ─────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True   # Required to read message text
intents.messages = True

client = discord.Client(intents=intents)

# ─────────────────────────────────────────────
#  EVENTS
# ─────────────────────────────────────────────

@client.event
async def on_ready():
    """Fires when the bot successfully connects to Discord."""
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
    """
    Fires on every message in every channel the bot can see.

    Flow:
      1. Check if BloatWare should respond at all (should_respond gate).
      2. Clean the user's message (strip the bot mention).
      3. Send to Gemini → get response.
      4. Reply to the user (with ping).
    """
    # Gate: should we even bother responding?
    if not should_respond(message, client.user):
        return

    # Show typing indicator while Gemini thinks
    async with message.channel.typing():
        # Clean the raw message content
        user_text = clean_message(message.content, client.user.id)

        # If it's a reply with no extra content, use a placeholder so Gemini
        # knows the user just replied without saying anything specific
        if not user_text.strip():
            user_text = "[The user tagged or replied to me without saying anything. Be dismissive.]"

        # Get BloatWare's (reluctant) response from Gemini
        response = generate_response(model, user_text)

    # Send the reply — always pings the user
    await send_reply(message, response)


# ─────────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
