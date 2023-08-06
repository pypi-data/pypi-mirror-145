import os

HEALTH_FILENAME = "/tmp/stock_service.health"


def touch(fname=HEALTH_FILENAME, times=None):
    """
    Method to create an empty file used for readiness check in consumers
    """
    with open(fname, "a"):
        os.utime(fname, times)


def remove(fname=HEALTH_FILENAME):
    """
    Method that deletes the readiness check file.
    """
    os.remove(fname)
