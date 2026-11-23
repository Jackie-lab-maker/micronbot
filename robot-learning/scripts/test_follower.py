import numpy as np
import cv2
from lerobot.cameras.opencv import OpenCVCameraConfig
from lerobot.robots.so_follower import SOFollower, SOFollowerRobotConfig

config = SOFollowerRobotConfig(
    port="/dev/tty.usbmodem5C931508261",
    id="my_follower",
    arm_profile="am-follower-6dof",
    cameras={
        "camera2": OpenCVCameraConfig(index_or_path=2, width=640, height=480, fps=30),
    },
)

robot = SOFollower(config)
robot.connect()
try:
    obs = robot.get_observation()
    for key, value in obs.items():
        if isinstance(value, np.ndarray):
            print(f"{key}: image {value.shape}")
            cv2.imwrite("test_frame.png", value[:, :, ::-1])
        else:
            print(f"{key}: {value:.2f}")
finally:
    robot.disconnect()
