import json
import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import psycopg2
from address import detect_address
from dotenv import load_dotenv

load_dotenv()

DATABASE = os.getenv('DATABASE_URL')
TOKEN = os.getenv('BOT_TOKEN')
BOT_ID = TOKEN.split(':')[0]
CHAT_ID = int(os.getenv('CHAT_ID'))
COLLECTION = detect_address(os.getenv('COLLECTION'))['bounceable']['b64url']

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
if not isinstance(HEROKU_APP_NAME, type(None)):
    WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
    WEBHOOK_PATH = f'/webhook/{TOKEN}'
    WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

    WEBAPP_HOST = '0.0.0.0'
    WEBAPP_PORT = os.getenv('PORT', default=8000)
    bot_mode = "WEBHOOK"
else:
    bot_mode = "POLLING"

API_TOKEN = os.getenv('TONCENTER_API_KEY')

TONCENTER_BASE = 'https://toncenter.com/api/v2/'
headers = {
    'cookie': 'csrftoken=vO44viQbEDlbcKiLz56aaE8tLmjzc5XtVqUTZo6zgItxRNehF7VRGlCVdQR3dul9',
    'x-csrftoken': 'vO44viQbEDlbcKiLz56aaE8tLmjzc5XtVqUTZo6zgItxRNehF7VRGlCVdQR3dul9',
    'referer': 'https://getgems.io/collection/EQATbIOeT9ziq7Jf76dJlnWIAiZggY2TeDteAh46D4QICBZj/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

english = json.loads(open('en.json', 'r').read())
english['my_nft'] = f'have passed <a href="tg://user?id={BOT_ID}">verification</a>. This is my Fingerprint:'

russian = json.loads(open('ru.json', 'rb').read())
russian['my_nft'] = f'прошёл <a href="tg://user?id={BOT_ID}">верификацию</a>. Это мой Fingerprint:'
