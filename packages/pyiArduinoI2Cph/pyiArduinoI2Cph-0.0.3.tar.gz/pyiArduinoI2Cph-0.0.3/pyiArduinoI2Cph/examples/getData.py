from time import sleep
# Подключаем библиотеку   для работы с pH-метром I2C-flash.
from pyiArduinoI2Cph import *

#   Объявляем объект sensor для работы с функциями и методами библиотеки pyiArduinoI2Cph, указывая адрес модуля на шине I2C.
sensor = pyiArduinoI2Cph(0x09)

while True:
    print("Кислотность = ", end='')

    #   Выводим водородный показатель жидкости с 1 знаком после запятой.
    print(sensor.getPH(), end='')

    print(" pH.")
    sleep(1)
