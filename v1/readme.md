## Dremio Basic AI Agent Template V1

This is a template for a basic AI agent that can be used to interact with Dremio.

## The Flow of the Code

- `env.py` - loads the environment variables
- `dremio_connect.py` - function to connect to Dremio
- `dremio_langcain_tool.py` - function to interact with Dremio and return string with results for AI agent
- `initialize_agent.py` - initializes the agent
- `run.py` - runs the agent (this should be the only file you have to edit)

## How to Ask a Question

To do two things:

- In run.py edit the SQL query for the data from which you want to ask a question, make it as a narrow as possible to avoid hitting 90,000 token limit.

- Then run the script with your question for example:

```bash
python run.py "What is the average age of the people in the dataset?"
```

## More Details on How Each File Works

- [truncate.py](./docs/truncate.md) *this function isn't used anywhere currently*
- [env.py](./docs/env.md)
- [dremio_connect.py](./docs/dremio_connect.md)
- [dremio_langchain_tool.py](./docs/dremio_langchain_tool.md)
- [initialize_agent.py](./docs/initialize_agent.md)
- [run.py](./docs/run.md)
