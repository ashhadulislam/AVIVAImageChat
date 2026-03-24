# GenAI Discord Image Caption Bot

A lightweight GenAI bot built with **Discord.py** and **Ollama** that can:

- Receive image uploads through Discord
- Generate a **short caption**
- Generate **3 keywords/tags**
- Reply back with the caption and the uploaded image
- Maintain the **last 3 interactions per user**
- Cache repeated images to avoid reprocessing
- Summarize recent captions with a `/summary` command

---

## Features

### 1. Image Description
Users can upload an image using the `/image` slash command.  
The bot will:

- Analyze the image using a local vision model
- Generate a short caption
- Generate 3 keywords/tags
- Send the result back in Discord

#### Demo

![Demo](https://raw.githubusercontent.com/ashhadulislam/AVIVAImageChat/main/demo1.gif)

### 2. Message History Awareness
The bot keeps the **last 3 interactions per user** in memory.  
This can be used for lightweight personalization and summarization.

![Message History](https://raw.githubusercontent.com/ashhadulislam/AVIVAImageChat/main/msgHistory.png)

### 3. Basic Caching
The bot computes an **MD5 hash** of each uploaded image.  
If the same image is uploaded again, the cached result is returned instead of calling the model again.

![Caching Demo](https://raw.githubusercontent.com/ashhadulislam/AVIVAImageChat/main/demo2-hash.gif)

### 4. Summary Command
The `/summary` command summarizes the recent captions generated for that user.

---

## Tech Stack

- **Python**
- **Discord.py**
- **Ollama**
- **LLaVA 7B** for image understanding
- **Phi-3** for summarization
- **Pillow** for image preprocessing
- **Requests** for HTTP calls to Ollama

---

## Models Used

### Vision Model
- `llava:7b`
- Used for image captioning and keyword generation

### Text Model
- `phi3`
- Used for summarizing recent image captions

---

## System Flow

```text
User uploads image in Discord
        ↓
Discord bot receives attachment URL
        ↓
Bot downloads image
        ↓
Bot computes image hash
        ↓
If cached:
    return cached caption
Else:
    preprocess image
    send image to Ollama (llava:7b)
    receive caption + tags
    store in cache
        ↓
Store interaction in per-user history
        ↓
Reply to user with caption and image
```

---

## Setup Instructions

### 1. Setting up a Discord Bot

Reference: https://discordpy.readthedocs.io/

#### Install Discord.py
```bash
python3 -m pip install -U discord.py
```

### Create a Discord Bot
1. Go to the **Discord Developer Portal**
2. Click on **Applications**
3. Click **New Application**
4. Go to the **Bot** tab
5. Click **Add Bot**
6. Copy the **Bot Token**

### Add Bot to Server
1. Go to **OAuth2 → URL Generator**
2. Select:
   - `bot`
   - `applications.commands`
3. Under **Bot Permissions**, select:
   - `Send Messages`
4. Copy the generated URL
5. Open it in your browser
6. Select the Discord server to add the bot

---

### 2. Setting up Ollama

Reference: https://ollama.com/

#### Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
Pull Required Models
```bash
ollama pull llava:7b
ollama pull phi3
```
Start Ollama
```bash
ollama serve
```
Ollama runs locally at:

http://localhost:11434

---

### 3. Back End of the Bot

Run the bot locally using:

```bash
python test.py
```
---


