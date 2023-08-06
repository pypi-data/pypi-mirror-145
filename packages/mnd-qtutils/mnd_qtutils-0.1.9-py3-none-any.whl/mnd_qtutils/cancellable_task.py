from collections import Generator
import threading

import pypegraph.action


class TaskProgress:

    def __init__(self, progress_value: float = 0, progress_state: str = ""):
        self._progress_value: float = progress_value
        self._progress_state: str = progress_state

    @property
    def progress_value(self):
        return self._progress_value

    @progress_value.setter
    def progress_value(self, value: float):
        self._progress_value = value

    @property
    def progress_state(self):
        return self._progress_state

    @progress_state.setter
    def progress_state(self, state: str):
        self._progress_state = state


class CancellableTask:

    def __init__(self):
        self._running = False
        self._cancel = False
        self._thread = None

        self.event_execution_started = pypegraph.action.Action()
        self.event_execution_finished = pypegraph.action.Action()  # este evento se invoca en el hilo secundario (generalmente)
        self.event_execution_cancelled = pypegraph.action.Action()
        self.event_notify_progress = pypegraph.action.Action()  # este evento se invoca en el hilo secundario (generalmente)

    def is_running(self):
        return self._running

    def execute(self, function, *params, **kparams) -> bool:
        if not self._running:
            self._thread = threading.Thread(target=self._executor, args=(function, *params), kwargs=kparams, daemon=True)
            self._thread.start()
            self.event_execution_started.invoke()
            return True
        return False

    def __call__(self, function, *params, **kparams) -> bool:
        return self.execute(function, *params, **kparams)

    def cancel(self):
        if self._thread and self._running:
            self._cancel = True
            self._thread.join()
            self._thread = None
            self._cancel = False
            self.event_execution_cancelled.invoke()

    def wait_to_finish(self):
        if self._thread and self._running:
            self._thread.join()

    def _executor(self, function, *params, **kparams):
        self._running = True

        res = function(*params, **kparams)
        return_value = None
        if isinstance(res, Generator):
            for yield_value in res:
                return_value = yield_value
                self._handle_yield(yield_value)
                if self._cancel:
                    self._running = False
                    return
        else:
            return_value = res

        self._running = False
        self.event_execution_finished.invoke(return_value)

    def _handle_yield(self, yield_value):
        if yield_value is None or not isinstance(yield_value, TaskProgress):
            return
        self.event_notify_progress.invoke(yield_value)


if __name__ == '__main__':
    def f(N):
        l = [x for x in range(N)]
        for x in l:
            yield x
        print("finished")

    task = CancellableTask()

    task.execute(f, 10000000)
    task.wait_to_finish()
    task.execute(f, N=10000000)
    task.wait_to_finish()
