import re
import yt_dlp
import discord
import datetime
import clipboard
import threading
from discord.ext import commands
from urllib import parse, request
from asyncio import run_coroutine_threadsafe

# -reconnect_delay_max 15 -reconnect 0 -reconnect_streamed 0 
YDL_OPTIONS = {'format':"bestaudio",'skip-download':True,'youtube_include_dash_manifest': False}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn -movflags +faststart'} #-movflags +faststart

class downloader(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.player = {}

    def get_voice_channel(self, channel_id):
        for vc in self.client.voice_clients:
            if vc.channel.id == channel_id:
                return vc.channel 
        return False
    
    def minimal_play(self, ctx, canaul):
        ctx.voice_client.play(discord.FFmpegPCMAudio(playing[0]['url2'],**FFMPEG_OPTIONS), after=lambda e: self.tocak(ctx))
        coro = canaul.send(f'Tocando `{playing[0]["name"]} : {playing[0]["duration"]}`')
        fut = run_coroutine_threadsafe(coro, self.client.loop)
        return fut

    def tocak(self,ctx):
        print('to popando')
        canaul = self.client.get_channel(int(playing[0]['channel_id']))

        if self.player[canaul.guild.id]["loop"] == False:
            if len(queue) == 0:
                coro = canaul.send(f'Não estou tocando mais nada :(')
                del self.player[canaul.guild.id]
                fut = run_coroutine_threadsafe(coro, self.client.loop)

                try: fut.result()
                except: pass
                
            playing.pop()

            if len(queue) != 0:
                playing.append(queue[0])
                queue.pop(0)

                fut = self.minimal_play(ctx, canaul)

                try: fut.result()
                except: pass
        else:
            fut = self.minimal_play(ctx, canaul)

            try: fut.result()
            except: pass

    @commands.command(aliases=['play', 'p'], brief='comando para tocar uma musica')
    async def tocar(self,ctx,url=None,*,resto=None):
        getRadio = self.client.get_cog('radio')
        if getRadio.tocando.get(ctx.guild.id) and getRadio.tocando[ctx.guild.id]["tocando"] == True:
            await self.client.get_cog('radio').radio(ctx, "parar")
        
        await ctx.send('Já já começo a toca :3 (xinga o gamer ai por esse delay)')

        if url == None and not ctx.message.attachments:
            if ctx.author.id == 359163391375441920:
                url = clipboard.paste()
            else:
                await ctx.send('cade a url animaç')
                return

        if url != None:
            if url.startswith('https://open.spotify') == True:
                await ctx.send('mano eu não to aceitando spotify ainda, vai xingar o gamer pra colocar isso'); return

            if not ctx.message.author.voice:
                await ctx.send('Você não está em uma call ou eu nao vejo ela :('); return

            channel = ctx.message.author.voice.channel

            if not ctx.guild.id in self.player.keys():

                if not self.get_voice_channel(ctx.message.author.voice.channel.id):

                    try: await channel.connect()
                    except: await ctx.send('Não consegui conectar na call'); return

                self.player[ctx.guild.id] = {"playing":[],"queue":[],"channel_id":[channel.id],"paused":False,"loop":False}

            global player;      player = self.player[ctx.guild.id]
            global playing;     playing = self.player[ctx.guild.id]["playing"]
            global queue;       queue = self.player[ctx.guild.id]["queue"]
            global channel_id;  channel_id = self.player[ctx.guild.id]["channel_id"]

            #fix em caso tenha trocado de call
            if channel_id != channel.id: channel_id = channel.id

            #thread
            if url.startswith('https://youtu.be') != True and url.startswith('https://www.youtube.com') != True and url.startswith('https://youtube.com') != True and url.startswith('https://media.discordapp') != True and url.startswith('https://cdn.discordapp') != True:
                queryString = parse.urlencode({'search_query': f'{url} {resto}'})
                htmContent = request.urlopen('http://www.youtube.com/results?' + queryString)
                searchResults = re.findall('/watch\?v=(.{11})', htmContent.read().decode())
                url = f'https://www.youtube.com/watch?v={searchResults[0]}'

            if url.find('list=') != -1:
                druh = url.split('list=')
                url = druh[0]
        
        #thread?
        if not ctx.message.attachments:
            if url.startswith('https://media.discordapp') != True and url.startswith('https://cdn.discordapp') != True:
                
                #with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)

                    #global title
                    title = info['title']
                    seconds = info['duration']
                    url2 = info['formats'][4]['url']

                    duration = str(datetime.timedelta(seconds=seconds))
                    if duration.startswith("0"):
                        cu = duration.split(":")
                        duration = f'{cu[1]}:{cu[2]}'

                eita = {"name" : title, "duration" : duration, "id" : int(ctx.message.author.voice.channel.id), "channel_id" : int(ctx.message.channel.id) ,"url2" : url2, "type" : 'url'}
            
            else:
                crying_cat_face = url.split('/')
                title = crying_cat_face[len(crying_cat_face)-1]
                duration = '??'
                url2 = url

                eita = {"name" : title, "duration" : duration, "id" : int(ctx.message.author.voice.channel.id), "channel_id" : int(ctx.message.channel.id) ,"url2" : url2, "type" : 'file'}
            
            if playing == []:
                source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
                ctx.voice_client.play(source, after=lambda e: self.tocak(ctx))
                playing.append(eita)
                await ctx.send(f'Tocando `{playing[0]["name"]} : {playing[0]["duration"]}`')
            else:
                queue.append(eita)
                qunt = int(len(queue))
                await ctx.send(f'Sua musica foi colocada na playlist, `{queue[qunt-1]["name"]} : {queue[qunt-1]["duration"]}`')
        else:
            title = ctx.message.attachments[0].filename[:-4]
            duration = '??'
            url2 = ctx.message.attachments[0].url

            eita = {"name" : title, "duration" : duration, "id" : int(ctx.message.author.voice.channel.id), "channel_id" : int(ctx.message.channel.id) ,"url2" : url2, "type" : 'file'}
            
            if playing == []:
                source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
                ctx.voice_client.play(source, after=lambda e: self.tocak(ctx))
                playing.append(eita)
                await ctx.send(f'Tocando `{playing[0]["name"]} : {playing[0]["duration"]}`')
            else:
                queue.append(eita)
                qunt = int(len(queue))
                await ctx.send(f'Sua musica foi colocada na playlist, `{queue[qunt-1]["name"]} : {queue[qunt-1]["duration"]}`')

    @commands.command(brief='coloca a musica atual em loop')
    async def loop(self,ctx):
        if not ctx.guild.id in self.player.keys():
            await ctx.send('eu ach oque eu não etou tocando nada no momentmo'); return

        if self.player[ctx.guild.id]["loop"] == False:
            self.player[ctx.guild.id]["loop"] = True
            await ctx.send(f'Loop ligado maninho: {self.player[ctx.guild.id]["loop"]}')
        else:
            self.player[ctx.guild.id]["loop"] = False
            await ctx.send(f'Loop desligado mainho: {self.player[ctx.guild.id]["loop"]}')

    @commands.command(aliases=['s'], brief='pula a musica atual')
    async def skip(self,ctx):
        if not ctx.guild.id in self.player.keys():
            await ctx.send('eu ach oque eu não etou tocando nada no momentmo'); return
        
        playing = self.player[ctx.guild.id]["playing"]
        queue = self.player[ctx.guild.id]["queue"]

        if len(playing) != 0:
            ctx.voice_client.stop()
        else:
            await ctx.send('eu ach oque eu não etou tocando nada no momentmo'); return
        
        if len(queue) != 0:
            await ctx.send(f'A `{playing[0]["name"]} : {playing[0]["duration"]}` foi skippada, tocando `{queue[0]["name"]} : {queue[0]["duration"]}`')
        else:
            await ctx.send(f'A `{playing[0]["name"]} : {playing[0]["duration"]}` foi skippada.')

    @commands.command(aliases=['queue', 'q'], brief='comando de queue')
    async def lista(self,ctx,sex=None, sex2:int=None):
        if not ctx.guild.id in self.player.keys():
            await ctx.send('eu ach oque eu não etou tocando nada no momentmo'); return

        playing = self.player[ctx.guild.id]["playing"]
        queue = self.player[ctx.guild.id]["queue"]

        if sex not in ['clear', 'remove']:
            contagem = 0
            nume = len(queue)
            listinha = ''
            if playing != []:
                listinha += f"`--> {playing[0]['name']} : {playing[0]['duration']} <--`\n"
                while nume != 0:
                    listinha += f"`[{contagem+1}] {queue[contagem]['name']} : {queue[contagem]['duration']}`\n"
                    contagem += 1
                    nume -= 1
                await ctx.send(f'{listinha}')
            else:
                await ctx.send('Não estou tocando nada no momento')

        elif sex == 'clear':
            if len(queue) >= 1:
                await ctx.send(f'Dei clear na queue, removi {len(queue)} musicas')
            else:
                await ctx.send(f'Dei clear, mas não tinha nada na queue :/')
            queue = []

        elif sex == 'remove':
            if sex2 == None:
                await ctx.send(f'Você digita `*queue remove (número)` para remover a musica enumerada da queue')
            elif sex2 <= 0:
                await ctx.send(f'Como raios eu vou remover a musica `{sex2}` da queue (não coloqe numeros Negativos por favor somente positivos)')
            else:
                if len(queue) >= sex2:
                    await ctx.send(f'A `{queue[sex2-1]["name"]} : {queue[sex2-1]["duration"]}` foi removida da queue.')
                    queue.pop(sex2-1)
                else:
                    await ctx.send(f'Como vc quer remover um numero acima da quantidade da queue? (a queue está com {len(queue)} musicas)')

    @commands.command(aliases=['pausar'], brief='pausa a musica')
    async def pause(self,ctx):
        if not ctx.guild.id in self.player.keys():
            await ctx.send('eu ach oque eu não etou tocando nada no momentmo'); return

        if playing != []:
            paused = self.player[ctx.guild.id]["paused"]
            
            if paused != False:
                await ctx.send(f'`{playing[0]["name"]} já está pausada, digite *resume`')
            else:
                ctx.voice_client.pause()
                self.player[ctx.guild.id]["paused"] = True
                await ctx.send(f'`{playing[0]["name"]}` foi pausada')
        else:
            await ctx.send(f'Não está tocando nada no momento')

    @commands.command(aliases=['resumir'], brief='volta a tocar a musica')
    async def resume(self,ctx):
        if not ctx.guild.id in self.player.keys():
            await ctx.send('eu ach oque eu não etou tocando nada no momentmo'); return

        if playing != []:
            paused = self.player[ctx.guild.id]["paused"]
            print(paused)
            if paused != False:
                ctx.voice_client.resume()
                self.player[ctx.guild.id]["paused"] = False
                await ctx.send(f'`{playing[0]["name"]}` foi resumida')
            else:
                await ctx.send(f'`{playing[0]["name"]}` já está tocando')
        else:
            await ctx.send(f'Não está tocando nada no momento')

    @commands.command(aliases=['stop'], brief='para todas as musicas')
    async def parar(self,ctx):
        if not ctx.guild.id in self.player.keys():
            await ctx.send('eu ach oque eu não etou tocando nada no momentmo'); return

        if playing != []:
            self.player[ctx.guild.id]["paused"] = False
            self.player[ctx.guild.id]["loop"] = False
            self.player[ctx.guild.id]["queue"] = []
            ctx.voice_client.stop()
            await ctx.send(f'`{playing[0]["name"]}` foi parada')
        else:
            await ctx.send(f'Não está tocando nada no momento')

async def setup(client):
    await client.add_cog(downloader(client))