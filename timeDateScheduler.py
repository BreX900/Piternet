from datetime import datetime

from utility.pattern import Singleton


class TimeDateScheduler(metaclass=Singleton):
    def __init__(self, startWorking, stopWorking, startHolidays, stopHolidays):
        self._startWorking = startWorking
        self._stopWorking = stopWorking
        self._startHolidays = startHolidays
        self._stopHolidays = stopHolidays
    def getStart(self):
        dtn = datetime.now()
        if TimeDateScheduler.isHolidays(dtn):
            return dtn.replace(**self._startHolidays)
        else:
            return dtn.replace(**self._startWorking)
    def getStop(self):
        dtn = datetime.now()
        if TimeDateScheduler.isHolidays(dtn):
            return dtn.replace(**self._stopHolidays)
        else:
            return dtn.replace(**self._stopWorking)
    @staticmethod
    def isHolidays(dtn=datetime.now()):
        weekDay = dtn.weekday()
        return weekDay == 5 or weekDay == 6

class TimeDateSchedulerPiternet(TimeDateScheduler):
    def __init__(self):
        super().__init__(startWorking={'hour': 7, 'minute': 0, 'second': 0, 'microsecond': 0},
                         stopWorking={'hour': 1, 'minute': 30, 'second': 0, 'microsecond': 0},
                         startHolidays={'hour': 7, 'minute': 0, 'second': 0, 'microsecond': 0},
                         stopHolidays={'hour': 4, 'minute': 0, 'second': 0, 'microsecond': 0})