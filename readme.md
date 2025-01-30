## Dremio Basic AI Agent Templates

## Getting Started

- Clone the repository

- Create a python virtual environment and install dependencies
    - `python -m venv venv`
    - `source venv/bin/activate`
    - `pip install -r requirements.txt`

- rename `example.env` to `.env` and fill in the values (in the v1 or v2 folder)

**OPENAI API Keys are received from https://platform.openai.com/account/api-keys**

- [Dremio Agent V1](./v1/readme.md)
- [Dremio Agent V2](./v2/readme.md) 
- [Dremio Agent V3](./v3/readme.md)

| **Component**         | **V1**                  | **V2**             | **V3** |
|----------------------|--------------------------------|--------------------------------|-------|
| **Dremio Connection** | `DremioQueryTool` via Arrow Flight | SQLAlchemy via `sqlalchemy_dremio` | |
| **Query Execution**   | `_run(query: str) → Pandas DataFrame` | `sql_agent.run(natural_language_query)` | |
| **Query Generation**  | Manually crafted queries | AI-generated SQL queries | |
| **LLM Integration**   | OpenAI LLM with manual queries | OpenAI LLM auto-generating SQL | |
| **Web UI** | NO | NO | YES |
