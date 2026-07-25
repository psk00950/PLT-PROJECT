import os

from PySide6.QtGui import (
    QImage,
    QPainter,
    QDesktopServices
)

from PySide6.QtCore import (
    QRectF,
    Qt,
    QUrl
)

from PySide6.QtPrintSupport import (
    QPrinter
)


MAX_IMAGE_SIZE = 30000


# =====================================
# MM TO PIXELS
# =====================================

def mm_to_pixels(
    mm,
    dpi
):

    return int(
        mm * dpi / 25.4
    )


# =====================================
# PNG / JPG EXPORT
# =====================================

def export_scene(

    scene,

    filename,

    dpi=600,

    border_mm=1.5,

    quality=95,

    transparent=False

):

    try:

        rect = scene.itemsBoundingRect()

        if rect.isEmpty():
            return False

        border = mm_to_pixels(
            border_mm,
            dpi
        )

        width = (
            int(rect.width())
            + border * 2
        )

        height = (
            int(rect.height())
            + border * 2
        )

        if width <= 0:
            return False

        if height <= 0:
            return False

        if width > MAX_IMAGE_SIZE:
            return False

        if height > MAX_IMAGE_SIZE:
            return False

        image = QImage(
            width,
            height,
            QImage.Format_ARGB32
        )

        if transparent:

            image.fill(
                Qt.transparent
            )

        else:

            image.fill(
                scene.backgroundBrush()
                .color()
            )

        image.setDotsPerMeterX(
            int(dpi / 25.4 * 1000)
        )

        image.setDotsPerMeterY(
            int(dpi / 25.4 * 1000)
        )

        painter = QPainter(
            image
        )

        painter.setRenderHint(
            QPainter.Antialiasing,
            True
        )

        painter.setRenderHint(
            QPainter.TextAntialiasing,
            True
        )

        target = QRectF(
            0,
            0,
            width,
            height
        )

        source = QRectF(
            rect.left() - border,
            rect.top() - border,
            rect.width() + border * 2,
            rect.height() + border * 2
        )

        scene.render(
            painter,
            target,
            source,
            Qt.KeepAspectRatio
        )

        painter.end()

        if filename.lower().endswith(
            ".png"
        ):

            return image.save(
                filename,
                "PNG"
            )

        return image.save(
            filename,
            "JPG",
            quality
        )

    except Exception:

        return False


# =====================================
# PDF EXPORT
# =====================================

def export_pdf(
    scene,
    filename
):

    try:

        printer = QPrinter(
            QPrinter.HighResolution
        )

        printer.setOutputFormat(
            QPrinter.PdfFormat
        )

        printer.setOutputFileName(
            filename
        )

        painter = QPainter(
            printer
        )

        scene.render(
            painter
        )

        painter.end()

        return True

    except Exception:

        return False


# =====================================
# CONVERSION REPORT
# =====================================

def generate_report(

    output_folder,

    success_count,

    failed_count,

    results

):

    report_file = os.path.join(
        output_folder,
        "Conversion_Report.txt"
    )

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "PLT Batch Converter Pro\n"
        )

        file.write(
            "Developed by Prasanna Kumar Palika\n"
        )

        file.write(
            "=================================\n\n"
        )

        file.write(
            f"Success : {success_count}\n"
        )

        file.write(
            f"Failed  : {failed_count}\n\n"
        )

        file.write(
            "DETAILS\n"
        )

        file.write(
            "---------------------------------\n"
        )

        for entry in results:

            file.write(
                entry + "\n"
            )

    return report_file


# =====================================
# OPEN OUTPUT FOLDER
# =====================================

def open_output_folder(
    folder
):

    if not os.path.exists(
        folder
    ):
        return

    QDesktopServices.openUrl(
        QUrl.fromLocalFile(
            folder
        )
    )


# =====================================
# FORMAT EXTENSION
# =====================================

def get_extension(
    output_format
):

    output_format = (
        output_format
        .strip()
        .upper()
    )

    if output_format == "PNG":
        return ".png"

    if output_format == "PDF":
        return ".pdf"

    return ".jpg"