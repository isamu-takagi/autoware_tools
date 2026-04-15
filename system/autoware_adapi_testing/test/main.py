from autoware_adapi_testing.adapi import ADAPI
from autoware_adapi_testing.logic.event import CallEvent
from autoware_adapi_testing.logic.event import WaitEvent
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import PoseWithCovarianceStamped
from rclpy.clock import Clock


def generate_scenario(api: ADAPI, clock: Clock):
    return [
        WaitEvent(api.localization.state.is_received),
        CallEvent(api.localization.initialize.request, self_pose(clock)),
        WaitEvent(api.localization.state.is_initialized),
        WaitEvent(api.routing.state.is_received),
        CallEvent(api.routing.set_route_points.request, goal_pose(clock)),
        WaitEvent(api.routing.state.is_set),
        WaitEvent(api.operation_mode.state.is_autonomous_available),
        CallEvent(api.operation_mode.change_autonomous.request),
        WaitEvent(api.routing.state.is_arrived),
        # TODO: check vehicle position
    ]


def self_pose(clock: Clock):
    pose = PoseWithCovarianceStamped()
    pose.header.frame_id = "map"
    pose.header.stamp = clock.now().to_msg()
    pose.pose.pose.position.x = 3730.140869140625
    pose.pose.pose.position.y = 73727.7734375
    pose.pose.pose.position.z = 0.0
    pose.pose.pose.orientation.x = 0.0
    pose.pose.pose.orientation.y = 0.0
    pose.pose.pose.orientation.z = 0.24019710926824225
    pose.pose.pose.orientation.w = 0.970724136250449
    return pose


def goal_pose(clock: Clock):
    pose = PoseStamped()
    pose.header.frame_id = "map"
    pose.header.stamp = clock.now().to_msg()
    pose.pose.position.x = 3828.23974609375
    pose.pose.position.y = 73725.5078125
    pose.pose.position.z = 0.0
    pose.pose.orientation.x = 0.0
    pose.pose.orientation.y = 0.0
    pose.pose.orientation.z = -0.9701766104447044
    pose.pose.orientation.w = 0.24239914303896443
    return pose
