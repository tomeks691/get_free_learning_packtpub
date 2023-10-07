import os
import requests
from bs4 import BeautifulSoup
import discord
from dotenv import load_dotenv, find_dotenv

def get_daily_book():
    url = "https://www.packtpub.com/free-learning"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    book_images = soup.find_all(class_="product-image")
    for book_image in book_images:
        if book_image.has_attr('src'):
            image = book_image['src']
        if book_image.has_attr('alt'):
            title = book_image['alt']
    return image, title

def send_to_discord(image, title):
    load_dotenv(find_dotenv())
    discord_token = os.environ.get("DISCORD_BOT_TOKEN")
    channel_id = int(os.environ.get("DISCORD_CHANNEL_ID"))

    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        channel = client.get_channel(channel_id)

        if channel:
            embed = discord.Embed(title=title)
            embed.set_image(url=image)
            await channel.send(embed=embed)

            await client.close()

    client.run(discord_token)

image, title = get_daily_book()
send_to_discord(image, title)
