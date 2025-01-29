## Dremio Basic AI Agent Template V2

This is a template for a basic AI agent that can be used with Dremio, unlike V1, V2 can indepently explore the list of tables and their schemas in an effort to answer the question prompt.

## The Flow of the Code

- `env.py` - loads the environment variables
- `DremioSQLDatabase.py` - a custom langchain Subclass the behaves like a Dremio SQLAlchemy Dialect but assembles parameterized queries client side to work with langchain.
- `connection.py` - establishes connection to dremio and builds out llm setup
- `agent.py` - initializes the agent
- `run.py` - defines initial prompt and receives question from command line input.

## How to Ask a Question

To do two things:

- Then run the script with your question for example:

```bash
python run.py "What is the average age of the people in the dataset?"
```

## More Details on How Each File Works

- [DremioSQLDatabase.py](./docs/DremioSQLDatabase.md)
- [connection.py](./docs/connection.md)
- [agent.py](./docs/agent.md)
- [run.py](./docs/run.md)
