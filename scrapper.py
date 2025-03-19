import os
import json
import re

# Define the path to the data folder
data_folder = r"c:\Users\ancie\Desktop\HTML\prac\python_practice\data"

def clean_text(value):
    """
    Recursively clean text fields in the JSON data by removing <DT_..._...> patterns.
    """
    if isinstance(value, str):
        # Remove patterns like <DT_..._...>
        return re.sub(r"<DT_[^>]+>", "", value)
    elif isinstance(value, list):
        # Recursively clean each item in the list
        return [clean_text(item) for item in value]
    elif isinstance(value, dict):
        # Recursively clean each value in the dictionary
        return {key: clean_text(val) for key, val in value.items()}
    return value  # Return the value as is if it's not a string, list, or dict

# Iterate through all files in the data folder
for filename in os.listdir(data_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(data_folder, filename)
        
        # Open and load the JSON file
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {filename}")
                continue
        
        # Clean the data by removing <DT_..._...> patterns
        cleaned_data = clean_text(data)
        
        # Save the cleaned JSON back to the file
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(cleaned_data, file, indent=4)
        
        print(f"Processed file: {filename}")