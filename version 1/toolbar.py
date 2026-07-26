from PySide6.QtWidgets import (
    QToolBar,
    QColorDialog,
    QInputDialog,
    QComboBox
)

from PySide6.QtGui import QAction

# code change chedhama
class ViewerToolBar(QToolBar):

    def __init__(self, parent=None):

        super().__init__("Toolbar", parent)

        # -----------------------------
        # File
        # -----------------------------

        self.actionOpen = QAction("📂 Open", self)
        self.addAction(self.actionOpen)

        self.actionExportJPG = QAction("💾 JPG", self)
        self.addAction(self.actionExportJPG)

        self.actionExportPNG = QAction("🖼 PNG", self)
        self.addAction(self.actionExportPNG)

        self.addSeparator()

        # -----------------------------
        # Zoom
        # -----------------------------

        self.actionZoomIn = QAction("＋", self)
        self.addAction(self.actionZoomIn)

        self.actionZoomOut = QAction("－", self)
        self.addAction(self.actionZoomOut)

        # Editable Zoom Box
        self.zoomBox = QComboBox()

        self.zoomBox.setEditable(True)

        self.zoomBox.addItems([
            "25",
            "50",
            "75",
            "100",
            "125",
            "150",
            "200",
            "300",
            "400",
            "500",
            "750",
            "1000"
        ])

        self.zoomBox.setCurrentText("100")

        self.zoomBox.setMinimumWidth(80)

        self.addWidget(self.zoomBox)

        self.actionFit = QAction("Fit", self)
        self.addAction(self.actionFit)

        self.actionActual = QAction("100%", self)
        self.addAction(self.actionActual)

        self.addSeparator()

        # -----------------------------
        # Display
        # -----------------------------

        self.actionLineColor = QAction("🎨 Line", self)
        self.addAction(self.actionLineColor)

        self.actionLineWidth = QAction("📏 Width", self)
        self.addAction(self.actionLineWidth)

        self.actionBackground = QAction("🖼 Background", self)
        self.addAction(self.actionBackground)

        self.addSeparator()

        # -----------------------------
        # Theme
        # -----------------------------

        self.actionDarkMode = QAction("🌙 Dark", self)

        self.actionDarkMode.setCheckable(True)

        self.addAction(self.actionDarkMode)

    # ---------------------------------------------------

    def choose_color(self, current_color, parent):

        color = QColorDialog.getColor(
            current_color,
            parent,
            "Choose Colour"
        )

        if color.isValid():
            return color

        return None

    # ---------------------------------------------------

    def choose_line_width(self, current_width, parent):

        width, ok = QInputDialog.getInt(
            parent,
            "Line Width",
            "Enter line width",
            current_width,
            1,
            20
        )

        if ok:
            return width

        return None

    # ---------------------------------------------------

    def get_zoom_percent(self):

        try:

            return float(self.zoomBox.currentText())

        except:

            return 100.0

    # ---------------------------------------------------

    def set_zoom_percent(self, value):

        self.zoomBox.setCurrentText(str(int(value)))