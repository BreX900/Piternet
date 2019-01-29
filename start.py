import asyncio
import logging
import os
from logging import config

from utility.configLogger import configLogger
from piternet import Board, Piternet


if __name__ == '__main__':
    TAG = "START - "
    config.dictConfig(configLogger("View"))
    logger = logging.getLogger(__name__)
    logger.info(TAG+"PID: "+str(os.getpid()))


    if True:
        board = Board()
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(Piternet(board).runForever())
        loop.run_forever()
    else:
        board = Board()
        try:
            logger.info(TAG+Board.resetAll())
            application = TurnChangeWindows()
            application.mainloop()
        finally:
            logger.info(TAG + Board.reset())
