import cv2 as cv
from PySide2 import QtGui
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QLabel, QSizePolicy
import qimage2ndarray

import mnd_utils.image
import mnd_utils.misc


class AspectRatioImage(QLabel):

    def __init__(self, ratio=1.0, height_controls_width=True, parent=None):
        super(AspectRatioImage, self).__init__(parent=parent)
        self.ratio = ratio
        self.height_controls_width = height_controls_width
        self.adjusted_to_size = (-1, -1)

        if height_controls_width:
            self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored))
        else:
            self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred))

        self.image = None

    def resizeEvent(self, event: QtGui.QResizeEvent):
        event.accept()

        size = event.size()
        if size == self.adjusted_to_size:  # avoid possible infinite recursion loop
            return
        self.adjusted_to_size = size

        width = size.width()
        height = size.height()
        if self.height_controls_width:
            width = round(height * self.ratio)
        else:
            height = round(width * self.ratio)

        self.resize(width, height)

        if self.image is not None:
            self.set_image(self.image)

    def set_image(self, img):
        self.image = img
        size = self.size()
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img = mnd_utils.image.fit_in_size(img, (size.width(), size.height()))
        image = qimage2ndarray.array2qimage(img)
        self.setPixmap(QPixmap.fromImage(image))


if __name__ == '__main__':
    import sys
    from PySide2 import QtWidgets
    from PySide2.QtWidgets import QWidget, QApplication, QFrame

    app = QApplication(sys.argv)

    window = QWidget()
    window.setMinimumSize(100, 100)

    hlayout = QtWidgets.QHBoxLayout()
    vlayout = QtWidgets.QVBoxLayout()
    label = QLabel('Hello world')
    label.setFrameStyle(QFrame.Box)
    label.setLineWidth(2)
    arimg1 = AspectRatioImage(ratio=1, height_controls_width=True)
    arimg1.set_image(mnd_utils.misc.test_img(1))
    arimg2 = AspectRatioImage(ratio=0.1, height_controls_width=False)
    arimg2.set_image(mnd_utils.misc.test_img(2))
    widget = QWidget()
    widget.setLayout(vlayout)

    hlayout.addWidget(arimg1)
    hlayout.addWidget(label)
    hlayout.addStretch()
    hlayout.addWidget(widget)
    vlayout.addWidget(arimg2)
    window.setLayout(hlayout)

    window.show()

    sys.exit(app.exec_())
