from PySide6.QtCore import (
    QSettings
)


class SettingsManager:

    def __init__(self):

        self.settings = QSettings(
            "PrasannaKumarPalika",
            "PLTBatchConverterPro"
        )

    # ===================================
    # Output Folder
    # ===================================

    def save_output_folder(
        self,
        value
    ):

        self.settings.setValue(
            "output_folder",
            value
        )

    def get_output_folder(self):

        return self.settings.value(
            "output_folder",
            ""
        )

    # ===================================
    # DPI
    # ===================================

    def save_dpi(
        self,
        value
    ):

        self.settings.setValue(
            "dpi",
            value
        )

    def get_dpi(self):

        return self.settings.value(
            "dpi",
            "600"
        )

    # ===================================
    # Output Format
    # ===================================

    def save_format(
        self,
        value
    ):

        self.settings.setValue(
            "format",
            value
        )

    def get_format(self):

        return self.settings.value(
            "format",
            "PNG"
        )

    # ===================================
    # Line Width
    # ===================================

    def save_line_width(
        self,
        value
    ):

        self.settings.setValue(
            "line_width",
            value
        )

    def get_line_width(self):

        return int(
            self.settings.value(
                "line_width",
                2
            )
        )

    # ===================================
    # Auto Open Folder
    # ===================================

    def save_auto_open(
        self,
        value
    ):

        self.settings.setValue(
            "auto_open",
            value
        )

    def get_auto_open(self):

        return self.settings.value(
            "auto_open",
            True,
            type=bool
        )

    # ===================================
    # Transparent PNG
    # ===================================

    def save_transparent_png(
        self,
        value
    ):

        self.settings.setValue(
            "transparent_png",
            value
        )

    def get_transparent_png(self):

        return self.settings.value(
            "transparent_png",
            False,
            type=bool
        )

    # ===================================
    # Window Geometry
    # ===================================

    def save_geometry(
        self,
        geometry
    ):

        self.settings.setValue(
            "geometry",
            geometry
        )

    def get_geometry(self):

        return self.settings.value(
            "geometry"
        )

    # ===================================
    # Theme
    # ===================================

    def save_theme(
        self,
        theme
    ):

        self.settings.setValue(
            "theme",
            theme
        )

    def get_theme(self):

        return self.settings.value(
            "theme",
            "Dark"
        )

    # ===================================
    # Last Used Folder
    # ===================================

    def save_last_folder(
        self,
        folder
    ):

        self.settings.setValue(
            "last_folder",
            folder
        )

    def get_last_folder(self):

        return self.settings.value(
            "last_folder",
            ""
        )

    # ===================================
    # Statistics
    # ===================================

    def save_total_converted(
        self,
        count
    ):

        self.settings.setValue(
            "total_converted",
            count
        )

    def get_total_converted(self):

        return int(
            self.settings.value(
                "total_converted",
                0
            )
        )

    # ===================================
    # Clear All Settings
    # ===================================

    def clear_all(self):

        self.settings.clear()