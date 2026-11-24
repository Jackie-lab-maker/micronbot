# Hardware

Hardware notes for MicronBot: bill of materials, wiring, CAD and print files, photos, and assembly notes.

## What is known so far

| Item | Detail |
| --- | --- |
| Base | AlohaMini2 mobile base, 3D printed, with three base wheel servos and a motorized lift |
| Arms | Two AM-ARM200 arms (standard, not Pro) |
| Compute | Raspberry Pi 5 on the robot (Trial 2), with a 12V to 5V converter |
| Servo adapters | Three: left arm, right arm, mobile base (the stock software expects two, with the base and lift on the left arm's bus) |
| Cameras | Five: one on each arm, one on the lifter chest, two on the head |
| Teleoperation | Meta Quest 3 controllers as a fake leader arm |

The USB layout for three adapters and five cameras on the Pi's four ports is not confirmed yet.

## Suggested layout

- `bom/` bill of materials
- `wiring/` wiring diagrams and port maps
- `cad/` CAD and print files
- `photos/` build photos
