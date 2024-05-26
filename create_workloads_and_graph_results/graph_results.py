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
from matplotlib import ticker


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


def sort_after_size(df_in, sizes_in_bytes):
    df_thrpt1 = df_in.copy()
    df_thrpt1["message_size"] = [value[0] for value in sizes_in_bytes]

    sizes_sorted = sorted(sizes_in_bytes, key=lambda x: x[1], reverse=False)

    # List defining the desired order
    sorted_data_sizes = [size[0] for size in sizes_sorted]

    # Convert the 'size' column to a categorical type with the specified order
    df_thrpt1['message_size'] = pd.Categorical(df_thrpt1['message_size'], categories=sorted_data_sizes, ordered=True)

    # return sorted by the 'size' column
    return df_thrpt1.sort_values('message_size')


def sort_after_mbps(df_in, throughput):
    df_ltcy1 = df_in.copy()
    data = [value for key, value in throughput.items()]
    df_to_add = pd.DataFrame(data, columns=['throughput', 'size'])

    df_ltcy1 = pd.concat([df_ltcy1, df_to_add], axis=1)

    df_large = df_ltcy1[df_ltcy1['size'] == 8192]
    df_small = df_ltcy1[df_ltcy1['size'] == 1024]
    df_large = df_large.sort_values(by='throughput', ascending=True)
    df_small = df_small.sort_values(by='throughput', ascending=True)

    df_large['throughput'] = (df_large['throughput'] / 1_000_000).astype(int)
    df_small['throughput'] = (df_small['throughput'] / 1_000_000).astype(int)
    return df_small, df_large


def add_throughput(df_in):
    df_put = df_in.copy()

    df_put['message_size_bytes'] = df_put['message_size'].apply(size_to_bytes)

    df_put['message_size_bytes'] = df_put['message_size_bytes'].astype(int)

    df_put['Kafka-mbps'] = df_put['Kafka-exactly-once'] * df_put['message_size_bytes']
    df_put['Kafka-mbps'] = (df_put['Kafka-mbps']).round().astype(int)

    if 'RabbitMQ' in df_put.columns:
        df_put['RabbitMQ-mbps'] = df_put['RabbitMQ'] * df_put['message_size_bytes']
        df_put['RabbitMQ-mbps'] = (df_put['RabbitMQ-mbps']).round().astype(int)

    return df_put


def get_thrpt_ltcy(df_in, variable_x, measurement, size_in_bytes, col_name):
    df_save = df_in.copy()
    rate = [value[0] for value in variable_x.values()]
    variables = [value[1] for value in variable_x.values()]
    df_save['rate'] = rate
    df_save[col_name] = variables

    if 'consumeRate' == measurement:
        list_of_sizes = [size_in_bytes[0] for _ in range(len(df_save))]
        df_save['message_size'] = [size[0] for size in list_of_sizes]
        df_save = add_throughput(df_save)

    df_max = df_save[df_save['rate'] == 0]
    df_1k = df_save[df_save['rate'] == 1000]
    return df_max, df_1k


def create_plot_data(test_dict, measurement):
    first_key = next(iter(test_dict.keys()))
    test_match = re.search(r'.+?(?=-RabbitMQ|-Kafka)', first_key)
    test = test_match.group()

    message_sizes = []
    groups = {}
    throughput = {}
    partitions = {}
    prods_cons = {}
    topics = {}

    for key in test_dict:
        current_test_data = test_dict[key]
        broker_match = re.search(r'(?<=tests-).+?(?<=[Qe])-', key)
        broker = broker_match.group()
        broker = broker[:-1]

        rate_match = re.search(r'.+?(?= rate)', current_test_data['workload'])
        rate = rate_match.group()
        rate = rate[:-1]

        # Get value
        size = current_test_data['messageSize']
        num_partition = current_test_data['partitions']
        num_prod_con = current_test_data['consumersPerTopic']
        num_topic = current_test_data['topics']
        # Add value to dictionary
        throughput[int(rate) + size] = (int(rate) * size, size)
        partitions[int(rate) + num_partition] = (int(rate), num_partition)
        prods_cons[int(rate) + num_prod_con] = (int(rate), num_prod_con)
        topics[int(rate) + num_topic] = (int(rate), num_topic)

        print(key + ' ' + current_test_data['timestamp'])
        if size not in message_sizes:
            message_sizes.append(size)
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

    sizes_in_bytes = [(bytes_to_size(size), size) for size in message_sizes]

    if test == 'Throughput_tests':
        df_message_size = sort_after_size(df_hist, sizes_in_bytes)
        df_message_size = add_throughput(df_message_size)
        return df_message_size.reset_index(drop=True)
    elif test == 'Latency_tests':
        df_size_1kb, df_size_8kb = sort_after_mbps(df_hist, throughput)
        return df_size_1kb.reset_index(drop=True), df_size_8kb.reset_index(drop=True)
    elif test == 'Producer_Consumer_tests':
        df_0k, df_1k = get_thrpt_ltcy(df_hist, prods_cons, measurement, sizes_in_bytes, 'producer/consumer')
        return df_0k.reset_index(drop=True), df_1k.reset_index(drop=True)
    elif test == 'Partitions_tests':
        df_0k, df_1k = get_thrpt_ltcy(df_hist, partitions, measurement, sizes_in_bytes, 'partitions')
        df_part_output = pd.concat([df_0k, df_1k], axis=0)
        return df_part_output.reset_index(drop=True)
    elif test == 'Topics_tests':
        df_0k, df_1k = get_thrpt_ltcy(df_hist, topics, measurement, sizes_in_bytes, 'topics')
        df_0k = df_0k.sort_values(by='topics', ascending=True)
        df_1k = df_1k.sort_values(by='topics', ascending=True)
        df_part_output = pd.concat([df_0k, df_1k], axis=0)
        return df_part_output.reset_index(drop=True)


