import json, math, re
from pathlib import Path

cal_path = Path.home() / ".cache/huggingface/lerobot/calibration/robots/so_follower/my_follower.json"
urdf_path = Path("assets/am_arm200/am-arm200.urdf")
cal = json.load(open(cal_path))
s = urdf_path.read_text()

for joint in ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_yaw"]:
    lo, hi = cal[joint]["range_min"], cal[joint]["range_max"]
    half_deg = (hi - lo) / 2 * 360 / 4095
    half_rad = math.radians(half_deg)
    pat = r'(<joint\s+name="' + joint + r'".*?<limit\s+lower=")[^"]+("\s+upper=")[^"]+(")'
    s, n = re.subn(pat, rf'\g<1>{-half_rad:.4f}\g<2>{half_rad:.4f}\g<3>', s, count=1, flags=re.DOTALL)
    print(f"{joint}: +/-{half_deg:.1f} deg  patched={n}")

urdf_path.write_text(s)
