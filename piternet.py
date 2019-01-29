from datetime import datetime
from typing import List

from scheduler import SchedulerWorks, WorkCycle, CycleWeek, Day, Worker
from utility.board import Board
import os

import logging


class Piternet(object):
    ONLINE = 1
    _pin = 5

    def __init__(self, board):
        self.log = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self._board = board
        self.log.info("Init Piternet - " + str(self.status()))

    async def runForever(self):
        await self.setScheduler()
        works: List[WorkCycle] = []

        days: List[Day] = Day.FRIDAY, Day.SATURDAY, Day.SUNDAY
        tmpWorks: List[WorkCycle] = []
        for day in days:
            tmpWorks.append(WorkCycle(CycleWeek(day, hour=8, minute=0, second=0), WorkerStart(self)))
            tmpWorks.append(WorkCycle(CycleWeek(day, hour=4, minute=0, second=0), WorkerStop(self)))

        for work in tmpWorks:
            works.append(work)

        days: List[Day] = Day.MONDAY, Day.TUESDAY, Day.WEDNESDAY, Day.THURSDAY
        tmpWorks: List[WorkCycle] = []
        for day in days:
            tmpWorks.append(WorkCycle(CycleWeek(day, hour=8, minute=0, second=0), WorkerStart(self)))
            tmpWorks.append(WorkCycle(CycleWeek(day, hour=1, minute=30, second=0), WorkerStop(self)))

        for work in tmpWorks:
            works.append(work)

        scheduler: SchedulerWorks = SchedulerWorks(works)
        await scheduler.runForever()

    def start(self):
        self.log.info("INTERNET CONNECTION: Starting - Modem:"+str(self.status()))
        self._board.output(Piternet._pin, Board.LOW)
        self.log.info("INTERNET CONNECTION: Started - Modem:"+str(self.status()))

    def stop(self):
        self.log.info("INTERNET CONNECTION: Stopping - Modem:"+str(self.status()))
        self._board.output(Piternet._pin, Board.HIGH)
        self.log.info("INTERNET CONNECTION: Stopped - "+str(self.status()))

    def restart(self):
        self.log.info("INTERNET CONNECTION: Restarting")
        self.stop()

    def restartStepTwo(self):
        self.start()
        self.log.info("INTERNET CONNECTION: Restarted")

    def _isPinOn(self):
        return self._board.signal(Piternet._pin) == Board.LOW

    def isOnline(self):
        return self.status()["Piternet:"]
    def status(self):
        status = {"Pin":0, "Piternet:":0}
        if self._isPinOn():
            status["Pin"] = 1
            hostname = "google.com"  # example
            if not os.system("ping -c 1 " + hostname + " > /dev/null"):
                status["Piternet:"] = 1
        return status

    def setScheduler(self):
        dtn = datetime.now()
        if dtn.hour < 7:  # Start
            datetimeScheduler = self._timeDateScheduler.getStart()
            self.log.info("SchedulerStarPiternet: " + str(datetimeScheduler))
            self._scheduler.add_job(self.start, 'date', run_date=datetimeScheduler)
            if dtn.hour < 4:# ShutDown
                datetimeScheduler = self._timeDateScheduler.getStop()
                self.log.info("SchedulerStopInternet: Date: " + str(datetimeScheduler))
                self._scheduler.add_job(self.stop, 'date', run_date=datetimeScheduler)
        # NextSetScheduler
        try:
            dtn = dtn.replace(day=dtn.day + 1, hour=0, minute=1, second=0, microsecond=0)
        except ValueError:
            try:
                dtn = dtn.replace(month=dtn.month + 1, day=1, hour=0, minute=1, second=0, microsecond=0)
            except ValueError:
                dtn = dtn.replace(year=dtn.year + 1, month=1, day=1, hour=0, minute=1, second=0, microsecond=0)
        self.log.info("SetNextSchedulerInternet: " + str(dtn))
        self._scheduler.add_job(self.setScheduler, 'date', run_date=dtn)


class WorkerStart(Worker):
    def __init__(self, piternet: Piternet):
        self.piternet: Piternet = piternet

    async def working(self):
        self.piternet.start()


class WorkerStop(Worker):
    def __init__(self, piternet: Piternet):
        self.piternet: Piternet = piternet

    async def working(self):
        self.piternet.stop()


