import logging
from unittest import TestCase


from pyguardian.utils.pyguardian_logging import PyGuardianLogger


class TestPyGuardianLogger(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.TEST_LOGGER = PyGuardianLogger("TestLogger")
        logging.disable(logging.NOTSET)

    def test_info(self):
        with self.assertLogs("TestLogger", level=logging.INFO) as log_test:
            self.TEST_LOGGER.info("something")

        self.assertEqual(log_test.output, ["INFO:TestLogger:something"])

    def test_debug(self):
        with self.assertLogs("TestLogger", level=logging.DEBUG) as log_test:
            self.TEST_LOGGER.debug("something")

        self.assertEqual(log_test.output, ["DEBUG:TestLogger:something"])

    def test_warn(self):
        with self.assertLogs("TestLogger", level=logging.WARN) as log_test:
            self.TEST_LOGGER.warn("something")

        self.assertEqual(log_test.output, ["WARNING:TestLogger:something"])

    def test_error(self):
        with self.assertLogs("TestLogger", level=logging.ERROR) as log_test:
            self.TEST_LOGGER.error("something")

        self.assertEqual(log_test.output, ["ERROR:TestLogger:something"])

    def test_critical(self):
        with self.assertLogs("TestLogger", level=logging.CRITICAL) as log_test:
            self.TEST_LOGGER.critical("something")

        self.assertEqual(log_test.output, ["CRITICAL:TestLogger:something"])

