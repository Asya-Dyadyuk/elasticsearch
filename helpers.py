import pandas as pd
from config_generator import generate_date_config
from utils import find_numeric_columns, find_date_columns


def process_files(csv_file, output_file):
    """
    Updates the configuration file with columns, numeric types, and date formats from the CSV file.

    Args:
        csv_file (str): Path to the CSV file containing data.
        output_file (str): Path to the output configuration file.
    """
    try:
        # Read CSV file into DataFrame
        df = pd.read_csv(csv_file)
        columns = list(df.columns)

        # Prepare input section
        input_section = (
            'input {\n'
            '    file {\n'
            '        path => "/root/data/Clickup_Tasks.csv"\n'
            '        start_position => beginning\n'
            '        ignore_older => 86400000\n'
            '    }\n'
            '}\n'
        )

        # Convert column names to string format for the configuration
        columns_str = '["' + '", "'.join(columns) + '"]'
        filter_section = (
            'filter {\n'
            '    csv {\n'
            '        separator => ","\n'
            '        skip_header => "true"\n'
            '        columns => %s\n'  
            '        convert => {\n'
        ) % (columns_str)

        # Determine numeric columns and their types
        numeric_columns = find_numeric_columns(df)
        convert_section = '\n'.join([f''
                                     f'"{column}" => "{data_type}"' for column, data_type in numeric_columns.items()])
        filter_section += convert_section + '\n'

        # Determine date columns and their formats
        date_dict = find_date_columns(df)
        date_section = generate_date_config(date_dict)
        filter_section += date_section + '\n}\n'

        # Prepare output section
        output_section = (
            'output {\n'
            '    elasticsearch {\n'
            '        hosts => "127.0.0.1:9200"\n'
            '        index => "clickup_tasks"\n'
            '        document_id => %s\n'
            '        action => "update"\n'
            '        doc_as_upsert => true\n'
            '    }\n'
            '    stdout { codec => rubydebug }\n'
            '}\n'
        ) % (df.values[1][2])

        # Combine all sections into new content
        new_content = input_section + filter_section + output_section

        # Write the new content to the output file
        with open(output_file, 'w') as f:
            f.write(new_content)

    except (FileNotFoundError, PermissionError) as e:
        print("Error: File not found or permission denied")
