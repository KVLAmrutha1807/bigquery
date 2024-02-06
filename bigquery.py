from google.cloud import bigquery

# Set up BigQuery client
client = bigquery.Client(project='silver-origin-410908')

def execute_query(sql_query):
    query_job = client.query(sql_query)
    results = query_job.result()
    return results

if __name__ == "__main__":
    while True:
        # Get the user question interactively
        question = input("Enter your question (type 'exit' to end): ")

        if question.lower() == 'exit':
            break

        # Import the generated query from gemini.py
        from gemini import generate

        # Generate SQL query based on user question
        generated_query = generate(question)

        # Execute the generated query on BigQuery
        results = execute_query(generated_query)

        # Print the results
        print("Query Results:")
        for row in results:
            print(row)
