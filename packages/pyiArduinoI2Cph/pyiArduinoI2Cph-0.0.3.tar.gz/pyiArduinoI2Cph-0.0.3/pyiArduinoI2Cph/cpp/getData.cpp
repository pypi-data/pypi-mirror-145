#include "Serial.h"
                                                  //
#include "../iarduino_I2C_pH.h"                   //   Подключаем библиотеку   для работы с pH-метром I2C-flash.
iarduino_I2C_pH sensor(0x09);                     //   Объявляем объект sensor для работы с функциями и методами библиотеки iarduino_I2C_pH, указывая адрес модуля на шине I2C.
                                                  //   Если объявить объект без указания адреса (iarduino_I2C_pH sensor;), то адрес будет найден автоматически.
void setup(){                                     //
     sensor.begin();                              //   Инициируем работу с pH-метром I2C-flash.
}                                                 //
                                                  //
void loop(){                                      //
     Serial.print("Кислотность = " );             //
     Serial.print(sensor.getPH() ,1);             //   Выводим водородный показатель жидкости с 1 знаком после запятой.
     Serial.print(" pH.\r\n"       );             //
     delay(1000);                                 //
}                                                 //

int main()
{
	setup();
	for (;;)
		loop();
}
