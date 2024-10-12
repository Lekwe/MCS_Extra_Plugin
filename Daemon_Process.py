import os
import MCSM_Remote
import threading
import time
import requests
from config import *
import mcrcon
import wmi
import sys


a = 0
if debug_mode == 1:
    host = '192.168.1.114'
    UUID = 'e214277d8f2143d99e40b846ff8fce33'
else:
    host = '127.0.0.1'
    UUID = '5a9bafef57794181a80219ce6c4a7cfc'
if in_out == 1:
    port = rcon_port_in
    nginx_port = nginx_port_in
    server_path = 'Newest_with_network'
    backup_path = 'Backups'
else:
    port = rcon_port_out
    nginx_port = nginx_port_out
    server_path = 'MCS_Outside'
    backup_path = 'Outside_Backups'
    UUID = '4d2f22d4ceb742e6871df912318c62c1'
# host = '192.168.1.114'
# UUID = '016a626cc52941d09b99644667fda79a'
# port = 57614
# nginx_port = 16724
# server_path = 'MCS_Creative'
# backup_path = 'Creative_Backups'
rcon = mcrcon.MCRcon(host, password, port)
# 连接到服务器


def get_logs():
    """
    获取完整服务器日志
    :return:
    """
    # print('http://{}:16722/logs/latest.log'.format(host))
    all_text = requests.get('http://{}:{}/logs/latest.log'.format(host, nginx_port)).text
    return all_text


def check_reply():
    global a, stop_
    msg = get_logs().split('\n')[-2]
    while 'MEP' not in msg:
        if stop_:
            break
        msg = get_logs().split('\n')[-2]
        # print(msg)
        pass
    a = 1
    return


rcon.connect()
rcon.command('say §6§l[DAEMON PREC]§3§lMEP守护进程已启动。')
rcon.disconnect()


while 114514 == 114514:
    newest_message = get_logs().split('\n')[-2]
    player_name = newest_message.split('<')[-1].split('>')[0].split(']')[-1]
    if newest_message.split('>')[-1][1:3] == '$$' and player_name in allowed_list and 'update_logs' not in newest_message and 'wx' not in newest_message:
        with open('MEP_Status.log', mode='r') as f1:
            status = f1.read()
            f1.close()
        if newest_message.split('$$')[-1].replace('\n', '').replace('\r', '') == 'restart':
            if player_name in admin_list:
                rcon.connect()
                time.sleep(1)
                rcon.command('say \n§6§l[DAEMON PREC]§3§l即将尝试重启MEP。')
                rcon.disconnect()
                time.sleep(2)
                os.system('taskkill /im MEP.exe /f')
                rcon.connect()
                rcon.command('say \n§6§l[DAEMON PREC]§3§l已终止现有的MEP进程。')
                time.sleep(3)
                os.system('start MEP.exe')
                time.sleep(3)
                rcon.command('say \n§6§l[DAEMON PREC]§3§l已尝试启动MEP。')
                rcon.disconnect()
                exit()
            else:
                rcon.connect()
                time.sleep(1)
                rcon.command('tell {} §6§l[DAEMON PREC]§3§l你暂无权限使用守护进程, 请向以下人员寻求帮助。'.format(player_name))
                for mem in admin_list:
                    rcon.command('tell {} &b{}'.format(player_name, mem))
                rcon.disconnect()
        elif newest_message.split('$$')[-1].replace('\n', '').replace('\r', '') == 'self_check':
            rcon.connect()
            time.sleep(1)
            rcon.command('say \n§6§l[DAEMON PREC]§3§l正在检查进程数。')
            wmi_obj = wmi.WMI()
            processes = wmi_obj.Win32_Process()
            a, b = 0, 0
            for process in processes:
                # print(f"Process ID: {process.ProcessId}, Name: {process.Name}")
                if process.Name == 'Daemon_Process.exe':
                    a += 1
                elif process.Name == 'MEP.exe':
                    b += 1
            rcon.command('say §6§l[DAEMON PREC]§3§l检查完成, \n共有§9§l{}§3§l个守护进程, §9§l{}§3§l个MEP进程。'.format(str(a), str(b)))
            rcon.command('say §6§l[DAEMON PREC]§3§lMEP状态为§9§l{}。'.format(status))
            rcon.disconnect()

        else:
            if status == '1':
                pass
            else:
                stop_ = False
                check_reply_process = threading.Thread(target=check_reply)
                check_reply_process.start()
                time.sleep(2)
                if a == 1:
                    print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}]Running.')
                    a = 0
                else:
                    rcon.connect()
                    print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}]Offline.')
                    a = 0
                    rcon.command('say \n§6§l[DAEMON PREC]§3§l检测到MEP疑似无法正常使用，即将尝试重启。')
                    rcon.disconnect()
                    time.sleep(2)
                    os.system('taskkill /im MEP.exe /f')
                    rcon.connect()
                    rcon.command('say \n§6§l[DAEMON PREC]§3§l已终止现有的MEP进程。')
                    time.sleep(3)
                    os.system('start MEP.exe')
                    time.sleep(3)
                    rcon.command('say \n§6§l[DAEMON PREC]§3§l已尝试启动MEP。')
                    rcon.disconnect()
                    sys.exit()
                stop_ = True
                check_reply_process.join()
    time.sleep(0.1)
