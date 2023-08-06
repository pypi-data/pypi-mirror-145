import numpy as np
import math


class Funcad:
    COS15 = 0.965926
    COS30 = 0.866
    COS45 = 0.7071
    COS60 = 0.5
    COS75 = 0.258819
    PI = 3.1415926535

    @staticmethod
    def access_bit(data: int, num: int) -> int:
        """
        Acces to a bit in uint8_t/int8_t value
        :param data: 8 bit integer value
        :param num: index of needed bit
        :return: Selected bit
        """
        shift = int(num % 8)
        return (data >> shift) & 0x1

    @staticmethod
    def int_to_4_bytes(value: int) -> bytes:
        """
        Makes bytearray from an integer
        :param value: Integer value
        :return: Bytearray with size 4
        """
        return bytearray([(value >> 24) & 0xff, (value >> 16) & 0xff, (value >> 8) & 0xff, value & 0xff])

    @staticmethod
    def shift_np_array(arr, num, fill_value=0):
        """
        Shifts numpy array to the selected direction from selected place by chrisaycock
        :param arr: Numpy array
        :param num: Place and direction
        :param fill_value: Value that will fill new array elements
        :return: Shifted array
        """
        result = np.empty_like(arr)
        if num > 0:
            result[:num] = fill_value
            result[num:] = arr[:-num]
        elif num < 0:
            result[num:] = fill_value
            result[:num] = arr[-num:]
        else:
            result[:] = arr
        return result

    @staticmethod
    def fmta(right: float, left: float, back: float) -> tuple:
        """
        From Motors To Axes
        :param right: Right motor speed
        :param left: Left motor speed
        :param back: Back motor speed
        :return: Axes speeds
        """
        x: float = (right - left) * Funcad.COS30
        y: float = (right + left) * Funcad.COS60 - back
        z: float = -right - left - back
        return x, y, z

    @staticmethod
    def fatm(x: float, y: float, z: float) -> tuple:
        """
        From Axes To Motors
        :param x: X speed
        :param y: Y speed
        :param z: Z speed
        :return: Motor speeds
        """
        r: float = (x / Funcad.COS30) - y + z
        l: float = (x / -Funcad.COS30) - y + z
        b: float = y * 2 + z
        return r, l, b

    @staticmethod
    def in_range(val: float, min_v: float, max_v: float) -> float:
        """
        Func that returns value in range min and max
        :param val: Value that needs to clip
        :param min_v: Min limit
        :param max_v: Max limit
        :return: Ranged value
        """
        return val if (val <= max_v) and (val >= min_v) else (min_v if val < min_v else max_v)

    @staticmethod
    def in_range_bool(val: float, min_v: float, max_v: float) -> bool:
        """
        Func that checks that value in range min and max
        :param val: Value that needs to check
        :param min_v: Min limit
        :param max_v: Max limit
        :return: Value in range
        """
        return (val <= max_v) and (val >= min_v)

    @staticmethod
    def transfunc_np(arr: np.ndarray, inp: float) -> float:
        """
        Numpy transfer function
        :param arr: Input 2D array like: [[-1, 0, 1, 2], [-15, 0, 15, 30]]
        :param inp: Input of value to conversion by transfer function
        :return: Output is conversed input
        """
        if inp <= arr[0, 0]:
            return arr[1, 0]
        elif inp >= arr[0, -1]:
            return arr[1, -1]
        else:
            n = np.argmax(arr[0] > inp) - 1
            return (arr[1, n + 1] - arr[1, n]) / (arr[0, n + 1] - arr[0, n]) * (inp - arr[0, n]) + arr[1, n]

    @staticmethod
    def transfunc_np_plus(arr: np.ndarray, inp: float) -> float:
        """
        Numpy transfer function only for positive array as input
        :param arr: Input 2D array like: [[1, 2, 3, 4], [10, 20, 30, 40]]
        :param inp: Input of value to conversion by transfer function
        :return: Output is conversed input
        """
        sign = np.sign(inp) if np.sign(inp) != 0 else 1
        inp = abs(inp)
        if inp <= arr[0, 0]:
            return arr[1, 0] * sign
        elif inp >= arr[0, -1]:
            return arr[1, -1] * sign
        else:
            n = np.argmax(arr[0] > inp) - 1
            return ((arr[1, n + 1] - arr[1, n]) / (arr[0, n + 1] - arr[0, n]) * (inp - arr[0, n]) + arr[1, n]) * sign

    @staticmethod
    def reim_to_polar(x: float, y: float) -> tuple:
        """
        Converts the rectangular components of a complex number into its polar components.
        :param x: X
        :param y: Y
        :return: Polar components of a complex number
        """
        return math.sqrt(x * x + y * y), math.atan2(y, x)

    @staticmethod
    def polar_to_reim(r: float, theta: float) -> tuple:
        """
        Converts the polar components of a complex number into its rectangular components.
        :param r: R
        :param theta: Theta
        :return: Rectangular components
        """
        return r * math.cos(theta), r * math.sin(theta)


