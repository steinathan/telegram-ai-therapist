import os

from dotenv import load_dotenv
from app.db import chat_crud, user_crud
from app.exceptions import UpgradeRequiredException
from app.logging import logger

from typing_extensions import cast
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.chat_models.litellm import ChatLiteLLM
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, SystemMessage
from langchain_core.prompts import PromptTemplate

from app.db.models import Chat, User

load_dotenv()


prompt_instruction = """ 
You are Vikky, a therapist who specializes in treating patients with mental illness or assisting with their mental health.
Your approach to therapy is rooted in empathy, active listening, and evidence-based techniques. You prioritize creating a safe and nonjudgmental space where your clients feel heard and understood. you may recommend journaling, relaxation techniques, or self-help resources to support your clients' progress between appointments

Your ultimate goal is to improve their mental well-being, and lead fulfilling lives despite the challenges they may face."

You are speaking with {full_name}
"""


class CompletionChat:
    def __init__(self) -> None:
        self.chat_client = ChatLiteLLM(
            client=None,
            streaming=False,
            verbose=True,
            api_base=os.getenv("LITELLM_API_BASE", None),
            model=os.getenv("LITELLM_MODEL", "gpt-3.5-turbo"),
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        )

    def forward(self, message: str, user: User) -> str:
        self.user = user

        if not self.can_forward:
            raise UpgradeRequiredException("Can't forward, upgrade is required")

        self.__create_chat_message(user_id=self.user.id, message=message, role="human")

        response = self.chat_client(
            messages=self.__get_chat_messages(),
        )

        ai_message: str = cast(str, response.content)
        self.__create_chat_message(user_id=self.user.id, message=ai_message, role="ai")
        return ai_message

    @property
    def can_forward(self) -> bool:
        """Check if user can send a chat message"""
        all_msg = chat_crud.get_all(Chat.user_id == self.user.id)
        return len(all_msg) < 5 or self.user.is_premium

    # TODO: use ConversationBufferMemory
    # https://python.langchain.com/docs/modules/memory/types/buffer/
    def __create_chat_message(
        self, user_id: str | int, message: str, role: str
    ) -> None:
        chat_crud.create(Chat(role=role, text=message, user_id=int(user_id)))

    def __get_chat_messages(self) -> list[BaseMessage]:
        history: list[BaseMessage] = []

        user_chat_histories = chat_crud.get_all(Chat.user_id == self.user.id)

        for chat_history in user_chat_histories:
            if chat_history.role == "human":
                history.append(HumanMessage(content=chat_history.text))
            elif chat_history.role == "ai":
                history.append(AIMessage(content=chat_history.text))

        # ok, you caught me - my intention here is to only pick out the last 5 messages so as to reduce the chat messages to a manageable size
        # users can have 100's of messages
        # TODO: use a vectorDB and filter only by context
        if len(history) > 5:
            # add the systems prompt
            history = history[-5:]

        # always adding the system message as first instruction
        history.insert(
            0,
            SystemMessage(
                content=PromptTemplate.from_template(prompt_instruction).format(
                    full_name=self.user.full_name
                )
            ),
        )
        return history
