from discord.ext import commands
    
class sendmessage(commands.Cog):    
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def send(self,ctx,message=None):
        if message: await ctx.send(message)
        else: await ctx.send('Digite uma mensagem para eu enviar')

async def setup(client):
    await client.add_cog(sendmessage(client))
