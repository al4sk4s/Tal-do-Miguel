import discord
from discord.ext import commands

class join_left(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['entra', 'entrar','connect'], brief="entra em um canal de voz")
    async def join(self,ctx):
        if not ctx.author.voice:
            await ctx.send('Você não está conectado em um canal de voz'); return

        if not ctx.voice_client: await ctx.author.voice.channel.connect()
            
        elif ctx.voice_client.channel != ctx.author.voice.channel:

            await ctx.voice_client.move_to(ctx.author.voice.channel)
        
        await ctx.send('Me conectei a sua chamada')

    @commands.command(aliases=['sai', 'sair','disconnect'], brief="sai de um canal de voz")
    async def left(self,ctx):
        if not ctx.author.voice:
            await ctx.send('Você não está conectado em um canal de voz'); return

        if ctx.voice_client:

            if ctx.voice_client.channel != ctx.author.voice.channel:
                await ctx.send('Esteja na mesma chamada para me desconectar'); return
            
            await ctx.voice_client.disconnect()
            await ctx.send('Me desconectei a sua chamada')

        else: await ctx.send('Eu não estou conectado a uma chamada')

async def setup(client):
    await client.add_cog(join_left(client))