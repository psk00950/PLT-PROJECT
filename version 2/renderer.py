from PySide6.QtGui import (
    QPainterPath,
    QPen,
    QColor
)

from PySide6.QtWidgets import (
    QGraphicsPathItem
)

from PySide6.QtCore import Qt


class Renderer:

    def __init__(self):

        self.pen = QPen(
            QColor(0, 0, 0)
        )

        self.pen.setWidth(2)

        self.pen.setCapStyle(
            Qt.RoundCap
        )

        self.pen.setJoinStyle(
            Qt.RoundJoin
        )

        # Line width stays constant
        # during zoom
        self.pen.setCosmetic(True)

    # =====================================
    # Line Colour
    # =====================================

    def set_line_color(
        self,
        color
    ):

        self.pen.setColor(color)

    def get_line_color(self):

        return self.pen.color()

    # =====================================
    # Line Width
    # =====================================

    def set_line_width(
        self,
        width
    ):

        self.pen.setWidth(width)

    def get_line_width(self):

        return self.pen.width()

    # =====================================
    # Render Drawing
    # =====================================

    def render(
        self,
        scene,
        lines
    ):

        scene.clear()

        if not lines:
            return

        path = QPainterPath()

        for start, end in lines:

            path.moveTo(
                start[0],
                start[1]
            )

            path.lineTo(
                end[0],
                end[1]
            )

        item = QGraphicsPathItem(
            path
        )

        item.setPen(
            self.pen
        )

        scene.addItem(
            item
        )

    # =====================================
    # Calculate Statistics
    # =====================================

    def get_statistics(
        self,
        lines,
        file_size_mb=0
    ):

        if not lines:

            return {

                "segments": 0,
                "width": 0,
                "height": 0,
                "file_size": f"{file_size_mb:.2f} MB"

            }

        xs = []
        ys = []

        for start, end in lines:

            xs.extend(
                [
                    start[0],
                    end[0]
                ]
            )

            ys.extend(
                [
                    start[1],
                    end[1]
                ]
            )

        width = (
            max(xs)
            - min(xs)
        )

        height = (
            max(ys)
            - min(ys)
        )

        return {

            "segments": len(lines),

            "width": int(width),

            "height": int(height),

            "file_size": f"{file_size_mb:.2f} MB"

        }

    # =====================================
    # Calculate Bounds
    # =====================================

    def get_bounds(
        self,
        lines
    ):

        if not lines:
            return None

        xs = []
        ys = []

        for start, end in lines:

            xs.extend(
                [
                    start[0],
                    end[0]
                ]
            )

            ys.extend(
                [
                    start[1],
                    end[1]
                ]
            )

        return {

            "min_x": min(xs),
            "max_x": max(xs),

            "min_y": min(ys),
            "max_y": max(ys)

        }

    # =====================================
    # Clear Scene
    # =====================================

    def clear_scene(
        self,
        scene
    ):

        scene.clear()