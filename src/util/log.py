#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


FORMAT = "%(asctime)-15s [%(process)d][%(levelname)-8s][%(name)s]: %(message)s"


def setup_logging():
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
