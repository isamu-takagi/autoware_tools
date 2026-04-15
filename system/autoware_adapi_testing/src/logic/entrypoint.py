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

from ament_index_python import get_package_share_directory
from autoware_adapi_testing.adapi import ADAPI
from rclpy.node import Node


class Entrypoint(Node):
    def __init__(self):
        super().__init__("autoware_adapi_testing")
        self.timer = self.create_timer(1.0, self.on_timer)
        self.api = ADAPI(self)
        self.tasks = self.load_scenario(
            self.get_package_file_path("autoware_adapi_testing", "test/main.py")
        )

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

    def get_package_file_path(self, package, file):
        return get_package_share_directory(package) + "/" + file

    def load_scenario(self, path):
        import importlib.util

        spec = importlib.util.spec_from_file_location("scenario", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.generate_scenario(self.api, self.get_clock())
