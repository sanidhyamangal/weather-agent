import asyncio
import os

from dotenv import load_dotenv
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.ollama import Ollama
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec

load_dotenv()

llm = Ollama(model=os.getenv("OLLAMA_MODEL"), temperature=0.3, request_timeout=120.0)

mcp_client = BasicMCPClient("http://127.0.0.1:8000/sse")
mcp_tool = McpToolSpec(client=mcp_client)

SYSTEM_PROMPT = """
You are an AI agent which interacts with tool calling.

Before you can interact with the User, you need to work with tools that calls NWS APIs.
"""


async def get_agent(mcp_tool: McpToolSpec, llm: Ollama) -> FunctionAgent:
    tools = await mcp_tool.to_tool_list_async()
    agent = FunctionAgent(
        name="Agent to Handle News Forecast",
        description="An agent which interacts with weather NWS api to get forecasts and alerts",
        tools=tools,
        llm=llm,
        system_prompt=SYSTEM_PROMPT,
    )

    return agent


async def main():
    agent: FunctionAgent = await get_agent(mcp_tool, llm)

    response = await agent.run("What is Weather forecast for Nashville,TN?")

    print(response)


asyncio.run(main=main())
