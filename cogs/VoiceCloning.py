import discord
from discord import app_commands
from discord.ext import commands, tasks

from typing import Optional

from controllers.voice import TTSController

class VoiceCloning(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.controller = TTSController()

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info("TTS is ready")

    @commands.hybrid_group(name="clone", invoke_without_command=True, aliases=["voice", "v"])
    async def clone(self, ctx: commands.Context):
        """TTS commands"""
        # if no subcommand is invoked, make input the prompt
        await self.generate(ctx, prompt=ctx.message.content[len(ctx.prefix + ctx.invoked_with) + 1:])

    @clone.command(name="generate")
    async def generate(self, ctx: commands.Context, *, prompt: str, voice: Optional[str] = "jlaw"):
        """Generate an audio file using the TTS model"""
        await ctx.send(f"Added {prompt} to queue.")
        payload = {
            "text": prompt,
            "voice": voice
        }
        self.bot.queue.add(self.controller.generate, payload, ctx, prompt)

    @generate.autocomplete("voice")
    async def voice_autocomplete(self, ctx: commands.Context, prompt: str):
        voices = []
        for voice in self.controller.get_voices():
            if prompt.lower() in voice.lower():
                voices.append(voice)
        return voices

async def setup(bot):
    await bot.add_cog(VoiceCloning(bot))