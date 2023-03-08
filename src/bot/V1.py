import discord
import discord.ext.commands as commands

import src.chatgpt.V1 as chatgpt
import src.database.V1 as database

intents = discord.Intents.default()
intents.message_content = True


class BotWrapper():
    def __init__(self, db_url: str):
        self.db_client = database.connect_to_database(db_url)
        self.bot = self.create_bot()

    def create_bot(self) -> commands.Bot:
        bot = commands.Bot(intents=intents, command_prefix='/')

        @bot.event
        async def on_ready():
            print('ChatGPT Discord Bot is ready')
            print('Version: V1')

        @bot.group(name='register')
        async def register(ctx: commands.Context):
            '''
            register auth data of chatgpt from user
            '''
            if ctx.invoked_subcommand is None:
                await ctx.channel.send('Please specify a auth type')
                await ctx.message.delete()

        @register.command(name='access_token')
        async def register_access_token(ctx: commands.Context, *, token: str):
            '''
            register access_token of chatgpt from user
            '''
            user_uuid = ctx.message.author.id
            user_auth = {
                'access_token': token
            }
            database.set_user_auth(self.db_client, user_uuid, user_auth)
            await ctx.channel.send('auth data is successfully registered.')
            await ctx.message.delete()

        @bot.command(name='chatgpt')
        async def chatgpt_command(ctx: commands.Context, *, prompt: str):
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
                user_auth = database.get_user_auth(self.db_client, user_uuid)
                last_conversation = database.get_last_conversation(self.db_client, user_uuid)
            except Exception as e:
                print(e.with_traceback(None))
                await ctx.reply('You are not registered, please register first')
                return
            
            try:
                chatbot_instance = chatgpt.get_chatbot_instance(user_auth)
                response, conversation_id = chatgpt.ask(
                    chatbot_instance,
                    prompt,
                    last_conversation,
                )
                database.set_last_conversation(self.db_client, user_uuid, conversation_id)
                await ctx.reply(response)
            except Exception as e:
                print(e.with_traceback(None))
                await ctx.reply('Something went wrong, please try again later')
            
        return bot