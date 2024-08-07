from helpers import process_files

# Define file paths
csv_file = "./data/Clickup_Tasks.csv"
output_file = "./data/ClickUp_Tasks.conf"

# Update the configuration file
process_files(csv_file, output_file)
