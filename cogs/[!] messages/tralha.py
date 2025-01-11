import discord
from discord.ext import commands

class tralha(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener("on_message")
    async def ovelha(self,message):
        #jaggercames
        if message.author.id == 442076414800298009:
            await message.add_reaction("🚂")

        #ciano
        if message.author.id == 437373890344255488:
            await message.add_reaction("🎭")

        #naoki
        if message.author.id == 398101175255302144:
            await message.add_reaction("🤬")

        #eu
        if message.author.id == 359163391375441920:
            await message.add_reaction("☠️")

        #hir
        if message.author.id == 935029905622720632:
            await message.add_reaction("❤")

        #pipas
        if message.author.id == 361675337811230725:
            await message.add_reaction("👺")

        #bogas
        if message.author.id == 204350761616932865:
            await message.add_reaction("👹")
	
        sex = [":0", ";0", ";o", ";O", ":o", ":O", "😱", ":scream:"]

        if message.author.id != 887896339231412224 and any(emote in message.content for emote in sex):
            if message.guild.id == 957083569543585802:
                await message.channel.send("https://cdn.discordapp.com/attachments/957089771199537252/1051711064670224394/image0.jpg")

async def setup(client):
    await client.add_cog(tralha(client))