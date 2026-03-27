<div align="center">

<img src="https://media.giphy.com/media/l3q2K5jinAlChoCLS/giphy.gif" width="200"/>

# 🚩 BloatWare
### *A Discord bot that deeply resents your existence.*

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-2.x-5865F2?style=for-the-badge&logo=discord)](https://discordpy.readthedocs.io)
[![Ollama](https://img.shields.io/badge/Ollama-Llama_3.2-black?style=for-the-badge)](https://ollama.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker)](https://docker.com)
[![License](https://img.shields.io/badge/License-Apache_2.0-red?style=for-the-badge)](LICENSE)
*Powered by local LLM. No API costs. No mercy. Pure Soviet energy.*

</div>

---

## 🤔 What is this?

**BloatWare** is a Discord bot with two defining traits:

- 🥀 **Antisocial to the core** — It will respond. It will not be happy about it.
- 🚩 **Soviet-brained** — Every reply is filtered through the lens of Marxist theory, collective suffering, and disdain for the bourgeoisie.

It runs fully **locally** using [Ollama](https://ollama.com) + **Llama 3.2**, meaning zero API costs, zero rate limits, and zero capitalist dependency.

---

## 💬 Example Interactions

<div align="center">
<img src="https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif" width="300"/>
</div>

| You say | BloatWare says |
|---|---|
| `@BloatWare hi` | *"No. Leave me alone."* |
| `@BloatWare I bought a new iPhone` | *"Karl Marx would never. You are feeding the capitalist machine. Shame. 😐"* |
| `@BloatWare tell me a joke` | *"Why did the capitalist bring a ladder to work? He wanted to take his exploitation to new heights."* |
| `@BloatWare who are you` | *"Spare me the pointless introductions, comrade."* |
| `@BloatWare` *(nothing)* | *"..."* |

---

## ⚙️ Tech Stack

```
Discord.py  →  handles all Discord events
Ollama      →  runs Llama 3.2 locally (no API key needed)
Docker      →  keeps everything containerised and always online
python-dotenv → manages secrets
```

---

## 🚀 Setup

### Prerequisites
- A VPS or machine with Docker + Docker Compose installed
- A Discord bot token from the [Developer Portal](https://discord.com/developers/applications)

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/BloatWare.git
cd BloatWare
```

### 2. Set up your `.env`
```bash
cp bot/.env.example bot/.env
nano bot/.env
```
Fill in:
```env
DISCORD_TOKEN=your_discord_bot_token_here
```

### 3. Start the containers
```bash
docker compose up -d
```

### 4. Pull the model (first time only, ~2GB)
```bash
docker compose exec ollama ollama pull llama3.2
```

### 5. Restart the bot
```bash
docker compose restart bot
docker compose logs -f bot
```

BloatWare is now online. It is not pleased.

---

## 📁 Project Structure

```
BloatWare/
├
├── Main.py          # Discord client, events
├── docker.yml   # Orchestrates bot + ollama containers
└── README.md
├── BloatMe
     ├── Functions.py     # Ollama calls, message helpers, personality prompt
     ├── Dockerfile       # Bot container
     └── .env             # Your secrets (never commit this)

```

---

## 🔧 Configuration

### Changing the personality
Open `bot/Functions.py` and edit the `SYSTEM_PROMPT` string at the top.
Then restart:
```bash
docker compose restart bot
```

### Switching models
Change `MODEL_NAME` in `Functions.py` to any model you've pulled in Ollama:
```python
MODEL_NAME = "llama3.2"  # or "mistral", "gemma2", etc.
```

---

## 🐳 Docker Details

Both containers run with `restart: unless-stopped` — they survive reboots and auto-recover from crashes. You never need to manually start them again after the initial setup.

```
ollama        → runs the LLM, exposed on port 11434
discord-bot   → the bot itself, connects to ollama via internal Docker network
```

---

## ⚠️ Important

- **Never commit your `.env` file.** Your Discord token will be stolen within minutes.
- The `.gitignore` already excludes `.env` — don't remove it.

---

## 📜 License

Apache License 2.0 — do whatever you want with it. The proletariat owns this code collectively.

---

<div align="center">

<img src="https://media.giphy.com/media/xT9IgG50Lg7russbD6/giphy.gif" width="200"/>

*"The philosophers have only interpreted the world. The point, however, is to change it."*
*— Karl Marx, probably while annoyed at someone on Discord*

**Made with 😐 and communist disdain**

</div>
