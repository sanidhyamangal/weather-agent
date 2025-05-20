import asyncio
import os
from logging import getLogger

import streamlit as st
from dotenv import load_dotenv
from llama_index.core.agent.workflow import FunctionAgent, ToolCall, ToolCallResult
from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.tools.mcp import McpToolSpec

from weather_agent.utils import get_default_ollama_model, get_mcp_tool

load_dotenv()

logger = getLogger(__name__)

SYSTEM_PROMPT = """
You are an AI agent which interacts with tool calling.

Before you can interact with the User, you need to work with tools that calls NWS APIs.
"""


async def get_agent(tool: McpToolSpec, llm: FunctionCallingLLM):
    tools = await tool.to_tool_list_async()
    agent = FunctionAgent(
        name="Weather Agent", tools=tools, llm=llm, system_prompt=SYSTEM_PROMPT
    )

    return agent


async def handle_user_input(
    agent: FunctionAgent,
    user_input: str,
    chat_history: list[dict[str, str]] | None = None,
):
    handler = agent.run(user_input, chat_history=chat_history)

    async for event in handler.stream_events():
        if isinstance(event, ToolCall):
            logger.info(f"Tool call: {event.tool_name} with args: {event.tool_kwargs}")
        elif isinstance(event, ToolCallResult):
            logger.info(
                f"Tool call result: {event.tool_name} with result: {event.tool_output}"
            )

    response = await handler
    return str(response)


async def main():
    llm = get_default_ollama_model()

    # extract the url from the env variable
    mcp_tool = get_mcp_tool(os.getenv("WEATHER_MCP_SERVER_URL"))

    st.set_page_config(
        page_title="Weather Agent",
        page_icon="🌤️",
        layout="centered",
        initial_sidebar_state="auto",
    )

    st.title("Weather Agent")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! I am a weather agent. How can I help you today?",
            }
        ]

    agent = await get_agent(mcp_tool, llm)

    if prompt := st.chat_input("Ask me anything about weather!"):
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking...."):
                response = await handle_user_input(
                    agent, st.session_state.messages[-1]["content"]
                )
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)


if __name__ == "__main__":
    asyncio.run(main())
