import socket
import threading
import time
import traceback
import warnings

from .holder import *


class ListenPort:
    def __init__(self, port: int, is_camera: bool = False):
        self.__port = port
        self.__is_camera = is_camera

        self.thread = None
        self.__stop_thread = False
        self.out_string = ""
        self.out_bytes = b""

        self.ip_end_point = ('127.0.0.1', self.__port)
        self.sct = None

    def start_listening(self):
        self.thread = threading.Thread(target=self.listening, args=())
        self.thread.start()

    def listening(self):
        self.sct = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if LOG_LEVEL < LOG_EXC_INFO:
            print("connected: " + str(self.__port))
        while not self.__stop_thread:
            try:
                if self.__is_camera:
                    self.sct.sendto("Wait for size".encode('utf-16-le'), self.ip_end_point)
                    image_size, _ = self.sct.recvfrom(4)
                    # print(len(image_size))
                    if len(image_size) < 4:
                        continue
                    buffer_size = (image_size[3] & 0xff) << 24 | (image_size[2] & 0xff) << 16 | \
                                  (image_size[1] & 0xff) << 8 | (image_size[0] & 0xff)
                    self.sct.sendto("Wait for image".encode('utf-16-le'), self.ip_end_point)
                    local_bytes = b""
                    # check_iters = 0
                    for i in range(0, buffer_size // 1024):
                        local_bytes += self.sct.recvfrom(1024)[0]
                        self.sct.sendto("Got data".encode('utf-16-le'), self.ip_end_point)
                        # check_iters += 1
                        # print(check_iters)
                    # print(check_iters)
                    if buffer_size % 1024 > 0:
                        local_bytes += self.sct.recvfrom(buffer_size % 1024)[0]
                    self.out_bytes = local_bytes
                else:
                    self.sct.sendto("Wait for data".encode('utf-16-le'), self.ip_end_point)
                    self.out_bytes, _ = self.sct.recvfrom(1024)
                    self.out_string = self.out_bytes.decode('utf-16-le')
            except OSError:
                # первый случай:
                # вызывается при грубом отключении от сервера.
                # возникает при подключении к роботу
                # и дальнейшем отключении робота без остановки этой программы
                # второй случай:
                # вызывается при попытке запустить программу, когда робот отключен
                break
            except (Exception, EOFError):
                if LOG_LEVEL < LOG_NOTHING:
                    traceback.print_exc()
        if LOG_LEVEL < LOG_EXC_INFO:
            print("disconnected: " + str(self.__port))

    def reset_out(self):
        self.out_string = ""
        self.out_bytes = b""

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

        self.thread = None
        self.__stop_thread = False
        self.out_string = ""
        self.server_result = b""

        self.ip_end_point = ('127.0.0.1', self.__port)
        self.sct = None

    def start_talking(self):
        self.thread = threading.Thread(target=self.talking, args=())
        self.thread.start()

    def talking(self):
        self.sct = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if LOG_LEVEL < LOG_EXC_INFO:
            print("connected: " + str(self.__port))
        while not self.__stop_thread:
            try:
                self.sct.sendto((self.out_string + "$").encode('utf-16-le'), self.ip_end_point)
                self.server_result, _ = self.sct.recvfrom(1024)
            except OSError:
                # первый случай:
                # вызывается при грубом отключении от сервера.
                # возникает при подключении к роботу
                # и дальнейшем отключении робота без остановки этой программы
                # второй случай:
                # вызывается при попытке запустить программу, когда робот отключен
                break
            except (Exception, EOFError):
                if LOG_LEVEL < LOG_NOTHING:
                    traceback.print_exc()
        if LOG_LEVEL < LOG_EXC_INFO:
            print("disconnected: " + str(self.__port))

    def reset_out(self):
        self.out_string = ""

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
