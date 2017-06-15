import RPi._GPIO as GPIO
import time
import mysql.connector as mc

RS = 17
RW = 27
E = 22

D4 = 5
D5 = 6
D6 = 13
D7 = 19

class LCD:

    def __init__(self,par_RS,par_RW,par_E,par_DB4,par_DB5,par_DB6,par_DB7):
        self.__RS = par_RS
        self.__RW = par_RW
        self.__E = par_E
        self.__DB4 = par_DB4
        self.__DB5 = par_DB5
        self.__DB6 = par_DB6
        self.__DB7 = par_DB7

        allpins = [self.__RS,self.__RW,self.__E, self.__DB4, self.__DB5, self.__DB6, self.__DB7]

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for pin in allpins:
            GPIO.setup(pin, GPIO.OUT)


        self.__pins = [par_DB7,par_DB6,par_DB5,par_DB4]
        self.__delay_instructie = 0.005


    def __eHoogInstructie(self):
        GPIO.output(self.__E, 1)
        GPIO.output(self.__RS, 0)
        GPIO.output(self.__RW, 0)

    def __eLaagInstructie(self):
        GPIO.output(self.__E, 0)
        GPIO.output(self.__RS, 0)
        GPIO.output(self.__RW, 0)

    def __eHoogData(self):
        GPIO.output(self.__E, 1)
        GPIO.output(self.__RS, 1)
        GPIO.output(self.__RW, 0)

    def __eLaagData(self):
        GPIO.output(self.__E, 0)
        GPIO.output(self.__RS, 1)
        GPIO.output(self.__RW, 0)

    def FunctionSet(self):
        self.__eHoogInstructie()
        GPIO.output(self.__RS, GPIO.LOW)
        GPIO.output(self.__RW, GPIO.LOW)
        GPIO.output(self.__DB7, GPIO.LOW)
        GPIO.output(self.__DB6, GPIO.LOW)
        GPIO.output(self.__DB5, GPIO.HIGH)
        GPIO.output(self.__DB4, GPIO.LOW)
        self.__eLaagInstructie()
        time.sleep(self.__delay_instructie)

    def Display_On(self):
        self.__eHoogInstructie()
        GPIO.output(self.__RS, GPIO.LOW)
        GPIO.output(self.__RW, GPIO.LOW)
        GPIO.output(self.__DB7, GPIO.LOW)
        GPIO.output(self.__DB6, GPIO.LOW)
        GPIO.output(self.__DB5, GPIO.LOW)
        GPIO.output(self.__DB4, GPIO.LOW)
        self.__eLaagInstructie()
        self.__eHoogInstructie()
        GPIO.output(self.__DB7, GPIO.HIGH)
        GPIO.output(self.__DB6, GPIO.HIGH)
        GPIO.output(self.__DB5, GPIO.HIGH)
        GPIO.output(self.__DB4, GPIO.HIGH)
        self.__eLaagInstructie()
        time.sleep(self.__delay_instructie)

    def Clear_Display(self):
        self.__eHoogInstructie()
        GPIO.output(RS, GPIO.LOW)
        GPIO.output(self.__RW, GPIO.LOW)
        GPIO.output(self.__DB7, GPIO.LOW)
        GPIO.output(self.__DB6, GPIO.LOW)
        GPIO.output(self.__DB5, GPIO.LOW)
        GPIO.output(self.__DB4, GPIO.LOW)
        self.__eLaagInstructie()
        self.__eHoogInstructie()
        GPIO.output(self.__DB7, GPIO.LOW)
        GPIO.output(self.__DB6, GPIO.LOW)
        GPIO.output(self.__DB5, GPIO.LOW)
        GPIO.output(self.__DB4, GPIO.HIGH)
        self.__eLaagInstructie()
        time.sleep(self.__delay_instructie)

    def Reset(self):
        self.__eHoogInstructie()
        GPIO.output(self.__RS, GPIO.LOW)
        GPIO.output(self.__RW, GPIO.LOW)
        GPIO.output(self.__DB7, GPIO.LOW)
        GPIO.output(self.__DB6, GPIO.LOW)
        GPIO.output(self.__DB5, GPIO.HIGH)
        GPIO.output(self.__DB4, GPIO.HIGH)
        self.__eLaagInstructie()
        self.__eHoogInstructie()
        GPIO.output(self.__DB7, GPIO.HIGH)
        GPIO.output(self.__DB6, GPIO.LOW)
        GPIO.output(self.__DB5, GPIO.HIGH)
        GPIO.output(self.__DB4, GPIO.HIGH)
        self.__eLaagInstructie()

    def __setGPIODataBits(self,data, instructie):
        x = data
        deel1 = x & 0xF0
        filter = 0x80

        if instructie:
            self.__eHoogInstructie()
        else:
            self.__eHoogData()

        for i in range(0, 4):
            deel1 = data & filter
            GPIO.output(self.__pins[i], deel1)
            filter >>= 1

        if instructie:
            self.__eLaagInstructie()
        else:
            self.__eLaagData()

        deel2 = x & 0x0F
        deel2 = deel2 << 4

        if instructie:
            self.__eHoogInstructie()
        else:
            self.__eHoogData()

        for i in range(0, 4):
            deel2 = data & filter
            GPIO.output(self.__pins[i], deel2)
            filter >>= 1

        if instructie:
            self.__eLaagInstructie()
        else:
            self.__eLaagData()

    def __set_DDRAM(self,plaats):
        self.__setGPIODataBits(0x80 | plaats, 1)

    def WriteText(self,text):
        i = 1
        for letter in text:
            # 2 keer doorklokken
            number = ord(letter)
            self.__setGPIODataBits(number, 0)
            time.sleep(self.__delay_instructie)
            if i == 16:
                print("JA")
                self.__set_DDRAM(0x40)
            i += 1

    def WriteCO2Waarde(self,waarde):
        i = 1
        self.__set_DDRAM(0x00)
        CO2 = "CO2: "
        CO2 += str(waarde)
        CO2 += " ppm"
        for letter in CO2:
            number = ord(letter)
            self.__setGPIODataBits(number, 0)
            time.sleep(self.__delay_instructie)

    def WriteTempWaarde(self,waarde):
        i = 1
        self.__set_DDRAM(0x40)
        temp = "Temperatuur: "
        temp += str(waarde)
        temp += " C"
        for letter in temp:
            number = ord(letter)
            self.__setGPIODataBits(number, 0)
            time.sleep(self.__delay_instructie)

    def WriteLuchtvochtigheidWaarde(self,waarde):
        i = 1
        self.__set_DDRAM(0x14)
        luchtvochtigheid = "Luchtv: "
        luchtvochtigheid += str(waarde)
        luchtvochtigheid += " %"
        for letter in luchtvochtigheid:
            number = ord(letter)
            self.__setGPIODataBits(number, 0)
            time.sleep(self.__delay_instructie)

    def WriteComfortniveauWaarde(self,waarde):
        i = 1
        self.__set_DDRAM(0x54)
        comfortniveau = "Comfortniveau: "
        comfortniveau += str(waarde)
        for letter in comfortniveau:
            number = ord(letter)
            self.__setGPIODataBits(number, 0)
            time.sleep(self.__delay_instructie)

