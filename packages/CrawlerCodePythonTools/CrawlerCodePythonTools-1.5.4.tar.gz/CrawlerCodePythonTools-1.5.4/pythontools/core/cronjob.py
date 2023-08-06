from pythontools.core import logger
from threading import Thread
import time, traceback, re, sys
from datetime import datetime, timedelta

_MANAGER = None
_CRONJOBS = []
_UPDATE_INTERVAL = 60


class CronJob:

    def __init__(self, name, interval, function, wait_for_last_job=True):
        self.name = name
        self.interval = interval
        self.function = function
        self.wait_for_last_job = wait_for_last_job
        self._current_thread = None
        self._last_run = 0
        self._next_run = 0
        self._calc_next_run()

    def run(self):
        if self._current_thread is None:
            def _function(self):
                try:
                    self.function()
                except Exception as e:
                    logger.log(f"§cCronJob '{self.name}' throw exception: {e}")
                    traceback.print_exc()
                if self.wait_for_last_job is True:
                    self._current_thread = None
            self._current_thread = Thread(target=_function, args=[self])
            self._current_thread.start()
            self._last_run = time.time()
            if self.wait_for_last_job is False:
                self._current_thread = None
        self._calc_next_run()

    def _calc_next_run(self):
        if type(self.interval) is int:
            self._next_run = self._last_run + self.interval
            return
        if type(self.interval) is str:
            if ":" in self.interval:
                regex = re.compile(r'((?P<hours>\d+?):)?((?P<minutes>\d+?):)?((?P<seconds>\d+?):)?')
                parts = regex.match(self.interval + ":")
                if parts:
                    parts = parts.groupdict()
                    global _UPDATE_INTERVAL
                    if parts["minutes"] and _UPDATE_INTERVAL > 60:
                        _UPDATE_INTERVAL = 60
                    if parts["seconds"] and _UPDATE_INTERVAL > 1:
                        _UPDATE_INTERVAL = 1
                    for name, val in parts.items():
                        parts[name] = int(val) if val else 0
                    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                    delta = timedelta(**parts)
                    self._next_run = (today + delta).timestamp()
                    if time.time() > self._next_run:
                        self._next_run = (today + timedelta(days=1) + delta).timestamp()
                    return
            else:
                if self.interval.lower() in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
                    wday_ofs = time.strptime(self.interval, "%A").tm_wday
                    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                    self._next_run = (today - timedelta(days=today.weekday()) + timedelta(days=wday_ofs)).timestamp()
                    if time.time() > self._next_run:
                        self._next_run = (today - timedelta(days=today.weekday()) + timedelta(weeks=1, days=wday_ofs)).timestamp()
                    return
        self._next_run = sys.maxsize
        logger.log(f"§cCronJob '{self.name}' will never execute!")
        return


def register_cron_job(cronjob: CronJob):
    global _CRONJOBS, _MANAGER, _UPDATE_INTERVAL
    if type(cronjob.interval) is int and cronjob.interval < _UPDATE_INTERVAL:
        _UPDATE_INTERVAL = cronjob.interval
    _CRONJOBS.append(cronjob)
    if _MANAGER is None:
        def _manager():
            while True:
                for job in _CRONJOBS:
                    if time.time() > job._next_run:
                        job.run()
                time.sleep(_UPDATE_INTERVAL)
        _MANAGER = Thread(target=_manager)
        _MANAGER.start()


# --- deprecated --- #
registerCronJob = register_cron_job
# --- deprecated --- #
