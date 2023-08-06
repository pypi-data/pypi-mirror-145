# -*- coding: utf-8 -*-

# @File    : ws_server.py
# @Date    : 2022-03-31
# @Author  : chenbo

__author__ = 'chenbo'

import base64
import hashlib
import socket
from struct import pack, unpack
import threading
import json


class WebSocketConn:

    def __init__(self, conn):
        self.conn = conn
        request = self.conn.recv(1024).strip().decode('utf-8', 'ignore').split('\r\n')

        # parse headers into dict
        self.headers = dict([line.split(': ', 1) for line in request[1:]])

        # perform WebSocket handshake
        self._handshake()

    def _handshake(self):
        key = self.headers.get('Sec-WebSocket-Key') + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        resp_key = base64.standard_b64encode(hashlib.sha1(key.encode()).digest()).decode()
        res_header = {
            'Upgrade': 'websocket',
            'Connection': 'Upgrade',
            'Sec-WebSocket-Accept': resp_key,
        }
        response = 'HTTP/1.1 101 Switching Protocols\r\n'
        for i in res_header:
            response += '%s: %s\r\n' % (i, res_header[i])
        response += '\r\n'
        self.conn.send(response.encode())

    def recv(self):
        '''
        retrieve data from the client.
        '''
        buffer = self.conn.recv(2)
        if buffer:
            # read the three possible content-length number
            length = buffer[1] - 2 ** 7
            if length == 126:
                length, = unpack('>H', self.conn.recv(2))
            elif length == 127:
                length, = unpack('>Q', self.conn.recv(8))

            # get the masking key for the content
            mask = self.conn.recv(4)

            # encoded content
            buffer = self.conn.recv(length)

            decoded = ''
            for i in range(length):
                # decode the content
                decoded += chr(buffer[i] ^ mask[i % 4])
            return decoded

    def send(self, data):
        '''
        send content in form of WebSocket data frame.
        '''
        buffer = b''
        # initial 4 bits
        buffer += pack('>B', 129)

        # length of the content
        if len(data) > 126:
            if len(data) < 2 ** 10:
                buffer += pack('>BH', 126, len(data))
            else:
                buffer += pack('>BQ', 127, len(data))
        else:
            buffer += pack('>B', len(data))

        # append content
        buffer += data.encode()

        self.conn.send(buffer)

    def close(self):
        '''
        close the connection.
        '''
        self.conn.close()


class WebSocket:
    def __init__(self, addr):
        '''
        a WebSocket socket.
        @param addr: the address to bind with, i.e. (host, port)
        '''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.sock.bind(addr)

    def listen(self, num):
        '''
        maximum clients to listen to.
        '''
        self.sock.listen(num)

    def accept(self):
        '''
        accept the connection from a client.
        '''
        conn, self.addr = self.sock.accept()
        self.conn = WebSocketConn(conn)
        return self.conn, self.addr


class WebSocketServer:
    def __init__(self, sock):
        '''
        a WebSocket server class with multithreading.
        '''
        self.sock = sock
        self.player_pool = []
        self.mini_cli: dict = {}

    def run(self):
        '''
        run server.
        '''
        # lock for controlling the player pool
        lock = threading.Lock()
        while True:
            conn, addr = self.sock.accept()
            threading.Thread(target=self.handle, args=(conn, addr, lock)).start()

    def handle(self, conn: WebSocketConn, addr: tuple, lock: threading.Lock):

        while True:
            try:
                buffer = conn.recv()
                key = conn.headers["Sec-WebSocket-Key"]
                if buffer:
                    if buffer == 'é':
                        print('结束')
                        mini_c: SocketClient = self.mini_cli.pop(key)
                        mini_c.close()
                        conn.close()
                        return 0

                    req: dict = {}
                    try:
                        req = json.loads(buffer.strip())
                    except Exception as e:
                        conn.send(f'-1|0|{e}')

                    self.__echo__(req, conn, lock)
                    # msg_type = req.setdefault('type', None)
                    # if msg_type:
                    #     if msg_type == 'minicap':
                    #         mini = SocketClient()
                    #         mini.connect('localhost', 10010)
                    #         for data in mini.recv():
                    #             conn.send(json.dumps({'type': 'minicap', 'content': data}))
                    # else:
                    #     if req.get('id') >= len(self.player_pool):
                    #         lock.acquire()
                    #         self.player_pool.append(req)
                    #         lock.release()
                    #     else:
                    #         self.player_pool[req.get('id')] = req
                    #     conn.send(json.dumps(self.player_pool))
            except Exception as e:
                conn.close()
                return 0

    def __echo__(self, buffer: dict, conn: WebSocketConn, lock: threading.Lock):
        msg_type = buffer.setdefault('type', None)
        key = conn.headers["Sec-WebSocket-Key"]
        if msg_type == 'minicap':
            mini_c: SocketClient = self.mini_cli.setdefault(key, None)
            if mini_c:
                return
            print("初始化minicap")
            mini_c = SocketClient()
            mini_c.run('localhost', 10010, conn)
            lock.acquire()
            self.mini_cli[key] = mini_c
            lock.release()


class SocketClient:

    def __init__(self):
        self.isRun = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP

    def run(self, host: str, port: str, conn: WebSocketConn):
        print('run')
        threading.Thread(target=self.__repeat__, args=(host, port, conn)).start()

    def __repeat__(self, host: str, port: str, conn: WebSocketConn):
        print('__repeat__', self.isRun)
        self.sock.connect((host, port))  # 要连接的IP与端口
        while self.isRun:
            print('请求minicap')
            self.send('1920x1080/0')
            data = self.sock.recv(1024)  # 把接收的数据定义为变量
            print('minicap 数据', data)
            conn.send(f'0|1|{data}')

    def send(self, msg: str):
        self.sock.send(msg.encode())

    def close(self):
        self.isRun = False
        self.sock.close()


if __name__ == '__main__':
    sock = WebSocket(('0.0.0.0', 10022))
    sock.listen(10)
    server = WebSocketServer(sock)
    server.run()
