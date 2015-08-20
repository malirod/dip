from src.util.path import delete_dir
from src.config import SRC_DIR, OUTPUT_DIR

from fabric.api import local, task
from multiprocessing import cpu_count
from subprocess import Popen


@task
def setup_env():
    local('sudo apt-get install fabric libjpeg-dev beanstalkd')
    local('pip install -r requirements.txt')


def start_worker():
    print "Starting worker"
    Popen(['python', './worker.py'])


def start_client():
    print "Starting client"
    Popen(['python', './client.py'])


@task
def process():
    from src.util.path import working_directory, setup_pythonpath

    setup_pythonpath(SRC_DIR)

    WORKERS_COUNT = cpu_count()
    with working_directory(SRC_DIR):
        start_client()
        for i in range(0, WORKERS_COUNT):
            start_worker()


@task
def clean():
    delete_dir(OUTPUT_DIR)
