from .dev import connection
from . import line_sensor_cls


class RT2:
    """
    Class for RT-2 robot
    """

    def __init__(self):
        self.__right_motor_speed = 0.0
        self.__left_motor_speed = 0.0
        self.__back_motor_speed = 0.0

        self.__lift_servo_pos = 0.0
        self.__grip_servo_pos = 0.0

        self.__right_motor_enc = 0.0
        self.__left_motor_enc = 0.0
        self.__back_motor_enc = 0.0

        self.__reset_right_enc = False
        self.__reset_left_enc = False
        self.__reset_back_enc = False

        self.__reset_imu = False

        self.__button_ems = False
        self.__button_start = False
        self.__button_reset = False
        self.__button_stop = False

        self.__led_green = False
        self.__led_red = False

        self.__right_us = 0.0
        self.__left_us = 0.0
        self.__right_ir = 0.0
        self.__left_ir = 0.0
        self.__imu = 0.0
        self.__line_sensor = line_sensor_cls.LineSensor()

        self.__bytes_from_camera = b''

        self.__other_channel = connection.TalkPort(65431)
        self.__motors_channel = connection.TalkPort(65432)
        self.__oms_channel = connection.TalkPort(65433)
        self.__resets_channel = connection.TalkPort(65434)
        self.__encs_channel = connection.ListenPort(65435)
        self.__sensors_channel = connection.ListenPort(65436)
        self.__buttons_channel = connection.ListenPort(65437)
        self.__camera_channel = connection.ListenPort(65438, True)

    def connect(self):
        self.__other_channel.start_talking()
        self.__motors_channel.start_talking()
        self.__oms_channel.start_talking()
        self.__resets_channel.start_talking()
        self.__encs_channel.start_listening()
        self.__sensors_channel.start_listening()
        self.__buttons_channel.start_listening()
        self.__camera_channel.start_listening()

    def disconnect(self):
        self.__other_channel.stop_talking()
        self.__motors_channel.stop_talking()
        self.__oms_channel.stop_talking()
        self.__resets_channel.stop_talking()
        self.__encs_channel.stop_listening()
        self.__sensors_channel.stop_listening()
        self.__buttons_channel.stop_listening()
        self.__camera_channel.stop_listening()

    def __update_other(self):
        self.__other_channel.out_string = connection.ParseChannels.join_bool_channel(
                (
                    self.__led_green,
                    self.__led_red,
                ))

    def __update_motors(self):
        self.__motors_channel.out_string = connection.ParseChannels.join_float_channel(
            (
                self.__right_motor_speed,
                self.__left_motor_speed,
                self.__back_motor_speed,
            ))

    def __update_oms(self):
        self.__oms_channel.out_string = connection.ParseChannels.join_float_channel(
            (
                self.__lift_servo_pos,
                self.__grip_servo_pos,
            ))

    def __update_resets(self):
        self.__resets_channel.out_string = connection.ParseChannels.join_bool_channel(
            (
                self.__reset_right_enc,
                self.__reset_left_enc,
                self.__reset_back_enc,
                self.__reset_imu,
            ))

    def __update_encs(self):
        values = connection.ParseChannels.parse_float_channel(self.__encs_channel.out_string)
        if len(values) == 3:
            self.__right_motor_enc = values[0]
            self.__left_motor_enc = values[1]
            self.__back_motor_enc = values[2]

    def __update_sensors(self):
        values = connection.ParseChannels.parse_float_channel(self.__sensors_channel.out_string)
        if len(values) == 9:
            self.__right_us = values[0]
            self.__left_us = values[1]
            self.__right_ir = values[2]
            self.__left_ir = values[3]
            self.__imu = values[4]
            self.__line_sensor.s1 = values[5]
            self.__line_sensor.s2 = values[6]
            self.__line_sensor.s3 = values[7]
            self.__line_sensor.s4 = values[8]

    def __update_buttons(self):
        values = connection.ParseChannels.parse_bool_channel(self.__buttons_channel.out_string)
        if len(values) == 4:
            self.__button_ems = values[0]
            self.__button_start = values[1]
            self.__button_reset = values[2]
            self.__button_stop = values[3]

    def __update_camera(self):
        # because of 640x480
        if len(self.__camera_channel.out_bytes) == 921600:
            self.__bytes_from_camera = self.__camera_channel.out_bytes

    @property
    def right_motor_speed(self):
        return self.__right_motor_speed

    @right_motor_speed.setter
    def right_motor_speed(self, value):
        self.__right_motor_speed = value
        self.__update_motors()

    @property
    def left_motor_speed(self):
        return self.__left_motor_speed

    @left_motor_speed.setter
    def left_motor_speed(self, value):
        self.__left_motor_speed = value
        self.__update_motors()

    @property
    def back_motor_speed(self):
        return self.__back_motor_speed

    @back_motor_speed.setter
    def back_motor_speed(self, value):
        self.__back_motor_speed = value
        self.__update_motors()

    @property
    def lift_servo_pos(self):
        return self.__lift_servo_pos

    @lift_servo_pos.setter
    def lift_servo_pos(self, value):
        self.__lift_servo_pos = value
        self.__update_oms()

    @property
    def grip_servo_pos(self):
        return self.__grip_servo_pos

    @grip_servo_pos.setter
    def grip_servo_pos(self, value):
        self.__grip_servo_pos = value
        self.__update_oms()

    @property
    def reset_right_enc(self):
        return self.__reset_right_enc

    @reset_right_enc.setter
    def reset_right_enc(self, value):
        self.__reset_right_enc = value
        self.__update_resets()

    @property
    def reset_left_enc(self):
        return self.__reset_left_enc

    @reset_left_enc.setter
    def reset_left_enc(self, value):
        self.__reset_left_enc = value
        self.__update_resets()

    @property
    def reset_back_enc(self):
        return self.__reset_back_enc

    @reset_back_enc.setter
    def reset_back_enc(self, value):
        self.__reset_back_enc = value
        self.__update_resets()

    @property
    def reset_imu(self):
        return self.__reset_imu

    @reset_imu.setter
    def reset_imu(self, value):
        self.__reset_imu = value
        self.__update_resets()

    @property
    def led_green(self):
        return self.__led_green

    @led_green.setter
    def led_green(self, value):
        self.__led_green = value
        self.__update_other()

    @property
    def led_red(self):
        return self.__led_red

    @led_red.setter
    def led_red(self, value):
        self.__led_red = value
        self.__update_other()

    @property
    def right_motor_enc(self):
        self.__update_encs()
        return self.__right_motor_enc

    @property
    def left_motor_enc(self):
        self.__update_encs()
        return self.__left_motor_enc

    @property
    def back_motor_enc(self):
        self.__update_encs()
        return self.__back_motor_enc

    @property
    def button_ems(self):
        self.__update_buttons()
        return self.__button_ems

    @property
    def button_start(self):
        self.__update_buttons()
        return self.__button_start

    @property
    def button_reset(self):
        self.__update_buttons()
        return self.__button_reset

    @property
    def button_stop(self):
        self.__update_buttons()
        return self.__button_stop

    @property
    def line_sensor(self) -> line_sensor_cls.LineSensor:
        self.__update_sensors()
        return self.__line_sensor

    @property
    def right_us(self):
        self.__update_sensors()
        return self.__right_us

    @property
    def left_us(self):
        self.__update_sensors()
        return self.__left_us

    @property
    def right_ir(self):
        self.__update_sensors()
        return self.__right_ir

    @property
    def left_ir(self):
        self.__update_sensors()
        return self.__left_ir

    @property
    def imu(self):
        self.__update_sensors()
        return self.__imu

    @property
    def bytes_from_camera(self):
        self.__update_camera()
        return self.__bytes_from_camera
