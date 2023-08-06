import time
import os
import pytesseract
from PIL import ImageGrab
import requests

import logging
from .simulate_operate import SimulateOperate
from .client import Client

Logger = logging.getLogger()

class ValidateCode():

    @classmethod
    def validate_code(cls, img_origin_x, img_origin_y, length, high, img_dir, psm='7', oem='3',
                      white_list='0123456789QWERTYUIOPASDFGHJKLZXCVBNM+-'):

        '''获取验证码截图，并识别验证码'''

        img = ImageGrab.grab(
            (img_origin_x, img_origin_y, img_origin_x + length, img_origin_y + high)
        )
        img = img.convert('L')
        content = pytesseract.image_to_string(
            img, config='--psm {} --oem {} -c tessedit_char_whitelist={}'.format(psm, oem, white_list)
        )
        img.save(fp=r'{}/bitmap.png'.format(img_dir))
        img.close()
        # content = cls.get_validate_code_from_req(r"{}/bitmap.png".format(img_dir))
        code = ''
        for s in content:
            if s in white_list:
                code += s

        return str(code)

    @classmethod
    def check_validate_code(cls,code_error_type,code_error_cls,code_error_tit,pngs_dir,client_name):

        '''检查验证码是否输错，通过弹窗弹出或者图片检查'''

        if code_error_type == 'pop_window':
            time.sleep(0.5)
            code_error_handle = SimulateOperate.get_window_handle(code_error_cls, code_error_tit)
            if code_error_handle == 0:
                return 1
            else:
                SimulateOperate.close_window(code_error_handle)
                # time.sleep(0.5)
                return 0

        elif code_error_type == 'error_img':
            img_path = os.path.join(pngs_dir, '%s_code_error.png' % client_name)
            check_res = SimulateOperate.check_img_exists(img_path)
            if check_res:
                return 0
            else:
                return 1

    @staticmethod
    def get_validate_code_from_req(img_path):

        url = 'http://192.168.1.68:16999/validate_code/en'
        files = {'file': open(img_path, 'rb')}
        r = requests.post(url, files=files)

        return r.json()['data'][0]

    @classmethod
    def get_validate_code(self, window_handle, code_img_origin_offset,code_img_size,img_dir,code_type='num&eng'):

        '''获取验证码'''

        white_list = '0123456789QWERTYUIOPASDFGHJKLZXCVBNM+-qwertyuiopasdfghjklzxcvbnm'
        validate_code_pos = SimulateOperate.cal_pos_by_window_handle(window_handle, code_img_origin_offset)
        if code_type == 'num':
            white_list = '0123456789'
        elif code_type == 'num&eng':
            white_list = '0123456789QWERTYUIOPASDFGHJKLZXCVBNM+-qwertyuiopasdfghjklzxcvbnm'
        elif code_type == 'cal':
            white_list = '0123456789+-'
        validate_code = self.validate_code(validate_code_pos[0], validate_code_pos[1], code_img_size[0],
                                           code_img_size[1], img_dir, white_list=white_list)

        if code_type == 'cal':
            try:
                validate_code = eval(validate_code)
            except:
                pass
        print(validate_code)
        if validate_code == '' or validate_code is None or validate_code == ' ':
            validate_code = '1111'

        return validate_code

    @classmethod
    def input_validate_code_and_login(cls, window_handle, need_click, code_button_offset, code_input_offset,
                                      code_img_origin_offset,code_img_size,img_dir,login_button,
                                      code_error_type,client_name,code_error_cls,code_error_tit,code_type='num&eng'):

        '''处理验证码，并点击登录按钮'''

        try:
            if need_click:
                SimulateOperate.move_and_click_left_by_window_handle(window_handle, code_button_offset)
            SimulateOperate.move_and_click_left_by_window_handle(window_handle, code_input_offset)
            validate_code = cls.get_validate_code(window_handle, code_img_origin_offset, code_img_size, img_dir,code_type=code_type)
            SimulateOperate.input_by_window_handle(window_handle, code_input_offset, validate_code, content_type='eng', right=10,
                                 backspace=10)
            SimulateOperate.move_and_click_left_by_window_handle(window_handle, login_button)
            if len(validate_code) != 4:
                return 0
            code_res = cls.check_validate_code(code_error_type,code_error_cls,code_error_tit,img_dir,client_name)
        except:
            code_res = 1

        return code_res


