import sys
from initialize_agent import agent

if __name__ == "__main__":
    # Example question for the agent
    question = sys.argv[1] if len(sys.argv) > 1 else "What is the average temperature in NYC?"

    # SQL query to fetch the required data
    query = """
    SELECT station, "name", "date", awnd, prcp, snow, snwd, tempmax, tempmin  FROM Samples."samples.dremio.com"."NYC-weather.csv";
    """

    # Combine the question and query for the agent
    response = agent.run(f"Run this query: {query} and answer the question: {question}")
    print(response)