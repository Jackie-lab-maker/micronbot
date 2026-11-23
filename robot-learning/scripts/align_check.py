import numpy as np
import matplotlib
matplotlib.use("macosx")
import matplotlib.pyplot as plt
from lerobot.model.kinematics import RobotKinematics
from lerobot.robots.so_follower import SOFollower, SOFollowerRobotConfig

JOINTS = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_yaw", "wrist_roll"]
LINKS = ["left_Base", "left_Rotation_Pitch", "left_Upper_Arm", "left_Lower_Arm",
         "left_Wrist_Pitch_Roll", "left_wrist_yaw", "left_Fixed_Jaw", "gripper_tip"]

kin = RobotKinematics(
    urdf_path="assets/am_arm200/am-arm200-ik.urdf",
    target_frame_name="gripper_tip",
    joint_names=JOINTS,
)
robot = SOFollower(SOFollowerRobotConfig(
    port="/dev/tty.usbmodem5C931508261", id="my_follower", arm_profile="am-follower-6dof"))
robot.connect()
robot.bus.disable_torque()

plt.ion()
fig, (ax_side, ax_top) = plt.subplots(1, 2, figsize=(12, 6))

def draw(q):
    kin.forward_kinematics(q)
    Ts = [kin.robot.get_T_world_frame(n) for n in LINKS]
    P = np.array([T[:3, 3] for T in Ts]) * 1000
    T, o = Ts[-1], P[-1]
    views = ((ax_side, 1, 2, "y (mm)", "z (mm)", "side view"),
             (ax_top, 0, 1, "x (mm)", "y (mm)", "top view"))
    for ax, i, j, xl, yl, title in views:
        ax.cla()
        ax.plot(P[:, i], P[:, j], "k-o", lw=3)
        for col, c in enumerate("rgb"):
            d = T[:3, col] * 100
            ax.plot([o[i], o[i] + d[i]], [o[j], o[j] + d[j]], c, lw=3)
        ax.set_xlim(-450, 450); ax.set_ylim(-250, 450)
        ax.set_aspect("equal"); ax.grid(True)
        ax.set_xlabel(xl); ax.set_ylabel(yl); ax.set_title(title)
    fig.suptitle("  ".join(f"{n[:9]}={v:6.1f}" for n, v in zip(JOINTS, q)))
    plt.pause(0.001)

try:
    while plt.fignum_exists(fig.number):
        pos = robot.bus.sync_read("Present_Position")
        draw(np.array([pos[j] for j in JOINTS]))
except KeyboardInterrupt:
    pass
finally:
    robot.disconnect()
