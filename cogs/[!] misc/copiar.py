import discord
import clipboard
from discord.ext import commands

class copiar(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief="copia para meu ctrl+v uma mensagem")
    async def copy(self,ctx,*,message):
        teste = clipboard.paste()
        if teste == message:
            await ctx.send('eu já copoeo essa mensagen')
        else:
            clipboard.copy(message)
            await ctx.send('cupiei i num sô lixuh coméia')

async def setup(client):
    await client.add_cog(copiar(client))