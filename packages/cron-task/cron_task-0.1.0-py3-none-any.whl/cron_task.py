import datetime
import functools
from threading import Thread

STARTED = "started"
STOPPED = "stopped"


class Executor:
    def __init__(self):
        self.tasks = []
        self.state = STOPPED

    def run_scheduled(self):
        executable_tasks = (task for task in self.tasks if task.is_executable)
        for task in executable_tasks:
            self._execute_task(task)

    def every(self, interval):
        task = Task(interval, self)
        return task

    def start(self):
        self.state = STARTED
        self._thread = Thread(target=self._main_loop, name="Task Runner")
        self._thread.daemon = True
        self._thread.start()

    def shutdown(self):
        self.state = STOPPED
        self._thread.join()
        del self._thread

    def _execute_task(self, task):
        task.run()

    def _main_loop(self):
        while self.state != STOPPED:
            self.run_scheduled()


class Task:
    def __init__(self, interval, runner=None):
        self.interval = interval
        self.interval_unit = None
        self.runner = runner
        self.last_run = None
        self.next_run = None
        self.callable_func = None
        self.timedelta = None

    @property
    def seconds(self):
        self.interval_unit = "seconds"
        return self

    @property
    def minutes(self):
        self.interval_unit = "minutes"
        return self

    @property
    def hours(self):
        self.interval_unit = "hours"
        return self

    def execute(self, callable_func, *args, **kwargs):
        self.callable_func = functools.partial(callable_func, *args, **kwargs)
        functools.update_wrapper(self.callable_func, callable_func)
        self._set_next_run()
        self.runner.tasks.append(self)
        return self

    @property
    def is_executable(self):
        return datetime.datetime.now() >= self.next_run

    def run(self):
        callable_func = self.callable_func()
        self.last_run = datetime.datetime.now()
        self._set_next_run()
        return callable_func

    def _set_next_run(self):
        self.timedelta = datetime.timedelta(**{self.interval_unit: self.interval})
        self.next_run = datetime.datetime.now() + self.timedelta
