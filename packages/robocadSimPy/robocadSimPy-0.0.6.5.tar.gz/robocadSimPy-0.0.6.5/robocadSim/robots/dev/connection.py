import socket
import threading
import time
import warnings
from .holder import *


class ListenPort:
    def __init__(self, port: int, is_camera=False):
        self.__port = port
        self.__is_camera = is_camera

        # other
        self.__stop_thread = False
        self.out_string = ''
        self.out_bytes = b''

        self.sct = None
        self.thread = None

    def start_listening(self):
        self.thread = threading.Thread(target=self.listening, args=())
        self.thread.start()

    def listening(self):
        self.sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.sct.connect(('127.0.0.1', self.__port))
        if LOG_LEVEL < LOG_EXC_INFO:
            print("connected: " + str(self.__port))
        while not self.__stop_thread:
            try:
                if self.__is_camera:
                    self.sct.sendall("Wait for size".encode('utf-16-le'))
                    image_size = self.sct.recv(4)
                    if len(image_size) < 4:
                        continue
                    buffer_size = (image_size[3] & 0xff) << 24 | (image_size[2] & 0xff) << 16 | \
                                  (image_size[1] & 0xff) << 8 | (image_size[0] & 0xff)
                    self.sct.sendall("Wait for image".encode('utf-16-le'))
                    self.out_bytes = self.sct.recv(buffer_size)
                else:
                    self.sct.sendall("Wait for data".encode('utf-16-le'))
                    self.out_bytes = self.sct.recv(1024)
                    self.out_string = self.out_bytes.decode('utf-16-le')
            except (ConnectionAbortedError, BrokenPipeError):
                # возникает при отключении сокета
                break
        if LOG_LEVEL < LOG_EXC_INFO:
            print("disconnected: " + str(self.__port))
        self.sct.shutdown(socket.SHUT_RDWR)
        self.sct.close()

    def reset_out(self):
        self.out_string = ''
        self.out_bytes = b''

    def stop_listening(self):
        self.__stop_thread = True
        self.reset_out()
        if self.sct is not None:
            self.sct.shutdown(socket.SHUT_RDWR)
            if self.thread is not None:
                st_time = time.time()
                # если поток все еще живой, ждем 1 секунды и закрываем сокет
                while self.thread.is_alive():
                    if time.time() - st_time > 1:
                        if LOG_LEVEL < LOG_EXC_WARN:
                            warnings.warn("Something went wrong. Rude disconnection on port " + str(self.__port),
                                          category=ConnectionResetWarning)
                        self.sct.close()
                        st_time = time.time()


class TalkPort:
    def __init__(self, port: int):
        self.__port = port

        # other
        self.__stop_thread = False
        self.out_string = ''

        self.sct = None
        self.thread = None

    def start_talking(self):
        self.thread = threading.Thread(target=self.talking, args=())
        self.thread.start()

    def talking(self):
        self.sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.sct.connect(('127.0.0.1', self.__port))
        if LOG_LEVEL < LOG_EXC_INFO:
            print("connected: " + str(self.__port))
        while not self.__stop_thread:
            try:
                self.sct.sendall((self.out_string + "$").encode('utf-16-le'))
                _ = self.sct.recv(1024)  # ответ сервера
            except (ConnectionAbortedError, BrokenPipeError):
                # возникает при отключении сокета
                break
        if LOG_LEVEL < LOG_EXC_INFO:
            print("disconnected: " + str(self.__port))
        self.sct.shutdown(socket.SHUT_RDWR)
        self.sct.close()

    def reset_out(self):
        self.out_string = ''

    def stop_talking(self):
        self.__stop_thread = True
        self.reset_out()
        if self.sct is not None:
            self.sct.shutdown(socket.SHUT_RDWR)
            if self.thread is not None:
                st_time = time.time()
                # если поток все еще живой, ждем 1 секунды и закрываем сокет
                while self.thread.is_alive():
                    if time.time() - st_time > 1:
                        if LOG_LEVEL < LOG_EXC_WARN:
                            warnings.warn("Something went wrong. Rude disconnection on port " + str(self.__port),
                                          category=ConnectionResetWarning)
                        self.sct.close()
                        st_time = time.time()


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
