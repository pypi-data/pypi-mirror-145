cdef extern from "iarduino_I2C_pH.cpp":
    pass

cdef extern from "iarduino_I2C_pH.h":
    cdef cppclass iarduino_I2C_pH:
        iarduino_I2C_pH() except +
        iarduino_I2C_pH(unsigned char) except +
        bint begin()
        bint changeAddress(unsigned char)
        bint reset()
        unsigned char getAddress()
        unsigned char getVersion()

        bint getPullI2C();
        bint setPullI2C(bint);
        bint setCalibration(unsigned char, float);
        float getKnownPH(unsigned char);
        bint setKnownPH(unsigned char, float);
        float getKy();
        bint setKy(float);
        float getVstp();
        bint setVstp(float);
        float getVin();
        float getVout();
        float getVn();
        float getPHn();
        bint setPHn(float);
        float getPH();
        unsigned char getCalibration();
