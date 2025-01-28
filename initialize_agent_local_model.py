from langchain.agents import initialize_agent, Tool, AgentType
from langchain.llms import HuggingFacePipeline
from transformers import pipeline
from dremio_langchain_tool import DremioQueryTool

# Step 1: Initialize the Dremio Tool
dremio_tool = DremioQueryTool(mode="software")  # Use "cloud" if connecting to Dremio Cloud

# Wrap the tool for LangChain
tools = [Tool(name=dremio_tool.name, func=dremio_tool.run, description=dremio_tool.description)]

# Step 2: Load a Local Model using Hugging Face Transformers
model_name = "gpt2"  # Replace with a better local model (e.g., EleutherAI/gpt-neo-125M or LLaMA)
local_pipeline = pipeline("text-generation", model=model_name, device=0)  # device=0 for GPU support

# Wrap the local model in a LangChain LLM
llm = HuggingFacePipeline(pipeline=local_pipeline)

# Step 3: Create the Agent
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)