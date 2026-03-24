
# This example requires the 'message_content' intent.

import discord
import hashlib
import time

import requests
import base64
from PIL import Image
from io import BytesIO
from discord import app_commands

bot_context={}
cache_image_hash={}

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()  # 🔥 REQUIRED

    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')    
    if not message.author in bot_context:
        bot_context[message.author]=[]
    
    if message.author == client.user:
        return            
    await message.channel.send('Well received!')
    

# /image command
@tree.command(name="image", description="Upload an image for captioning")
@app_commands.describe(file="Upload an image")
async def image(interaction: discord.Interaction, file: discord.Attachment):
    start_time = time.perf_counter()

    await interaction.response.defer()  # prevents timeout
    user_id = interaction.user.id
    if not user_id in bot_context:
        bot_context[user_id]=[]

    # Download image
    img_data = requests.get(file.url).content
    image_hash = hashlib.md5(img_data).hexdigest()
    prompt="Generate a short caption. Keep it brief. Also generate 3 keywords or tags."
    if image_hash in cache_image_hash:
        print('answer already')
        result=cache_image_hash[image_hash]        
    else:


        # Resize
        img = Image.open(BytesIO(img_data))
        img = img.resize((512, 512))
        img = img.convert("RGB")

        buffer = BytesIO()
        img.save(buffer, format="JPEG")

        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        

        # Send to Ollama
        payload = {
            "model": "llava:7b",
            "prompt": prompt,
            "images": [img_base64],
            "stream": False
        }

        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload
        )

        data = response.json()

        if "response" in data:
            result = data["response"].strip()
        else:
            result = f"Error: {data}"

    # Reply in Discord
    #await interaction.followup.send(result)
    bot_context[user_id].append({
        'user_input':prompt,
        'bot_output':result

        })
    bot_context[user_id]=bot_context[user_id][-3:]
    cache_image_hash[image_hash]=result
    print(bot_context[user_id])
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    await interaction.followup.send(
        content=f"{result}\n\n⏱️ Time: {elapsed_time:.2f}s",
        embed=discord.Embed().set_image(url=file.url)
    )




# /summary command
@tree.command(name="summary", description="Summarize old captions")
async def summary(interaction: discord.Interaction):

    await interaction.response.defer()  # prevents timeout
    user_id = interaction.user.id
    if not user_id in bot_context:
        bot_context[user_id]=[]

    
    prompt=f"Summarize these image captions in one short paragraph. \n{bot_context[user_id]}"

    

    # Send to Ollama
    payload = {
        "model": "phi3",
        "prompt": prompt,        
        "stream": False
    }

    response = requests.post(
        "http://localhost:11434/api/generate",
        json=payload
    )

    data = response.json()

    if "response" in data:
        result = data["response"].strip()
    else:
        result = f"Error: {data}"

    

    await interaction.followup.send(
        content=result
        
    )


# /summary command
@tree.command(name="help", description="Show usage instructions")
async def help(interaction: discord.Interaction):

    await interaction.response.defer()  # prevents timeout
    user_id = interaction.user.id
    help_text = """
    **Image Caption Bot Help**

    **/image**
    Upload an image to generate:
    • A short caption  
    • 3 keywords/tags  

    Usage:
    Type `/image` and attach a file

    ---

    **/summary**
    Summarizes your last few image captions (up to 3)

    Usage:
    Just type `/summary`

    ---

    **Features**
    • Remembers your last 3 interactions  
    • Avoids re-processing same images (fast responses)  

    ---

    Tip:
    Upload clear images for better captions!
    """    
    

    

    embed = discord.Embed(
        title="Help Menu",
        description=help_text,
        color=discord.Color.blue()
    )

    await interaction.followup.send(embed=embed)    




client.run('<Your bot token here>')
