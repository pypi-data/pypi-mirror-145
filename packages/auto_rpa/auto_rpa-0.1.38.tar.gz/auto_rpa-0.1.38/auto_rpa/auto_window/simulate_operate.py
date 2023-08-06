import pyautogui
import win32gui, win32con, win32api
import time
import pyperclip
from pynput.keyboard import Key, Controller
import ctypes

from win32con import IDC_APPSTARTING, IDC_ARROW, IDC_CROSS, IDC_HAND, \
    IDC_HELP, IDC_IBEAM, IDC_ICON, IDC_NO, IDC_SIZE, IDC_SIZEALL, \
    IDC_SIZENESW, IDC_SIZENS, IDC_SIZENWSE, IDC_SIZEWE, IDC_UPARROW, IDC_WAIT
from win32gui import LoadCursor

class Cursor(object):
    def __init__(self, cursor_type=None):
        _handle = LoadCursor(0, cursor_type)
        self.type = cursor_type
        self._handle = _handle

DEFAULT_CURSORS \
    = APPSTARTING, ARROW, CROSS, HAND, HELP, IBEAM, ICON, NO, SIZE, SIZEALL, \
      SIZENESW, SIZENS, SIZENWSE, SIZEWE, UPARROW, WAIT \
    = Cursor(IDC_APPSTARTING), Cursor(IDC_ARROW), Cursor(IDC_CROSS), \
      Cursor(IDC_HAND), Cursor(IDC_HELP), Cursor(IDC_IBEAM), Cursor(IDC_ICON), \
      Cursor(IDC_NO), Cursor(IDC_SIZE), Cursor(IDC_SIZEALL), \
      Cursor(IDC_SIZENESW), Cursor(IDC_SIZENS), Cursor(IDC_SIZENWSE), \
      Cursor(IDC_SIZEWE), Cursor(IDC_UPARROW), Cursor(IDC_WAIT)


pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1

