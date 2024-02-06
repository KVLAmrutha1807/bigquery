import os
import google.generativeai as genai

os.environ['GOOGLE_API_KEY'] = "AIzaSyAHaL4BHo_77l17oDcNjvlGJEIZgjsjSyE"  # Replace with your API key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Set up the model
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)
import json 
def load_schema_from_file(file_path):     
    with open(file_path, 'r') as file:         
        return json.load(file) # Load schema from fileschema = load_schema_from_file('schema.json')

def generate(question):
    # prompt_parts_1 = [
    #     """You are an expert in converting English questions to SQL code!
    #     The SQL database is in the format silver-origin-410908.movies.awards, where silver-origin-410908 refers to the project and movies refers to the SQL database and awards refers to table. The table has the following columns with datatypes:
    #     Award(STRING), Category(STRING), Nominee(STRING), Result(STRING)\n\n
    #     Always give silver-origin-410908.movies.awards as a table name in the generated query.
    #     If you are using alias name for table, then use it for every column name. 
    #     strictly dont use INTERSECT in the generated query. use alternte approach
    #     Strictly don't use joins in the generated query.
    #     Always use double quotes for dtrings. For example, "string".
    #     Avoid using the DISTINCT keyword, INTERSECT and UNION , and prefer the IN clause for better query efficiency.
    #     Strictly Don't use DISTINCT key word in the generated query. Use alternative approach in such cases
    #     For example,\nExample 1 - List the winners of the Academy Award for Best Picture in 1972\n``` SELECT Nominee FROM silver-origin-410908.movies.awards WHERE Award = 'Academy Awards, 1972' AND Category = 'Best Picture' AND Result = 'Won';\n```\n\n
    #     Example 2 - List the nominees and results for the BAFTA Award for Best Film in 1972\n```\nSELECT Nominee, Result FROM silver-origin-410908.movies.awards WHERE Award = 'BAFTA, 1972' AND Category = 'Best Film';\n```\n\n
    #     Example 3 - List the winners of the Golden Globe Award for Best Director in 1972\n```\nSELECT Nominee FROM silver-origin-410908.movies.awards WHERE Award = 'Golden Globe Awards, 1972' AND Category = 'Best Director' AND Result = 'Won';\n```\n\n
    #     Example 4 - List the nominees and results for the New York Film Critics Circle Award for Best Film in 1971\n SELECT Nominee, Result FROM silver-origin-410908.movies.awards WHERE Award = 'New York Film Critics Circle, 1971' AND Category = 'Best Film';
    #     Example 5 - Count the number of awards won by Gene Hackman\n```\nSELECT COUNT(*) FROM silver-origin-410908.movies.awards WHERE Nominee = 'Gene Hackman' AND Result = 'Won';\n```\n\nStrictly don't include ``` and \\n and SQL keywords in the beginning in the output. Just return only SQL query from SELECT to the end of the query and neglect the semicolon (;).
    #     Example 6 - find nominees that were nominated for both the Academy Award, 1972 and the BAFTA, 1972\n SELECT DISTINCT Nominee FROM silver-origin-410908.movies.awards WHERE (Award = 'Academy Awards, 1972' OR Award = 'BAFTA, 1972') AND Result = 'Nominated';
    #     Always generate the same working query for every time the same question is asked.
    #     If you give anything extra other than what is required, you will be punished.
    #    """,
    # ]
 
    file_path="project_schema.json"
    schema = load_schema_from_file(file_path)

    prompt_parts_1 = [
        f"""You are an expert in converting English questions to SQL code! The SQL database follows a standard format, 
        where the project, dataset, and table names can vary. The project name is silver-origin-410908. The JSON file '{schema}' provided contains the schema information for the database, 
        including the project ID, dataset ID, and table names along with their respective columns and data types. Always use double quotes 
        for strings in the generated SQL queries. Avoid using the DISTINCT keyword, INTERSECT, and UNION, preferring the IN clause for better 
        query efficiency. Strictly avoid using joins in the generated query. If an alias name is used for the table, ensure to use it for every column name. 
        Queries should be structured in the format 'projectname.datasetname.tablename', you can dynamically generate queries based on the schema provided. 
        For example, if the table name is "projectname.datasetname.tablename," ensure that the generated query follows this format.
        Always generate the same working query for every time the same question is asked. Any additional information beyond the required SQL query will be disregarded. 
        nStrictly don't include ``` and \\n and SQL keywords in the beginning in the output. Just return only SQL query from SELECT to the end of the query and neglect the semicolon (;).
        strictly Dont generate queries in capital letters, else you will be punished. Just use the names whatever it is there in {schema}. 
        always give column names, project name, dataset name, and table name in small letters.
        please structure the query neatly and give working sql queries.
        For example,\nExample 1 - List the winners of the Academy Award for Best Picture in 1972\n``` SELECT Nominee FROM silver-origin-410908.movies.awards WHERE Award = 'Academy Awards, 1972' AND Category = 'Best Picture' AND Result = 'Won';\n```\n\n
        Example 2 - List the nominees and results for the BAFTA Award for Best Film in 1972\n```\nSELECT Nominee, Result FROM silver-origin-410908.movies.awards WHERE Award = 'BAFTA, 1972' AND Category = 'Best Film';\n```\n\n
        Example 3 - List the winners of the Golden Globe Award for Best Director in 1972\n```\nSELECT Nominee FROM silver-origin-410908.movies.awards WHERE Award = 'Golden Globe Awards, 1972' AND Category = 'Best Director' AND Result = 'Won';\n```\n\n
        Example 4 - List the nominees and results for the New York Film Critics Circle Award for Best Film in 1971\n SELECT Nominee, Result FROM silver-origin-410908.movies.awards WHERE Award = 'New York Film Critics Circle, 1971' AND Category = 'Best Film';
        Example 5 - Count the number of awards won by Gene Hackman\n```\nSELECT COUNT(*) FROM silver-origin-410908.movies.awards WHERE Nominee = 'Gene Hackman' AND Result = 'Won';\n```\n\nStrictly don't include ``` and \\n and SQL keywords in the beginning in the output. Just return only SQL query from SELECT to the end of the query and neglect the semicolon (;).
        Example 6 - find nominees that were nominated for both the Academy Award, 1972 and the BAFTA, 1972\n SELECT DISTINCT Nominee FROM silver-origin-410908.movies.awards WHERE (Award = 'Academy Awards, 1972' OR Award = 'BAFTA, 1972') AND Result = 'Nominated';
        """
    ]

 

    prompt_parts = [prompt_parts_1[0], question]
    response = model.generate_content(prompt_parts)
    generated_query = response.text.strip()
    
    # Save the generated query to a file
    with open("generated_query.sql", "w") as file:
        file.write(generated_query)
    
    return generated_query
