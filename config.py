import os

from dotenv import load_dotenv

load_dotenv()

INPUT_FILE = os.getenv('INPUT_FILE')

OUTPUT_FILE = os.getenv('OUTPUT_FILE')

ITEM = os.getenv('ITEM')

BOT_LEVEL = os.getenv('BOT_LEVEL')
