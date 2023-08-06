# -*- coding: utf-8 -*-
# @Time    : 2022/4/4 9:59 下午
# @Author  : jeffery
# @FileName: get_server_ip.py
# @github  : https://github.com/jeffery0628
# @Description:

import paramiko
from tqdm import tqdm

if __name__ == '__main__':
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    all_ip = []
    wrong_ip = []
    for x in range(1):
        for y in tqdm(range(256)):
            ip = f'192.168.{x}.{y}'
            all_ip.append(ip)
            try:
                ssh.connect(hostname=ip, port=22, username='lizhen', password='lizhen123', timeout=0.5)
            except Exception as e:
                wrong_ip.append(ip)

    print(set(all_ip).difference(set(wrong_ip)))
