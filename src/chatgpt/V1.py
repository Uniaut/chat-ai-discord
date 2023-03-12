import functools

from revChatGPT.V1 import Chatbot


def ask(instance: Chatbot, prompt: str, conversation_id=None):
    for data in instance.ask(
        prompt=prompt,
        conversation_id=conversation_id,
    ):
        pass
    else:
        return data['message'], data['conversation_id']

@functools.lru_cache(maxsize=10)
def _get_chatbot_instance(user_auth: frozenset):
    config = dict(user_auth)
    return Chatbot(config=config)

def get_chatbot_instance(user_auth: dict):
    hashable_user_auth = frozenset(user_auth.items())
    return _get_chatbot_instance(hashable_user_auth)