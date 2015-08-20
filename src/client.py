#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util.path import get_input_files, get_file_ext
from config import (INPUT_DIR, VALID_EXTS, BEANSTALK_HOST,
                    BEANSTALK_PORT, BEANSTALK_TUBE)
from util.log import setup_logging

from os.path import join
import logging

import beanstalkc


logger = logging.getLogger('client')


def process_image(connection, input_file_path):
    try:
        logger.info('Processing file "{}"'.format(input_file_path))
        connection.put(input_file_path)
    except Exception as e:
        logger.error('Failed to process image {}. Error: {}'.format(input_file_path, e))


def process_input():
    logger.info('Creating connection')
    connection = beanstalkc.Connection(
        host=BEANSTALK_HOST, port=BEANSTALK_PORT, parse_yaml=False)
    connection.use(BEANSTALK_TUBE)
    files = get_input_files(INPUT_DIR)
    for item in files:
        if get_file_ext(item) in VALID_EXTS:
            process_image(connection, join(INPUT_DIR, item))
    logger.info('Done')


if __name__ == '__main__':
    setup_logging()
    process_input()
