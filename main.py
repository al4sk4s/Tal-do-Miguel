import os
import dotenv
import logging
import discord
from itertools import cycle
from colorama import Fore, Back, Style
from discord.ext import commands, tasks

#variables
paths = []
extensão = None

#set window title
os.system("title Taldo Miguel2.0's bot rewrite")

#load .env
dotenv.load_dotenv(dotenv.find_dotenv());

prefix = os.getenv("BOT_PREFIX")
owner = int(os.getenv("OWNER_ID", "0"))
discord_token = os.getenv("DISCORD_BOT_TOKEN")

#main client bot
client = commands.Bot(command_prefix = prefix, intents=discord.Intents.all())

#bot presence
with open("presence.txt", "r", encoding="utf-8") as arquivo:
    presences = [linha.strip() for linha in arquivo]

status = cycle(presences)

#folder scanner
def scanner():
    for folder in os.listdir('./cogs'):
        if folder.startswith('[!]'):
            print(f'[ ./cogs/{folder} ]')
            paths.append([f'./cogs/{folder}', f'cogs.{folder}', os.getcwd()+f'\cogs\{folder}'])

#file/cog finder
def find_file(name):
    for i in paths:
        for filename in os.listdir(i[0]):
            if filename[:-3] == name:
                return [f'{i[1]}.{name}', f'{i[2]}\{name}.py']

#pra preparar o loop
@client.event
async def on_ready():
    print('searching for directories. . .')
    scanner()
    
    print('starting to load. . .')
    num = 1

    for i in paths:
        for filename in os.listdir(i[0]):
            if filename.endswith('.py'):
                try:
                    await client.load_extension(f'{i[1]}.{filename[:-3]}')
                    print(Fore.LIGHTGREEN_EX + f'> [ {num} - {filename[:-3]} ]' + Style.RESET_ALL)
                    num += 1
                except:
                    print(Fore.LIGHTRED_EX + f'!! [ {num} - {filename[:-3]} ]' + Style.RESET_ALL)
        
        print(f'[{i[0]}] loaded. . .')

    change_status.start()

    print('connected!')

#o loop do status do tardomiugel
@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

#comando de load
@client.command(brief='carrega uma extensão')
async def load(ctx, extension):

    if ctx.message.author.id == owner:
        try:
            await client.load_extension(find_file(extension)[0])
            await ctx.send(f'[{extension}] carregada com sucesso')
        except:
            await ctx.send('Não foi possivel carregar sua extensão')
    else:
        await ctx.send("you're not an owner")

#comando de unload
@client.command(brief='descarrega uma extensão')
async def unload(ctx, extension):

    if ctx.message.author.id == owner:
        try:
            await client.unload_extension(find_file(extension)[0])
            await ctx.send(f'[{extension}] descarregada com sucesso')
        except:
            await ctx.send('Não foi possivel descarregar sua extensão')
    else:
        await ctx.send("you're not an owner")

#comando de reload
@client.command(brief='recarrega uma extensão')
async def reload(ctx, extension=None):
    global extensão

    if ctx.message.author.id == owner:

        if extension == None and extensão == None:
            await ctx.send('Nenhuma cog carregada no sistema para reload')

        try:
            await client.reload_extension(find_file(extension if extension != None else extensão)[0])
            if extension != None: extensão = extension
            await ctx.send(f'[{extensão}] recarregada com sucesso')
        except:
            await ctx.send('Não foi possivel recarregar sua extensão')
    else:
        await ctx.send("you're not an owner")

#deleta cogs
@client.command(brief='deleta uma extensão')
async def delete(ctx, extension):
    if ctx.message.author.id == owner:
        try:
            file_path = find_file(extension)
            if file_path != None:
                os.remove(file_path[1])
                await client.unload_extension(f'{file_path[0]}')
                await ctx.send(f'deletado {extension}.py com sucesso')
        except:
            await ctx.send('deu erro, ou essa extensao nao existe mais')
    else:
        await ctx.send("you're not an owner")

#rodar o token
client.run(discord_token, log_level=logging.WARNING)#, log_handler=None)