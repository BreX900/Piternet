import logging
from abc import ABCMeta, abstractmethod
from asyncio import sleep
from datetime import datetime, timedelta
from enum import Enum
from typing import List


log = logging.getLogger(__name__)


class Day(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    @staticmethod
    def now(dtn:datetime=None) -> 'Day':
        if dtn is None:
            dtn = datetime.now()
        return Day(dtn.weekday())

    @classmethod
    def isHolidays(cls, dtn:datetime=None) -> bool:
        day: Day = cls.now(dtn)
        return day == Day.SATURDAY or day == Day.SUNDAY

    def firstNext(self, dtn:datetime=None):
        if dtn is None:
            dtn = datetime.now()
        while self.now(dtn) != self:
            dtn = dtn + timedelta(days=1)
        return dtn


class DateTimeField(object):
    def __init__(self, month=None, day=None, hour=None, minute=None, second=None, microsecond=0):
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond

    @property
    def data(self):
        data = {}
        for key, value in self.__dict__.items():
            if value is not None:
                data[key] = value
        return data


class Cycle(object, metaclass=ABCMeta):
    def __init__(self):
        self._datetime = None

    @property
    def datetime(self) -> datetime:
        if self._datetime is None:
            return self.updateDatetime()
        return self._datetime

    @abstractmethod
    def updateDatetime(self) -> datetime: pass

    @staticmethod
    def timeLeftEndDay(datetime, dtn=None):
        if dtn is None:
            dtn = datetime.now()
        return (dtn.replace(day=dtn.day + 1, hour=0, minute=0, second=1) - datetime).total_seconds()


class CycleWeek(Cycle):
    def __init__(self, day:Day, hour=None, minute=None, second=None, microsecond=0):
        Cycle.__init__(self)
        self.day:Day = day
        self.field: DateTimeField = DateTimeField(None, None, hour, minute, second, microsecond)
        self._datetime = None

    def updateDatetime(self):
        self._datetime = self.day.firstNext(datetime.now().replace(**self.field.data))
        return self._datetime


class CycleDatetime(Cycle):
    def __init__(self, month=None, day=None, hour=None, minute=None, second=None, microsecond=0):
        Cycle.__init__(self)
        self.field: DateTimeField = DateTimeField(month, day, hour, minute, second, microsecond)
        self.extra = {self.__getLastKey() + "s": 1}

    def __getLastKey(self):
        beforeKey = 'year'
        for key, value in self.field.__dict__.items():
            if value:
                return beforeKey
            beforeKey = key

    def updateDatetime(self):
        self._datetime = datetime.now().replace(**self.field.data)
        if datetime.now() >= self._datetime:
            self._datetime = self._datetime + timedelta(**self.extra)
        return self._datetime


class Worker(object, metaclass=ABCMeta):
    @abstractmethod
    async def working(self): pass


class Work(object):
    def __init__(self, startAt: datetime, worker: Worker, name: str=None):
        self.datetime = startAt
        self.worker: Worker = worker
        self.name: str = name

    async def start(self):
        await self.attend()
        name: str = self.name + " s" if self.name else "S"
        log.info(name+"tart Working!")
        await self.worker.working()
        name: str = self.name + " f" if self.name else "F"
        log.info(name + "inish Working")

    async def attend(self):
        seconds = (self.datetime - datetime.now()).total_seconds()
        while seconds > 0:
            name: str = self.name + " s" if self.name else "S"
            log.info(name+"tart at: "+str(self.datetime)+" Left: "+str(timedelta(seconds=seconds)))
            await sleep(seconds)
            seconds = (self.datetime - datetime.now()).total_seconds()


class WorkCycle(Work):
    def __init__(self, startAt: Cycle, worker: Worker, name:str=None):
        self.cycleDateTime = startAt
        super().__init__(self.cycleDateTime.datetime, worker, name)

    async def start(self):
        await super().start()
        self.datetime = self.cycleDateTime.updateDatetime()


class SchedulerWorks(object):
    def __init__(self, works: List[Work], delete= True):
        self.works: List[Work] = works
        self.delete: bool = delete

    def __getWork(self) -> Work:
        now = datetime.now()
        work: Work = None
        removeWorks = []
        for tmpWork in self.works:
            if tmpWork.datetime > now:
                if (work is None) or (tmpWork.datetime < work.datetime):
                    work = tmpWork
            elif self.delete:
                removeWorks.append(tmpWork)
        if self.delete:
            if work:
                removeWorks.append(work)
            for tmpWork in removeWorks:
                self.works.remove(tmpWork)
        return work

    async def run(self):
        work: Work = self.__getWork()
        while work:
            try:
                await work.start()
            except:
                log.exception("SchedulerWorks.run...")
            work: Work = self.__getWork()

    async def runForever(self):
        self.delete = False
        while True:
            try:
                await self.run()
            except:
                log.exception("SchedulerWorks.runForever...")

