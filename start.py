from utility.configLogger import configLogger
from utility.development import devolopment
from piternet import Board
from turnChange import TurnChangeWindows

import logging.config

if __name__ == '__main__':
    TAG = "START - "
    logging.config.dictConfig(configLogger("View"))
    logger = logging.getLogger(__name__)
    logger.info(TAG+"MOD: "+devolopment())


    board = Board()
    try:
        logger.info(TAG+Board.resetAll())
        application = TurnChangeWindows()
        application.mainloop()
    finally:
        logger.info(TAG + Board.reset())
