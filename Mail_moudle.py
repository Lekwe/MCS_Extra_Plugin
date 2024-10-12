import os
import smtplib
import shutil
import time
import pathlib
from stat import S_ISDIR
from errno import EACCES
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# init
type_list = ['服务器自动外置异盘备份', '玩家发起的备份']
with open('auto_backup_latest_log.log', 'w', encoding='utf-8') as f:
    f.close()


def send_email(mail_content):
    sender = 'mcs_official@sina.com'
    # receiver = ['zscleo@qq.com', '2754049342@qq.com', 'b98818888@163.com', '1419864641@qq.com', 'sb_zhang@outlook.com']
    receiver = ['zscleo@qq.com', 'mcs_offical@163.com']
    mail_server = 'smtp.sina.cn'
    email_name = '玩家你好'
    username = "mcs_official@sina.com"
    password = 'cc6eb7bf4d662dd7'
    message = MIMEText(mail_content, 'html', 'utf-8')
    message['Subject'] = Header(email_name, charset='utf-8')
    message['From'] = formataddr(('MCS Official', 'mcs_official@sina.com'))
    message['To'] = ",".join(receiver)
    # 邮箱登录
    smtp = smtplib.SMTP()  # 实例化邮箱
    smtp.connect(mail_server)
    smtp.login(username, password)
    # 发送邮件
    smtp.sendmail(sender, receiver, message.as_string())
    smtp.quit()


def disk_info(which='all'):
    gb = 1024 ** 3
    total_b, used_b, free_b = shutil.disk_usage('C:')
    c_total = '磁盘总空间: {:6.2f} GB  '.format(total_b / gb)
    c_used = '已用空间 : {:6.2f} GB  '.format(used_b / gb)
    c_free = '可用空间 : {:6.2f} GB '.format(free_b / gb)

    total_d, used_d, free_d = shutil.disk_usage('D:')
    d_total = '磁盘总空间: {:6.2f} GB  '.format(total_d / gb)
    d_used = '已用空间 : {:6.2f} GB  '.format(used_d / gb)
    d_free = '可用空间 : {:6.2f} GB '.format(free_d / gb)
    if which == 'all':
        return [[c_total, c_used, c_free], [d_total, d_used, d_free]]
    elif which == 'c':
        return [c_total, c_used, c_free]
    elif which == 'd':
        return [d_total, d_used, d_free]


def get_now_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


list1 = []


def get_size(path):
    fileList = os.listdir(path)  # 获取path目录下所有文件
    for filename in fileList:
        pathTmp = os.path.join(path, filename)  # 获取path与filename组合后的路径
        if os.path.isdir(pathTmp):  # 判断是否为目录
            get_size(pathTmp)  # 是目录就继续递归查找
        elif os.path.isfile(pathTmp):  # 判断是否为文件
            filesize = os.path.getsize(pathTmp)  # 如果是文件，则获取相应文件的大小
            # print('目录中的子文件大小：%d字节' % filesize)
            list1.append(filesize)


def copy_folder(src, dst):
    """
    复制文件夹
    :param src: 原文件夹路径
    :param dst: 目标文件夹路径
    :return: none
    """
    names = os.listdir(src)
    if not os.path.exists(dst):
        os.makedirs(dst)

    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)

        try:
            if S_ISDIR(os.stat(srcname).st_mode):
                copy_folder(srcname, dstname)
            else:
                shutil.copy2(srcname, dstname)
            print('Copying: ' + srcname)
        except OSError as e:
            if e.errno != EACCES:
                raise
            print('failed', f'[{get_now_time()}] Log: 正在跳过 {srcname}(无法访问)\n')
            with open('auto_backup_latest_log.log', mode='a', encoding='utf-8') as f1:
                f1.write(f'[{get_now_time()}] Log: 正在跳过 {srcname}(无法访问)\n')
                f1.close()


# send_email('你现在收到的是一封来自MEP_Mail自动发送的测试邮件，猜猜不久会有什么功能吧！💕')
def backup_proc(backup_type=0):
    mail_content = "<b>备份类型:</b> {}\n<br/><b>存储路径:</b> {}\n<br/><b>发起时间:</b> {}\n<br/><b>完成时间:</b> {}\n<br/><b>现备份档数:</b> {}\n<br/><b>备份数据量:</b> {}<br/><b>备份占用空间:</b> {}<br/>\n<br/><b>磁盘空间(C:\):</b> {}\n<br/><b>磁盘空间(D:\):</b> {}\n\n<br/><br/><b>日志:</b>\n<br/>{}<br/><br/>"
    folder_name = get_now_time()
    copy_folder(r"D:\MCS_Server\Newest_with_network\server", r'C:\MCS_Backup_C\{}'.format(folder_name.replace(':', '-')))
    with open('auto_backup_latest_log.log', mode='a', encoding='utf-8') as f2:
        f2.write(f'[{get_now_time()}] Log: Copied Successfully.\n')
        f2.close()
    finishing_time = get_now_time()
    gb = 1024 ** 3
    path = r'C:\MCS_Backup_C\{}'.format(folder_name.replace(':', '-'))
    get_size(path)
    if sum(list1) / gb < 1:
        total_data = '%.3fMB ' % (sum(list1) / gb * 1024)
    else:
        total_data = '%.3fGB ' % (sum(list1) / gb)
    print('Completed')
    disk_c_info = ''.join(disk_info('c'))
    disk_d_info = ''.join(disk_info('d'))
    amount = len(os.listdir(r'C:\MCS_Backup_C'))
    with open('auto_backup_latest_log.log', mode='r', encoding='utf-8') as f3:
        log_content = f3.read()
        f3.close()
    get_size('C:\MCS_Backup_C')
    if sum(list1) / gb < 1:
        total_data2 = '%.3fMB ' % (sum(list1) / gb * 1024)
    else:
        total_data2 = '%.3fGB ' % (sum(list1) / gb)
    return mail_content.format(type_list[backup_type], r'C:\MCS_Backup_C\{}'.format(folder_name.replace(':', '-')), folder_name, finishing_time, amount, total_data, total_data2, disk_c_info, disk_d_info, log_content.replace('\n', '<br/>').replace('无法访问', '<span style="color:red">无法访问</span>').replace('正在跳过', '<span style="color:#d4ac0d">正在跳过</span>'))


a = backup_proc()
print(a + '此功能尚在完善，如有BUG请及时向腐竹反馈。🙃<br/><b>MCS Official</b>')
send_email(a + '此功能尚在完善，如有BUG请及时向腐竹反馈。🙃<br/><b>MCS Official</b>')
