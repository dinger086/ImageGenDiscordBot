import discord
from discord import app_commands
from discord.ext import commands, tasks

from typing import Optional

from controllers.stable import StableController
from views.stable import StableView
from config import config

class Stable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = config.stable_url
        self.controller = StableController()

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info("Stable is ready")

    @commands.hybrid_group(name="stable", invoke_without_command=True, aliases=["st"])
    async def stable(self, ctx: commands.Context):
        """Stable diffusion commands"""
        # if no subcommand is invoked, make input the prompt
        await self.generate(ctx, prompt=ctx.message.content[len(ctx.prefix + ctx.invoked_with) + 1:])

    @stable.command(name="generate")
    async def generate(self, ctx: commands.Context, *, prompt: str, seed: Optional[int] = -1, negative_prompt: Optional[str] = "", batch_size: Optional[int] = 3, n_iter: Optional[int] = 3, steps: Optional[int] = 25):
        """Generate an image using the stable diffusion model"""
        if not self.controller.is_server_ready():
            await ctx.send("Getting ready, please try again in a few seconds")
            return
        await ctx.send(f"Added {prompt} to queue.")
        payload = {
            "prompt": prompt,
            "seed": seed,
            "negative_prompt": negative_prompt,
            "batch_size": batch_size,
            "n_iter": n_iter,
            "steps": steps,
            "send_images": False,
            "save_images": True
        }
        #await ctx.send("options", view=StableView(ctx))
        self.bot.queue.add(self.controller.txt2img, payload, ctx, prompt)

    
    @commands.command(name="gif")
    async def gif(self, ctx: commands.Context, *, text: str):
        await self.txt2gif(ctx, text=text)


    @stable.command(name="txt2gif")
    async def txt2gif(self, ctx: commands.Context, *, text: str):
        """Convert text to gif"""
        payload = {
            "prompt": text,
            "batch_size": 1,
            "n_iter": 1,
            "steps": 25,
            "sampler_index": "DPM++ 2M Karras",
            "script_name": "seed travel",
            "script_args": [
                True, #Use random seeds
                4, #Number of seeds
                "", #Destination seeds
                10, #Number of steps
                "Linear", #Interpolation curve
                3, #Curve strength
                False, #Loop back to initial seed
                5, #Fps 
                False, #Show generated images in ui
                False, #Compare paths
                False, #Allow default sampler
                False, #Bump seed
                0, #Lead in/out
                "Lanczos", #Upscaler
                1, #Upscale ratio
                True, #Use cache
                0, #SSIM thresholdctx
                0, #SSIM Center Crop
                0.001, #SSIM min substep
                75, #SSIM min threshold
                0, #RIFE passes
                False, #Drop original frames
                True #Save extra status information
            ]
        }
        await ctx.send("Added to queue.")
        self.bot.queue.add(self.controller.txt2gif, payload, ctx, f"Finished {text}")

    @stable.command(name="help", aliases=["h"])
    async def help(self, ctx: commands.Context):
        """Help for stable diffusion"""
        await ctx.send_help(ctx.command)

    @commands.command(name="check")
    @commands.is_owner()
    async def check_unfinished(self, ctx: commands.Context):
        """Check and do any unfinished tasks"""
        for server in self.bot.guilds:
            print(server)
            for channel in server.text_channels:
                async for message in channel.history(limit=200):
                    print(message.content)
                    if message.author == self.bot.user and message.attachments != []:
                        break
                    if message.content.startswith(config.PREFIX) and not message.content.startswith(config.PREFIX + "check"):
                        context = await self.bot.get_context(message)
                        commands = [command for command in self.bot.commands if command.cog_name == "Stable"]
                        for command in commands:
                            if context.invoked_with == command.name or context.invoked_with in command.aliases:
                                print("Found unfinished task")
                                print(context.invoked_with)
                                await self.bot.invoke(context)
                                break



async def setup(bot):
    await bot.add_cog(Stable(bot))


