import os

from dotenv import load_dotenv
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.chat_models.litellm import ChatLiteLLM
from openai import OpenAI

load_dotenv()

openai_client = OpenAI()
chat_client = ChatLiteLLM(
    client=openai_client,
    streaming=False,
    verbose=True,
    api_base=os.getenv("LITELLM_API_BASE", None),
    model=os.getenv("LITELLM_MODEL", "gpt-3.5-turbo"),
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)
