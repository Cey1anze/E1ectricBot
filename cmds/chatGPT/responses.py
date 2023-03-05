from revChatGPT.V1 import AsyncChatbot
from revChatGPT.V3 import Chatbot
from Core import loadjson

config = loadjson.load_chatconfig()

OPENAI_EMAIL = config["OPENAI_EMAIL"]
OPENAI_PASSWORD = config["OPENAI_PASSWORD"]
SESSION_TOKEN = config["SESSION_TOKEN"]
OPENAI_API_KEY = config["openAI_key"]
ENGINE = config["OPENAI_ENGINE"]
CHAT_MODEL = config["CHAT_MODEL"]

if CHAT_MODEL == "UNOFFICIAL":
    unofficial_chatbot = AsyncChatbot(
        config={"email": OPENAI_EMAIL, "password": OPENAI_PASSWORD, "access_token": SESSION_TOKEN})
elif CHAT_MODEL == "OFFICIAL":
    offical_chatbot = Chatbot(api_key=OPENAI_API_KEY, engine=ENGINE)

responseMessage = ''


async def official_handle_response(message) -> str:
    global responseMessage
    responseMessage = offical_chatbot.ask(message)

    return responseMessage


async def unofficial_handle_response(message) -> str:
    global responseMessage
    async for response in unofficial_chatbot.ask(message):
        responseMessage = response["message"]

    return responseMessage
