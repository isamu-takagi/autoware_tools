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


class Event:
    pass


class WaitEvent(Event):
    def __init__(self, condition):
        self.condition = condition

    def __str__(self):
        cname = self.condition.__self__.__class__.__name__
        fname = self.condition.__name__
        return f"WaitEvent({cname}.{fname})"

    def execute(self):
        pass

    def is_complete(self):
        return self.condition()


class CallEvent(Event):
    def __init__(self, func, *args):
        self.func = func
        self.args = args
        self.done = False

    def __str__(self):
        cname = self.func.__self__.__class__.__name__
        fname = self.func.__name__
        return f"CallEvent({cname}.{fname})"

    def execute(self):
        self.done = self.func(*self.args)

    def is_complete(self):
        return self.done
