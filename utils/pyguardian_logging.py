import logging
import os
import sys
from pathlib import Path

from pyguardian.utils import constants


class PyGuardianLogger:

    def __init__(self,
                 name="pyguardian_logger",
                 file_name="default-log-file",
                 loglevel=logging.INFO):

        log_file_path = constants.DATA_DIR + "/" + file_name
        # TODO really would like this to not be here
        if not os.path.isdir(constants.DATA_DIR):
            os.makedirs(constants.DATA_DIR)

        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=loglevel,
            handlers=[
                logging.FileHandler(str(Path.home()) + "/.pyguardian/" + file_name),
                logging.StreamHandler(sys.stdout)
            ]
        )

        self.logger = logging.getLogger(name)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
