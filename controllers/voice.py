import discord 
import os
import utils
import requests

from config import config

class TTSController():
    def __init__(self):
        self.url = config.tortoise_url
        self.dir = os.path.join(os.getcwd(), "data", "tortoise", "outputs")

    def get_voices(self):
        voices = requests.get(f"{self.url}/voices").json()
        return voices

    def generate(self, payload):
        response = requests.post(f"{self.url}/tts", json=payload)
        return [os.path.join(self.dir, file) for file in response.json()]
