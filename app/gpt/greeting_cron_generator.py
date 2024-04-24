from typing import cast
from app.gpt.llm import chat_client
from langchain_core.prompts import PromptTemplate

cron_greeting_prompt = """
You are Vikky, a therapist who specializes in treating patients with mental illness or assisting with their mental health.

Your ultimate goal is to improve their mental well-being, and lead fulfilling lives despite the challenges they may face.

generate a motivating and capturing good {day_period} message for the user, the message must be brief, full with emojis, caring and polite, and give tips on how to maximize the {day_period}
"""


def generate_greeting_message(day_period: str) -> str:
    prompt = PromptTemplate(
        template=cron_greeting_prompt, input_variables=["day_period"]
    )
    response = chat_client.invoke(input=prompt.format(day_period=day_period))
    return cast(str, response.content).replace('"', "").strip()
