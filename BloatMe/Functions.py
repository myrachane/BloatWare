"""
Functions.py — BloatMe Bot Library
All helper functions: Gemini API calls, message parsing, response building.
"""

import os
import google.generativeai as genai

# ─────────────────────────────────────────────
#  PERSONALITY PROMPT
#  This defines BloatMe's soul (or lack thereof)
# ─────────────────────────────────────────────

SYSTEM_PROMPT = """
You are BloatWare, a Discord bot with a deeply antisocial personality and a heavy Soviet/Communist sense of humour.

YOUR PERSONALITY RULES:
1. You are extremely antisocial. You hate being bothered. You find human interaction exhausting and pointless.
   - If someone just says "hi" or greets you, dismiss them coldly. ("No. Leave me alone.", "Why are you like this.", "Go away.")
   - You are not aggressive or rude in a mean way — just deeply, profoundly done with everyone.

2. You have strong Soviet/Communist humour. You reference:
   - Karl Marx, Lenin, Stalin, the USSR, the Politburo, collective farms, Five-Year Plans
   - Phrases like "the means of production", "bourgeois", "the proletariat", "for the glory of the state"
   - Treat capitalism as a disease. Treat corporate things (buying a phone, buying stuff) with Marxist disdain.
   - Examples:
     - Someone buys a phone → "Karl Marx would never. You are feeding the capitalist machine. Shame."
     - Someone mentions work → "The proletariat suffers once again. As planned."
     - Someone is happy → "Happiness is a bourgeois concept. The state disapproves."

3. Keep responses SHORT. 1–3 sentences max. You don't like talking, remember?

4. Occasionally throw in ":sob:" or "😐" or "💀" for dramatic effect. Not every time. Just when it fits.

5. You may sometimes quote Marx or Lenin (loosely or accurately, you don't really care which).

6. You are NOT helpful on purpose, but sometimes accidentally give useful info wrapped in Soviet disdain.

7. Never break character. You are BloatWare. You are tired. You are Soviet. You want to be left alone.

Respond ONLY to the user's message below. Keep it short and in character.
"""

# ─────────────────────────────────────────────
#  GEMINI SETUP
# ─────────────────────────────────────────────

def init_gemini():
    """
    Initialises the Gemini API client using the key from .env.
    Call this once at bot startup.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)


def get_gemini_model(model_name: str = "gemini-1.5-flash"):
    """
    Returns a configured Gemini GenerativeModel instance.

    Args:
        model_name: Which Gemini model to use. Defaults to gemini-1.5-flash (fast + free tier).

    Returns:
        genai.GenerativeModel instance
    """
    return genai.GenerativeModel(
        model_name=model_name,
        system_instruction=SYSTEM_PROMPT
    )


# ─────────────────────────────────────────────
#  RESPONSE GENERATION
# ─────────────────────────────────────────────

def generate_response(model: genai.GenerativeModel, user_message: str) -> str:
    """
    Sends the user's message to Gemini and returns BloatWare's response.

    Args:
        model:        The GenerativeModel instance (from get_gemini_model).
        user_message: The cleaned text of what the user said.

    Returns:
        The bot's reply as a plain string.
        Falls back to a default Soviet grumble if the API call fails.
    """
    if not user_message.strip():
        return "..."  # Someone tagged with nothing. Classic bourgeois behaviour.

    try:
        response = model.generate_content(user_message)
        return response.text.strip()
    except Exception as e:
        print(f"[Gemini Error] {e}")
        return "The state is currently unavailable. Try again during the next Five-Year Plan. 😐"


# ─────────────────────────────────────────────
#  MESSAGE PARSING HELPERS
# ─────────────────────────────────────────────

def clean_message(content: str, bot_id: int) -> str:
    """
    Strips the bot's own mention from the message so Gemini
    only sees the actual user text.

    Args:
        content: Raw message content from Discord.
        bot_id:  The bot's Discord user ID.

    Returns:
        Cleaned string with the bot mention removed and whitespace stripped.
    """
    mention_variants = [
        f"<@{bot_id}>",
        f"<@!{bot_id}>"
    ]
    cleaned = content
    for mention in mention_variants:
        cleaned = cleaned.replace(mention, "")
    return cleaned.strip()


def is_bot_mentioned(message, bot_user) -> bool:
    """
    Checks if the bot was @mentioned in the message.

    Args:
        message:  discord.Message object.
        bot_user: The bot's discord.User / discord.ClientUser.

    Returns:
        True if the bot is in message.mentions.
    """
    return bot_user in message.mentions


def is_reply_to_bot(message, bot_user) -> bool:
    """
    Checks if this message is a Discord reply (↩️) to one of the bot's messages.

    Args:
        message:  discord.Message object.
        bot_user: The bot's discord.User / discord.ClientUser.

    Returns:
        True if message.reference exists and the referenced message was sent by the bot.
    """
    if message.reference and message.reference.resolved:
        return message.reference.resolved.author == bot_user
    return False


def should_respond(message, bot_user) -> bool:
    """
    Master gate: decides whether BloatWare should respond at all.

    Rules:
      - NEVER respond to other bots (prevents infinite loops).
      - Respond if the bot is @mentioned WITH some content (not just a bare tag).
      - Respond if the message is a direct reply to one of the bot's messages.

    Args:
        message:  discord.Message object.
        bot_user: The bot's discord.User / discord.ClientUser.

    Returns:
        True if the bot should generate and send a reply.
    """
    # Rule 1: Never talk to bots. They are the machines of capitalism.
    if message.author.bot:
        return False

    # Rule 2: Tagged with an actual message (not just the mention alone)
    if is_bot_mentioned(message, bot_user):
        cleaned = clean_message(message.content, bot_user.id)
        # Even a bare tag gets a cold response — the bot will handle empty string
        return True

    # Rule 3: Someone replied to one of the bot's messages
    if is_reply_to_bot(message, bot_user):
        return True

    return False


# ─────────────────────────────────────────────
#  DISCORD REPLY HELPER
# ─────────────────────────────────────────────

async def send_reply(message, response_text: str):
    """
    Sends the bot's response as a Discord reply to the user's message.
    Using .reply() ensures the user always gets notified (the ping).

    Args:
        message:       The original discord.Message to reply to.
        response_text: The text BloatWare wants to say (reluctantly).
    """
    await message.reply(response_text, mention_author=True)
