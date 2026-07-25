import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPixmap,
    QIcon,
    QColor
)

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QListWidget,
    QLabel,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QProgressBar,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QColorDialog,
    QSpinBox,
    QComboBox,
    QRadioButton,
    QButtonGroup,
    QGraphicsScene,
    QSplashScreen,
    QMessageBox
)

from parser import (
    parse_plt,
    get_drawing_statistics
)

from renderer import Renderer

from graphicsview import GraphicsView

from exporter import (
    export_scene,
    export_pdf,
    generate_report,
    open_output_folder
)

from settings_manager import (
    SettingsManager
)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.settings = SettingsManager()

        self.renderer = Renderer()

        self.current_lines = []

        self.success_count = 0
        self.failed_count = 0

        self.setWindowTitle(
            "PLT Batch Converter Pro | Developed by Prasanna Kumar Palika"
        )

        self.setWindowIcon(
            QIcon("assets/icon.ico")
        )

        self.setAcceptDrops(True)

        self.build_ui()

        self.load_settings()

        self.showMaximized()

        self.statusBar().showMessage(
            "Ready"
        )

    # =================================
    # UI
    # =================================

    def build_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        root = QHBoxLayout(central)

        # LEFT

        left = QVBoxLayout()

        logo = QLabel()

        pix = QPixmap(
            "assets/logo.png"
        )

        pix = pix.scaled(
            120,
            120,
            Qt.KeepAspectRatio
        )

        logo.setPixmap(pix)

        logo.setAlignment(
            Qt.AlignCenter
        )

        left.addWidget(logo)

        title = QLabel(
            "PLT Batch Converter Pro"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet(
            "font-size:22px;"
            "font-weight:bold;"
            "color:#00BCF2;"
        )

        left.addWidget(title)

        dev = QLabel(
            "Developed by\nPrasanna Kumar Palika"
        )

        dev.setAlignment(
            Qt.AlignCenter
        )

        left.addWidget(dev)

        file_group = QGroupBox(
            "PLT Files"
        )

        file_layout = QVBoxLayout()

        self.file_list = QListWidget()

        file_layout.addWidget(
            self.file_list
        )

        row = QHBoxLayout()

        self.btn_add = QPushButton(
            "Add Files"
        )

        self.btn_remove = QPushButton(
            "Remove"
        )

        self.btn_clear = QPushButton(
            "Clear"
        )

        row.addWidget(
            self.btn_add
        )

        row.addWidget(
            self.btn_remove
        )

        row.addWidget(
            self.btn_clear
        )

        file_layout.addLayout(row)

        file_group.setLayout(
            file_layout
        )

        left.addWidget(
            file_group
        )

        root.addLayout(
            left,
            2
        )

        # RIGHT

        right = QVBoxLayout()

        self.stats_label = QLabel(
            "Select a PLT file"
        )

        right.addWidget(
            self.stats_label
        )

        self.scene = QGraphicsScene()

        self.view = GraphicsView(
            self.scene
        )

        right.addWidget(
            self.view,
            6
        )

        # Appearance

        appearance = QGroupBox(
            "Appearance"
        )

        ap = QHBoxLayout()

        self.btn_line_color = QPushButton(
            "Line Colour"
        )

        self.btn_bg = QPushButton(
            "Background"
        )

        self.line_width = QSpinBox()

        self.line_width.setRange(
            1,
            20
        )

        self.line_width.setValue(
            2
        )

        ap.addWidget(
            QLabel("Width")
        )

        ap.addWidget(
            self.line_width
        )

        ap.addWidget(
            self.btn_line_color
        )

        ap.addWidget(
            self.btn_bg
        )

        appearance.setLayout(ap)

        right.addWidget(
            appearance
        )

        # Output

        output = QGroupBox(
            "Output"
        )

        op = QVBoxLayout()

        self.radio_png = QRadioButton(
            "PNG"
        )

        self.radio_jpg = QRadioButton(
            "JPG"
        )

        self.radio_pdf = QRadioButton(
            "PDF"
        )

        self.radio_png.setChecked(
            True
        )

        fmt = QHBoxLayout()

        fmt.addWidget(
            self.radio_png
        )

        fmt.addWidget(
            self.radio_jpg
        )

        fmt.addWidget(
            self.radio_pdf
        )

        op.addLayout(fmt)

        self.dpi_combo = QComboBox()

        self.dpi_combo.addItems(
            [
                "150",
                "300",
                "600",
                "1200"
            ]
        )

        op.addWidget(
            self.dpi_combo
        )

        folder_row = QHBoxLayout()

        self.output_folder = QLineEdit()

        self.btn_folder = QPushButton(
            "Browse"
        )

        self.btn_open_folder = QPushButton(
            "Open"
        )

        folder_row.addWidget(
            self.output_folder
        )

        folder_row.addWidget(
            self.btn_folder
        )

        folder_row.addWidget(
            self.btn_open_folder
        )

        op.addLayout(
            folder_row
        )

        output.setLayout(op)

        right.addWidget(output)

        self.progress = QProgressBar()

        right.addWidget(
            self.progress
        )

        self.progress_label = QLabel(
            "Ready"
        )

        right.addWidget(
            self.progress_label
        )

        self.log = QTextEdit()

        self.log.setReadOnly(True)

        right.addWidget(
            self.log
        )

        log_row = QHBoxLayout()

        self.btn_clear_logs = QPushButton(
            "Clear Logs"
        )

        log_row.addWidget(
            self.btn_clear_logs
        )

        right.addLayout(
            log_row
        )

        self.btn_convert = QPushButton(
            "🚀 Convert All"
        )

        right.addWidget(
            self.btn_convert
        )

        root.addLayout(
            right,
            5
        )

        # EVENTS

        self.btn_add.clicked.connect(
            self.add_files
        )

        self.btn_remove.clicked.connect(
            self.remove_selected
        )

        self.btn_clear.clicked.connect(
            self.file_list.clear
        )

        self.btn_folder.clicked.connect(
            self.select_folder
        )

        self.btn_open_folder.clicked.connect(
            self.open_folder
        )

        self.btn_convert.clicked.connect(
            self.convert_all
        )

        self.file_list.currentRowChanged.connect(
            self.preview_file
        )

        self.btn_line_color.clicked.connect(
            self.choose_line_color
        )

        self.btn_bg.clicked.connect(
            self.choose_background
        )

        self.btn_clear_logs.clicked.connect(
            self.log.clear
        )

    def add_files(self):

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "PLT Files",
            "",
            "PLT (*.plt *.hpgl)"
        )

        existing = set(
            self.file_list.item(i).text()
            for i in range(
                self.file_list.count()
            )
        )

        for file in files:

            if file not in existing:

                self.file_list.addItem(
                    file
                )

        if self.file_list.count() > 0:
            self.file_list.setCurrentRow(0)

    def preview_file(self):

        item = self.file_list.currentItem()

        if not item:
            return

        filename = item.text()

        self.current_lines = parse_plt(
            filename
        )

        self.renderer.render(
            self.scene,
            self.current_lines
        )

        self.view.fit_drawing()

        stats = get_drawing_statistics(
            self.current_lines
        )

        size_mb = (
            os.path.getsize(filename)
            / (1024 * 1024)
        )

        self.stats_label.setText(
            f"File: {os.path.basename(filename)} | "
            f"Segments: {stats['segments']:,} | "
            f"Size: {size_mb:.2f} MB | "
            f"W: {stats['width']} | "
            f"H: {stats['height']}"
        )

    def choose_line_color(self):

        color = QColorDialog.getColor()

        if color.isValid():

            self.renderer.set_line_color(
                color
            )

            self.preview_file()

    def choose_background(self):

        color = QColorDialog.getColor()

        if color.isValid():

            self.view.set_background_color(
                color
            )

    def select_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Output Folder"
        )

        if folder:

            self.output_folder.setText(
                folder
            )

    def open_folder(self):

        folder = self.output_folder.text()

        if folder:
            open_output_folder(folder)

    def remove_selected(self):

        row = self.file_list.currentRow()

        if row >= 0:
            self.file_list.takeItem(row)

    def convert_all(self):

        total = self.file_list.count()

        if total == 0:
            return

        output_folder = self.output_folder.text()

        if not output_folder:
            QMessageBox.warning(
                self,
                "Output Folder",
                "Select output folder"
            )
            return

        self.success_count = 0
        self.failed_count = 0

        results = []

        dpi = int(
            self.dpi_combo.currentText()
        )

        for i in range(total):

            file = self.file_list.item(i).text()

            try:

                lines = parse_plt(file)

                scene = QGraphicsScene()

                renderer = Renderer()

                renderer.set_line_color(
                    self.renderer.get_line_color()
                )

                renderer.set_line_width(
                    self.line_width.value()
                )

                renderer.render(
                    scene,
                    lines
                )

                name = os.path.splitext(
                    os.path.basename(file)
                )[0]

                if self.radio_png.isChecked():

                    target = os.path.join(
                        output_folder,
                        name + ".png"
                    )

                    export_scene(
                        scene,
                        target,
                        dpi=dpi
                    )

                elif self.radio_jpg.isChecked():

                    target = os.path.join(
                        output_folder,
                        name + ".jpg"
                    )

                    export_scene(
                        scene,
                        target,
                        dpi=dpi
                    )

                else:

                    target = os.path.join(
                        output_folder,
                        name + ".pdf"
                    )

                    export_pdf(
                        scene,
                        target
                    )

                self.success_count += 1

                results.append(
                    f"SUCCESS: {file}"
                )

            except Exception:

                self.failed_count += 1

                results.append(
                    f"FAILED: {file}"
                )

            pct = int(
                ((i + 1) / total) * 100
            )

            remaining = (
                total - (i + 1)
            )

            self.progress.setValue(
                pct
            )

            self.progress_label.setText(
                f"Processing {i+1}/{total} | Remaining {remaining}"
            )

            QApplication.processEvents()

        generate_report(
            output_folder,
            self.success_count,
            self.failed_count,
            results
        )

        self.statusBar().showMessage(
            "Conversion completed"
        )

    def load_settings(self):

        self.output_folder.setText(
            self.settings.get_output_folder()
        )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    splash = QSplashScreen(
        QPixmap("assets/logo.png")
    )

    splash.showMessage(
        "PLT Batch Converter Pro\nDeveloped by Prasanna Kumar Palika",
        Qt.AlignBottom | Qt.AlignCenter,
        Qt.white
    )

    splash.show()

    app.processEvents()

    window = MainWindow()

    window.show()

    splash.finish(window)

    sys.exit(app.exec())