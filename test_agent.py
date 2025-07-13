# main.py

import carla
import time
from symbolic_agent import SymbolicAgent  # ✅ Import your custom logic

client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()

# Get vehicle blueprint and spawn point
bp_lib = world.get_blueprint_library()
vehicle_bp = bp_lib.filter('vehicle.tesla.model3')[0]
spawn_point = world.get_map().get_spawn_points()[0]

# Spawn vehicle
vehicle = world.spawn_actor(vehicle_bp, spawn_point)
print("Vehicle spawned.")

# Turn off autopilot, use custom logic
agent = SymbolicAgent(vehicle,world)

print("Vehicle is driving using SymbolicAgent logic...")

try:
    for _ in range(1200):  # Run for ~60 seconds (20 FPS)
        control = agent.run_step()
        vehicle.apply_control(control)
        time.sleep(0.05)
finally:
    vehicle.destroy()
    print("Simulation done and vehicle destroyed.")
