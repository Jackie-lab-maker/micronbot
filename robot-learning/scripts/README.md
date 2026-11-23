# Scripts

Exact copies of the scripts used in the [setup log](../README.md), taken from the working `lerobot_alohamini` checkout.

They expect to live in the root of that checkout (they use relative paths such as `assets/am_arm200/...`), with `quest_teleop/` as a subfolder. Copy them there and run from that root:

```bash
cp robot-learning/scripts/*.py ~/lerobot_alohamini/
cp -r robot-learning/scripts/quest_teleop ~/lerobot_alohamini/
cd ~/lerobot_alohamini
python test_follower.py
```

`quest_teleop/server.py` also needs `cert.pem` and `key.pem` next to it. These are generated per machine (see Step 8 of the log) and are not stored in this repo.
