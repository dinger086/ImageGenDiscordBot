import discord
from discord import ui


class StableView(ui.View):
    def __init__(self, ctx: discord.ext.commands.Context):
        super().__init__(timeout=60)
        self.ctx = ctx

    @ui.button(label="Generate", style=discord.ButtonStyle.green)
    async def generate(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Generating...", ephemeral=True)
        await self.ctx.invoke(self.ctx.bot.get_command("stable generate"), prompt=self.ctx.message.content[len(self.ctx.prefix + self.ctx.invoked_with) + 1:])
        self.stop()

    @ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Cancelled", ephemeral=True)
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            return True
        await interaction.response.send_message("You cannot use this menu", ephemeral=True)
        return False

    async def on_timeout(self):
        await self.message.edit(view=None)
        await self.ctx.send("Timed out", delete_after=10)
        self.stop()