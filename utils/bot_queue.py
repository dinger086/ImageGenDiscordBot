import threading
import asyncio
import discord

class BotQueue():
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.thread = None

    def add(self, controller_func, contoller_args, ctx, view):
        self.queue.append((controller_func, contoller_args, ctx, view))
        if len(self.queue) == 1:
            self.bot.logger.info("Starting queue")
            self.thread = threading.Thread(target=self.process_queue)
            self.thread.start()

    def process_queue(self):
        while len(self.queue) > 0:
            self.bot.logger.info(f"Queue size: {len(self.queue)}")
            self.bot.logger.info(self.queue)
            controller_func, contoller_args, ctx, view = self.queue[0]
            files = controller_func(contoller_args)
            asyncio.run_coroutine_threadsafe(ctx.send(view, files=[discord.File(file) for file in files]), self.bot.loop)
            self.queue.pop(0)
        self.thread = None
        self.bot.logger.info("Queue finished")

        
