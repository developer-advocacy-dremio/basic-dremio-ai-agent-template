from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.llms import OpenAI
from dremio_langchain_tool import DremioQueryTool 

# Initialize the tool
dremio_tool = DremioQueryTool(mode="software")  # Use "cloud" if connecting to Dremio Cloud

# Wrap the tool for LangChain
tools = [Tool(name=dremio_tool.name, func=dremio_tool.run, description=dremio_tool.description)]

# Initialize an OpenAI LLM
llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)

# Create the agent
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
