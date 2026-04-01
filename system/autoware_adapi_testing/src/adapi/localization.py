# Copyright 2026 The Autoware Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from autoware_adapi_testing.adapi.qos import durable_qos
from autoware_adapi_v1_msgs.msg import LocalizationInitializationState
from autoware_adapi_v1_msgs.srv import InitializeLocalization
from rclpy.node import Node


class Localization:
    def __init__(self, node: Node):
        self.initialize = LocalizationInitialize(node)
        self.state = LocalizationState(node)


class LocalizationInitialize:
    def __init__(self, node: Node):
        self.clock = node.get_clock()
        self.stamp = None
        self.future = None
        self.client = node.create_client(InitializeLocalization, "/api/localization/initialize")

    def request(self, pose):
        if not self.client.service_is_ready():
            return False
        req = InitializeLocalization.Request()
        req.pose = [pose]
        self.stamp = self.clock.now()
        self.future = self.client.call_async(req)
        return True


class LocalizationState:
    def __init__(self, node: Node):
        self.sub = node.create_subscription(
            LocalizationInitializationState,
            "/api/localization/initialization_state",
            self.callback,
            durable_qos(),
        )
        self.msg = None

    def callback(self, msg):
        self.msg = msg

    def is_received(self):
        return self.msg is not None
