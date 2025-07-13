# symbolic_agent.py

import carla
import math

class SymbolicAgent:
    def __init__(self, vehicle, world):
        self.vehicle = vehicle
        self.map = world.get_map()

    def run_step(self):
        # Stop at red light
        traffic_light = self.vehicle.get_traffic_light()
        if traffic_light and traffic_light.get_state() == carla.TrafficLightState.Red:
            return carla.VehicleControl(throttle=0.0, brake=1.0)

        # Follow the next waypoint
        current_transform = self.vehicle.get_transform()
        location = current_transform.location
        waypoint = self.map.get_waypoint(location).next(2.0)[0]

        # Calculate steering angle
        steer = self._compute_steering(current_transform, waypoint.transform)

        # Basic forward driving with steering
        return carla.VehicleControl(throttle=0.4, steer=steer, brake=0.0)

    def _compute_steering(self, current_transform, target_transform):
        dx = target_transform.location.x - current_transform.location.x
        dy = target_transform.location.y - current_transform.location.y

        desired_yaw = math.atan2(dy, dx)
        current_yaw = math.radians(current_transform.rotation.yaw)

        angle_diff = desired_yaw - current_yaw
        angle_diff = math.atan2(math.sin(angle_diff), math.cos(angle_diff))  # Normalize angle

        steer = angle_diff / (math.pi / 2)  # Scale to [-1, 1]
        steer = max(-1.0, min(1.0, steer))  # Clamp
        return steer