def bytes_to_size(byte_value):
    kilobytes_threshold = 1024

    if byte_value < kilobytes_threshold:
        return f"{byte_value}B"
    else:
        kilobytes_value = byte_value / kilobytes_threshold
        return f"{kilobytes_value:.1f}KB"


def size_to_bytes(size_str):
    size_units = {'B': 1, 'KB': 1024, 'MB': 1024 ** 2, 'GB': 1024 ** 3}
    number, unit = re.findall(r'\d+\.\d+|\d+|[a-zA-Z]+', size_str)
    return int(float(number) * size_units[unit])


def create_histogram(df_in, ltcy_or_thrpt, filepath):
    df_plt = df_in.copy()
    # Create an index for each tick position
    x_indexes = np.arange(len(df_plt))

    # The width of the bars
    bar_width = 0.25

    # Logarithmic scaling of y-axis
    logarithmic_scale = False

    if 'partitions' in df_plt.columns:
        logarithmic_scale = True

    if 'throughput' in df_plt.columns:
        show_plt(bar_width, df_plt, x_indexes,
                 'RabbitMQ', 'Kafka-exactly-once',
                 'RabbitMQ', 'Kafka',
                 'Throughput(Mbps)', 'Latency(ms)',
                 'End-To-End Latency',
                 'throughput',
                 filepath,
                 logarithmic_scale=False)

    else:
        if ltcy_or_thrpt == 'thrpt':
            measurement, x_ticks = set_measurement_x_ticks(df_plt)
            broker_1, broker_2 = set_name_of_bars(df_plt)
            show_plt(bar_width, df_plt, x_indexes,
                     'RabbitMQ-mbps', 'Kafka-mbps',
                     broker_1, broker_2,
                     measurement, 'Throughput in Mbps',
                     'Throughput Comparison by ' + measurement,
                     x_ticks,
                     filepath,
                     logarithmic_scale)
        elif ltcy_or_thrpt == 'ltcy':
            measurement, x_ticks = set_measurement_x_ticks(df_plt)
            broker_1, broker_2 = set_name_of_bars(df_plt)
            show_plt(bar_width, df_plt, x_indexes,
                     'RabbitMQ', 'Kafka-exactly-once',
                     broker_1, broker_2,
                     measurement, 'Latency(ms)',
                     'Latency(ms) Comparison by ' + measurement,
                     x_ticks,
                     filepath,
                     logarithmic_scale)
        # If nan in ltcy_or_thrpt
        else:
            show_plt(bar_width, df_plt, x_indexes,
                     'RabbitMQ', 'Kafka-exactly-once',
                     'RabbitMQ', 'Kafka',
                     'Message Size', 'Throughput in msgs/s',
                     'Throughput Comparison by Message Size',
                     'message_size',
                     filepath,
                     logarithmic_scale=True)
    return df_plt


def set_measurement_x_ticks(df_plt):
    measurement = 'Message Size'
    x_ticks = 'message_size'
    if 'producer/consumer' in df_plt.columns:
        measurement = '# Producer/Consumer'
        x_ticks = 'producer/consumer'
    elif 'partitions' in df_plt.columns:
        measurement = '# Partitions'
        x_ticks = 'partitions'
    elif 'topics' in df_plt.columns:
        measurement = '# Topics'
        x_ticks = 'topics'

    return measurement, x_ticks


