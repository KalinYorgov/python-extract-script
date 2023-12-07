import os
import re
import zipfile

# Define the pattern to match <isscript> tags
isscript_pattern = r'(?s)<isscript.*?>(.*?)</isscript>'

# Function to extract .isml files from a zip file
def extract_isml_from_zip(zip_file_path, extraction_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)

# Function to extract <isscript> tags from .isml files
def extract_isscript_tags(directory, output_directory):
    isscript_files_data = {}
    files_processed = 0  # To keep track of how many files are processed
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith('pt_') and file.endswith('.isml'):
                files_processed += 1
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    contents = f.read()
                    isscripts = re.findall(isscript_pattern, contents, re.IGNORECASE)
                    if isscripts:
                        base_file_name = os.path.basename(file_path)
                        isscript_file_name = base_file_name.replace('.isml', '_isscripts.txt')
                        isscript_file_path = os.path.join(output_directory, isscript_file_name)
                        with open(isscript_file_path, 'w', encoding='utf-8') as nf:
                            for isscript in isscripts:
                                nf.write(f"// <isscript> from {base_file_name}\\n{isscript}\\n\\n")
                        isscript_files_data[isscript_file_path] = len(isscripts)
    print(f"Total .isml files processed: {files_processed}")
    return isscript_files_data, files_processed

# Function to create a log file with the summary of the extraction process
def create_extraction_log(files_processed, isscript_files_data, log_directory):
    # Base name for the log file
    base_log_name = 'extraction_log'
    log_extension = '.txt'

    # Find the highest existing log number
    existing_logs = [f for f in os.listdir(log_directory) if f.startswith(base_log_name) and f.endswith(log_extension)]
    highest_num = 0
    for log in existing_logs:
        num_part = log[len(base_log_name):-len(log_extension)]
        if num_part.isdigit():
            highest_num = max(highest_num, int(num_part))

    # Define the new log file name with incremented number
    new_log_num = highest_num + 1
    new_log_file = f"{base_log_name}{new_log_num}{log_extension}"
    new_log_path = os.path.join(log_directory, new_log_file)

    # Create the new log file
    total_files_with_scripts = len(isscript_files_data)
    total_script_tags = sum(isscript_files_data.values())

    with open(new_log_path, 'w', encoding='utf-8') as log_file:
        log_file.write(f"Total number of 'pt_' .isml files processed: {files_processed}\n")
        log_file.write(f"Total number of 'pt_' .isml files with isscript tags: {total_files_with_scripts}\n")
        log_file.write(f"Total number of isscript tags found: {total_script_tags}\n\n")

        for file_path, count in isscript_files_data.items():
            file_name = os.path.basename(file_path)
            log_file.write(f"{file_name}: {count} isscript tag(s) found\n")

    return new_log_path

# Define the paths
zip_file_path = 'path\\extracted_files\\templates.zip'  # Path to the zip file containing .isml files
extraction_path = 'path\\extracted_files\\extracted_templates'  # Where to extract .isml files from the zip
output_directory = 'path\\extracted_files\\extracted_scripts'  # Where to save extracted <isscript> scripts
log_file_path = 'path\\extracted_files\\log_files' # Where to save the log file

# Extracting .isml files from zip
extract_isml_from_zip(zip_file_path, extraction_path)

# Extracting <isscript> tags
isscript_files_data, files_processed = extract_isscript_tags(extraction_path, output_directory)

# Creating a log file
create_extraction_log(files_processed, isscript_files_data, log_file_path)
