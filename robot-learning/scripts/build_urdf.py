import re

SRC = "assets/am_arm200/am-arm200.urdf"
DST = "assets/am_arm200/am-arm200-ik.urdf"

AXES = {
    "shoulder_lift": "0 0 1",
    "wrist_roll": "0 0 -1",
}
TIP = """  <link name="gripper_tip" />
  <joint name="gripper_tip_joint" type="fixed">
    <parent link="left_Fixed_Jaw" />
    <child link="gripper_tip" />
    <origin xyz="0 0.07 0" rpy="0 0 0" />
  </joint>
"""

s = open(SRC).read()
for joint, axis in AXES.items():
    pat = r'(<joint\s+name="' + joint + r'".*?<axis\s+xyz=")[^"]*(")'
    s, n = re.subn(pat, r'\g<1>' + axis + r'\g<2>', s, count=1, flags=re.DOTALL)
    print(f"{joint}: axis -> {axis} (patched={n})")
if 'name="gripper_tip"' not in s:
    s = s.replace("</robot>", TIP + "</robot>")
    print("added gripper_tip")
open(SRC, "w").write(s)

ik, nv = re.subn(r"<visual>.*?</visual>\s*", "", s, flags=re.DOTALL)
ik, nc = re.subn(r"<collision>.*?</collision>\s*", "", ik, flags=re.DOTALL)
open(DST, "w").write(ik)
print(f"wrote {DST} ({nv} visual, {nc} collision blocks removed)")
