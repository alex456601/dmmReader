from flask import Flask
import pyvisa
from time import sleep
from datetime import datetime

app = Flask(__name__)

ergebnis = None

@app.route('/', methods = ['POST', 'GET'])

def messung():

    rm = pyvisa.ResourceManager('@py')
    dmm = rm.open_resource('TCPIP0::192.168.178.101::inst0::INSTR')
    print("Verbunden mit: " + dmm.query('*IDN?'))

    time = datetime.now().strftime("%H,%M,%S")
    date = datetime.now().strftime("%Y,%m,%d")


    #dmm.write("SYST:TIME " + time)
    #dmm.write("SYST: " + date)
    #dmm.write("SYST:TIME 15,00,05")

    dmm.timeout = 5000
    dmm.write("*CLS")
    dmm.write("*RST")

    scanIntervals = 0
    numberScans = 1
    channelDelay = 0.1
    scanlist = "(@101:103)"

    dmm.write("CONF:TEMP TC,T,(@101:103)")

    dmm.write("ROUTE:SCAN " + scanlist)
    dmm.write("ROUTE:SCAN:SIZE?")
    numberChannels = int(dmm.read())
    dmm.write("FORMAT:READING:CHAN ON")
    dmm.write("FORMAT:READING:TIME ON")
    dmm.write("ROUT:CHAN:DELAY " + str(channelDelay)+","+scanlist)
    dmm.write("TRIG:COUNT " + str(numberScans))
    dmm.write("TRIG:SOUR TIMER")
    dmm.write("TRIG:TIMER " + str(scanIntervals))
    dmm.write("INIT;:SYSTEM:TIME:SCAN?")
    #ausgabe vom Zeitpunkt der Messung
    print(dmm.read())

    sleep(3)
    points = 0
    while (points == 0):
        dmm.write("DATA:POINTS?")
        points = int(dmm.read())

    #jedes ergebnis hat eine Zeile
    for chan in range(1, 100):
        dmm.write("DATA:REMOVE? 1")
        raw = str(dmm.read())      #ergebnise
        print(raw[0:2] + raw[4] + "." + raw[5:8] + "°" + " " + raw[-4:-1])
        points = 0

        #wait for data
        while (points == 0):
            dmm.write("DATA:POINTS?")
            points = int(dmm.read())

    return str(ergebnis) and reset()

def reset():
    rm = pyvisa.ResourceManager('@py')
    dmm = rm.open_resource('TCPIP0::192.168.178.101::inst0::INSTR')
    dmm.write("*CLS")
    dmm.write("*RST")
    dmm.close()
    print("Verbindung unterbrochen")
    return


if __name__ == '__main__':

    app.run()