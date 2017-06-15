import Adafruit_DHT
import time
import mysql.connector as mc

connection = mc.connect(host="localhost", user="jacob", passwd="root", db="AIR_CHECK")

cursor = connection.cursor()

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)


luchtvochtigheid = humidity
temperatuur = temperature
print(luchtvochtigheid)
print(temperatuur)
#if humidity is not None and temperature is not None:
try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
        luchtvochtigheid = humidity
        temperatuur = temperature
        print('Temperatuur: {0:0.1f}*C'.format(temperature))
        print('Luchtvochtigheid: {0:0.1f}%'.format(humidity))
        comfortniveau = 9/5 * temperature - 0.55 * (1-humidity) * (9/5 * temperature - 26) + 32
        print(comfortniveau)
        q = "INSERT INTO tblMetingLTC(Luchtvochtigheid, Temperatuur, Comfortniveau, Tijdstip,    Serienummer) VALUES("+ str(round(luchtvochtigheid,1)) + ", " + str(round(temperatuur,1)) + "," + str(round(comfortniveau,1)) + ",now(), 'Jacob')"
        cursor.execute(q)
        connection.commit()
        q2 = "SELECT Metingsinterval FROM AIR_CHECK.tblMetingsintervalLTC WHERE Serienummer LIKE  'Jacob'"
        cursor.execute(q2)
        result = cursor.fetchone()
        print(result[0])
        time.sleep(float(result[0]))
        #time.sleep(5)
except KeyboardInterrupt:
    connection.close()

#else:
 # print('Geen data')