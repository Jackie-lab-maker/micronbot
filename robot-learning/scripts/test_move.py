import time
from lerobot.robots.so_follower import SOFollower, SOFollowerRobotConfig

config = SOFollowerRobotConfig(
    port="/dev/tty.usbmodem5C931508261",
    id="my_follower",
    arm_profile="am-follower-6dof",
)

robot = SOFollower(config)
robot.connect()
try:
    obs = robot.get_observation()
    start = {k: v for k, v in obs.items() if k.endswith(".pos")}
    print("start pan:", start["shoulder_pan.pos"])

    for i in range(1, 11):  # ease out by +5 units over ~0.5 s
        action = dict(start)
        action["shoulder_pan.pos"] = start["shoulder_pan.pos"] + 0.5 * i
        robot.send_action(action)
        time.sleep(0.05)
    time.sleep(1.0)

    for i in range(1, 11):  # ease back
        action = dict(start)
        action["shoulder_pan.pos"] = start["shoulder_pan.pos"] + 5 - 0.5 * i
        robot.send_action(action)
        time.sleep(0.05)
    print("done")
finally:
    robot.disconnect()
