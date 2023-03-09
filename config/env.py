import os
from dotenv import load_dotenv

class Env:
  def __init__(self):
    load_dotenv()

    self.ENVIRONMENT = os.environ['ENVIRONMENT']
    self.APP_HOST = os.environ['APP_HOST']
    self.APP_PORT = os.environ['APP_PORT']
    self.TEMPLATE_DIR = os.environ['TEMPLATE_DIR']
    self.STATIC_DIR = os.environ['STATIC_DIR']
    self.STOPWORDS_PATH = os.environ['STOPWORDS_PATH']
    self.DICTIONARY_PATH = os.environ['DICTIONARY_PATH']
    self.SLANG_WORD_COL = os.environ['SLANG_WORD_COL']
    self.FORMAL_WORD_COL = os.environ['FORMAL_WORD_COL']

env = Env()
