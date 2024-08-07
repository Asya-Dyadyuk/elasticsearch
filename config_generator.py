def generate_date_config(date_columns):
    """
    Generates a string configuration for date columns in the format required.

    Args:
        date_columns: A dictionary where keys are column names and values are the first valid dates.

    Returns:
        A string formatted with date configurations.
    """
    config_lines = []
    for column, _ in date_columns.items():
        line = f'date {{\n match => ["{column}", "dd/MM/yyyy"]\n target => "{column}"\n }}'
        config_lines.append(line)
    return '\n'.join(config_lines)
