"""
PLT / HPGL Parser
#pk gadu thopu gadu
Supported Commands
------------------
IN  - Initialize
SP  - Select Pen
PU  - Pen Up
PD  - Pen Down
PA  - Plot Absolute

Returns:
[
    ((x1, y1), (x2, y2)),
    ((x3, y3), (x4, y4))
]
"""

import re


NUMBER_RE = re.compile(
    r"-?\d+"
)


# ==================================
# Parse Coordinate Pairs
# ==================================

def parse_coordinates(data):

    values = NUMBER_RE.findall(
        data
    )

    for index in range(
        0,
        len(values),
        2
    ):

        if index + 1 >= len(values):
            break

        x = float(
            values[index]
        )

        y = float(
            values[index + 1]
        )

        yield x, y


# ==================================
# Main Parser
# ==================================

def parse_plt(filename):

    with open(
        filename,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        hpgl = file.read()

    hpgl = hpgl.replace(
        "\n",
        ""
    )

    hpgl = hpgl.replace(
        "\r",
        ""
    )

    commands = hpgl.split(";")

    lines = []

    current_x = 0.0
    current_y = 0.0

    pen_down = False

    for command in commands:

        command = command.strip()

        if not command:
            continue

        # --------------------------
        # Initialize
        # --------------------------

        if command.startswith("IN"):

            current_x = 0.0
            current_y = 0.0

            pen_down = False

            continue

        # --------------------------
        # Select Pen
        # --------------------------

        if command.startswith("SP"):
            continue

        # --------------------------
        # Pen Up
        # --------------------------

        if command.startswith("PU"):

            pen_down = False

            coordinates = (
                command[2:]
                .strip()
            )

            if coordinates:

                for x, y in parse_coordinates(
                    coordinates
                ):

                    current_x = x
                    current_y = y

            continue

        # --------------------------
        # Pen Down
        # --------------------------

        if command.startswith("PD"):

            pen_down = True

            coordinates = (
                command[2:]
                .strip()
            )

            if not coordinates:
                continue

            for x, y in parse_coordinates(
                coordinates
            ):

                lines.append(
                    (
                        (
                            current_x,
                            current_y
                        ),
                        (
                            x,
                            y
                        )
                    )
                )

                current_x = x
                current_y = y

            continue

        # --------------------------
        # Plot Absolute
        # --------------------------

        if command.startswith("PA"):

            coordinates = (
                command[2:]
                .strip()
            )

            if not coordinates:
                continue

            for x, y in parse_coordinates(
                coordinates
            ):

                if pen_down:

                    lines.append(
                        (
                            (
                                current_x,
                                current_y
                            ),
                            (
                                x,
                                y
                            )
                        )
                    )

                current_x = x
                current_y = y

    return lines


# ==================================
# Drawing Statistics
# ==================================

def get_drawing_statistics(
    lines
):

    if not lines:

        return {

            "segments": 0,
            "width": 0,
            "height": 0

        }

    x_values = []
    y_values = []

    for start, end in lines:

        x_values.extend(
            [
                start[0],
                end[0]
            ]
        )

        y_values.extend(
            [
                start[1],
                end[1]
            ]
        )

    width = (
        max(x_values)
        - min(x_values)
    )

    height = (
        max(y_values)
        - min(y_values)
    )

    return {

        "segments": len(lines),

        "width": int(width),

        "height": int(height)

    }