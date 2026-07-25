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

        self.pen = QPen(QColor(0, 0, 0))

        self.pen.setWidth(3)

        self.pen.setCapStyle(Qt.RoundCap)

        self.pen.setJoinStyle(Qt.RoundJoin)

        self.pen.setCosmetic(False)

    # -------------------------------------------------
    # Line Colour
    # -------------------------------------------------

    def set_line_color(self, color):

        self.pen.setColor(color)

    def get_line_color(self):

        return self.pen.color()

    # -------------------------------------------------
    # Line Width
    # -------------------------------------------------

    def set_line_width(self, width):

        self.pen.setWidth(width)

    def get_line_width(self):

        return self.pen.width()

    # -------------------------------------------------
    # Render
    # -------------------------------------------------

    def render(self, scene, lines):

        scene.clear()

        if not lines:
            return

        path = QPainterPath()

        first = True

        for start, end in lines:

            if first:

                path.moveTo(start[0], start[1])

                first = False

            else:

                path.moveTo(start[0], start[1])

            path.lineTo(end[0], end[1])

        item = QGraphicsPathItem(path)

        item.setPen(self.pen)

        scene.addItem(item)

    # -------------------------------------------------
    # Fit View
    # -------------------------------------------------

    def fit_view(self, view, scene):

        rect = scene.itemsBoundingRect()

        if rect.isEmpty():
            return

        view.fitInView(
            rect,
            Qt.KeepAspectRatio
        )