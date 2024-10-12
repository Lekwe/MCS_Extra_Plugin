import time
from config import *
import requests
import json


if debug_mode == 1:
    ip = '192.168.1.114'
    port = '23333'
    Remote_ID = 'df8eddb1d31a4262ae91592bf765e7a1'
    api_key = '6ab1a48793b6447c924a5977f62e2cea'
else:
    ip = '127.0.0.1'
    port = '23333'
    Remote_ID = '86cded418c4b4ca2b1bcd37ca37e7fca'
    api_key = '30f9b8ac7f5747cda5c0856a52bb8f70'


def start_server(uuid):
    response = requests.post('http://{}:{}/api/protected_instance/open?remote_uuid={}&uuid={}&apikey={}'.format(ip, port, Remote_ID, uuid, api_key))
    return [response.text, response.status_code]


def stop_server(uuid):
    response = requests.post(
        'http://{}:{}/api/protected_instance/stop?remote_uuid={}&uuid={}&apikey={}'.format(
            ip, port, Remote_ID, uuid, api_key))
    return [response.text, response.status_code]


def send_command(uuid, command):
    response = requests.post(
        'http://{}:{}/api/protected_instance/command?remote_uuid={}&uuid={}&apikey={}&command={}'.format(
            ip, port, Remote_ID, uuid, api_key, command))
    # print('http://{}:{}/api/protected_instance/command?remote_uuid={}&uuid={}&apikey={}&command={}'.format(
    #         ip, port, Remote_ID, uuid, api_key, command))
    return [response.text, response.status_code]


def server_status(uuid):
    """

    :param uuid:
    :return: 0 -> stopped  1 -> stopping  2 -> starting  3 -> running
    """
    response = requests.get('http://{}:{}/api/instance?remote_uuid={}&uuid={}&apikey={}'.format(ip, port, Remote_ID, uuid, api_key))
    return json.loads(response.text)['data']['status']


# for i in range(10):
#     print(type(server_status('e214277d8f2143d99e40b846ff8fce33')))
#     time.sleep(1)


# server_status('47e79a92e96d49b5a644643e85508847')
