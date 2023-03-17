import os

from revChatGPT.V1 import AsyncChatbot
from revChatGPT.V3 import Chatbot
from Core import loadjson
from cmds.chatGPT import personas
from typing import Union
from asgiref.sync import sync_to_async

config = loadjson.load_chatconfig()

OPENAI_EMAIL = config["OPENAI_EMAIL"]
OPENAI_PASSWORD = config["OPENAI_PASSWORD"]
SESSION_TOKEN = config["SESSION_TOKEN"]
OPENAI_API_KEY = config["openAI_key"]
ENGINE = config["OPENAI_ENGINE"]
CHAT_MODEL = config["CHAT_MODEL"]


def get_chatbot_model(model_name: str) -> Union[AsyncChatbot, Chatbot]:
    if model_name == "UNOFFICIAL":
        openai_email = OPENAI_EMAIL
        openai_password = OPENAI_PASSWORD
        session_token = SESSION_TOKEN
        return AsyncChatbot(config={"email": openai_email, "password": openai_password, "session_token": session_token,
                                    "model": ENGINE})
    elif model_name == "OFFICIAL":
        openai_api_key = OPENAI_API_KEY
        return Chatbot(api_key=openai_api_key, engine=ENGINE)


chatbot = get_chatbot_model(CHAT_MODEL)


async def official_handle_response(message) -> str:
    return await sync_to_async(chatbot.ask)(message)


async def unofficial_handle_response(message) -> str:
    async for response in chatbot.ask(message):
        responseMessage = response["message"]

    return responseMessage


# resets conversation and asks chatGPT the prompt for a persona
async def switch_persona(persona) -> None:
    CHAT_MODEL = os.getenv("CHAT_MODEL")
    if CHAT_MODEL == "UNOFFICIAL":
        chatbot.reset_chat()
        async for response in chatbot.ask(personas.PERSONAS.get(persona)):
            pass

    elif CHAT_MODEL == "OFFICIAL":
        chatbot.reset()
        await sync_to_async(chatbot.ask)(personas.PERSONAS.get(persona))
