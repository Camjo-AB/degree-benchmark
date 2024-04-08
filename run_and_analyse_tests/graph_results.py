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


def sort_after_size(df_thrpt, sizes_in_bytes):
    df_thrpt["size"] = [value[0] for value in sizes_in_bytes]

    sizes_sorted = sorted(sizes_in_bytes, key=lambda x: x[1], reverse=False)

    # List defining the desired order
    sorted_data_sizes = [size[0] for size in sizes_sorted]

    # Convert the 'size' column to a categorical type with the specified order
    df_thrpt['size'] = pd.Categorical(df_thrpt['size'], categories=sorted_data_sizes, ordered=True)

    # return sorted by the 'size' column
    return df_thrpt.sort_values('size')


def sort_after_mbps(df_ltcy, throughput):
    data = [value for key, value in throughput.items()]
    df_to_add = pd.DataFrame(data, columns=['throughput', 'size'])

    df_ltcy = pd.concat([df_ltcy, df_to_add], axis=1)

    df_8kb = df_ltcy[df_ltcy['size'] == 8192]
    df_1kb = df_ltcy[df_ltcy['size'] == 1024]
    df_8kb = df_8kb.sort_values(by='throughput', ascending=True)
    df_1kb = df_1kb.sort_values(by='throughput', ascending=True)

    df_8kb['throughput'] = (df_8kb['throughput'] / 1_000_000).astype(int)
    df_1kb['throughput'] = (df_1kb['throughput'] / 1_000_000).astype(int)
    return df_1kb, df_8kb


def create_plot_data(test_dict, measurement):
    first_key = next(iter(test_dict.keys()))
    test_match = re.search(r'.+?(?=-RabbitMQ|-Kafka)', first_key)
    test = test_match.group()

    data_sizes = []
    groups = {}
    throughput = {}

    for key in test_dict:
        current_test_data = test_dict[key]
        broker_match = re.search(r'(?<=tests-).+?(?<=[Qe])-', key)
        broker = broker_match.group()
        broker = broker[:-1]

        rate_match = re.search(r'.+?(?= rate)', current_test_data['workload'])
        rate = rate_match.group()
        rate = rate[:-1]

        size = current_test_data['messageSize']
        # if int(rate)+size not in throughput:
        throughput[int(rate) + size] = (int(rate) * size, size)

        print(key)
        if size not in data_sizes:
            data_sizes.append(size)
        if broker not in groups:
            groups[broker] = []
            measurement_values = current_test_data[measurement]
            if isinstance(measurement_values, list):
                max_value = max(measurement_values)
                groups[broker].append(max_value)
            else:
                groups[broker].append(measurement_values)
        else:
            measurement_values = current_test_data[measurement]
            if isinstance(measurement_values, list):
                max_value = max(measurement_values)
                groups[broker].append(max_value)
            else:
                groups[broker].append(measurement_values)

    df_hist = pd.DataFrame(groups)

    sizes_in_bytes = [(bytes_to_size(size), size) for size in data_sizes]

    if test == 'Throughput_tests':
        df_size = sort_after_size(df_hist, sizes_in_bytes)
        return df_size.reset_index(drop=True)
    else:
        df_size_1kb, df_size_8kb = sort_after_mbps(df_hist, throughput)
        return df_size_1kb.reset_index(drop=True), df_size_8kb.reset_index(drop=True)


def bytes_to_size(byte_value):
    kilobytes_threshold = 1024

    if byte_value < kilobytes_threshold:
        return f"{byte_value}B"
    else:
        kilobytes_value = byte_value / kilobytes_threshold
        return f"{kilobytes_value:.1f}KB"


def create_histogram(df_in):
    # Create an index for each tick position
    x_indexes = np.arange(len(df_in))

    # The width of the bars
    bar_width = 0.25

    # Plot the data
    plt.bar(x_indexes - bar_width, df_in['RabbitMQ'], width=bar_width, label='RabbitMQ')
    plt.bar(x_indexes, df_in['Kafka-exactly-once'], width=bar_width, label='Kafka')

    if 'throughput' in df_in.columns:
        # Add labels and title
        plt.xlabel('Throughput(Mbps)')
        plt.ylabel('Latency(ms)')
        plt.title('Max Aggregated End-To-End Latency')

        # Add xticks
        plt.xticks(ticks=x_indexes, labels=df_in['throughput'])
    else:
        # Add labels and title
        plt.xlabel('Message Size')
        plt.ylabel('Throughput in Events/seconds')
        plt.title('Throughput Comparison by Message Size')

        # Add xticks
        plt.xticks(ticks=x_indexes, labels=df_in['size'])

    # Set the y-axis to a logarithmic scale
    # plt.yscale('log')
    # plt.yscale('log', base=2)

    # Add a legend
    plt.legend()

    # Display the chart
    plt.tight_layout()
    plt.show()


def create_latency_histogram(dict_df):
    print('this is it')
    return 0


# HERE START THE CREATION OF DATA DICTIONARY
def data_dictionary_update(test_directory, filepath, data_dict, performance_data):
    variable_match = match_test_cast_to_variable(test_directory, filepath)
    broker_match = re.search(r'(?<=4c-|8c-|2c-|6c-).+?(?=-2024)', filepath)

    if not isinstance(variable_match, str):
        variable_value = variable_match.group()
    else:
        variable_value = variable_match
    broker_value = broker_match.group()

    key = str(test_directory + '-' + broker_value + '-' + variable_value)
    data_dict.update({key: performance_data})
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
    file_paths = [result_directory + '\\' + file for file in files_in_directory]

    data_dict = {}

    for file_path in file_paths:
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
    df = create_plot_data(throughput_tests_dict, 'consumeRate')
    create_histogram(df)

    df_1kb, df_8kb = create_plot_data(latency_tests_dict, 'aggregatedEndToEndLatency50pct')
    create_histogram(df_1kb)
    create_histogram(df_8kb)
