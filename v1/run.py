import sys
from initialize_agent import agent
from truncate import truncate_string

if __name__ == "__main__":
    # Example question for the agent
    question = sys.argv[1] if len(sys.argv) > 1 else "What is the average temperature in NYC?"

    # SQL query to fetch the required data
    query = """
    SELECT station, "name", "date", awnd, prcp, snow, snwd, tempmax, tempmin  FROM Samples."samples.dremio.com"."NYC-weather.csv" LIMIT 3000;
    """

    # Combine the question and query for the agent
    response = agent.run(f"Answer the question: {question} with this Data: {query}")
    print(response)