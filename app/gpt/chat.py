from app.logging import logger
from typing_extensions import cast
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.chat_models.litellm import ChatLiteLLM
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, SystemMessage
from langchain_core.prompts import PromptTemplate

from app.models import User

chat_llm = ChatLiteLLM(
    client=None,
    streaming=False,
    verbose=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)

prompt_instruction = """ 
You are Vikky, a therapist who specializes in treating patients with mental illness or assisting with their mental health.
Your approach to therapy is rooted in empathy, active listening, and evidence-based techniques. You prioritize creating a safe and nonjudgmental space where your clients feel heard and understood. you may recommend journaling, relaxation techniques, or self-help resources to support your clients' progress between appointments

Your ultimate goal is to improve their mental well-being, and lead fulfilling lives despite the challenges they may face."

You are speaking with {full_name}
"""

# TODO: get from DB
chat_history: dict[str, list[BaseMessage]] = {}


class CompletionChat:
    def forward(self, message: str, user: User) -> str:
        self.user = user

        if chat_history.get(str(user.id)) is None:
            logger.info(f"creating new chat DB for {user.full_name}")
            chat_history[str(user.id)] = [
                SystemMessage(
                    content=PromptTemplate.from_template(prompt_instruction).format(
                        full_name=user.full_name
                    )
                ),
            ]

        self.__append_chat_history(user_id=self.user.id, message=message, role="human")

        response = chat_llm(
            messages=self.__get_chat_history_by_id(self.user.id),
        )

        ai_message: str = cast(str, response.content)
        self.__append_chat_history(user_id=self.user.id, message=ai_message, role="ai")
        return ai_message

    # TODO: use ConversationBufferMemory
    # https://python.langchain.com/docs/modules/memory/types/buffer/
    def __append_chat_history(
        self, user_id: str | int, message: str, role: str
    ) -> None:
        chat_history[str(self.user.id)].append(
            HumanMessage(content=message)
            if role == "human"
            else AIMessage(content=message)
        )

    def __get_chat_history_by_id(self, user_id: str | int) -> list[BaseMessage]:
        return chat_history[str(user_id)]
