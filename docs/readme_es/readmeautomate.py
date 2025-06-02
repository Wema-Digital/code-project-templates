
"""
###  Python Script to Automate README Generation

This script reads values from a CSV file and replaces placeholders in the markdown template.

#### **Python Script (`generate_readme.py`)**

"""

import csv

def generate_readme(template_file, csv_file, output_file):
    # Read the CSV file into a dictionary
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = {rows[0].strip(): rows[1].strip() for rows in reader}

    # Read the template file
    with open(template_file, mode='r', encoding='utf-8') as file:
        template_content = file.read()

    # Replace placeholders with actual values from the CSV
    for key, value in data.items():
        template_content = template_content.replace(f"{{{{{key}}}}}", value)

    # Write the final README file
    with open(output_file, mode='w', encoding='utf-8') as file:
        file.write(template_content)

    print(f"README file generated successfully: {output_file}")

# Define file paths

template_file = "readme_template_es.md"
csv_file = "data.csv"
output_file = "ES/readme.md"

# Run the script
if __name__ == "__main__":

    generate_readme(template_file, csv_file, output_file)
