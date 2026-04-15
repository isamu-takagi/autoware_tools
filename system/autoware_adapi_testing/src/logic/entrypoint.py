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

from autoware_adapi_testing.adapi.localization import Localization
from autoware_adapi_testing.adapi.operation_mode import OperationMode
from autoware_adapi_testing.adapi.routing import Routing
from autoware_adapi_testing.logic.event import CallEvent
from autoware_adapi_testing.logic.event import WaitEvent
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import PoseWithCovarianceStamped
from rclpy.node import Node


class ADAPI:
    def __init__(self, node: Node):
        self.localization = Localization(node)
        self.routing = Routing(node)
        self.operation_mode = OperationMode(node)


class Entrypoint(Node):
    def __init__(self):
        super().__init__("autoware_adapi_testing")
        self.timer = self.create_timer(1.0, self.on_timer)
        self.api = ADAPI(self)

        self.tasks = []
        self.tasks.append(WaitEvent(self.api.localization.state.is_received))
        self.tasks.append(CallEvent(self.api.localization.initialize.request, self.self_pose()))
        self.tasks.append(WaitEvent(self.api.localization.state.is_initialized))
        self.tasks.append(WaitEvent(self.api.routing.state.is_received))
        self.tasks.append(CallEvent(self.api.routing.set_route_points.request, self.goal_pose()))
        self.tasks.append(WaitEvent(self.api.routing.state.is_set))
        self.tasks.append(WaitEvent(self.api.operation_mode.state.is_autonomous_available))
        self.tasks.append(CallEvent(self.api.operation_mode.change_autonomous.request))
        self.tasks.append(WaitEvent(self.api.routing.state.is_arrived))
        # TODO: check vehicle position

    def on_timer(self):

        while self.tasks:
            task = self.tasks[0]
            complete = task.is_complete()
            print(task, complete)
            if complete:
                self.tasks.pop(0)
                continue
            else:
                task.execute()
                break

    def self_pose(self):
        pose = PoseWithCovarianceStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.pose.position.x = 3730.140869140625
        pose.pose.pose.position.y = 73727.7734375
        pose.pose.pose.position.z = 0.0
        pose.pose.pose.orientation.x = 0.0
        pose.pose.pose.orientation.y = 0.0
        pose.pose.pose.orientation.z = 0.24019710926824225
        pose.pose.pose.orientation.w = 0.970724136250449
        return pose

    def goal_pose(self):
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = 3828.23974609375
        pose.pose.position.y = 73725.5078125
        pose.pose.position.z = 0.0
        pose.pose.orientation.x = 0.0
        pose.pose.orientation.y = 0.0
        pose.pose.orientation.z = -0.9701766104447044
        pose.pose.orientation.w = 0.24239914303896443
        return pose
