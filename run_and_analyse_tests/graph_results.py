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
import numpy as np
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


def create_maximum_histogram(dict_df, feature):
    first_key = next(iter(dict_df.keys()))
    title_match = re.search(r'.+?(?=-RabbitMQ|-Kafka)', first_key)
    title = title_match.group()

    if title not in ("Latency_tests", "Throughput_tests"):
        print('Histogram can only be created for Latency_tests and Throughput_tests')

    data_sizes = []
    groups = {}
    for key in dict_df:
        broker_match = re.search(r'(?<=tests-).+?(?=--)', first_key)
        broker = broker_match.group()
        size_match = re.search(r'(?<=e--|te-).+?(?=-size)', first_key)
        size = size_match.group()
        data_sizes.append(size)
        if broker not in groups:
            groups[broker] = []
            df_current = dict_df[key]
            max_value = df_current[feature]
            groups[broker].append(max_value.max())
        else:
            df_current = dict_df[key]
            max_value = df_current[feature].max()
            groups[broker].append(max_value)

    # Create an index for each tick position
    x_indexes = np.arange(len(data_sizes))

    # The width of the bars
    bar_width = 0.25

    # Plot the data
    plt.bar(x_indexes - bar_width, groups['RabbitMQ'], width=bar_width, label='Group 1')
    plt.bar(x_indexes, groups['Kafka-exactly-once'], width=bar_width, label='Group 2')

    # Add labels and title
    plt.xlabel('Data Size')
    plt.ylabel('Throughput in MB/seconds')
    plt.title('Throughput Comparison by Data Size')

    # Add xticks
    plt.xticks(ticks=x_indexes, labels=data_sizes)

    # Add a legend
    plt.legend()

    # Display the chart
    plt.tight_layout()
    plt.show()


def dataframes_update(test_directory, filepath, dataframes, performance_frame):
    variable_match = match_test_cast_to_variable(test_directory, filepath)
    broker_match = re.search(r'(?<=4c-|8c-|2c-|6c-).+?(?=-2024)', filepath)

    if not isinstance(variable_match, str):
        variable_value = variable_match.group()
    else:
        variable_value = variable_match
    broker_value = broker_match.group()

    key = str(test_directory + '-' + broker_value + '-' + variable_value)
    dataframes.update({key: performance_frame})
    pass


def match_test_cast_to_variable(test_directory, filepath):
    match test_directory:
        case 'Throughput_tests':
            variable_match = re.search(r'-(\d+(\.\d+)?K?B)-size', filepath)
            return variable_match
        case 'Latency_tests':
            variable_match = re.search(r'(?<=Latency_tests\\).+?(?=-1-topic)', filepath)
            return variable_match
        case 'Partitions_test':
            variable_match = re.search(r'(?<=-topic-).+?(?=-4p-|-8p-|-2p-|-6p-)', filepath)
            partition_match = re.search(r'(?<=Partitions_test\\).+?-rate', filepath)
            partition_value = partition_match.group()
            variable_value = variable_match.group()
            result = str(partition_value + '-' + variable_value)
            return result
        case 'Topics_tests':
            variable_match = re.search(r'(?<=-size-).+?(?<=-topic)', filepath)
            topic_match = re.search(r'(?<=Topics_tests\\).+?-rate', filepath)
            topic_value = topic_match.group()
            variable_value = variable_match.group()
            result = str(topic_value + '-' + variable_value)
            return result
        case 'Producer_Consumer_Test':
            return "four"
        case default:
            return "something"


def create_directory_dataframes(test_directory):
    parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    result_directory = os.path.join(parent_directory, 'run_and_analyse_tests', 'result', test_directory)

    files_in_directory = os.listdir(result_directory)
    file_directories = [result_directory + '\\' + file for file in files_in_directory]

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

        dataframes_update(test_directory, file_path, dataframes, performance_frame)

    return dataframes


def test():
    # Sample data
    data_sizes = ['10B', '100B', '1K', '10KB', '50KB', '100KB']
    group1 = [20, 35, 30, 35, 27, 24]
    group2 = [25, 32, 34, 20, 25, 27]
    group3 = [30, 38, 40, 35, 32, 30]

    # Create an index for each tick position
    x_indexes = np.arange(len(data_sizes))

    # The width of the bars
    bar_width = 0.25

    # Plot the data
    plt.bar(x_indexes - bar_width, group1, width=bar_width, label='Group 1')
    plt.bar(x_indexes, group2, width=bar_width, label='Group 2')
    plt.bar(x_indexes + bar_width, group3, width=bar_width, label='Group 3')

    # Add labels and title
    plt.xlabel('Data Size')
    plt.ylabel('Throughput in MB/seconds')
    plt.title('Throughput Comparison by Data Size')

    # Add xticks
    plt.xticks(ticks=x_indexes, labels=data_sizes)

    # Add a legend
    plt.legend()

    # Display the chart
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # Directories that include all the test data
    throughput_tests_dataframes = create_directory_dataframes('Throughput_tests')
    latency_tests_dataframes = create_directory_dataframes('Latency_tests')
    partitions_test_dataframes = create_directory_dataframes('Partitions_test')
    topics_tests_dataframes = create_directory_dataframes('Topics_tests')

    # Create the chart & histograms
    test()
    create_maximum_histogram(throughput_tests_dataframes, 'consumeRate')
