import os
import asyncio
import requests
from functools import partial


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

7. "https://github.com/myrachane/BloatWare" This Is your Main Github Repo if someone asks you about who made you just give them this link
Respond ONLY to the user's message. Keep it short and in character. No long explanations."""


OLLAMA_HOST = os.getenv("OLLAMA_HOST", "ollama")
OLLAMA_PORT = 11434
OLLAMA_URL  = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"

""" def init_ollama():
    #Checks Ollama is reachable on startup. Raises if not.
    try:
        requests.get(f"http://{OLLAMA_HOST}:11434", timeout=5)
        print(f"[Ollama] Reachable at {OLLAMA_HOST}:11434. BloatWare is ready (and annoyed).")
    except Exception:
        raise RuntimeError(
            f"Ollama not reachable at {OLLAMA_HOST}:11434!\n"
            "Run: docker compose exec ollama ollama pull llama3.2"
        ) """ # NOT USING THIS FOR NOW


def init_ollama():  # Imporved Version As Suggested
    try:
        r = requests.get(f"http://{OLLAMA_HOST}:{OLLAMA_PORT}", timeout=5)
        r.raise_for_status()
        print(f"[Ollama] Reachable at {OLLAMA_HOST}:{OLLAMA_PORT}.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Ollama connection failed: {e}")   



def _blocking_generate(user_message: str) -> str:
   #Synchronous Ollama request — always called via thread executor.
    payload = {
        "model": MODEL_NAME,
        "prompt": user_message,
        "system": SYSTEM_PROMPT,
        "stream": False,
        "options": {
            "temperature": 1.0,
            "num_predict": 120,
        }
    }
   # UPDATED RETRY LOGIC
  ''' def _blocking_generate(user_message: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": user_message,
        "system": SYSTEM_PROMPT,
        "stream": False,
        "options": {
            "temperature": 1.0,
            "num_predict": 120,
        }
    }
'''
    max_retries = 2
    for attempt in range(max_retries):
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        r.raise_for_status()
        return r.json().get("response", "...").strip()

    except requests.Timeout:
        if attempt == max_retries - 1:
            return "The Politburo is slow today... 😐"

    except requests.RequestException as e:
        if attempt == max_retries - 1:
            return f"Ollama error: {e}"


async def generate_response(user_message: str) -> str:
    if not user_message.strip():
        return "..."
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, partial(_blocking_generate, user_message))



def clean_message(content: str, bot_id: int) -> str:
    
    for mention in [f"<@{bot_id}>", f"<@!{bot_id}>"]:
        content = content.replace(mention, "")
    return content.strip()


def should_respond(message, bot_user) -> bool:
   
    if message.author.bot:
        return False
    if bot_user in message.mentions:
        return True
    if message.reference and message.reference.resolved:
        if message.reference.resolved.author == bot_user:
            return True
    return False


async def send_reply(message, response_text: str):
    MAX_LENGTH = 2000

    if len(response_text) > MAX_LENGTH:
        for chunk in range(0, len(response_text), MAX_LENGTH):
            await message.reply(
                response_text[chunk:chunk + MAX_LENGTH],
                mention_author=True
            )
    else:
        await message.reply(response_text, mention_author=True)
