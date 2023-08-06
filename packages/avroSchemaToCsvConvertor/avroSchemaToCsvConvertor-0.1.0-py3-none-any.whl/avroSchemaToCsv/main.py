import avro.schema
import avro.io
import csv
import json
import os, sys
import argparse

def avscToCsv(file) -> None:
    """
    Converts an Avro schema file to a CSV file.
    """
    # Read the schema file.
    with open(file, 'r') as f:
        schema = avro.schema.Parse(f.read())

    # Create a CSV file.
    csv_file = file.replace('.avsc', '.csv')
    csv_file = csv_file.replace('avro/', 'csv/')

    # Check if the CSV file exists, if it does, delete it.
    if os.path.isfile(csv_file):
        print('CSV file already exists, hence deleting it')
        os.remove(csv_file)

    # Open the CSV file.
    csv_file = open(csv_file, 'w')

    # Create a CSV writer.
    writer = csv.writer(csv_file)

    # Write the header.
    writer.writerow(['name', 'type', 'doc'])

    # Write the fields.
    for field in schema.fields:
        writer.writerow([field.name, field.type, field.doc])

    # Print the JSON schema.
    print(json.dumps(schema.to_json(), indent=2))

def main():
    """
    Main function.
    """
    # Parse the command line arguments.
    parser = argparse.ArgumentParser(description='Convert Avro schema to CSV.')
    parser.add_argument('--file', help='Avro schema file.')
    args = parser.parse_args()

    file = args.file
    
    # Check if the file exists.
    if not os.path.isfile(file):
        print('File does not exist: {}'.format(file))
        sys.exit(1)

    # Convert the Avro schema file to a CSV file.
    avscToCsv(file)

if __name__ == '__main__':
    main()
