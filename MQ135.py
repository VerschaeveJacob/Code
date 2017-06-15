import spidev
import time
import mysql.connector as mc


# open spi bus
spi = spidev.SpiDev()  # create spi object
spi.open(0, 0)  # open spi port 0, device (CS or CE) 0


# function to read SPI data from MPC3008 chip
# channel must be an integer 0-7
def ReadChannel(channel):
    # 3 bytes versturen
    # 1 , S D2 D1 D0 xxxx, 0
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) | adc[2]  # in byte 1 en 2 zit resultaat
    return data


#RS = ((5.O * RL) - (RL * Vout)) / Vout (RL = 10)

try:
    while True:
        connection = mc.connect(host="localhost", user="jacob", passwd="root", db="AIR_CHECK")
        cursor = connection.cursor()
        channel0 = ReadChannel(0)
        channel0_perc = format(channel0 * 4.7, '.2f')
        channel0_volt = channel0
        print("\nHet CO2 niveau is " + channel0_perc + "ppm (" + str(channel0_volt) + "V).")
        q = "INSERT INTO tblMetingCO2(CO2, Tijdstip, Serienummer) VALUES(" + channel0_perc +", now(), 'Jacob')"
        cursor.execute(q)
        connection.commit()
        q2 = "SELECT Metingsinterval FROM AIR_CHECK.tblMetingsintervalCO2 WHERE Serienummer LIKE  'Jacob'"
        cursor.execute(q2)
        result = cursor.fetchone()
        print(result[0])
        time.sleep(float(result[0]))
except KeyboardInterrupt:
    connection.close()
