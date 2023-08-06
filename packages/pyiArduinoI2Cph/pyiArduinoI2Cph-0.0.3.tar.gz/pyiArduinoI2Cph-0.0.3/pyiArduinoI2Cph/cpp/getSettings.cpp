// ПРИМЕР ПОЛУЧЕНИЯ НАСТРОЕК МОДУЛЯ:
#include "Serial.h"
                                                  //
#include "../iarduino_I2C_pH.h"                   //   Подключаем библиотеку   для работы с pH-метром I2C-flash.
iarduino_I2C_pH sensor(0x09);                     //   Объявляем объект sensor для работы с функциями и методами библиотеки iarduino_I2C_pH, указывая адрес модуля на шине I2C.
                                                  //   Если объявить объект без указания адреса (iarduino_I2C_pH sensor;), то адрес будет найден автоматически.
int main()
{
     sensor.begin();                              //   Инициируем работу с pH-метром I2C-flash.
     Serial.print("pH1  = "              );       //
     Serial.print(sensor.getKnownPH(1) ,2);       //   Выводим требуемый водородный показатель 1 жидкости для калибровки модуля кнопкой от 0 до 14,000 pH.
     Serial.print("pH.\r\npH2  = "       );       //
     Serial.print(sensor.getKnownPH(2) ,2);       //   Выводим требуемый водородный показатель 2 жидкости для калибровки модуля кнопкой от 0 до 14,000 pH.
     Serial.print("pH.\r\nKy   = "       );       //
     Serial.print(sensor.getKy()       ,3);       //   Выводим коэффициент усиления операционного усилителя от 1 до 65,535.
     Serial.print("\r\nVstp = "          );       //
     Serial.print(sensor.getVstp()     ,2);       //   Выводим шаг смещения напряжения датчика от 0,01 мВ до 655,35 мВ при смещении кислотности на 1 pH.
     Serial.print("мВ.\r\npHn  = "       );       //
     Serial.print(sensor.getPHn()      ,2);       //   Выводим нейтральную кислотность для датчика от 0 до 14,000 pH.
     Serial.print("pH.\r\n"              );       //
}                                                 //