def set_name_of_bars(df_plt):
    broker_1 = 'RabbitMQ'
    broker_2 = 'Kafka'
    if 'partitions' in df_plt.columns or 'topics' in df_plt.columns:
        rate_1 = df_plt['rate'].iloc[0]  # Get the first element
        rate_2 = df_plt['rate'].iloc[-1]  # Get the last element using -1 index

        if rate_1 == 0:
            rate_1 = 'max'
        broker_1 = 'Kafka rate ' + rate_1 + ' msgs/s'
        broker_2 = 'Kafka rate ' + str(rate_2) + ' msgs/s'

    return broker_1, broker_2


# def set_data(df_plt):
#     data_1 = 'RabbitMQ-mbps'
#     data_2 = 'Kafka-mbps'
#     if 'partitions' in df_plt.columns:
#         split_index = len(df_plt) // 2
#         data_1 = df_plt.iloc[:split_index]
#         data_2 = df_plt.iloc[split_index:]
#     return data_1, data_2
def show_plt(bar_width, df_in, x_indexes,
             data_broker_1, data_broker_2,
             bar_name_1, bar_name_2,
             x_label, y_label,
             title,
             x_ticks,
             directory,
             logarithmic_scale,
             ):
    part_df_1 = ''
    part_df_2 = ''

    # Plot the data
    if 'partitions' in df_in.columns or 'topics' in df_in.columns:
        split_index = len(df_in) // 2
        part_df_1 = df_in.iloc[:split_index]
        part_df_2 = df_in.iloc[split_index:]

        part_df_1.reset_index(drop=True)
        part_df_2.reset_index(drop=True)
        x_indexes = np.arange(len(part_df_1))

        plt.bar(x_indexes - bar_width, part_df_1.iloc[:, 0], width=bar_width, label=bar_name_1)
        plt.bar(x_indexes, part_df_2.iloc[:, 0], width=bar_width, label=bar_name_2)
    else:
        if 'RabbitMQ' in df_in.columns or 'RabbitMQ-mbps' in df_in.columns:
            plt.bar(x_indexes - bar_width, df_in[data_broker_1], width=bar_width, label=bar_name_1)

        if 'Kafka-exactly-once' in df_in.columns or 'Kafka-mbps' in df_in.columns:
            plt.bar(x_indexes, df_in[data_broker_2], width=bar_width, label=bar_name_2)

    # Add labels and title
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    # Add xticks
    if 'partitions' in df_in.columns or 'topics' in df_in.columns:
        plt.xticks(ticks=x_indexes, labels=part_df_1[x_ticks])
    else:
        plt.xticks(ticks=x_indexes, labels=df_in[x_ticks])

    if logarithmic_scale:
        # Set the y-axis to a logarithmic scale
        plt.yscale('log')
        # plt.yscale('log', base=2)

        if 'partitions' in df_in.columns or 'topics' in df_in.columns:
            values_broker_1 = part_df_1.iloc[:, 0]
            values_broker_2 = part_df_1.iloc[:, 0]
        else:
            values_broker_1 = df_in[data_broker_1]
            values_broker_2 = df_in[data_broker_2]

        values_list = values_broker_1.tolist() + values_broker_2.tolist()
        min_axis = min(values_list)
        max_axis = max(values_list)

        ax = plt.gca()
        ax.set_yscale('log')

        ticks = [2 ** i for i in range(int(np.floor(np.log2(min_axis))), int(np.ceil(np.log2(max_axis))))] + [max_axis]
        labels = [int(y) for y in ticks]
        ax.set_yticks(ticks)
        ax.set_yticklabels(labels)

    # Add a legend
    plt.legend()

    # Save chart to png
    if not os.path.exists(directory):
        os.makedirs(directory)

    title = title.replace(' ', '_')
    title = title.replace('#', 'number_of')
    title = title.replace('/', '_and_')
    file_path = directory + '\\' + title + '.png'
    if os.path.exists(file_path):
        file_path = file_path.replace('.png', '(2).png')
    plt.savefig(file_path, format='png', dpi=300, bbox_inches='tight')

    # Display the chart
    plt.tight_layout()
    plt.show()

    # Clear the current figure
    plt.clf()


# HERE START THE CREATION OF DATA DICTIONARY
def data_dictionary_update(test_directory, filepath, data_dict, performance_data):
    variable_match = match_test_cast_to_variable(test_directory, filepath)
    broker_match = re.search(r'(?<=4c-|8c-|2c-|6c-|1c-).+?(?=-2024)', filepath)

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
            variable_match = re.search(r'(?<=-topic-).+?(?=-4p-|-8p-|-2p-|-6p-|-1p-)', filepath)
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
            variable_match = re.search(r'(?<=partitions).+?(?=-RabbitMQ|-Kafka)', filepath)
            topic_match = re.search(r'(?<=Consumer_tests\\).+?(?<=-rate)', filepath)
            topic_value = topic_match.group()
            variable_value = variable_match.group()
            result = str(topic_value + '-' + variable_value)
            return result
        case default:
            return "something"


