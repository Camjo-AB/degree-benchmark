#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json
import os
import re

import matplotlib.pyplot as plt
import pandas as pd


# This function simulates reading your data files and extracting the publish rate
def read_data(file_path):

    with open(file_path, 'r') as f:
        data = json.load(f)

    return data


# Function to create a line chart with multiple series
def create_publish_rate_chart(publish_rates, labels):
    plt.figure(figsize=(10, 6))
    for rates, label in zip(publish_rates, labels):
        plt.plot([10 * x for x in range(len(rates))], rates, label=label)
    plt.title('Publish rate')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Rate (msg/s)')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Function to create a line chart with multiple series


def create_max_throughput_chart(data, labels):
    plt.figure(figsize=(10, 6))
    for rates, label in zip(publish_rates, labels):
        plt.plot([10 * x for x in range(len(rates))], rates, label=label)
    plt.title('Maximum Throughput')
    plt.xlabel('Data size')
    plt.ylabel('Rate (msg/s)')
    plt.legend()
    plt.grid(True)
    plt.show()


def dataframes_update(test_directory,filepath, dataframes, performance_frame):
    variable_match = re.search(r'-(\d+(\.\d+)?K?B)-size', filepath)
    variable_value, is_k = variable_match.groups()
    key = str(test_directory + variable_value)
    dataframes.update({key: performance_frame})
    pass


def create_directory_dataframes(test_directory):
    parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    result_directory = os.path.join(parent_directory, 'run_and_analyse_tests', 'result', test_directory)

    files_in_directory = os.listdir(result_directory)
    file_directories = [result_directory+'\\'+file for file in files_in_directory]
    values = 'consumeRate'

    dataframes = {}
    mainframe = pd.DataFrame()

    for file_path in file_directories:
        data = read_data(file_path)

        # Normalizing data except lists and dictionaries for mainframe
        flat_data = {k: v for k, v in data.items() if not isinstance(v, list)}
        primitive_data = {k: v for k, v in flat_data.items() if isinstance(v, (int, float, str))}

        if mainframe is None or len(mainframe) == 0:
            row = pd.json_normalize(primitive_data)
            pd.concat([mainframe, row], axis=0)
        else:
            mainframe.append(primitive_data, ignore_index=True)

        performance_data = {k: v for k, v in data.items() if isinstance(v, list)}
        performance_frame = pd.DataFrame(performance_data)

        dataframes_update(test_directory,file_path,dataframes, performance_frame)

    return 0

if __name__ == '__main__':
    # Directories that include all the test data
    throughput_tests_dataframe = create_directory_dataframes('Throughput_tests')
    # latency_tests_dataframe = create_directory_dataframe('Latency_tests')
    # partitions_test_dataframe = create_directory_dataframe('Partitions_test')
    # topics_tests_dataframe = create_directory_dataframe('Topics_tests')

    # Read the data from files
    rate_values = 'publishRate'
    publish_rates = read_data(file_paths, rate_values)

    # Create the chart
    create_publish_rate_chart(publish_rates, labels)
