import os
from pathlib import Path
from PySide2 import QtWidgets, QtCore

from mnd_qtutils.cancellable_task import CancellableTask, TaskProgress
from mnd_qtutils import qtutils


class ProgressTaskDialog(QtWidgets.QDialog):
    signal_execution_finished = QtCore.Signal()

    def __init__(self, function, params, kparams, cancellable: bool = True, cancellable_task: CancellableTask = None, dialog_title: str = None, parent=None):
        super(ProgressTaskDialog, self).__init__(parent=parent)
        self._cancellable_task = cancellable_task or CancellableTask()
        self._target_function = function
        self._params = params
        self._kparams = kparams
        self._task_result = None
        self._cancelled = False

        self._cancellable_task.event_notify_progress += self._update_task_info
        self._cancellable_task.event_execution_finished += self._on_execution_finished

        self.signal_execution_finished.connect(self._close_dialog)

        self.setWindowTitle(dialog_title or 'Ejecutando...')
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint)
        self._widget = qtutils.import_from_ui_file(os.path.join(Path(__file__).parent, 'cancellable_task_dialog_ui.py'))

        self._info_label = self._widget.info_label
        self._percent_label = self._widget.percent_label

        self._cancel_button: QtWidgets.QPushButton = self._widget.cancel_button
        if not cancellable:
            self._cancel_button.hide()
        else:
            self._cancel_button.clicked.connect(self._cancel_execution)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._widget)
        self.setLayout(layout)

        self._start_execution()

    @property
    def is_cancelled(self):
        return self._cancelled

    @property
    def task_result(self):
        return self._task_result

    def _start_execution(self):
        if not self._cancellable_task.execute(self._target_function, *self._params, **self._kparams):
            self._close_dialog(False)

    def _on_progress_received(self, progress):
        self.signal_progress_received.emit(progress)

    def _on_execution_finished(self, result):
        self._task_result = result
        self.signal_execution_finished.emit()

    @QtCore.Slot()
    def _close_dialog(self, success: bool = True):
        self._dispose_events()
        if success:
            self.accept()
        else:
            self.reject()
        self.close()

    @QtCore.Slot()
    def _update_task_info(self, progress: TaskProgress):
        if isinstance(progress, TaskProgress):
            text = progress.progress_state
            percent = progress.progress_value
            if text != '':
                self._info_label.setText(text)
            if percent > 0:
                str_percent = f'{"{:.2f}".format(percent)}%'
                self._percent_label.setText(str_percent)
            else:
                self._percent_label.setText('')

    @QtCore.Slot()
    def _cancel_execution(self):
        self._update_task_info(TaskProgress(progress_state='Cancelando...'))
        self._cancellable_task.cancel()
        self._cancelled = True
        self._close_dialog(True)

    def _dispose_events(self):
        self._cancellable_task.event_notify_progress -= self._on_progress_received
        self._cancellable_task.event_execution_cancelled -= self._on_execution_finished

    @staticmethod
    def create_task_dialog(function, *params, cancellable: bool = True, cancellable_task: CancellableTask = None, dialog_title: str = None, **kparams):
        dialog = ProgressTaskDialog(
            function,
            params=params,
            kparams=kparams,
            cancellable=cancellable,
            cancellable_task=cancellable_task,
            dialog_title=dialog_title)
        result = dialog.exec_()
        error = result == QtWidgets.QDialog.Rejected
        return dialog.is_cancelled, error, dialog.task_result


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = QtWidgets.QWidget()
    window.setMinimumSize(400, 400)
    window.show()

    ct = CancellableTask()
    def f():
        yield TaskProgress(0, 'printiando')
        for i in range(100000):
            print(i)
            yield TaskProgress(i, '')
        print('finished')
    # cancelled, error = CancellableTaskDialog.create_task_dialog(f, ct)
    cancelled, error, result = ProgressTaskDialog.create_task_dialog(f)
    print(cancelled, error)

    sys.exit(app.exec_())
