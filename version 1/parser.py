"""
parser.py

Simple HPGL / ArtCAM PLT parser.

Supported commands

IN
SP
PU
PD
PA
"""

import re

#oka comment
def parse_plt(filename):

    with open(filename, "r") as f:
        hpgl = f.read()

    # Remove line breaks
    hpgl = hpgl.replace("\n", "")
    hpgl = hpgl.replace("\r", "")

    # Split commands
    commands = hpgl.split(";")

    lines = []

    current_x = 0
    current_y = 0

    pen_down = False

    for cmd in commands:

        cmd = cmd.strip()

        if not cmd:
            continue

        # -----------------------------
        # Ignore
        # -----------------------------

        if cmd.startswith("IN"):
            continue

        if cmd.startswith("SP"):
            continue

        # -----------------------------
        # Pen Up
        # -----------------------------

        if cmd.startswith("PU"):

            pen_down = False

            coords = cmd[2:].strip()

            if coords:

                nums = re.findall(r"-?\d+", coords)

                for i in range(0, len(nums), 2):

                    if i + 1 >= len(nums):
                        break

                    current_x = float(nums[i])
                    current_y = float(nums[i + 1])

            continue

        # -----------------------------
        # Pen Down
        # -----------------------------

        if cmd.startswith("PD"):

            coords = cmd[2:].strip()

            pen_down = True

            if not coords:
                continue

            nums = re.findall(r"-?\d+", coords)

            for i in range(0, len(nums), 2):

                if i + 1 >= len(nums):
                    break

                x = float(nums[i])
                y = float(nums[i + 1])

                lines.append(
                    (
                        (current_x, current_y),
                        (x, y)
                    )
                )

                current_x = x
                current_y = y

            continue

        # -----------------------------
        # Plot Absolute
        # -----------------------------

        if cmd.startswith("PA"):

            coords = cmd[2:].strip()

            if not coords:
                continue

            nums = re.findall(r"-?\d+", coords)

            for i in range(0, len(nums), 2):

                if i + 1 >= len(nums):
                    break

                x = float(nums[i])
                y = float(nums[i + 1])

                if pen_down:

                    lines.append(
                        (
                            (current_x, current_y),
                            (x, y)
                        )
                    )

                current_x = x
                current_y = y

    return lines