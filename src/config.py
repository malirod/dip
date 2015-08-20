#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join, dirname

ROOT_DIRECTORY = dirname(dirname(__file__))
SRC_DIR = join(ROOT_DIRECTORY, 'src')
BEANSTALK_HOST = '127.0.0.1'
BEANSTALK_PORT = 11300
BEANSTALK_TUBE = 'dip'
BEANSTALK_JOB_WAIT_TIMEOUT = 3  # seconds
INPUT_DIR = join(ROOT_DIRECTORY, 'input')
OUTPUT_DIR = join(ROOT_DIRECTORY, 'output')

VALID_EXTS = ['.jpg']
RESOLUTIONS = [(2560, 1600),
               (2560, 1440),
               (1920, 1200),
               (1920, 1080),
               (1600, 1200),
               (1680, 1050),
               (1600, 900),
               (1440, 1080),
               (1440, 900),
               (1280, 720)]

# Override the settings with the local ones if exist
try:
    from local_config import *  # NOQA
except ImportError:
    pass