class SimulateOperate():

    @classmethod
    def click_hotkey(self,keys):

        time.sleep(0.1)
        if len(keys) == 2:
            key1 = keys[0]
            key2 = keys[1]
            pyautogui.hotkey(key1,key2, interval=0.01)
        elif len(keys) == 3:
            key1 = keys[0]
            key2 = keys[1]
            key3 = keys[3]
            pyautogui.hotkey(key1, key2,key3, interval=0.01)
        else:
            raise Exception('组合键参数数量不对')
        time.sleep(0.1)

    @classmethod
    def click_key(self, key):

        time.sleep(0.1)
        pyautogui.click()
        pyautogui.press(key)
        time.sleep(0.1)

    @classmethod
    def move_to(cls, position):

        pyautogui.moveTo(position[0], position[1])

    @classmethod
    def move_to_by_window_handle(cls, window_handle, offset):

        pos = cls.cal_pos_by_window_handle(window_handle, offset)
        cls.move_to(pos)

    @classmethod
    def double_click_delay(cls):
        time.sleep(0.05)
        pyautogui.click(clicks=2, interval=0.05)
        time.sleep(0.1)

    @classmethod
    def cal_pos_by_window_handle(cls, window_handle, offset):

        origin = cls.window_origin_location(window_handle)
        return [origin[0] + offset[0], origin[1] + offset[1]]

    @classmethod
    def click_left_delay(cls):

        time.sleep(0.1)
        pyautogui.click()
        time.sleep(0.1)

    @classmethod
    def move_and_click_left(cls, offset):

        cls.move_to(offset)
        cls.click_left_delay()
        time.sleep(0.5)

    @classmethod
    def move_and_click_left_by_window_handle(cls, window_handle, offset):

        cls.move_to_by_window_handle(window_handle, offset)
        time.sleep(0.5)
        cls.click_left_delay()

    @classmethod
    def click_right_delay(cls):

        time.sleep(0.1)
        pyautogui.click(button='right')
        time.sleep(0.1)

    @classmethod
    def move_and_click_right(cls, offset):

        cls.move_to(offset)
        cls.click_right_delay()
        time.sleep(0.5)

    @classmethod
    def move_and_click_right_by_window_handle(cls, window_handle, offset):

        cls.move_to_by_window_handle(window_handle, offset)
        time.sleep(0.5)
        cls.click_right_delay()

    @classmethod
    def move_and_click_left_by_img(cls, img_path):

        pos = pyautogui.locateCenterOnScreen(img_path, grayscale=True)
        cls.move_and_click_left(pos)

    @classmethod
    def check_img_exists(cls, img_path):

        res = pyautogui.locateCenterOnScreen(img_path, grayscale=True)
        if res is None:
            return False
        else:
            return True

    @classmethod
    def get_img_pos(cls, img_path):

        res = pyautogui.locateCenterOnScreen(img_path, grayscale=True)
        if res is None:
            raise Exception('找不到图片的位置')
        return res


    @classmethod
    def get_mouse_status(cls):

        '''获取鼠标状态'''

        curr_cursor_handle = win32gui.GetCursorInfo()[1]
        for cursor_handle in DEFAULT_CURSORS:
            if cursor_handle._handle == curr_cursor_handle:
                return cursor_handle.type
        return None

    @classmethod
    def wait_data_by_mouse_status(cls):

        '''判断鼠标是否处于繁忙状态'''

        normal_cursor_handle = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        curr_cursor_handle = win32gui.GetCursorInfo()[1]
        if normal_cursor_handle != curr_cursor_handle:
            return 1
        else:
            return 0

    @classmethod
    def reset_caplock(cls):
        if win32api.GetKeyState(20) == 1:
            win32api.keybd_event(20, 0, 0, 0)
            win32api.keybd_event(20, 0, win32con.KEYEVENTF_KEYUP, 0)

    @classmethod
    def clean_input(cls, window_handle, offset, right=100, backspace=100):

        cls.move_and_click_left_by_window_handle(window_handle, offset)
        pyautogui.press('right', presses=right)
        pyautogui.press('backspace', presses=backspace)

    @classmethod
    def input_by_window_handle(cls, window_handle, offset, content, content_type='eng', right=100, backspace=100):

        keyboard = Controller()

        cls.set_window_avaliable(window_handle)
        pos = cls.cal_pos_by_window_handle(window_handle, offset)
        pyautogui.moveTo(pos[0], pos[1])
        cls.double_click_delay()
        cls.reset_caplock()
        cls.clean_input(window_handle, offset, right, backspace)
        if content_type == 'eng':
            keyboard.type(content)
        elif content_type == 'chn':
            pyperclip.copy(content)
            pyautogui.hotkey('ctrl', 'v', interval=0.01)
        time.sleep(0.1)

    @classmethod
    def check_windows_lock(self):

        '''判断电脑是否锁屏'''

        u = ctypes.windll.LoadLibrary('user32.dll')
        result = u.GetForegroundWindow()
        if result == 0:
            return True
        else:
            return False

    @classmethod
    def set_window_avaliable(cls, window_handle):
        whs = list()
        win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), whs)
        if window_handle in whs:
            # send a keyboard signal, or it will raise Exception
            pyautogui.press('alt')
            if win32gui.GetForegroundWindow() != window_handle:
                win32gui.SetForegroundWindow(window_handle)

    @classmethod
    def window_size(cls, window_handle):
        '''
        :return:list, [length, height]
        '''
        rect = win32gui.GetWindowRect(window_handle)
        return [rect[2] - rect[0], rect[3] - rect[1]]

    @classmethod
    def window_origin_location(cls, window_handle):
        return win32gui.GetWindowRect(window_handle)[:2]

    @classmethod
    def close_window(cls, window_handle):

        '''关闭弹出框'''

        if window_handle == 0:
            return 0

        try:
            cls.set_window_avaliable(window_handle)
            win32gui.CloseWindow(window_handle)
            win32gui.PostMessage(window_handle, win32con.WM_CLOSE, 0, 0)
        except:
            pass

        return 0

    @classmethod
    def mini_window(cls, window_handle):

        '''缩小'''

        try:
            cls.set_window_avaliable(window_handle)
            win32gui.ShowWindow(window_handle, win32con.SW_MINIMIZE)
        except:
            pass

        return 0

    @classmethod
    def max_window(cls, window_handle):

        '''缩小'''

        try:
            cls.set_window_avaliable(window_handle)
            win32gui.ShowWindow(window_handle, win32con.SW_MAXIMIZE)
        except:
            pass

        return 0

    @classmethod
    def get_window_size_status(cls, window_handle):

        tup = win32gui.GetWindowPlacement(window_handle)
        if tup[1] == win32con.SW_SHOWMAXIMIZED:
            return 'max'
        elif tup[1] == win32con.SW_SHOWMINIMIZED:
            return 'min'
        elif tup[1] == win32con.SW_SHOWNORMAL:
            return 'nor'

    @classmethod
    def check_window_handle_exists(cls, window_handle):

        if win32gui.IsWindow(window_handle) == 1 and win32gui.IsWindowVisible(
                window_handle) == 1 and win32gui.IsWindowEnabled(
                window_handle) == 1:
            return True
        else:
            return False

    @classmethod
    def get_window_handle(cls, window_class, window_title):

        return win32gui.FindWindow(window_class, window_title)

    @classmethod
    def find_all_sub_window_handle(cls, parent_window_handle):

        sub_window_list = list()
        win32gui.EnumChildWindows(parent_window_handle, lambda hWnd, param: param.append(hWnd), sub_window_list)
        return sub_window_list

    @classmethod
    def find_window_handle_by_sub_cls_tit(cls, parent_window_class, window_class, window_title):

        parent_window_handle = cls.find_all_window_handle()
        for p_window_handle in parent_window_handle:
            t, c = win32gui.GetWindowText(p_window_handle), win32gui.GetClassName(p_window_handle)
            if c != parent_window_class:
                continue
            sub_window_handle = win32gui.FindWindowEx(p_window_handle, None, window_class, window_title)
            if sub_window_handle != 0:
                return p_window_handle
        return 0

    @classmethod
    def find_all_window_handle(cls):

        parent_window_list = list()
        win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), parent_window_list)
        return parent_window_list

    @classmethod
    def find_window_handle_by_fuzzy_tit(cls, tit):

        window_list = cls.find_all_window_handle()
        for i in window_list:
            t, c = win32gui.GetWindowText(i), win32gui.GetClassName(i)
            if tit in t:
                return i
        return 0

    @classmethod
    def check_window_is_show(cls, window_class=None, window_title=None, is_fuzzy=False, is_sub=False,
                             parent_window_class=None):

        if is_sub:
            window_handle = cls.find_window_handle_by_sub_cls_tit(parent_window_class, window_class, window_title)
        else:
            if is_fuzzy:
                window_handle = cls.find_window_handle_by_fuzzy_tit(window_title)
            else:
                window_handle = cls.get_window_handle(window_class, window_title)

        if window_handle == 0:
            return 0
        if cls.check_window_handle_exists(window_handle):
            cls.set_window_avaliable(window_handle)
            return window_handle
        else:
            return 0

    @classmethod
    def close_pop_window(cls, pop_windows=None):

        if pop_windows is not None:
            for w in pop_windows:
                window_handle = cls.check_window_is_show(w.get('window_class'), w.get('window_title'),
                                                         w.get('is_fuzzy'), w.get('is_sub'),
                                                         w.get('parent_window_class'))

                if window_handle != 0:
                    if w.get('shut_off_button_offset') is None:
                        cls.close_window(window_handle)
                    else:
                        cls.move_and_click_left_by_window_handle(window_handle, w['shut_off_button_offset'])

    @classmethod
    def pixel_check_by_window_handle(cls, window_handle, window_color, window_color_pos, reverse=False,
                                     try_distance=10, match_times=1, horizontal=True, step=1):
        '''
        检查坐标颜色
        @param window_handle: 句柄
        @param window_color: 对比的窗口颜色
        @param window_color_pos: 窗口颜色起始坐标
        @param reverse: 结果是否取反
        @param try_distance: 尝试比较的次数
        @param match_times: 成功匹配的次数
        @param horizontal: 横向比较或者纵向比较
        @param step: 每次像素移动的步长
        @return: 成功失败
        '''

        pos = cls.cal_pos_by_window_handle(window_handle, window_color_pos)
        count = 0
        ori_x = int(pos[0])
        ori_y = int(pos[1])
        for i in range(0, try_distance, step):
            if horizontal:
                x, y = ori_x + i, ori_y
            else:
                x, y = ori_x, ori_y + i
            if pyautogui.pixelMatchesColor(x, y, window_color):
                count += 1

        if count >= match_times:
            match_res = True
        else:
            match_res = False

        if not reverse:
            return int(match_res)
        else:
            return int(bool(1 - match_res))

    @classmethod
    def pixel_check_by_pos(cls, window_color, window_color_pos, try_distance=10, match_times=1, horizontal=True, step=1):

        pos = window_color_pos
        count = 0
        ori_x = int(pos[0])
        ori_y = int(pos[1])
        for i in range(0, try_distance, step):
            if horizontal:
                x, y = ori_x + i, ori_y
            else:
                x, y = ori_x, ori_y + i
            if pyautogui.pixelMatchesColor(x, y, window_color):
                count += 1

        if count >= match_times:
            match_res = True
        else:
            match_res = False

        return match_res

    @classmethod
    def click_by_color(cls, window_handle, window_color, start_pos, try_distance=100, match_times=5, horizontal=False,
                       step=1):

        '''
        检查坐标颜色
        @param window_handle: 句柄
        @param window_color: 对比的窗口颜色
        @param start_pos: 窗口颜色起始坐标
        @param try_distance: 尝试比较的次数
        @param match_times: 需要匹配的次数
        @param horizontal: 横向比较或者纵向比较
        @param step: 每次像素移动的步长
        @return: 成功失败
        '''

        pos = cls.cal_pos_by_window_handle(window_handle, start_pos)
        ori_x = int(pos[0])
        ori_y = int(pos[1])
        count = 0
        for i in range(0, try_distance, step):
            if horizontal:
                x, y = ori_x + i, ori_y
            else:
                x, y = ori_x, ori_y + i
            if pyautogui.pixelMatchesColor(x, y, window_color):
                count += 1
                if count >= match_times:
                    cls.move_and_click([x, y])
                    break

        return None

    @classmethod
    def window_handle_img(cls, threshold=115):

        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        return table

    @classmethod
    def wait_window_init(cls, wait_times=20):

        cls.move_to([100, 100])
        time.sleep(2)

        n = 0
        while n < wait_times:
            if cls.wait_data_by_mouse_status() == 0:
                break
            n += 1
            time.sleep(1)

    @classmethod
    def wait_data_load_by_mouse_status(cls, wait_times=60):

        time.sleep(0.5)
        n = 0
        while n < wait_times:
            if cls.wait_data_by_mouse_status() == 0:
                break
            n += 1
            time.sleep(1)

