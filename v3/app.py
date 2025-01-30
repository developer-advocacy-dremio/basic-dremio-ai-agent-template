from flask import Flask, render_template, request, jsonify
from agent import sql_agent

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        question = request.form.get("question", "").strip()

        if not query and not question:
            return jsonify({"error": "Please provide either a SQL query or a natural language question."})

        input_text = f"""
        Run the following query: {query}
        Using the Data Answer the following question: {question}
        """
        
        response = sql_agent.run(input_text)

        return jsonify({"response": response})

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
