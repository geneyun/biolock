import serial
import time
import cryptography


class FPS(object):
    def __init__(self, port='COM3', baudrate=9600, timeout=5):
        self.ser = None
        self.open = False

    def start(self,port='COM3', baudrate=9600, timeout=5):
        self.ser= serial.Serial(port=port,baudrate=baudrate,timeout=timeout)

        counter = 0
        while counter < 2:
            self.ser.write(b'!')
            if self.ser.read() == b'!':
                self.ser.write(b'x')
                self.open = True
                break
            counter += 1


    def close(self):
        self.ser.write(b'y')
        self.ser.close()
        self.open = False

    def led_on(self):
        self.ser.write(b'n')

    def led_off(self):
        self.ser.write(b'm')

    def get_enrolled_count(self):
        self.ser.write(b'b')
        return int(self.ser.read())

    def check_enrolled(self, id_num):
        self.ser.write(b'c')
        self.ser.write(chr(id_num))
        return self.ser.read() == 'y'

    def is_press_finger(self):
        self.ser.write(b'd')
        return self.ser.read() == 'y'

    def delete_id(self, id_num):
        self.ser.write(b'e')
        self.ser.write(chr(id_num))

    def delete_all(self):
        self.ser.write(b'f')

    def exists(self):
        self.ser.write(b'j')
        b = self.ser.read()
        return b == b'1'

    def verify(self, id_num):
        self.ser.write(b'g')
        self.ser.write(chr(id_num))
        s = ''
        for i in range(32):
            s = s+self.ser.read()
        return s

    def identify(self):
        self.ser.write(b'h')
        s = ''
        for i in range(32):
            n = self.ser.read()
            s = s + n
        return s

    def identify2(self):
        #generate keys
        keys = cryptography.key_gen()
        n = cryptography.to_bytes(keys[0])

        self.ser.write(b'v')
        #write n
        for i in range(4):
            self.ser.write(bytes([n[i]]))
        #write e
        self.ser.write(bytes([keys[1]]))
        print self.ser.read()
        print self.ser.read()
        print self.ser.read()
        print self.ser.read()
        print self.ser.read()
        # s = ''
        # for i in range(32):
        #     n = self.ser.read()
        #     s = s + n
        # return s

    def enroll_start(self):
        self.ser.write(b'q')
        return self.ser.read() == 'k'

    def enroll1(self):
        self.ser.write(b'r')
        res = self.ser.read()
        return res == 'k'

    def enroll2(self):
        self.ser.write(b's')
        res = self.ser.read()
        return res == 'k'

    def enroll3(self):
        self.ser.write(b't')
        res = self.ser.read()
        return res == 'k'