class BaseAction():

    # 动作基类
    def __init__(self,config,action_conf):

        self.config = config
        self.action_conf = action_conf
        self.window_name = action_conf['window_name']
        self.func_name = action_conf['func_name']
        self._set_window_handle()
        self.params = action_conf['params']

        pass

    def _set_window_handle(self):

        if self.func_name == 'check_window':
            self.window_handle = 0
            return

        if self.window_name is None or self.window_name == '':
            self.window_handle = 0
        else:
            self.window_handle = self.config.action_window_map[self.window_name].get('window_handle', 0)
            n = 0
            while n < 3:
                if SimulateOperate.check_window_handle_exists(self.window_handle):
                    break
                window_conf = self.config.action_window_map[self.window_name]
                self.window_handle = SimulateOperate.get_window_handle2(window_conf['window_class'], window_conf['window_title'],
                                                                     window_conf['is_fuzzy'], window_conf['is_sub'],
                                                                     window_conf['parent_window_class'])
                n += 1
                time.sleep(1)

            if self.window_handle == 0:
                raise Exception('找不到该动作所需窗口句柄，请检查窗口配置')
            else:
                self.config.action_window_map[self.window_name]['window_handle'] = self.window_handle
                SimulateOperate.set_window_avaliable(self.window_handle)

    def before_func(self):

        time.sleep(self.action_conf['before_wait_seconds'])

        if self.action_conf['set_window_avaliable']:
            SimulateOperate.set_window_avaliable(self.window_handle)

        if self.action_conf['close_pop_window']:
            SimulateOperate.close_pop_window(self.config.pop_windows)

    def after_func(self):

        time.sleep(self.action_conf['after_wait_seconds'])

    def open_client(self):

        Logger.debug('打开客户端')
        start_type = self.params.get('start_type',1)
        proc_remark = None
        if start_type == 3:
            proc_remark = self.config.account_id
        Client.open_client(self.config.client_path,start_type,proc_remark)
        return 1

    def close_client(self):

        Logger.debug('关闭客户端')
        start_type = self.params.get('start_type', 1)
        proc_remark = None
        if start_type == 3:
            proc_remark = self.config.account_id
        Client.close_client(self.config.client_path,start_type,proc_remark)
        return 1

    def wait_by_seconds(self):

        Logger.info('通过判断鼠标状态等待窗口初始化:{}'.format(self.window_name))
        wait_times = self.params['wait_times']
        time.sleep(wait_times)

        return 1

    def wait_window_init_by_mouse(self):

        Logger.debug('通过判断鼠标状态等待窗口初始化:{}'.format(self.window_name))
        wait_times = self.params['wait_times']
        res = SimulateOperate.wait_window_init(wait_times)
        if res == 0:
            raise Exception('通过鼠标状态判断窗口初始化超时')

        return 1

    def check_window(self):

        Logger.debug('检查窗口:{}'.format(self.window_name))
        window_conf = self.config.action_window_map[self.window_name]
        window_handle = SimulateOperate.check_window_is_show(window_conf['window_class'], window_conf['window_title'],
                                                             window_conf['is_fuzzy'], window_conf['is_sub'],
                                                             window_conf['parent_window_class'])
        if window_handle!=0:
            window_conf['window_handle'] = window_handle
            SimulateOperate.set_window_avaliable(window_handle)
        return window_handle

    def max_window(self):

        Logger.debug('放大窗口:{}'.format(self.window_name))
        SimulateOperate.max_window(self.window_handle)

    def input_by_offset(self):

        offset = self.params['offset']
        content = self.params['content']
        Logger.debug('输入内容:{}'.format(content))
        SimulateOperate.input_by_window_handle(self.window_handle,offset,content)
        return 1

    def click_hotkey(self):

        keys = self.params['keys']
        Logger.debug('敲击键盘组合键:{}'.format(str(keys)))
        SimulateOperate.click_hotkey(keys)

        return 1

    def click_key(self):

        key = self.params['key']
        Logger.debug('敲击键盘:{}'.format(key))
        SimulateOperate.click_key(key)

        return 1

    def input_validate_code_and_login(self):

        Logger.debug('输入验证按并登录')
        window_handle = self.window_handle
        need_click = self.params['need_click']
        code_button_offset = self.params['code_button_offset']
        code_input_offset = self.params['code_input_offset']
        code_img_origin_offset = self.params['code_img_origin_offset']
        code_img_size = self.params['code_img_size']
        login_button_offset = self.params['login_button_offset']
        code_error_type = self.params['code_error_type']
        code_error_cls = self.params['code_error_class']
        code_error_tit = self.params['code_error_title']
        img_dir = self.config.img_dir
        client_name = self.config.client_full_name
        code_type = self.params.get('code_type','num&eng')
        res = ValidateCode.input_validate_code_and_login(window_handle, need_click, code_button_offset, code_input_offset,
                                      code_img_origin_offset, code_img_size,img_dir, login_button_offset,
                                      code_error_type, client_name, code_error_cls, code_error_tit,code_type)
        return res

    def click_left_by_offset(self):

        Logger.debug('点击左键')
        offset = self.params['offset']
        SimulateOperate.move_and_click_left_by_window_handle(self.window_handle,offset)
        return 1

    def run(self,func):

        self.before_func()
        res = func()
        self.after_func()

        # if self.action_conf.get('error_exit',True):
        #     self.before_func()
        #     res = func()
        #     self.after_func()
        # else:
        #     try:
        #         self.before_func()
        #         res = func()
        #         self.after_func()
        #     except Exception as e:
        #         res = 1
        #         Logger.warning('{}-运行出错:{}'.format(func.__name__,str(e)))

        return res

    def __call__(self):

        func = getattr(self,self.func_name)
        need_retry = self.action_conf.get('need_retry',False)
        if need_retry:
            retry_times = self.action_conf['retry_times']
            n = 0
            res = 0
            while n < retry_times:
                if res == 0:
                    res = self.run(func)
                    n += 1
                    Logger.debug('重试函数：{},重试次数：{}'.format(func.__name__,n))
                    time.sleep(1)
                else:
                    break
            if n >= retry_times:
                raise Exception('重试超时')
        else:
            res = self.run(func)

        if res == 0:
            Logger.error('执行结果错误', exc_info=True)
            raise Exception('执行结果错误')

        return res