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

import simplejson as json


def test_json():
    a_json_object = {
        "workload": "0B rate 4 producers and 4 consumers on 1 topic / 1 partition",
        "driver": "Kafka-exactly-once",
        "messageSize": 1024,
        "topics": 1,
        "partitions": 1,
        "producersPerTopic": 4,
        "consumersPerTopic": 4,
        "publishRate": [31014.955459138753, 21356.05146538597, 21769.7332954624, 26840.560944611094, 32159.743025163014,
                        31647.206690205545, 24414.246338578287, 22717.60437105778, 24859.128972763796,
                        29266.865942634286, 22520.960571853102, 18198.810914077712, 18235.052664691117,
                        22149.25692329416, 30847.582470294627, 29280.796683640023, 30385.217804546708,
                        27498.063480525416, 30128.605933170762, 33111.39434766499, 24443.469955928096,
                        24164.085683270758, 29543.63259175442, 26430.635332529047, 27143.096242312236,
                        31399.981943307317, 32437.53542646387, 31920.612094238157],
    }
    content = json.dumps(a_json_object)
    print(content)


def read_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    print('This means the JSON data was read from: ' + file_path)
    return data


if __name__ == '__main__':
    test_json()
    data_dict_1 = read_data(
        'C:\\Users\\Gustav Normelli\\degree-benchmark\\create_workloads_and_graph_results\\result\\0K-rate-1KB-size-1-topic-1-partitions-8p-8c-Kafka-exactly-once-2024-05-27-19-01-00.json')
    data_dict_2 = read_data('C:\\Users\\Gustav Normelli\\degree-benchmark\\create_workloads_and_graph_results\\result'
                            '\\Producer_Consumer_tests\\0K-rate-1KB-size-1-topic-1-partitions-1p-1c-Kafka-exactly-once'
                            '-2024-04-11-12-13-00.json')
    print('Here it is!')
