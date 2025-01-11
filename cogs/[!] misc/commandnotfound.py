from discord.ext import commands
    
class commandnotfound(commands.Cog):    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            # Aqui você pode tratar o comando não encontrado da maneira que desejar
            #await ctx.send(f"Não achei esse comando ai zé mané: ```{error}```")
            await ctx.send(f"```{error}```")

async def setup(client):
    await client.add_cog(commandnotfound(client))