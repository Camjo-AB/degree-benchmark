import json
import matplotlib.pyplot as plt

# This function simulates reading your data files and extracting the publish rate
def read_data(file_paths):
    publish_rates = []
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Assume data['publishRate'] is a list of publish rate values
            publish_rates.append(data['publishRate'])
    return publish_rates

# Function to create a line chart with multiple series
def create_publish_rate_chart(publish_rates, labels):
    plt.figure(figsize=(10, 6))
    for rates, label in zip(publish_rates, labels):
        plt.plot([10*x for x in range(len(rates))], rates, label=label)
    plt.title('Publish rate')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Rate (msg/s)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    # Replace 'file_path_1.json', 'file_path_2.json' with the actual paths to your JSON files
    file_paths = [
                  'result/1-topic-1-partitions-1kb-4p-4c-50k-Kafka-exactly-once-2024-03-18-16-49-31.json',
                  'result/1-topic-1-partitions-1kb-4p-4c-50k-RabbitMQ-2024-03-18-08-09-35.json']  # and so on...
    labels = ['1-topic-1-partitions-1kb-4p-4c-50k-Kafka', '1-topic-1-partitions-1kb-4p-4c-50k-RabbitMQ']  # Replace with your actual labels

    # Read the data from files
    publish_rates = read_data(file_paths)

    # Create the chart
    create_publish_rate_chart(publish_rates, labels)