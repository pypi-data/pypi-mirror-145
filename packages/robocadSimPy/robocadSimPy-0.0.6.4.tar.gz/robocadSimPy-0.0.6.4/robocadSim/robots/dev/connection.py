import socket
import threading
from .holder import *


class ListenPort:
    def __init__(self, port: int, is_camera=False):
        self.__port = port
        self.__is_camera = is_camera

        # other
        self.__stop_thread = False
        self.out_string = ''
        self.out_bytes = b''

    def start_listening(self):
        listening_thread = threading.Thread(target=self.listening, args=())
        listening_thread.start()

    def listening(self):
        sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        sct.connect(('127.0.0.1', self.__port))
        if LOG_LEVEL < LOG_EXC_INFO:
            print("connected: " + str(self.__port))
        while not self.__stop_thread:
            buffer_size = 1024
            if self.__is_camera:
                data = sct.recv(4)
                buffer_size = (data[3] & 0xff) << 24 | (data[2] & 0xff) << 16 | (data[1] & 0xff) << 8 | (data[0] & 0xff)
                sct.sendall(b'Received')
            self.out_bytes = sct.recv(buffer_size)
            if not self.__is_camera:
                self.out_string = self.out_bytes.decode('utf-16-le')
            sct.sendall(b'Received')
        if LOG_LEVEL < LOG_EXC_INFO:
            print("disconnected: " + str(self.__port))
        sct.shutdown(socket.SHUT_RDWR)
        sct.close()

    def reset_out(self):
        self.out_string = ''
        self.out_bytes = b''

    def stop_listening(self):
        self.__stop_thread = True
        self.reset_out()


class TalkPort:
    def __init__(self, port: int):
        self.__port = port

        # other
        self.__stop_thread = False
        self.out_string = ''

    def start_talking(self):
        listening_thread = threading.Thread(target=self.talking, args=())
        listening_thread.start()

    def talking(self):
        sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        sct.connect(('127.0.0.1', self.__port))
        if LOG_LEVEL < LOG_EXC_INFO:
            print("connected: " + str(self.__port))
        while not self.__stop_thread:
            sct.sendall((self.out_string + "$").encode('utf-16-le'))
        if LOG_LEVEL < LOG_EXC_INFO:
            print("disconnected: " + str(self.__port))
        sct.shutdown(socket.SHUT_RDWR)
        sct.close()

    def reset_out(self):
        self.out_string = ''

    def stop_talking(self):
        self.__stop_thread = True
        self.reset_out()


class ParseChannels:
    @staticmethod
    def parse_float_channel(txt: str):
        try:
            return tuple(map(float, txt.replace(',', '.').split(';')))
        except (Exception, ValueError):
            return tuple()

    @staticmethod
    def parse_bool_channel(txt: str):
        try:
            return tuple(map(bool, map(int, txt.split(';'))))
        except (Exception, ValueError):
            return tuple()

    @staticmethod
    def join_float_channel(lst: tuple):
        return ';'.join(map(str, lst))

    @staticmethod
    def join_bool_channel(lst: tuple):
        return ';'.join(map(str, map(int, lst)))