# This function simulates reading your data files and extracting the publish rate
def read_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    return data


def create_directory_data_dictionary(test_directory):
    parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    result_directory = os.path.join(parent_directory, 'create_workloads_and_graph_results', 'result', test_directory)

    files_in_directory = os.listdir(result_directory)
    file_paths = [result_directory + '\\' + file for file in files_in_directory]

    data_dict = {}

    for file_path in file_paths:
        data = read_data(file_path)
        data_dictionary_update(test_directory, file_path, data_dict, data)

        time_match = re.search(r"2024.*?(?=.json)", file_path)
        time_value = time_match.group()
        data['timestamp'] = time_value

    graph_directory = os.path.join(parent_directory, 'create_workloads_and_graph_results', 'result', 'Graphs',
                                   test_directory)
    return data_dict, graph_directory


if __name__ == '__main__':
    # Directories that include all the test data
    throughput_tests_dict, thrpt_filepath = create_directory_data_dictionary('Throughput_tests')
    latency_tests_dict, ltcy_filepath = create_directory_data_dictionary('Latency_tests')
    prod_cons_tests_dict, prod_cons_filepath = create_directory_data_dictionary('Producer_Consumer_tests')
    partitions_tests_dict, prt_filepath = create_directory_data_dictionary('Partitions_tests')
    topics_tests_dict, tpc_filepath = create_directory_data_dictionary('Topics_tests')

    # Throughput tests charts - Max throughput: on  100b, 500b, 1kb, 2kb, 4kb message size
    df_thrpt = create_plot_data(throughput_tests_dict, 'consumeRate')
    # df_ltcy_msgs_size = create_plot_data(throughput_tests_dict, "aggregatedEndToEndLatency99pct")

    df_mbps = create_histogram(df_thrpt, 'thrpt', thrpt_filepath)
    df_size = create_histogram(df_thrpt, 'nan', thrpt_filepath)
    # latency for message size max throughput
    # df_latency = create_histogram(df_ltcy_msgs_size, 'ltcy', thrpt_filepath)

    # ----------------------------------------------------------------------------------
    # Latency tests charts - producer rate~, message size: 1Kb, 8Kb
    df_1kb_99pct, df_8kb_99pct = create_plot_data(latency_tests_dict, "aggregatedEndToEndLatency99pct")

    df_1kb_99pct = create_histogram(df_1kb_99pct, 'nan', ltcy_filepath)
    df_8kb_99pct = create_histogram(df_8kb_99pct, 'nan', ltcy_filepath)

    # ----------------------------------------------------------------------------------
    # Producer/Consumer tests charts - Max throughput: on 1kb message size, Latency: on 1kb message size producer
    # rate 1k
    df_thrpt_max, df_thrpt_1k = create_plot_data(prod_cons_tests_dict, 'consumeRate')
    df_ltcy_max, df_ltcy_1k = create_plot_data(prod_cons_tests_dict, 'aggregatedEndToEndLatency99pct')

    df_prod_cons_thrpt_max = create_histogram(df_thrpt_max, 'thrpt', prod_cons_filepath)
    df_prod_cons_thrpt_1k = create_histogram(df_thrpt_1k, 'thrpt', prod_cons_filepath)
    df_prod_cons_ltcy_max = create_histogram(df_ltcy_max, 'ltcy', prod_cons_filepath)
    df_prod_cons_ltcy_1k = create_histogram(df_ltcy_1k, 'ltcy', prod_cons_filepath)

    # ----------------------------------------------------------------------------------
    # Partitions test charts - Max throughput: on 1kb message size, Latency: on 1kb message size producer rate 1k
    df_thrpt_part = create_plot_data(partitions_tests_dict, 'consumeRate')
    df_ltcy_part = create_plot_data(partitions_tests_dict, 'aggregatedEndToEndLatency99pct')

    df_part_thrpt = create_histogram(df_thrpt_part, 'thrpt', prt_filepath)
    df_part_ltcy = create_histogram(df_ltcy_part, 'ltcy', prt_filepath)

    # ----------------------------------------------------------------------------------
    # Topics test charts - Max throughput: on 1kb message size, Latency: on 1kb message size producer rate 1k
    df_thrpt_topic = create_plot_data(topics_tests_dict, 'consumeRate')
    df_ltcy_topic = create_plot_data(topics_tests_dict, 'aggregatedEndToEndLatency99pct')

    df_topic_thrpt = create_histogram(df_thrpt_topic, 'thrpt', tpc_filepath)
    df_topic_ltcy = create_histogram(df_ltcy_topic, 'ltcy', tpc_filepath)
