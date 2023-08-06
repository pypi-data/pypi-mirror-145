import os
import copy

class Config():

    def __init__(self, conf):

        self.conf_copy = copy.deepcopy(conf)
        self.set_base_conf()
        self.set_account_conf()
        self.set_oprate_conf()

    def set_base_conf(self):

        base_conf = self.conf_copy['base_conf']
        self.client_dir = base_conf['client_dir']
        self.log_dir = base_conf['log_dir']
        self.img_dir = base_conf['img_dir']

        if not os.path.exists(self.client_dir):
            raise Exception('客户端目录不存在')
        if not os.path.exists(self.img_dir):
            os.makedirs(self.img_dir)
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def set_account_conf(self):

        account_conf = self.conf_copy['account_conf']
        self.account_id = account_conf['accountId']
        self.pass_word = account_conf['password']
        self.client_path = os.path.join(self.client_dir, account_conf['brokerClientPath'])
        if not os.path.exists(self.client_path):
            raise Exception('客户端路径不存在-{}'.format(self.client_path))

    def check_field_none(self, value):

        if value is None or value == '':
            return True
        else:
            return False

    def check_fields(self, conf, fields, error_msg, _type='none'):

        for field in fields:
            res = False
            if _type == 'none':
                res = self.check_field_none(conf.get(field))
            elif _type == 'list':
                res = not isinstance(conf.get(field), list)
            elif _type == 'bool':
                res = not isinstance(conf.get(field), bool)
            if res:
                raise Exception(error_msg.format(field))

    def format_window_conf(self,conf):

        window_name = conf.get('window_name')
        error_msg = 'window_conf-' + window_name + '-{}:配置不正确'

        self.check_fields(conf, ['window_name', 'window_type'], error_msg)
        try:
            conf['window_handle'] = int(conf['window_handle'])
        except:
            conf['window_handle'] = 0

        if self.check_field_none(conf.get('is_fuzzy')):
            conf['is_fuzzy'] = False
        if not isinstance(conf.get('is_fuzzy'), bool):
            raise Exception(error_msg.format('is_fuzzy'))

        if 'window_class' not in conf.keys():
            raise Exception(error_msg.format('window_class'))

        if 'window_title' not in conf.keys():
            raise Exception(error_msg.format('window_title'))

        if self.check_field_none(conf.get('is_sub')):
            conf['is_sub'] = False
        if not isinstance(conf.get('is_sub'), bool):
            raise Exception(error_msg.format('is_sub'))

        if conf['is_sub']:
            if self.check_field_none(conf.get('parent_window_class')):
                raise Exception(error_msg.format('parent_window_class'))
        if conf.get('parent_window_class') is None:
            conf['parent_window_class'] = None

        if self.check_field_none(conf.get('shut_off_button_offset')):
            conf['shut_off_button_offset'] = None

        return conf

    def format_action_params(self,error_msg, func_name, params):

        if params is None or params == '':
            params = {}

        if func_name == 'check_window':
            pass

        elif func_name == 'input_by_offset':
            if not isinstance(params.get('offset'), list):
                raise Exception(error_msg.format('offset'))
            if self.check_field_none(params.get('content')):
                raise Exception(error_msg.format('content'))
            if params['content'][0] == '$' and params['content'][-1] == '$':
                content = params['content'].replace('$', '')
                content = getattr(self, content)
                if self.check_field_none(params.get('content')):
                    raise Exception(error_msg.format('content'))
                params['content'] = content

        elif func_name == 'input_validate_code':
            self.check_fields(params, ['code_error_type', 'code_type'], error_msg)
            self.check_fields(params,
                         ['code_img_origin_offset', 'code_img_size', 'code_input_offset', 'login_button_offset'],
                         error_msg, 'list')
            self.check_fields(params, ['need_click'], error_msg, 'bool')
            if params['need_click']:
                self.check_fields(params, ['code_button_offset'], error_msg, 'list')
            if params['code_error_type'] == 'pop_window':
                if params['code_error_class'] is None and params['code_error_title'] is None:
                    raise Exception(error_msg.format('code_error_class-code_error_title'))

        elif func_name == 'click_left_by_offset':
            self.check_fields(params, ['offset'], error_msg, 'list')

        elif func_name == 'wait_window_init_by_mouse':
            if self.check_field_none(params.get('wait_times')):
                params['wait_times'] = 30

        return params

    def format_action(self, conf):

        conf_copy = copy.deepcopy(conf)
        if self.check_field_none(conf_copy.get('window_name')):
            conf_copy['window_name'] = None

        if self.check_field_none(conf_copy.get('step_name')):
            conf_copy['step_name'] = ''

        if self.check_field_none(conf_copy.get('error_exit')):
            conf_copy['error_exit'] = True

        if self.check_field_none(conf_copy.get('need_retry')):
            conf_copy['need_retry'] = False
            conf_copy['retry_times'] = 0
        if conf_copy['need_retry']:
            conf_copy['retry_times'] = int(conf_copy.get('retry_times'))

        if self.check_field_none(conf_copy.get('close_pop_window')):
            conf_copy['close_pop_window'] = True

        if self.check_field_none(conf_copy.get('set_window_avaliable')):
            conf_copy['set_window_avaliable'] = True

        if self.check_field_none(conf_copy.get('before_wait_seconds')):
            conf_copy['before_wait_seconds'] = 0
        else:
            try:
                int(conf_copy['before_wait_seconds'])
            except:
                conf_copy['before_wait_seconds'] = 0

        if self.check_field_none(conf_copy.get('after_wait_seconds')):
            conf_copy['after_wait_seconds'] = 0
        else:
            try:
                int(conf_copy['after_wait_seconds'])
            except:
                conf_copy['after_wait_seconds'] = 0

        return conf_copy

    def set_oprate_conf(self):

        oprate_conf = self.conf_copy['oprate_conf']
        window_conf = oprate_conf['window_conf']

        self.action_window_map = {}
        self.pop_windows = []
        for w in window_conf:
            new_w = self.format_window_conf(w)
            w_type = new_w['window_type']
            if w_type == 'action_window':
                self.action_window_map[new_w['window_name']] = new_w
            elif w_type == 'pop_window':
                self.pop_windows.append(new_w)

        action_confs = oprate_conf['action_confs']
        self.action_confs = []

        for i in range(0,len(action_confs)):

            error_msg = 'action_confs-' + str(i) + '-{}:配置不正确'
            ac = action_confs[i]
            func_name = ac.get('func_name')
            if self.check_field_none(func_name):
                raise Exception(error_msg.format('func_name'))

            ac_conf = self.format_action(ac)
            ac_conf['params'] = self.format_action_params(error_msg,func_name,ac['params'])
            self.action_confs.append(ac_conf)

if __name__ == '__main__':
    pass
