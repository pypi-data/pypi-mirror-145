cdef extern from "<stdint.h>" nogil:
    ctypedef signed char int8_t
    ctypedef signed short int16_t
    ctypedef signed int int32_t
    ctypedef signed long int64_t
    ctypedef unsigned char uint8_t
    ctypedef unsigned short uint16_t
    ctypedef unsigned int uint32_t
    ctypedef unsigned long long uint64_t

cdef extern from "iarduino_I2C_TDS.cpp":
    pass

cdef extern from "iarduino_I2C_TDS.h":
    cdef cppclass iarduino_I2C_TDS:
        iarduino_I2C_TDS() except +
        iarduino_I2C_TDS(unsigned char) except +
        bint begin()
        bint changeAddress(unsigned char)
        bint reset()
        unsigned char getAddress()
        unsigned char getVersion()

        bint getPullI2C()
        bint setPullI2C(bint)

        uint16_t getFrequency()
        bint setFrequency(uint16_t)
        bint setCalibration(uint8_t, uint16_t)
        uint16_t getKnownTDS(uint8_t)
        bint setKnownTDS(uint8_t, uint16_t)
        float getKa()
        bint setKa(float)
        float getKb()
        bint setKb(float)
        float getKt()
        bint setKt(float)
        float getKp()
        bint setKp(float)
        bint set_t(float)
        float get_T()
        bint set_T(float)
        uint32_t getRo()
        float getVout()
        uint16_t get_S()
        uint16_t getEC()
        uint16_t getTDS()
        uint8_t getCalibration()
