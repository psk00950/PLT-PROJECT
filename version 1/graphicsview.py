from PySide6.QtWidgets import QGraphicsView
from PySide6.QtGui import QPainter, QMouseEvent
from PySide6.QtCore import Qt


class GraphicsView(QGraphicsView):

    def __init__(self, scene):
        super().__init__(scene)

        # ---------------------------------
        # Rendering
        # ---------------------------------

        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.TextAntialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)

        self.setTransformationAnchor(
            QGraphicsView.AnchorUnderMouse
        )

        self.setResizeAnchor(
            QGraphicsView.AnchorUnderMouse
        )

        self.setViewportUpdateMode(
            QGraphicsView.FullViewportUpdate
        )

        self.setDragMode(
            QGraphicsView.NoDrag
        )

        self.setBackgroundBrush(Qt.white)

        # ---------------------------------
        # Zoom
        # ---------------------------------

        self.zoom_step = 1.20

        self.current_zoom = 100.0

        # ---------------------------------
        # Panning
        # ---------------------------------

        self.panning = False

        self.pan_start = None

    # =====================================================
    # Mouse Wheel
    # =====================================================

    def wheelEvent(self, event):

        if event.angleDelta().y() > 0:

            self.zoom_in()

        else:

            self.zoom_out()

    # =====================================================
    # Zoom In
    # =====================================================

    def zoom_in(self):

        self.scale(
            self.zoom_step,
            self.zoom_step
        )

        self.current_zoom *= self.zoom_step

    # =====================================================
    # Zoom Out
    # =====================================================

    def zoom_out(self):

        self.scale(
            1 / self.zoom_step,
            1 / self.zoom_step
        )

        self.current_zoom /= self.zoom_step

    # =====================================================
    # Set Zoom Percentage
    # =====================================================

    def set_zoom(self, percent):

        if percent <= 0:
            return

        self.resetTransform()

        factor = percent / 100.0

        self.scale(
            factor,
            factor
        )

        self.current_zoom = percent

    # =====================================================
    # 100%
    # =====================================================

    def actual_size(self):

        self.set_zoom(100)

    # =====================================================
    # Fit Drawing
    # =====================================================

    def fit_drawing(self):

        rect = self.scene().itemsBoundingRect()

        if rect.isEmpty():
            return

        self.fitInView(
            rect,
            Qt.KeepAspectRatio
        )

    # =====================================================
    # Background Colour
    # =====================================================

    def set_background_color(self, color):

        self.setBackgroundBrush(color)

        self.scene().setBackgroundBrush(color)

    # =====================================================
    # Mouse Press
    # =====================================================

    def mousePressEvent(self, event: QMouseEvent):

        if event.button() == Qt.MiddleButton:

            self.panning = True

            self.pan_start = event.pos()

            self.setCursor(
                Qt.ClosedHandCursor
            )

            event.accept()

            return

        super().mousePressEvent(event)

    # =====================================================
    # Mouse Move
    # =====================================================

    def mouseMoveEvent(self, event: QMouseEvent):

        if self.panning:

            delta = event.pos() - self.pan_start

            self.pan_start = event.pos()

            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x()
            )

            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y()
            )

            event.accept()

            return

        super().mouseMoveEvent(event)

    # =====================================================
    # Mouse Release
    # =====================================================

    def mouseReleaseEvent(self, event: QMouseEvent):

        if event.button() == Qt.MiddleButton:

            self.panning = False

            self.setCursor(
                Qt.ArrowCursor
            )

            event.accept()

            return

        super().mouseReleaseEvent(event)

    # =====================================================
    # Double Click
    # =====================================================

    def mouseDoubleClickEvent(self, event):

        self.fit_drawing()

        super().mouseDoubleClickEvent(event)