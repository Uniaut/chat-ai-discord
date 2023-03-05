auth = {}

async def get_user_auth(user_uuid):
    if user_uuid in auth:
        return auth[user_uuid]
    else:
        raise Exception('no auth data')

async def set_user_auth(user_uuid, user_auth):
    auth[user_uuid] = user_auth