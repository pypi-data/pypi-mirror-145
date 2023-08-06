# -*- coding: utf-8 -*-
import logging
import os
import pytesseract
import warnings
from .init_config import Config
from .base_action import BaseAction
from .client import Client

Logger = logging.getLogger()
warnings.filterwarnings('ignore')

def set_tesseract_cmd():
    for key, value in os.environ.items():
        for p in value.split(';'):
            if 'Tesseract-OCR' in p:
                path = os.path.join(p.split('Tesseract-OCR')[0], 'Tesseract-OCR', 'tesseract.exe')
                pytesseract.pytesseract.tesseract_cmd = path
                return

class Actuator():

    def __init__(self, conf, action_cls = BaseAction, conf_cls = Config):
        self.config = conf_cls(conf)
        self.action_cls = action_cls
        set_tesseract_cmd()

    def run(self,step_name=None):

        Logger.info('=============================================================')
        Logger.info('开始处理账号{}'.format(self.config.account_id))
        for i in range(0,len(self.config.action_confs)):
            action_conf = self.config.action_confs[i]
            _step_name = action_conf.get('step_name')
            # 只执行某一步
            if step_name is not None:
                if _step_name != step_name:
                    continue
            step = i + 1
            Logger.info('开始执行第{}-{}步'.format(step, _step_name))
            try:
                self.action_cls(self.config,action_conf)()
            except Exception as e:
                Logger.error('{}-第{}-{}步报错：{}'.format(self.config.account_id,step,_step_name,str(e)), stack_info=True, exc_info=True)
                break
        Client.close_client(self.config.client_path)
        Logger.info('=============================================================')
        Logger.info('\n\n')

if __name__ == '__main__':
    pass
