import discord
from discord.ext import commands

class cebolinha(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['cebolonha'], brief="transforma seu texto na fala do cebolinha")
    async def cebolinha(self,ctx,*,mensagem=None):
        if mensagem == None:
            await ctx.send('Coloque uma mensagem pala eu tladuzi pala cebolês')
        mensag = ''
        last = ''
        MORSE_CODE_DICT = {'r':'l','R':'L'}
        for letter in mensagem:
            if letter != ' ':
                try:
                    if letter != last:
                        mensag += MORSE_CODE_DICT[letter]
                        last = letter
                    else:
                        pass
                except:
                    mensag += letter
                    last = ''
            else:
                mensag += ' '
                last = ''
        await ctx.send(mensag)

async def setup(client):
    await client.add_cog(cebolinha(client))