import os
from datetime import datetime as dt
import logging
import logging.config
import requests
import socket

def get_host_ip():
    ip = ''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

class HttpStreamHandle(logging.Handler):

    def __init__(self, url):
        super(HttpStreamHandle, self).__init__()
        self.url = url

    def map_record_to_data(self, record):

        keys = ['asctime', 'name', 'filename', 'funcName', 'levelname', 'message', 'lineno',
                'pathname', 'process', 'processName', 'thread', 'threadName']

        data = {}

        for key in keys:
            data[key] = getattr(record, key)
        data['ip'] = get_host_ip()

        return data

    def emit(self, record):
        data = self.map_record_to_data(record)
        try:
            requests.post(self.url, json=data)
        except:
            pass

log_conf = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '【%(asctime)s-%(filename)s-%(lineno)s-%(levelname)s】%(message)s',
        },
        'plain': {
            'format': '%(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'filename': '',
            'formatter': 'default',
            'encoding': 'utf-8',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
        'propagate': False,
    },
    'disable_existing_loggers': True,
}
def init_log(log_dir, log_url=None, level='INFO'):

    log_conf['handlers']['file']['filename'] = os.path.join(log_dir, 'atuo_%s.log' % dt.now().strftime('%Y%m%d'))
    log_conf['root']['level'] = level
    logging.config.dictConfig(log_conf)
    if log_url != '' and log_url is not None:
        logger = logging.getLogger()
        http_stream_handle = HttpStreamHandle(log_url)
        http_stream_handle.setLevel('WARNING')
        logger.addHandler(http_stream_handle)

if __name__ == '__main__':
    pass

