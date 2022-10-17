import logging as log


def get_logger():
    """
    :description: This is just a dummy placeholder for logging, this module can be
    configured and developed to manage the logs as per company standard,
    By configuring this logs can be delivered to logz.io, elastic search, cloudwatch, redis logger etc.
    :return:
    """
    log.basicConfig(format='%(levelname)s:%(message)s', level=log.DEBUG)
    return log
