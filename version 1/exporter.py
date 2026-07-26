from PySide6.QtGui import (
    QImage,
    QPainter,
    QColor
)

from PySide6.QtCore import (
    QRectF,
    Qt
)
# added this comment in line 11
#added this comment in line 12
def mm_to_pixels(mm, dpi):
    return int(mm * dpi / 25.4)


def export_scene(
    scene,
    filename,
    dpi=600,
    border_mm=1.5,
    quality=100
):

    rect = scene.itemsBoundingRect()

    if rect.isEmpty():
        return False

    # -----------------------------
    # Border
    # -----------------------------

    border = mm_to_pixels(border_mm, dpi)

    width = int(rect.width()) + border * 2
    height = int(rect.height()) + border * 2

    if width <= 0 or height <= 0:
        return False

    # -----------------------------
    # Image Format
    # -----------------------------

    if filename.lower().endswith(".png"):

        image = QImage(
            width,
            height,
            QImage.Format_ARGB32
        )

    else:

        image = QImage(
            width,
            height,
            QImage.Format_RGB32
        )

    # -----------------------------
    # Background
    # -----------------------------

    background = scene.backgroundBrush().color()

    image.fill(background)

    image.setDotsPerMeterX(int(dpi / 25.4 * 1000))
    image.setDotsPerMeterY(int(dpi / 25.4 * 1000))

    # -----------------------------
    # Paint
    # -----------------------------

    painter = QPainter(image)

    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.setRenderHint(QPainter.TextAntialiasing, True)
    painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

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

    # -----------------------------
    # Save
    # -----------------------------

    if filename.lower().endswith(".png"):

        return image.save(filename, "PNG")

    return image.save(
        filename,
        "JPG",
        quality
    )