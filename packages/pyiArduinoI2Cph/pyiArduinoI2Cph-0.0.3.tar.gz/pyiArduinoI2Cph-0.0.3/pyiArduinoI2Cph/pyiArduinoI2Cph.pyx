# distutils: language = c++
# cython: language_level = 3

from iarduino_I2C_pH cimport iarduino_I2C_pH
#from time import sleep

DEF_CHIP_ID_FLASH   =   0x3C
DEF_CHIP_ID_METRO   =   0xC3
DEF_MODEL_PH        =   0x1A

# Адреса регистров модуля:
REG_FLAGS_0         =   0x00
REG_BITS_0          =   0x01
REG_FLAGS_1         =   0x02
REG_BITS_1          =   0x03
REG_MODEL           =   0x04
REG_VERSION         =   0x05
REG_ADDRESS         =   0x06
REG_CHIP_ID         =   0x07
REG_PH_KNOWN_PH     =   0x0A
REG_PH_KNOWN_PH_1   =   0x0C
REG_PH_KNOWN_PH_2   =   0x0E
REG_PH_CALIBRATION  =   0x10
REG_PH_Ky           =   0x11
REG_PH_Ustp         =   0x13
REG_PH_pHn          =   0x15
REG_PH_Uin          =   0x17
REG_PH_Uout         =   0x19
REG_PH_Un           =   0x1B
REG_PH_pH           =   0x1D

# Позиция битов и флагов:
PH_BIT_CALC_2       =   0x02
PH_BIT_CALC_1       =   0x01

NO_BEGIN = 1

cdef class pyiArduinoI2Cph:
    cdef iarduino_I2C_pH c_module

    def __cinit__(self, address=None, auto=None):

        if address is not None:

            self.c_module = iarduino_I2C_pH(address)

            if auto is None:
                #sleep(.5)
                if not self.c_module.begin():

                    print("ошибка инициализации модуля.\n"
                          "Проверьте подключение и адрес модуля,"
                          " возможно не включен интерфейс I2C.\n"
                          " Запустите raspi-config и включите интерфейс"
                          ", инструкция по включению:"
                          " https://wiki.iarduino.ru/page/raspberry-i2c-spi/")

        else:

            self.c_module = iarduino_I2C_pH()

            if auto is None:
                #sleep(.5)
                if not self.c_module.begin():

                    print("ошибка инициализации модуля.\n"
                          "Проверьте подключение и адрес модуля, "
                          " возможно не включен интерфейс I2C.\n"
                          " Запустите raspi-config и включите интерфейс"
                          ", инструкция по включению:"
                          " https://wiki.iarduino.ru/page/raspberry-i2c-spi/")

    def begin(self):
        return self.c_module.begin()

    def changeAddress(self, unsigned char newAddr):
        return self.c_module.changeAddress(newAddr)

    def reset(self):
        return self.c_module.reset()

    def getAddress(self):
        return self.c_module.getAddress()

    def getVersion(self):
        return self.c_module.getVersion()

    def getPullI2C(self):
        return self.c_module.getPullI2C()

    def setPullI2C(self, flag):
        if flag is None:
            return self.c_module.setPullI2C(True)
        if flag is not None:
            return self.c_module.setPullI2C(flag)


    def setCalibration(self, num, pH):
        return self.c_module.setCalibration(num, pH)

    def getKnownPH(self, num):
        return self.c_module.getKnownPH(num)

    def setKnownPH(self, num, pH):
        return self.c_module.setKnownPH(num, pH)

    def getKy(self):
        return self.c_module.getKy()

    def setKy(self, Ky):
        return self.c_module.setKy(Ky)

    def getVstp(self):
        return self.c_module.getVstp()

    def setVstp(self, Vstp):
        return self.c_module.setVstp(Vstp)

    def getVin(self):
        return self.c_module.getVin()

    def getVout(self):
        return self.c_module.getVout()

    def getVn(self):
        return self.c_module.getVn()

    def getPHn(self):
        return self.c_module.getPHn()

    def setPHn(self, PHn):
        return self.c_module.setPHn(PHn)

    def getPH(self):
        return self.c_module.getPH()

    def getCalibration(self):
        return self.c_module.getCalibration()

