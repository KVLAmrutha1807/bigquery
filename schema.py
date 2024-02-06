from google.cloud import bigquery
import json

# # def get_table_schema(project_id, dataset_id, table_id):
# #     # Create a BigQuery client
# #     client = bigquery.Client(project=project_id)

# #     # Construct the table reference
# #     table_ref = client.dataset(dataset_id).table(table_id)

# #     # Get the table information
# #     table = client.get_table(table_ref)

# #     # Get the schema of the table
# #     schema = table.schema

# #     return schema

# # def write_schema_to_json(schema, output_file):
# #     # Convert schema to JSON-compatible dictionary
# #     schema_dict = [{'name': field.name, 'type': field.field_type} for field in schema]

# #     # Write schema to JSON file
# #     with open(output_file, 'w') as json_file:
# #         json.dump(schema_dict, json_file, indent=4)

# # # Example usage
# # project_id = "silver-origin-410908"
# # dataset_id = "employees"
# # table_id = "countries"

# # schema = get_table_schema(project_id, dataset_id, table_id)
# # output_file = "schema.json"
# # write_schema_to_json(schema, output_file)
# # print(f"Schema has been written to {output_file}")
# from google.cloud import bigquery
# import json

# def get_project_schema(project_id, dataset_id):
#     # Create a BigQuery client
#     client = bigquery.Client(project=project_id)

#     # List all tables in the dataset
#     dataset_ref = client.dataset(dataset_id)
#     tables = client.list_tables(dataset_ref)

#     project_schema = {}

#     # Iterate over each table and retrieve its schema
#     for table in tables:
#         table_ref = dataset_ref.table(table.table_id)
#         table_schema = client.get_table(table_ref).schema
#         project_schema[table.table_id] = [{'name': field.name, 'type': field.field_type} for field in table_schema]

#     return project_schema

# def write_schema_to_json(schema, output_file):
#     # Write schema to JSON file
#     with open(output_file, 'w') as json_file:
#         json.dump(schema, json_file, indent=4)

# # Example usage
# project_id = "silver-origin-410908"
# dataset_id = "employees"
# output_file = "project_schema.json"

# project_schema = get_project_schema(project_id, dataset_id)
# write_schema_to_json(project_schema, output_file)
# print(f"Schema for the entire project has been written to {output_file}")
from google.cloud import bigquery
import json

def get_project_schema(project_id):
    # Create a BigQuery client
    client = bigquery.Client(project=project_id)

    # List all datasets in the project
    datasets = client.list_datasets()

    project_schema = {}

    # Iterate over each dataset and retrieve its tables and schema
    for dataset in datasets:
        dataset_id = dataset.dataset_id
        dataset_ref = client.dataset(dataset_id)
        tables = client.list_tables(dataset_ref)
        dataset_schema = {}

        # Retrieve schema for each table in the dataset
        for table in tables:
            table_ref = dataset_ref.table(table.table_id)
            table_schema = client.get_table(table_ref).schema
            dataset_schema[table.table_id] = [{'name': field.name, 'type': field.field_type} for field in table_schema]

        # Store dataset schema in project schema
        project_schema[dataset_id] = dataset_schema

    return project_schema

def write_schema_to_json(schema, output_file):
    # Write schema to JSON file
    with open(output_file, 'w') as json_file:
        json.dump(schema, json_file, indent=4)

# Example usage
project_id = "silver-origin-410908"
output_file = "project_schema.json"

project_schema = get_project_schema(project_id)
write_schema_to_json(project_schema, output_file)
print(f"Schema for the entire project has been written to {output_file}")
