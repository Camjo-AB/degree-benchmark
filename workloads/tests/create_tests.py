import fileinput
import os
import re

def create_files(file_names, content_template, config):
    for dir_file, param in zip(file_names, config):
        filename = f"{dir_file[1]}.yaml"
        file_path = os.path.join(dir_file[0], filename)
        content = content_template.format(**param)
        with open(file_path, 'w') as file:
            file.write(content)  # Write the content to the file

def interpret_lines(lines):
    results = []

    for line in lines:
        # Initialize default values for variables
        rate = size = topic = partition = producers = consumers = payload = None
        duration = 5

        # Find and interpret the 'rate' (interpreting 'K' as thousands)
        rate_match = re.search(r'(\d+)(K?)-rate', line[1])
        if rate_match:
            rate_value, is_k = rate_match.groups()
            rate = int(rate_value) * 1000 if is_k else int(rate_value)

        # Find and interpret the 'size' (interpreting 'K' as 1024, 'B' as bytes)
        size_match = re.search(r'(\d+)(K?B)-size', line[1])
        if size_match:
            size_value, is_k = size_match.groups()
            if int(size_value)==5:
                size_value = 1.5
                size = int(size_value * 1024)
                payload = str(size_value) + 'kB' if is_k == 'KB' else str(int(size_value)) + 'B'
            else:
                size = int(size_value) * 1024 if is_k == 'KB' else int(size_value)
                payload = str(size_value)+'kB' if is_k == 'KB' else str(int(size_value))+'B'

        # Find and interpret the 'topic'
        topic_match = re.search(r'(\d+)-topic', line[1])
        if topic_match:
            topic = int(topic_match.group(1))

        # Find and interpret the 'partition'
        partition_match = re.search(r'(\d+)-partitions', line[1])
        if partition_match:
            partition = int(partition_match.group(1))

        # Find and interpret the 'producers' (denoted by 'p')
        producers_match = re.search(r'(\d+)p', line[1])
        if producers_match:
            producers = int(producers_match.group(1))

        # Find and interpret the 'consumers' (denoted by 'c')
        consumers_match = re.search(r'(\d+)c', line[1])
        if consumers_match:
            consumers = int(consumers_match.group(1))

        # Compile results
        result = {
            'rate': rate,
            'size': size,
            'payload': payload,
            'topic': topic,
            'partition': partition,
            'producers': producers,
            'consumers': consumers,
            'duration': duration
        }
        results.append(result)

    return results


def generate_markdown_table():
    lines = fileinput.input(['tests.txt'])
    # Assuming each line is a new column in the table
    header = "| Tests | Status | # Pods in Cluster | Comments |"
    separator = "| :---: | :---: | :---: | :---: |"
    rows = [header, separator]

    # Generating rows with each test in its own row
    for line in lines:
        # Clean the line and prepare it for a single column table
        clean_line = line.strip()
        row = f"| {clean_line} |  |  |  |"
        rows.append(row)

    # Join all rows into a single string
    markdown_table = "\n".join(rows)

    # Optionally, write the markdown table to a file
    with open('tests_table.md', 'w') as md_file:
        md_file.write(markdown_table)

    print("Markdown table generated and saved to tests_table.md")


def main():
    list_of_files = []
    directory = ''  # Initialize outside the loop to maintain the last seen directory

    for line in fileinput.input(['tests.txt']):
        line = line.strip()  # Strip whitespace and newline characters
        if line.startswith('*'):
            directory = line[1:].strip()  # Remove '*' and trim spaces
            full_dir_path = os.path.join(os.getcwd(), directory)
            if not os.path.exists(full_dir_path):
                os.makedirs(full_dir_path)
        else:
            # Only append non-directory lines with the current directory
            pair = (directory, line)
            list_of_files.append(pair)

    content = ""
    with open('content.txt', 'r') as file:
        content = file.read()

    config = interpret_lines(list_of_files)
    create_files(list_of_files, content, config)
    generate_markdown_table()


if __name__ == "__main__":
    main()
