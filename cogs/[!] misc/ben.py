import random
import discord
from discord.ext import commands

class ben(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ben(self,ctx,*,pergunta):
        chances = [1, 2, 3, 4]
        sexo = random.choice(chances)
        if sexo == 1:
            await ctx.send('Yes')
        elif sexo == 2:
            await ctx.send('No...')
        elif sexo == 3:
            await ctx.send('ughlh')
        else:
            await ctx.send('HoHoHo')
        
async def setup(client):
    await client.add_cog(ben(client))