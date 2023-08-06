from PySide2 import QtWidgets, QtCore
from typing import Optional


class ImageEditLayout(QtWidgets.QLayout):

    eventGeometryChanged = QtCore.Signal()

    minimum_zoom = 0.05

    def __init__(self, ratio: float, zoom: float = 1, parent: QtWidgets.QWidget = None):
        super(ImageEditLayout, self).__init__(parent=parent)
        self._ratio = ratio
        self._zoom = zoom
        self._center_offset_x = 0
        self._center_offset_y = 0
        self._item: Optional[QtWidgets.QLayoutItem] = None

    @property
    def ratio(self):
        return self._ratio

    @ratio.setter
    def ratio(self, value):
        self._ratio = value
        self.update()

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        self._zoom = value
        self._zoom = max(self._zoom, self.minimum_zoom)
        self.update()

    def add_zoom(self, amount: float):
        self.zoom += amount

    def add_center_offset(self, offset_x, offset_y):
        self._center_offset_x += offset_x
        self._center_offset_y += offset_y
        self.update()

    def _have_item(self) -> bool:
        return self._item is not None

    def _center_to_topleft(self, container_width, container_height, item_width, item_height, container_x, container_y):
        left = (container_width - item_width) / 2 + container_x
        top = (container_height - item_height) / 2 + container_y
        return left, top

# QLayout overrides ****************************************************************************************************

    def addItem(self, item: QtWidgets.QLayoutItem):
        if not self._have_item():
            self._item = item

    def count(self) -> int:
        count = 1 if self._have_item() else 0
        return count

    def setGeometry(self, geometry: QtCore.QRect):
        super(ImageEditLayout, self).setGeometry(geometry)

        if not self._have_item():
            return

        geom_height = geometry.height()
        geom_width = geometry.width()

        geom_half_width = geom_width / 2
        geom_half_height = geom_height / 2

        item_height = geom_height * self._zoom
        item_width = item_height * self._ratio

        item_half_width = item_width / 2
        item_half_height = item_height / 2

        # clamp offsets
        if item_width > geom_half_width:
            self._center_offset_x = max(self._center_offset_x, -item_half_width)
            self._center_offset_x = min(self._center_offset_x, item_half_width)
        else:
            self._center_offset_x = max(self._center_offset_x, -(geom_half_width - item_half_width))
            self._center_offset_x = min(self._center_offset_x, geom_half_width - item_half_width)

        if item_height > geom_half_height:
            self._center_offset_y = max(self._center_offset_y, -item_half_height)
            self._center_offset_y = min(self._center_offset_y, item_half_height)
        else:
            self._center_offset_y = max(self._center_offset_y, -(geom_half_height - item_half_height))
            self._center_offset_y = min(self._center_offset_y, geom_half_height - item_half_height)

        item_x = geometry.x() + geom_half_width - item_half_width + self._center_offset_x
        item_y = geometry.y() + geom_half_height - item_half_height + self._center_offset_y
        item_height = round(item_height)
        item_width = round(item_width)
        item_x = round(item_x)
        item_y = round(item_y)

        item_geom = QtCore.QRect(0, 0, item_width, item_height)
        self._item.setGeometry(item_geom)
        self._item.widget().move(item_x, item_y)
        self.eventGeometryChanged.emit()

    def sizeHint(self) -> QtCore.QSize:
        size = QtCore.QSize(0, 0)

        if self._have_item():
            item_size_hint = self._item.sizeHint()
            height_hint = round(item_size_hint.height() / self.zoom)
            size.setHeight(height_hint)
            size.setWidth(item_size_hint.width())

        return size

    def minimumSize(self) -> QtCore.QSize:
        size = QtCore.QSize(0, 0)

        if self._have_item():
            size = self._item.minimumSize()

        return size

    def itemAt(self, index: int) -> QtWidgets.QLayoutItem:
        if index < self.count():
            return self._item
        return None

    def takeAt(self, index: int) -> QtWidgets.QLayoutItem:
        item = self._item
        self._item = None
        return item

# **********************************************************************************************************************
