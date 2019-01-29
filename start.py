import asyncio
import logging
from logging import config

from utility.configLogger import configLogger
from utility.development import devolopment
from piternet import Board, Piternet


if __name__ == '__main__':
    TAG = "START - "
    config.dictConfig(configLogger("View"))
    logger = logging.getLogger(__name__)
    logger.info(TAG+"MOD: "+devolopment())


    if True:
        board = Board()
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(Piternet(board).runForever())
    else:
        board = Board()
        try:
            logger.info(TAG+Board.resetAll())
            application = TurnChangeWindows()
            application.mainloop()
        finally:
            logger.info(TAG + Board.reset())
