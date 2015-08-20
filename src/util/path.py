#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import contextlib


def setup_pythonpath(path):
    sys.path.append(path)


def get_input_files(input_dir):
    files = [f for f in os.listdir(input_dir) if os.path.isfile(
        os.path.join(input_dir, f))]
    return files


def get_file_ext(path):
    return os.path.splitext(path)[1]


def get_output_dir_name(input_file_path):
    from config import OUTPUT_DIR
    dest_dir = os.path.join(
        OUTPUT_DIR, os.path.splitext(os.path.basename(input_file_path))[0])
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    return dest_dir


@contextlib.contextmanager
def working_directory(path):
    """
    A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.

    """
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def delete_dir(directory):
    from shutil import rmtree
    rmtree(directory, ignore_errors=True)
