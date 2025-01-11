import discord
from discord.ext import commands

tocando = False

class radio(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.tocando = {}
        # valor[828727751649132554] = {"tocando" : False}

    @commands.command()
    async def radio(self,ctx, parar=None):
        global tocando
        sexo = ['parar', 'stop', 'desligar', 'off']

        getPlayer = self.client.get_cog('downloader')
        if getPlayer.player.get(ctx.guild.id):
            await self.client.get_cog('downloader').parar(ctx)

        if not ctx.guild.id in self.tocando.keys():
            self.tocando[ctx.guild.id] = {"tocando" : False}

        if parar == None:
            if not ctx.voice_client:
                if not ctx.author.voice.channel:
                    await ctx.send('Por favor, entre em uma call para iniciar a radio')
                else:
                    await ctx.author.voice.channel.connect()

            if self.tocando[ctx.guild.id]["tocando"] == False:
                stream_url = "https://stm6.xcast.com.br:9328/stream" #https://sws.onradio.biz:10875/;
                ctx.voice_client.play(discord.FFmpegPCMAudio(stream_url, executable=r"C:\ffmpeg\ffmpeg.exe"))
                await ctx.send("📻 A radio café radio Iniciou!!!!!! 📻", file=discord.File('C:\\Users\\gamer\\Downloads\\bote\\radio.jpg'))
                self.tocando[ctx.guild.id]["tocando"] = True
            else:
                await ctx.send('Já estou tocando o radio. Se você quiser parar o radio, digite **radio parar*')

        elif parar in sexo:
            if self.tocando[ctx.guild.id]["tocando"] == True:
                ctx.voice_client.stop()
                await ctx.send(f"📻 Você {ctx.author.name} desligou a radio café :c 📻")
                del self.tocando[ctx.guild.id]
            else:
                if not ctx.voice_client or self.tocando[ctx.guild.id]["tocando"] == False:
                    await ctx.send('Não estou em modo rádio no momento :3')
        else:
            await ctx.send('Não entendi esse comando')

async def setup(client):
    await client.add_cog(radio(client))