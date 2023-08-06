import cv2 as cv
import mnd_utils.image
from PySide2 import QtWidgets, QtCore
from PySide2 import QtGui
import qimage2ndarray

from mnd_qtutils.image_edit_layout import ImageEditLayout


class ImageEditWidget(QtWidgets.QWidget):

    def __init__(self, zoom_sensitivity=0.1,  parent=None):
        super(ImageEditWidget, self).__init__(parent=parent)

        self._zoom_sensitivity = zoom_sensitivity
        self._image = None

        self._drag_start_position = None

        self._layout: ImageEditLayout = ImageEditLayout(1, 1)
        self._layout.eventGeometryChanged.connect(self._update_image)

        self._image_label = QtWidgets.QLabel()
        self._layout.addWidget(self._image_label)

        self.setLayout(self._layout)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        angle_delta = event.angleDelta().y()
        degrees = angle_delta / 8
        steps = degrees / 15

        zoom_amount = steps * self._zoom_sensitivity
        self._layout.add_zoom(zoom_amount)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MiddleButton:
            self._drag_start_position = event.pos()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if event.buttons() != QtCore.Qt.MiddleButton:
            return
        pos = event.pos()
        delta = pos - self._drag_start_position
        self._layout.add_center_offset(delta.x(), delta.y())
        self._drag_start_position = pos

    def map_widget_position_to_relative_image_position(self, position: QtCore.QPoint):
        widget_pos = self._image_label.pos()
        widget_size = self._image_label.size()
        relative_x = (position.x() - widget_pos.x()) / widget_size.width()
        relative_y = (position.y() - widget_pos.y()) / widget_size.height()
        return relative_x, relative_y

    def set_image(self, img):
        self._image = img
        h, w = img.shape[:2]
        ratio = w / h
        self._layout.ratio = ratio
        self._update_image()

    def _update_image(self):
        if self._image is None:
            return
        size = self._image_label.size()
        img = cv.cvtColor(self._image, cv.COLOR_BGR2RGB)
        img = mnd_utils.image.fit_in_size(img, (size.width(), size.height()))
        image = qimage2ndarray.array2qimage(img)
        self._image_label.setPixmap(QtGui.QPixmap.fromImage(image))


if __name__ == '__main__':
    import sys
    import mnd_utils.misc

    app = QtWidgets.QApplication(sys.argv)

    window = ImageEditWidget()
    window.setMinimumSize(400, 400)

    img = mnd_utils.misc.test_img()
    window.set_image(img)

    window.show()

    sys.exit(app.exec_())
