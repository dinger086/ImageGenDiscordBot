import os

class Config():
    def __init__(self):
        self.TOKEN = os.environ.get('DISCORD_TOKEN')
        self.PREFIX = "$"
        self.debug = False
        self.debug_channel = 0 #Enter a channel id for debugging
        self.stable_url = "http://127.0.0.1:7860"
        self.tortoise_url = "http://127.0.0.1:8501"
        self.default_options = {
            "negative_prompt": "",
            "magic_prompt": False,
            "model": "",
        }

        self.LOOK_BACK = 100
        self.EMBED_COLOR = 0x00ff00
        self.EMBED_COLOR_ERROR = 0xff0000
        self.EMBED_COLOR_WARNING = 0xffff00
        self.EMBED_COLOR_INFO = 0x0000ff
        self.EMBED_COLOR_SUCCESS = 0x00ff00


config = Config()