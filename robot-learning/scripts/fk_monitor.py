import time
import numpy as np
from lerobot.model.kinematics import RobotKinematics
from lerobot.robots.so_follower import SOFollower, SOFollowerRobotConfig

JOINTS = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_yaw", "wrist_roll"]

kin = RobotKinematics(
    urdf_path="assets/am_arm200/am-arm200-ik.urdf",
    target_frame_name="left_Fixed_Jaw",
    joint_names=JOINTS,
)
config = SOFollowerRobotConfig(
    port="/dev/tty.usbmodem5C931508261",
    id="my_follower",
    arm_profile="am-follower-6dof",
)
robot = SOFollower(config)
robot.connect()
robot.bus.disable_torque()
try:
    while True:
        pos = robot.bus.sync_read("Present_Position")
        q = np.array([pos[j] for j in JOINTS])
        T = kin.forward_kinematics(q)
        x, y, z = T[:3, 3] * 1000
        print("\033[H\033[J", end="")
        for j in JOINTS:
            print(f"{j:14s}{pos[j]:8.1f} deg")
        print(f"\nwrist point (mm): x={x:8.1f}  y={y:8.1f}  z={z:8.1f}")
        print("\nCtrl-C to stop.")
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    robot.disconnect()