LCD = LCD(RS,RW,E,D4,D5,D6,D7)



try:
    while True:
        LCD.FunctionSet()
        LCD.Display_On()
        LCD.Clear_Display()
        connection = mc.connect(host="localhost", user="jacob", passwd="root", db="AIR_CHECK")
        cursor = connection.cursor()
        q = "SELECT CO2 FROM AIR_CHECK.tblMetingCO2 ORDER BY Tijdstip DESC LIMIT 1;"
        cursor.execute(q)
        result_CO2 = cursor.fetchone()
        q1 = "SELECT Temperatuur FROM AIR_CHECK.tblMetingLTC ORDER BY Tijdstip DESC LIMIT 1;"
        cursor.execute(q1)
        result_temp = cursor.fetchone()
        q2 = "SELECT Luchtvochtigheid FROM AIR_CHECK.tblMetingLTC ORDER BY Tijdstip DESC LIMIT 1;"
        cursor.execute(q2)
        result_luchtvochtigheid = cursor.fetchone()
        q3 = "SELECT Comfortniveau FROM AIR_CHECK.tblMetingLTC ORDER BY Tijdstip DESC LIMIT 1;"
        cursor.execute(q3)
        result_comfortniveau = cursor.fetchone()
        LCD.WriteText("Temp: ")
        LCD.WriteCO2Waarde(result_CO2[0])
        print(result_CO2[0])
        LCD.WriteTempWaarde(result_temp[0])
        print(result_temp[0])
        LCD.WriteLuchtvochtigheidWaarde(result_luchtvochtigheid[0])
        print(result_luchtvochtigheid[0])
        LCD.WriteComfortniveauWaarde(result_comfortniveau[0])
        print(result_comfortniveau[0])

        time.sleep(10)
        LCD.Reset()
except KeyboardInterrupt:
    connection.close()