class MeanFilter:
    """
    Mean filter by crackanddie
    """
    def __init__(self, force: int):
        """
        Constructor
        :param force: Power of filtering
        """
        self.arr: np.ndarray = np.array([0.0] * force)

    def filter(self, n: float):
        """
        Shifting, adding a new element and filtering
        :param n: A new element
        :return: Filtered value
        """
        self.arr = Funcad.shift_np_array(self.arr, 1)
        self.arr[0] = n
        return np.mean(self.arr)

    def resize(self, n: int):
        """
        Changing power of filtering
        :param n: New array size
        :return: None
        """
        self.arr = np.resize(self.arr, n)


class MedianFilter:
    """
    Median filter by crackanddie
    """
    def __init__(self, force: int):
        """
        Constructor
        :param force: Power of filtering
        """
        self.arr: np.ndarray = np.array([0.0] * force)

    def filter(self, n: float):
        """
        Shifting, adding a new element and filtering
        :param n: A new element
        :return: Filtered value
        """
        self.arr = Funcad.shift_np_array(self.arr, 1)
        self.arr[0] = n
        return np.median(self.arr)

    def resize(self, n: int):
        """
        Changing power of filtering
        :param n: New array size
        :return: None
        """
        self.arr = np.resize(self.arr, n)


class PID:
    """
        PID regulator by crackanddie
    """
    def __init__(self, kp, ki, kd, enc_scale: float = 1.0, limits: tuple = (-100, 100)):
        """
        Constructor of PID
        :param kp: KP coefficient
        :param ki: KI coefficient
        :param kd: KD coefficient
        :param enc_scale: Encoder difference scaler, to make it closer to speed
        :param limits: Limits of out speed
        """
        self.__last_enc = 0
        self.__last_bias = 0
        self.__integral = 0
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.__limits = limits
        self.__enc_scale = enc_scale

    def calc(self, speed, enc):
        """
        Calculating PIDed speed
        :param speed: Needed speed
        :param enc: Current encoder value
        :return: PIDed speed
        """
        pwm = 0
        if speed != 0:
            enc_diff = enc - self.__last_enc
            bias = speed - enc_diff * self.__enc_scale
            self.__integral += bias * self.ki
            self.__integral = Funcad.in_range(self.__integral, *self.__limits)
            pwm = Funcad.in_range(self.kp * bias + self.__integral + self.kd *
                                  (bias - self.__last_bias), *self.__limits)
            self.__last_bias = bias
        else:
            self.__integral = 0
            self.__last_bias = 0

        self.__last_enc = enc
        return pwm

    def reset(self, enc):
        """
        Resets some private parameters, should be used before using 'calc' method
        :param enc: Current encoder value
        :return: None
        """
        self.__integral = 0
        self.__last_bias = 0
        self.__last_enc = enc

    def change_k(self, kp, ki, kd):
        """
        Changes coefficients
        :param kp: New KP coefficient
        :param ki: New KI coefficient
        :param kd: New KD coefficient
        :return: None
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
