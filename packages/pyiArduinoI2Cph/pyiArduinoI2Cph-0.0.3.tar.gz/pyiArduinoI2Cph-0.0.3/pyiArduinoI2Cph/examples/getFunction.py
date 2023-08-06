# ПРИМЕР ПОЛУЧЕНИЯ И ВЫЧИСЛЕНИЯ ДАННЫХ:

from time import sleep

#   Подключаем библиотеку   для работы с pH-метром I2C-flash.
from pyiArduinoI2Cph import *

#   Объявляем объект sensor для работы с функциями и методами библиотеки pyiArduinoI2Cph, указывая адрес модуля на шине I2C.
sensor = pyiArduinoI2Cph(0x09)

while True:
     print("Кислотность = pHn+"      , end='')
     print("( Vn -Vout)/( Vstep *Ky)", end='')
     print("\r\n            = "      , end='')
     print(sensor.getPHn()           , end='')
     print("+("                      , end='')
     print(sensor.getVn()            , end='')
     print("-"                       , end='')
     print(sensor.getVout()          , end='')
     print(")/("                     , end='')
     print(sensor.getVstp()/1000     , end='')
     print("* "                      , end='')
     print(sensor.getKy()            , end='')
     print(") = "                    , end='')
     print(sensor.getPH()            , end='')
     print(" pH.\r\n"                , end='')
     sleep(1)
