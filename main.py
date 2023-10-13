import discord
from discord import Webhook
import aiohttp
import tracemalloc
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
channelid = 1162355674043383831 # id of the channel you want to track

tracemalloc.start()

intents = discord.Intents.all()
client = discord.Client(intents=intents, status=discord.Status.offline)

def getEmbeds(ctx):
    return '\n'.join(ctx.attachments[x].url for x in range(len(ctx.attachments)))

async def get_sticker_urls(ctx):
    sticker_urls = []

    for sticker in ctx.stickers:
        sticker_url = sticker.url
        sticker_urls.append(sticker_url)

    return sticker_urls

async def Spy(ctx, id, webhookLink):
    if ctx.channel.id == id:
        channel = client.get_channel(id)
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(webhookLink, session=session)
            attachments = getEmbeds(ctx)

            sticker_urls = await get_sticker_urls(ctx)

            if ctx.reference is not None:
                reply = await channel.fetch_message(ctx.reference.message_id)
                reply_attachments = getEmbeds(reply) if len(reply.attachments) > 0 else ''
                reply_content = f'**Reply to {reply.author.display_name} ({reply.author.name})**: {reply.content}\n{reply_attachments}\n'

                if sticker_urls:
                    reply_content += '\n**Attachments**:\n' + '\n'.join(sticker_urls)

                content = reply_content + (ctx.content or '') + (f'\n**Author Attachments**:\n{attachments}' if attachments else '')
            else:
                content = (ctx.content or '') + (f'\n**Author Attachments**:\n{attachments}' if attachments else '')

                if sticker_urls:
                    content += '\n**Attachments**:\n' + '\n'.join(sticker_urls)

            await webhook.send(content=content, username=f'{ctx.author.display_name} ({ctx.author.name})', avatar_url=ctx.author.avatar)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(ctx):
    await Spy(ctx, channelid, 'webhook url')

client.run(TOKEN)
