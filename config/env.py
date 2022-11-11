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

env = Env()
