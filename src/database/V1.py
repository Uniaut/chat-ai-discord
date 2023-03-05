'''
document example:
{
    'user_uuid': '1234567890',
    'auth': {
        'type': 'access_token',
        'value': {
            'access_token': '...'
        }
    },
    'conversation': {
        'last_conversation_id': '1234567890',
    }
}
'''
import pymongo

'''
Constant Configuration
'''
DATABASE_NAME = 'chatgpt-discord-V1'

def connect_to_database(server_url: str) -> pymongo.MongoClient:
    client = pymongo.MongoClient(server_url)
    return client


async def get_user_data(client: pymongo.MongoClient, user_uuid: str) -> dict:
    user_data = await client[DATABASE_NAME]['user'].find_one(
        {'user_uuid': user_uuid}
    )
    return user_data

async def set_user_data(client: pymongo.MongoClient, user_uuid: str, user_data: dict) -> None:
    await client[DATABASE_NAME]['user'].update_one(
        {'user_uuid': user_uuid},
        {'$set': user_data},
        upsert=True
    )

'''
auth getter/setter
'''
async def get_user_auth(client: pymongo.MongoClient, user_uuid: str) -> dict:
    return (await get_user_data(client, user_uuid))['auth']

async def set_user_auth(client: pymongo.MongoClient, user_uuid: str, user_auth: dict) -> None:
    await set_user_data(client, user_uuid, {
        'auth': user_auth
    })

'''
last conversation getter/setter
'''
async def get_last_conversation(client: pymongo.MongoClient, user_uuid: str) -> str:
    return (await get_user_data(client, user_uuid))['conversation']['last_conversation_id']

async def set_last_conversation(client: pymongo.MongoClient, user_uuid: str, conversation_id: str) -> None:
    await set_user_data(client, user_uuid, {
        'conversation': {
            'last_conversation_id': conversation_id
        }
    })
