import functools

from revChatGPT.V1 import Chatbot


async def ask(instance, prompt, conversation_id):
    for data in instance.ask(
        prompt=prompt,
        conversation_id=conversation_id,
    ):
        pass

    return data['message'], data['conversation_id']


@functools.cache
def _get_instance(user_auth: frozenset):
    config = dict(user_auth)
    return Chatbot(config=config)

def get_instance(user_auth: dict):
    return _get_instance(frozenset(user_auth.items()))