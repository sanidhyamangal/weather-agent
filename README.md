# weather-agent
An AI agent to interact with NWS MCP server to get weather forecasts and alerts for a given location.
Author: Sanidhya Mangal

## Implementation Approach
Entire project works on two core principles.
- **MCP**: Developed a model context protocol server to wrap up all the function call and API call to NWS server to ensure agent can communicate with MCP layer rather than calling different functions.
- **Agent**: Developed an autonomus `FunctionalAgent` to interact with MCP server and get responses for the given workflow.

### Project Structure
```sh
.
├── app.py
├── dist
│   ├── weather_agent-0.1.0-py3-none-any.whl
│   └── weather_agent-0.1.0.tar.gz
├── pyproject.toml
├── README.md
├── src
│   ├── weather_agent
│   │   ├── __init__.py
│   │   ├── scripts
│   │   │   └── test_scripts.py
│   │   ├── utils.py
│   │   └── weather_mcp_server
│   │       ├── __init__.py
│   │       ├── utils.py
│   │       └── weather.py
│   └── weather_agent.egg-info
│       ├── dependency_links.txt
│       ├── PKG-INFO
│       ├── requires.txt
│       ├── SOURCES.txt
│       └── top_level.txt
└── uv.lock
```

## Setup and Running Instructions

### Environment Setup
- Requires Python 3.10 or later.
- Uses `uv` for dependency management. Install `uv` as per the instructions [here](https://docs.astral.sh/uv/) and run:
  `uv sync`

#### Environment Variables
You can refer to `.env.template` to setup `.env` file for configuring environ variable or can simple set them using `export` command

### Model and API Setup
- The chatbot uses Ollama to run LLM models. Download and install it from [Ollama](https://ollama.com).
- Download the [`mistral:7b`](https://ollama.com/library/mistral) model with:
  `ollama pull mistral:7b`

### Running MCP Server
To start MCP server you can run following command:
```sh
uv run weather-mcp-server
```

This command will main function within, `weather.py` to start MCP server. 
>Entrypoint and command name could be modified within `pyproject.toml`

### Running UI
To start UI please run following command:
```sh
uv run streamlit app.py
```
> If UI window doesn't open automaticall please feel free to navigate to URL mentioned in console.