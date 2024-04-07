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
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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


def create_latency_data(dict_df, feature):
    print('this is it')
    return 0


def sort_after_size(df_hist, sizes_in_bytes):
    df_hist["size"] = [value[0] for value in sizes_in_bytes]

    sizes_sorted = sorted(sizes_in_bytes, key=lambda x: x[1], reverse=False)

    # List defining the desired order
    sorted_data_sizes = [size[0] for size in sizes_sorted]

    # Convert the 'size' column to a categorical type with the specified order
    df_hist['size'] = pd.Categorical(df_hist['size'], categories=sorted_data_sizes, ordered=True)

    # return sorted by the 'size' column
    return df_hist.sort_values('size')


def sort_after_mbps(df_hist, sizes_in_bytes):
    pass


def create_maximum_data(dict_df, feature):
    data_sizes = []
    groups = {}

    for key in dict_df:
        current_test = dict_df[key]
        broker_match = re.search(r'(?<=tests-).+?(?<=[Qe])-', key)
        broker = broker_match.group()
        broker = broker[:-1]

        size = current_test['messageSize']
        print(key)
        if size not in data_sizes:
            data_sizes.append(size)
        if broker not in groups:
            groups[broker] = []
            feature_values = current_test[feature]
            max_value = max(feature_values)
            groups[broker].append(max_value)
        else:
            feature_values = current_test[feature]
            max_value = max(feature_values)
            groups[broker].append(max_value)

    df_hist = pd.DataFrame(groups)

    sizes_in_bytes = [(bytes_to_size(size), size) for size in data_sizes]

    if dict_df['messageSize']:
        df_sorted = sort_after_size(df_hist, sizes_in_bytes)
    else:
        df_sorted = sort_after_mbps(df_hist, sizes_in_bytes)

    return df_sorted.reset_index(drop=True)


def bytes_to_size(byte_value):
    kilobytes_threshold = 1024

    if byte_value < kilobytes_threshold:
        # For values less than 1024, represent as bytes
        return f"{byte_value}B"
    else:
        # Convert to KB for values 1024 and above
        kilobytes_value = byte_value / kilobytes_threshold
        return f"{kilobytes_value:.1f}KB"


def create_maximum_throughput_histogram(df_in):
    # Create an index for each tick position
    x_indexes = np.arange(len(df_in))

    # The width of the bars
    bar_width = 0.25

    # Plot the data
    plt.bar(x_indexes - bar_width, df_in['RabbitMQ'], width=bar_width, label='RabbitMQ')
    plt.bar(x_indexes, df_in['Kafka-exactly-once'], width=bar_width, label='Kafka')

    # Add labels and title
    plt.xlabel('Data Size')
    plt.ylabel('Throughput in Events/seconds')
    plt.title('Throughput Comparison by Data Size')

    # Set the y-axis to a logarithmic scale
    # plt.yscale('log')

    # Add xticks
    plt.xticks(ticks=x_indexes, labels=df_in['size'])

    # Add a legend
    plt.legend()

    # Display the chart
    plt.tight_layout()
    plt.show()


# HERE START THE CREATION OF DATA DICTIONARY
def data_dictionary_update(test_directory, filepath, dataframes, performance_frame):
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
        case 'Partitions_tests':
            variable_match = re.search(r'(?<=-topic-).+?(?=-4p-|-8p-|-2p-|-6p-)', filepath)
            partition_match = re.search(r'(?<=Partitions_tests\\).+?-rate', filepath)
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
        case 'Producer_Consumer_tests':
            return "four"
        case default:
            return "something"


# This function simulates reading your data files and extracting the publish rate
def read_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    return data


def create_directory_data_dictionary(test_directory):
    parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    result_directory = os.path.join(parent_directory, 'run_and_analyse_tests', 'result', test_directory)

    files_in_directory = os.listdir(result_directory)
    file_directories = [result_directory + '\\' + file for file in files_in_directory]

    data_dict = {}

    for file_path in file_directories:
        data = read_data(file_path)
        data_dictionary_update(test_directory, file_path, data_dict, data)

    return data_dict


if __name__ == '__main__':
    # Directories that include all the test data
    throughput_tests_dict = create_directory_data_dictionary('Throughput_tests')
    latency_tests_dict = create_directory_data_dictionary('Latency_tests')
    partitions_tests_dict = create_directory_data_dictionary('Partitions_tests')
    topics_tests_dict = create_directory_data_dictionary('Topics_tests')

    # Create the chart & histograms
    # test()
    # df = create_maximum_data(throughput_tests_dict, 'consumeRate')
    # create_maximum_throughput_histogram(df)

    df = create_maximum_data(latency_tests_dict, 'consumeRate')
    df = create_latency_data(df, 'publishLatency50pct')
