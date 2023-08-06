import cv2 as cv
import numpy as np
import qimage2ndarray
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QFile
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtUiTools import QUiLoader


def import_from_ui_file(ui_file_path: str):
	ui_file = QFile(ui_file_path)
	ui_file.open(QFile.ReadOnly)
	loader = QUiLoader()
	return loader.load(ui_file)


def setup_widget_from_ui(ui_file_path: str, parent: QtWidgets.QWidget):
	widget = import_from_ui_file(ui_file_path)

	layout = QtWidgets.QVBoxLayout()
	layout.setContentsMargins(0, 0, 0, 0)
	parent.setLayout(layout)
	layout.addWidget(widget)

	return widget


def setup_widget_from_py_ui(pyui_file_path: str, parent: QtWidgets.QWidget):
	widget = import_from_ui_file(pyui_file_path)

	layout = QtWidgets.QVBoxLayout()
	layout.setContentsMargins(0, 0, 0, 0)
	parent.setLayout(layout)
	layout.addWidget(widget)

	return widget


def icon_from_image(img: np.ndarray):
	return QIcon(QPixmap.fromImage(qimage2ndarray.array2qimage(img)))


def remove_widget_from_list_widget(list_widget: QtWidgets.QListWidget, widget: QtWidgets.QWidget):
	items_count = list_widget.count()

	for i in range(items_count):
		item = list_widget.item(i)
		wgt = list_widget.itemWidget(item)
		if wgt == widget:
			list_widget.takeItem(list_widget.row(item))
			break


def get_image_from_drop_event(event: QtGui.QDropEvent):
	mime_data = event.mimeData()
	image = None
	if mime_data.hasUrls():
		urls = mime_data.urls()
		if len(urls) > 1:
			return
		image_path: str = urls[0].url()
		if not image_path.startswith("file:///"):
			return
		# is a file
		image_path = image_path.replace("file:///", '')
		image = cv.imread(image_path)
	elif mime_data.hasFormat('application/x-qabstractitemmodeldatalist'):
		model = QtGui.QStandardItemModel()

		model.dropMimeData(event.mimeData(), QtCore.Qt.CopyAction, 0, 0, QtCore.QModelIndex())
		item = model.item(0, 0)
		image = item.data(QtCore.Qt.UserRole)
	elif mime_data.hasImage():
		print("has image")
	return image