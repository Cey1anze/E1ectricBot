from revChatGPT.revChatGPT import Chatbot
from Basic_bot.Core import loadjson

GPTbot = loadjson.load_chatconfig()

config = {
    "email": GPTbot['email'],
    "password": GPTbot['password'],
}

if GPTbot['session_token']:
    config.update(session_token = GPTbot['session_token'])

chatbot = Chatbot(config, conversation_id=None)
chatbot.refresh_session()

def handle_response(prompt) -> str:
    response = chatbot.get_chat_response(prompt, output="text")
    responseMessage = response['message']

    return responseMessage
