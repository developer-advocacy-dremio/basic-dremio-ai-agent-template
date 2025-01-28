## Dremio Basic AI Agent Template

This is a template for a basic AI agent that can be used to interact with Dremio.

## Getting Started

- Clone the repository

- Create a python virtual environment and install dependencies
    - `python -m venv venv`
    - `source venv/bin/activate`
    - `pip install -r requirements.txt`

- rename `example.env` to `.env` and fill in the values

## The Flow of the Code

- `env.py` - loads the environment variables
- `dremio_connect.py` - function to connect to Dremio
- `dremio_langcain_tool.py` - function to interact with Dremio and return string with results for AI agent
- `initialize_agent.py` - initializes the agent
- `run.py` - runs the agent (this should be the only file you have to edit)