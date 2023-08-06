# -*- coding: utf-8 -*-

# @File    : test_sockt.py
# @Date    : 2022-03-31
# @Author  : chenbo

__author__ = 'chenbo'

import socket
import base64

HOST = '192.168.1.101'
PORT = 10010
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
s.connect((HOST, PORT))  # 要连接的IP与端口

index = 1
while index < 3:
    s.send('1920x1080/0'.encode())
    data = s.recv(1024)  # 把接收的数据定义为变量
    if index == 1:
        print(data)
    else:
        print(data[3:])
    index += 1

s.close()  # 关闭连接
