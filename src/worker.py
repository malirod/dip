#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util.path import get_file_ext, get_output_dir_name, delete_dir
from util.image import resize_img
from util.log import setup_logging
from config import (RESOLUTIONS, BEANSTALK_HOST, BEANSTALK_JOB_WAIT_TIMEOUT,
                    BEANSTALK_PORT, BEANSTALK_TUBE)

from PIL import Image
from os.path import join
import logging

import beanstalkc


PROCESSED_FILE_NAME = '{}X{}{}'
logger = logging.getLogger('worker')


def process_image(connection, input_file_path):
    logger.info('Processing: {}'.format(input_file_path))
    dest_dir = get_output_dir_name(input_file_path)
    img_ext = get_file_ext(input_file_path)
    try:
        original_image = Image.open(input_file_path)
        original_width, original_height = original_image.size
        new_file_name = PROCESSED_FILE_NAME.format(
            str(original_width), str(original_height), img_ext)
        original_image.save(join(dest_dir, new_file_name))

        for (new_width, new_height) in RESOLUTIONS:
            # skip the original file and the higher resolutions
            if new_width >= original_width and new_height >= original_height:
                continue

            resized_img = resize_img(original_image.copy(), (new_width, new_height))
            if resized_img is None:
                logger.error('Failed to resize the image "{}"'.format(input_file_path))
                continue
            new_file_name = PROCESSED_FILE_NAME.format(
                str(new_width), str(new_height), img_ext)
            resized_img.save(join(dest_dir, new_file_name))
        return True
    except Exception as e:
        logger.error('Failed to process image {}. Error: {}'.format(input_file_path, e))
        # delete the output dir
        delete_dir(dest_dir)
    return False


def serve():
    logger.info('Creating connection')
    connection = beanstalkc.Connection(
        host=BEANSTALK_HOST, port=BEANSTALK_PORT, parse_yaml=False)
    connection.watch(BEANSTALK_TUBE)

    while True:
        logger.info('Waiting for the job')
        job = connection.reserve(timeout=BEANSTALK_JOB_WAIT_TIMEOUT)
        logger.info('Waited for the job')
        if job is None:
            logger.info('Nothing to do. Terminating.')
            break
        if process_image(connection, job.body):
            job.delete()
        else:
            logger.info('Failed to process the job: {}'.format(job.body))
            job.release()
    logger.info('Done')


if __name__ == '__main__':
    setup_logging()
    serve()
