import discord
import discord.ext.commands as commands
# import discord context
from discord.ext.commands.context import Context

import src.chatgpt as chatgpt
import src.database as database

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix='/')


dialog = {}


@bot.event
async def on_ready():
    print("Ready")


@bot.command(name='register')
async def register(ctx: Context, *args):
    '''
    register auth data of chatgpt from user
    '''
    user_uuid = ctx.message.author.id
    user_auth = {
        'access_token': ' '.join(args)
    }
    await database.set_user_auth(user_uuid, user_auth)
    await ctx.channel.send('auth data is successfully registered.')
    await ctx.message.delete()


@bot.command(name='myask')
async def myask(ctx: Context, *args):
    '''
    send a prompt to chatgpt, bot replies with a response
    1. get registerd user aut if not, suggest to register
    2. get chatbot instance if not, create one
    3. send prompt to chatbot instance
    4. get response from chatbot instance

    params:
        ctx: discord context
        *args: prompt
    '''
    user_uuid = ctx.message.author.id
    try:
        user_auth = await database.get_user_auth(user_uuid)
    except Exception as e:
        dm_channel = await ctx.message.author.create_dm()
        await dm_channel.send('You are not registered, please register first')
        return
    
    chatbot_instance = chatgpt.get_instance(user_auth)
    prompt = ' '.join(args)
    last_conversation_id = dialog.get(user_uuid, None)

    response, conversation_id = await chatgpt.ask_v1(chatbot_instance, prompt, last_conversation_id)

    dialog[user_uuid] = conversation_id
    await ctx.reply(response)

