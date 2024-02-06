import streamlit as st
from google.cloud import bigquery

# Set up BigQuery client
client = bigquery.Client(project='silver-origin-410908')

def execute_query(sql_query):
    query_job = client.query(sql_query)
    results = query_job.result()
    return results

# Streamlit App
def main():
    st.title("Gemini SQL Query Generator")

    # Get the user question interactively
    question = st.text_input("Enter your question:")

    if st.button("Generate and Execute"):
        # Import the generated query from gemini.py
        from gemini import generate

        # Generate SQL query based on user question
        generated_query = generate(question)

        # Execute the generated query on BigQuery
        results = execute_query(generated_query)

        # Display the results
        st.write("Generated SQL Query:")
        st.code(generated_query, language='sql')

        st.write("Query Results:")
        for row in results:
            st.write(row)

if __name__ == "__main__":
    main()
