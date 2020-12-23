# -*- coding: utf-8 -*-

try:
    from win32.lib import win32con
    from win32.win32api import GetSystemMetrics
    from win32.win32gui import GetDC
    from win32.win32print import GetDeviceCaps

    win32_flag = True
except:
    win32_flag = False
    screen_scale_rate_ = 1

    from src.API import write_error
    write_error("[INFO] 没有win32, 无法自动获取屏幕缩放比例,设置为: {}".format(screen_scale_rate_))


def get_real_resolution():
    """获取真实的分辨率"""
    hDC = GetDC(0)
    # 横向分辨率
    w = GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # 纵向分辨率
    h = GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h


def get_screen_size():
    """获取缩放后的分辨率"""
    w = GetSystemMetrics(0)
    h = GetSystemMetrics(1)
    return w, h


def get_screen_rate():
    if win32_flag:
        real_resolution = get_real_resolution()
        screen_size = get_screen_size()
        screen_scale_rate = round(real_resolution[0] / screen_size[0], 2)
    else:
        screen_scale_rate = screen_scale_rate_
    return screen_scale_rate


if __name__ == '__main__':
    print("get_screen_rate:", get_screen_rate())
