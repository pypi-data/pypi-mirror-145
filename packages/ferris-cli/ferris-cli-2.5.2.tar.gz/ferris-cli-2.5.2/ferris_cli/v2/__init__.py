import sys
import time
import functools
from inspect import getmembers, isfunction, ismethod

from ferris_cli.v2.services.config import ApplicationConfigurator
from ferris_cli.v2.services.broker import FerrisBroker
from ferris_cli.v2.services.events import FerrisEvents
from ferris_cli.v2.services.notifications import FerrisNotificatons
from ferris_cli.v2.services.logging_handler import FerrisLogging
from ferris_cli.v2.services.storage import MinioService
from ferris_cli.v2.services.oidc import FerrisOIDC
from ferris_cli.v2.services.postgres import PostgreSQL


class ExecutionTime:

    def __init__(self, console=False, module_name=None):

        self.module_name = module_name
        self.logtime_data = {}

        if self.module_name is not None:
            self.auto_decorate()

    def timeit(self, method):

        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = method(*args, **kwargs)
            end_time = time.perf_counter()
            current_time = round((end_time - start_time) * 1000, 4)
            total_time = round((end_time - start_time) * 1000, 4)  # time in milliseconds

            if method.__name__ in self.logtime_data:
                curr = self.logtime_data[method.__name__]
                tt = curr["total_time"] + total_time
                count = curr["times_called"] + 1
                avg_time = round(tt / count, 4)
                self.logtime_data[method.__name__] = {'times_called': count, "total_time": tt, "average_time": avg_time, "current_time": current_time}
            else:
                self.logtime_data[method.__name__] = {'times_called': 1, "total_time": total_time, "average_time": total_time, "current_time": current_time}

        return wrapper

    def auto_decorate(self):
        try:
            module = sys.modules[self.module_name]
            items = getmembers(module, isfunction)
            for name, addr in items:
                setattr(module, name, self.timeit(addr))
        except KeyError as e:
            raise Exception(f'Error Occured')


