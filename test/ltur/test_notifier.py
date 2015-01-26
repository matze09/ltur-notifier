# -*- coding: utf-8 -*-
__author__ = 'mloeks'

import unittest
import os
import logging
from datetime import datetime, timedelta

from ltur.notifier import LturNotifier


class TestLturNotifier(unittest.TestCase):

    def setUp(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        logging.basicConfig(level=logging.DEBUG)

    def test_ltur_notifier(self):
        test_config_file = self.BASE_DIR + '/../../data/test/test_config.py'
        notifier = LturNotifier(test_config_file)
        notifier.run()

if __name__ == '__main__':
    unittest.main()