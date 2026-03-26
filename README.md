# BloatWare 🚩
> An antisocial, Soviet-humoured Discord bot powered by the Gemini API.
> It does not want to talk to you. It will anyway.

---

## Setup

### 1. Install dependencies
```bash
pip install discord.py google-generativeai python-dotenv
```

### 2. Fill in your `.env`
```
DISCORD_TOKEN=your_discord_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
```

- Get your Discord bot token from the [Discord Developer Portal](https://discord.com/developers/applications)
  - Enable **Message Content Intent** under Bot → Privileged Gateway Intents
- Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### 3. Run the bot
```bash
python Main.py
```

---

## Behaviour

| Trigger | Example | BloatWare does |
|---|---|---|
| Tagged with a message | `@BloatWare hi` | Dismisses you coldly |
| Tagged about buying stuff | `@BloatWare I bought a phone` | Marxist disdain |
| Reply to bot's message | *(reply arrow)* `okay but why` | Responds reluctantly |
| Tagged with nothing | `@BloatWare` | "..." |
| Another bot talks | — | Ignored completely |

---

## File Structure

```
BloatMe/
├── .env           # Your secrets (never commit this!)
├── __init__.py    # Package marker
├── Functions.py   # All logic: Gemini calls, message parsing, reply helpers
├── Main.py        # Bot entry point, Discord events
└── README.md      # You are here
```

---

## Personality

BloatWare runs on a custom system prompt that makes it:
- **Antisocial** — Finds conversation physically painful
- **Soviet** — References Marx, Lenin, collective farms, the proletariat
- **Brief** — 1–3 sentences max, because talking is exhausting
- **Consistent** — Never breaks character

You can tweak the `SYSTEM_PROMPT` in `Functions.py` to adjust the personality.

---

*"From each according to his ability, to each according to his needs. You have no needs. Go away."*
