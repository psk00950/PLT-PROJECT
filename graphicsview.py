from PySide6.QtWidgets import (
    QGraphicsView
)

from PySide6.QtGui import (
    QPainter
)

from PySide6.QtCore import (
    Qt
)


class GraphicsView(QGraphicsView):

    MIN_ZOOM = 0.05
    MAX_ZOOM = 50.0

    def __init__(self, scene):

        super().__init__(scene)

        # =================================
        # Rendering Quality
        # =================================

        self.setRenderHint(
            QPainter.Antialiasing,
            True
        )

        self.setRenderHint(
            QPainter.TextAntialiasing,
            True
        )

        self.setRenderHint(
            QPainter.SmoothPixmapTransform,
            True
        )

        # =================================
        # Zoom Behaviour
        # =================================

        self.zoom_factor = 1.15

        self.current_zoom = 1.0

        self.setTransformationAnchor(
            QGraphicsView.AnchorUnderMouse
        )

        self.setResizeAnchor(
            QGraphicsView.AnchorUnderMouse
        )

        # =================================
        # Background
        # =================================

        self.setBackgroundBrush(
            Qt.white
        )

        # =================================
        # Drag & Drop Support
        # =================================

        self.setAcceptDrops(True)

        # =================================
        # Panning
        # =================================

        self.panning = False

        self.pan_start = None

    # =================================
    # Zoom Using Mouse Wheel
    # =================================

    def wheelEvent(self, event):

        if event.angleDelta().y() > 0:

            if self.current_zoom < self.MAX_ZOOM:

                self.scale(
                    self.zoom_factor,
                    self.zoom_factor
                )

                self.current_zoom *= (
                    self.zoom_factor
                )

        else:

            if self.current_zoom > self.MIN_ZOOM:

                self.scale(
                    1 / self.zoom_factor,
                    1 / self.zoom_factor
                )

                self.current_zoom /= (
                    self.zoom_factor
                )

    # =================================
    # Fit Drawing
    # =================================

    def fit_drawing(self):

        rect = (
            self.scene()
            .itemsBoundingRect()
        )

        if rect.isEmpty():
            return

        self.fitInView(
            rect,
            Qt.KeepAspectRatio
        )

        self.current_zoom = 1.0

    # =================================
    # Actual Size
    # =================================

    def actual_size(self):

        self.resetTransform()

        self.current_zoom = 1.0

    # =================================
    # Set Background Color
    # =================================

    def set_background_color(
        self,
        color
    ):

        self.setBackgroundBrush(
            color
        )

        self.scene().setBackgroundBrush(
            color
        )

    # =================================
    # Mouse Press
    # =================================

    def mousePressEvent(
        self,
        event
    ):

        if (
            event.button()
            == Qt.MiddleButton
        ):

            self.panning = True

            self.pan_start = (
                event.pos()
            )

            self.setCursor(
                Qt.ClosedHandCursor
            )

            return

        super().mousePressEvent(
            event
        )

    # =================================
    # Mouse Move
    # =================================

    def mouseMoveEvent(
        self,
        event
    ):

        if self.panning:

            delta = (
                event.pos()
                - self.pan_start
            )

            self.pan_start = (
                event.pos()
            )

            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value()
                - delta.x()
            )

            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value()
                - delta.y()
            )

            return

        super().mouseMoveEvent(
            event
        )

    # =================================
    # Mouse Release
    # =================================

    def mouseReleaseEvent(
        self,
        event
    ):

        if (
            event.button()
            == Qt.MiddleButton
        ):

            self.panning = False

            self.setCursor(
                Qt.ArrowCursor
            )

            return

        super().mouseReleaseEvent(
            event
        )

    # =================================
    # Double Click = Fit Drawing
    # =================================

    def mouseDoubleClickEvent(
        self,
        event
    ):

        self.fit_drawing()

        super().mouseDoubleClickEvent(
            event
        )

    # =================================
    # Drag Enter
    # =================================

    def dragEnterEvent(
        self,
        event
    ):

        if event.mimeData().hasUrls():

            event.acceptProposedAction()

        else:

            event.ignore()

    # =================================
    # Drag Move
    # =================================

    def dragMoveEvent(
        self,
        event
    ):

        if event.mimeData().hasUrls():

            event.acceptProposedAction()

        else:

            event.ignore()