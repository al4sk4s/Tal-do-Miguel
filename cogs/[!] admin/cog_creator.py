import os
import discord
from discord.ext import commands

class cog_creator(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.paths = []
    
    #path scanner
    def scanner(self):
        for folder in os.listdir('./cogs'):
            if folder.startswith('[!]'):
                self.paths.append([folder, os.getcwd()+f'\\cogs\\{folder}'])
    
    #file/cog finder
    def find_file(self, path, name):
        for filename in os.listdir(path):
            if filename == name: return True
        return False
    
    def default_cog(self, name):
        return f"""from discord.ext import commands
    
class {name}(commands.Cog):    
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def [](self,ctx):
        await ctx.send('teste!')

async def setup(client):
    await client.add_cog({name}(client))
"""

    @commands.command(aliases=['criar','newcog'], brief="Criador de extensões, exemplo: [prefix]create test.py")
    async def create(self,ctx, name=None):
        if ctx.message.author.id != int(os.getenv("OWNER_ID", "0")):
            await ctx.send('Você não tem permição para rodar este comando'); return;
    
        if name == None: await ctx.send('Escreva o nome da sua nova cog, exemplo: [prefix]create test.py'); return

        self.scanner(); num = 1; options = ""

        for path in self.paths:
            options += f"[{num}] {path[0]}\n"
            num += 1

        await ctx.send(f"Escolha uma das opções abaixo respondendo com o número correspondente dentro de 30 segundos:\n{options}")

        def check(message):
            return (
                message.author == ctx.author and
                message.channel == ctx.channel and
                message.content.isdigit() and
                int(message.content) in range(1, num)
            )

        try:
            # Aguarda a resposta do usuário por 15 segundos
            msg = await self.client.wait_for('message', timeout=15.0, check=check)
            choice = int(msg.content)

            await ctx.send(f'Path selecionado: {self.paths[choice-1][0]}')

            #checa se há um arquivo com esse nome no diretorio
            if self.find_file(self.paths[choice-1][1], name) == True:
                await ctx.send('Já existe uma cog com este nome neste diretório.'); self.paths = []; return;

            try:

                open(self.paths[choice-1][1]+f'\\{name}', 'x').close()

                with open(self.paths[choice-1][1]+f'\\{name}', 'a') as archive: archive.write(self.default_cog(name[:-3]))

                await ctx.reply(f'{name} criado com sucesso!')
            
            except: await ctx.send('Não consegui criar o arquivo desejado')

        except discord.TimeoutError: await ctx.send("Tempo esgotado! Comando cancelado.")
        
        self.paths = []

async def setup(client):
    await client.add_cog(cog_creator(client))