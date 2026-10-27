import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def main():
    model_client = OpenAIChatCompletionClient(
        model="gemini-3.1-flash-lite",
        api_key=os.environ["GEMINI_API_KEY"],
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        model_info={
            "vision": True,
            "function_calling": True,
            "json_output": True,
            "family": "unknown",
            "structured_output": True,
        },
    )

    try:
        agent = AssistantAgent(
            name="hr_assistant",
            model_client=model_client,
            system_message="You are an HR assistant.",
        )

        await Console(
            agent.run_stream(
                task=(
                    "Write a job description for a Junior Python Developer "
                    "in exactly five lines: one title followed by four short "
                    "sentences, each on its own line. Do not add extra text."
                )
            )
        )
    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())