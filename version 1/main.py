import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QGraphicsScene
)
# my first gits
from PySide6.QtGui import QColor

from parser import parse_plt
from renderer import Renderer
from exporter import export_scene
from graphicsview import GraphicsView
from toolbar import ViewerToolBar


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("HPGL / PLT Viewer")

        self.resize(1200, 800)

        # -------------------------------------
        # Scene
        # -------------------------------------

        self.scene = QGraphicsScene(self)

        self.view = GraphicsView(self.scene)

        self.setCentralWidget(self.view)

        # -------------------------------------
        # Renderer
        # -------------------------------------

        self.renderer = Renderer()

        self.lines = []

        self.current_file = None

        # -------------------------------------
        # Toolbar
        # -------------------------------------

        self.toolbar = ViewerToolBar(self)

        self.addToolBar(self.toolbar)

        self.connect_toolbar()

        # -------------------------------------
        # File Actions
        # -------------------------------------

        self.toolbar.actionOpen.triggered.connect(
            self.open_file
        )

        self.toolbar.actionExportPNG.triggered.connect(
            self.export_png
        )

        self.toolbar.actionExportJPG.triggered.connect(
            self.export_jpg
        )
            # =====================================================
    # Open PLT File
    # =====================================================

    def open_file(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open HPGL File",
            "",
            "HPGL Files (*.plt *.hpgl);;All Files (*)"
        )

        if not filename:
            return

        self.current_file = filename

        try:

            self.lines = parse_plt(filename)

            self.renderer.render(
                self.scene,
                self.lines
            )

            self.view.fit_drawing()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    # =====================================================
    # Export PNG
    # =====================================================

    def export_png(self):

        if not self.lines:
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export PNG",
            "",
            "PNG (*.png)"
        )

        if not filename:
            return

        if not filename.lower().endswith(".png"):
            filename += ".png"

        export_scene(
            self.scene,
            filename
        )

    # =====================================================
    # Export JPG
    # =====================================================

    def export_jpg(self):

        if not self.lines:
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export JPG",
            "",
            "JPEG (*.jpg)"
        )

        if not filename:
            return

        if not filename.lower().endswith(".jpg"):
            filename += ".jpg"

        export_scene(
            self.scene,
            filename
        )
            # =====================================================
    # Zoom In
    # =====================================================

    def zoom_in(self):

        self.view.zoom_in()

        self.toolbar.set_zoom_percent(
            self.view.current_zoom
        )

    # =====================================================
    # Zoom Out
    # =====================================================

    def zoom_out(self):

        self.view.zoom_out()

        self.toolbar.set_zoom_percent(
            self.view.current_zoom
        )

    # =====================================================
    # Set Zoom
    # =====================================================

    def set_zoom(self):

        zoom = self.toolbar.get_zoom_percent()

        self.view.set_zoom(zoom)

        self.toolbar.set_zoom_percent(
            self.view.current_zoom
        )

    # =====================================================
    # Actual Size (100%)
    # =====================================================

    def actual_size(self):

        self.view.actual_size()

        self.toolbar.set_zoom_percent(100)

    # =====================================================
    # Fit Drawing
    # =====================================================

    def fit_drawing(self):

        self.view.fit_drawing()

    # =====================================================
    # Line Colour
    # =====================================================

    def choose_line_colour(self):

        colour = self.toolbar.choose_color(
            self.renderer.get_line_color(),
            self
        )

        if colour is None:
            return

        self.renderer.set_line_color(colour)

        self.renderer.render(
            self.scene,
            self.lines
        )

    # =====================================================
    # Line Width
    # =====================================================

    def choose_line_width(self):

        width = self.toolbar.choose_line_width(
            self.renderer.get_line_width(),
            self
        )

        if width is None:
            return

        self.renderer.set_line_width(width)

        self.renderer.render(
            self.scene,
            self.lines
        )
            # =====================================================
    # Background Colour
    # =====================================================

    def choose_background(self):

        colour = self.toolbar.choose_color(
            self.scene.backgroundBrush().color(),
            self
        )

        if colour is None:
            return

        self.view.set_background_color(colour)

    # =====================================================
    # Dark Mode
    # =====================================================

    def dark_mode(self, checked):

        if checked:

            background = QColor(40, 40, 40)

            line = QColor(255, 255, 255)

        else:

            background = QColor(255, 255, 255)

            line = QColor(0, 0, 0)

        self.view.set_background_color(background)

        self.renderer.set_line_color(line)

        self.renderer.render(
            self.scene,
            self.lines
        )

    # =====================================================
    # Connect Toolbar
    # =====================================================

    def connect_toolbar(self):

        self.toolbar.actionZoomIn.triggered.connect(
            self.zoom_in
        )

        self.toolbar.actionZoomOut.triggered.connect(
            self.zoom_out
        )

        self.toolbar.zoomBox.currentTextChanged.connect(
            self.set_zoom
        )

        self.toolbar.actionFit.triggered.connect(
            self.fit_drawing
        )

        self.toolbar.actionActual.triggered.connect(
            self.actual_size
        )

        self.toolbar.actionLineColor.triggered.connect(
            self.choose_line_colour
        )

        self.toolbar.actionLineWidth.triggered.connect(
            self.choose_line_width
        )

        self.toolbar.actionBackground.triggered.connect(
            self.choose_background
        )

        self.toolbar.actionDarkMode.toggled.connect(
            self.dark_mode
        )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()

   ## window.connect_toolbar()

    window.show()

    sys.exit(app.exec())