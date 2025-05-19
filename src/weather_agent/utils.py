import os

from llama_index.llms.ollama import Ollama
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec


def get_default_ollama_model(temperature: float = 0.3, **options) -> Ollama:
    """Function to get the default ollama model"""
    return Ollama(
        model=os.getenv("OLLAMA_MODEL"),
        temperature=temperature,
        request_timeout=120.0,
        **options,
    )


def get_mcp_tool(url: str) -> McpToolSpec:
    """function to get the mcp tools from the url using sse client

    Args:
        url (str): url to the mcp server


    Returns:
        McpToolSpec: MCPToolSpec Object
    """

    mcp_client = BasicMCPClient(f"{url}/sse")
    mcp_tool = McpToolSpec(client=mcp_client)

    return mcp_tool
