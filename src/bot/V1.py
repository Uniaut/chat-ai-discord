import discord
import discord.app_commands as app_commands
import discord.ext.commands as commands

import src.chatgpt.V1 as chatgpt
import src.database.V1 as database

intents = discord.Intents.default()
intents.message_content = True


class BotWrapper():
    def __init__(self, db_url: str):
        self.db_client = database.connect_to_database(db_url)
        self.bot: discord.Client = self.create_bot()


    def create_bot(self):
        app = discord.Client(intents=intents, command_prefix='/')
        tree = app_commands.CommandTree(app)

        @app.event
        async def on_ready():
            await tree.sync()
            print('ChatGPT Discord Bot is ready')
            print('Version: V1')

        @tree.command(name='register')
        async def register(interaction: discord.Interaction, *, token: str):
            '''
            register auth data of chatgpt from user
            '''
            await interaction.response.send_message('...', delete_after=0)
            user_uuid = interaction.user.id
            user_auth = {
                'access_token': token
            }
            database.set_user_auth(self.db_client, user_uuid, user_auth)
            await interaction.channel.send('Auth data is successfully registered.')

        @tree.command(name='chatgpt')
        async def chatgpt_command(interaction: discord.Interaction, *, prompt: str):
            '''
            send a prompt to chatgpt, bot replies with a response
            1. get registerd user aut if not, suggest to register
            2. get chatbot instance if not, create one
            3. send prompt to chatbot instance
            4. get response from chatbot instance
            '''
            user_uuid = interaction.user.id
            try:
                user_auth = database.get_user_auth(self.db_client, user_uuid)
                last_conversation = database.get_last_conversation(self.db_client, user_uuid)
            except Exception as e:
                print(e.with_traceback(None))
                await interaction.response.send_message('You have not registered your access token, please register first')
                return
            
            try:
                chatbot_instance = chatgpt.get_chatbot_instance(user_auth)
                response, conversation_id = chatgpt.ask(
                    chatbot_instance,
                    prompt,
                    last_conversation,
                )
                database.set_last_conversation(self.db_client, user_uuid, conversation_id)
                await interaction.response.send_message(response)
            except Exception as e:
                print(e.with_traceback(None))
                await interaction.response.send_message('Something went wrong, please try again later')
        
        @tree.command(name='help')
        async def help_command(interaction: discord.Interaction):
            '''
            show help message
            '''
            await interaction.response.send_message('''
                /register <token> - register auth data of chatgpt from user
                /chatgpt <prompt> - send a prompt to chatgpt, bot replies with a response
                /help - show help message
            ''')

        return app
    

    def run(self, token: str, **kwargs):
        self.bot.run(token, **kwargs)