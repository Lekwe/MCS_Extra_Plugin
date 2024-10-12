import shutil
import time


def disk_info(which='all'):
    gb = 1024 ** 3
    total_b, used_b, free_b = shutil.disk_usage('C:')
    c_total = '磁盘总空间: {:6.2f} GB '.format(total_b / gb)
    c_used = '已用空间 : {:6.2f} GB '.format(used_b / gb)
    c_free = '可用空间 : {:6.2f} GB '.format(free_b / gb)

    total_d, used_d, free_d = shutil.disk_usage('D:')
    d_total = '磁盘总空间: {:6.2f} GB '.format(total_d / gb)
    d_used = '已用空间 : {:6.2f} GB '.format(used_d / gb)
    d_free = '可用空间 : {:6.2f} GB '.format(free_d / gb)
    if which == 'all':
        return [[c_total, c_used, c_free], [d_total, d_used, d_free]]
    elif which == 'c':
        return [c_total, c_used, c_free]
    elif which == 'd':
        return [d_total, d_used, d_free]


def now_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


print(now_time())
