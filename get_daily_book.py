import os

import requests
import telepot
from bs4 import BeautifulSoup
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


def send_to_telegram(image, title):
    load_dotenv(find_dotenv())
    api_bot = os.environ.get("api_bot")
    chat_id = os.environ.get("chat_id")
    bot = telepot.Bot(api_bot)
    bot.sendMessage(chat_id, title)
    bot.sendPhoto(chat_id, image)


image, title = get_daily_book()
send_to_telegram(image, title)
