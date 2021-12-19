from flask import Flask, render_template

import pyvisa
from time import sleep
from datetime import datetime


app = Flask(__name__)

ergebnis = None





@app.route('/')

def messung():

    rm = pyvisa.ResourceManager('@py')
    dmm = rm.open_resource('TCPIP0::192.168.178.101::inst0::INSTR')
    print("Verbunden mit: " + dmm.query('*IDN?'))

    time = datetime.now().strftime("%H,%M,%S")
    date = datetime.now().strftime("%Y,%m,%d")
    zeitpunkt= datetime.now().strftime("%Y.%m.%d-%H:%M:%S")

    dmm.write("SYST:TIME " + time)
    dmm.write("SYST:DATE " + date)

    dmm.timeout = 5000
    dmm.write("*CLS")
    dmm.write("*RST")

    scanIntervals = 0
    numberScans = 1
    channelDelay = 0.1
    scanlist = "(@101:105)"

    dmm.write("CONF:TEMP TC,T,(@101:105)")

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
    leeren()
    #ausgabe vom Zeitpunkt der Messung
    print(dmm.read())

    sleep(3)
    points = 0
    while (points == 0):
        dmm.write("DATA:POINTS?")
        points = int(dmm.read())


    #\n after every data
    print("Werte:")
    for chan in range(1, numberChannels + 1):
        dmm.write("DATA:REMOVE? 1")
        raw = str(dmm.read())  # ergebnisse
        with open("static/output.csv", "a") as csv_file:
            print(str([raw[0:2] + raw[4] + "." + raw[5:8], raw[-4:-1], zeitpunkt]))
            data = str([raw[0:2] + raw[4] + "." + raw[5:8], raw[-4:-1], zeitpunkt])
            csv_file.write("%s" % data + "\n")
            csv_file.close()
        points = 1


        #wait for data
        while (points == 0):
            dmm.write("DATA:POINTS?")
            points = int(dmm.read())




    dmm.close()
    return str(ergebnis)

def leeren():

    with open("static/output.csv", "w") as csv_file:
        csv_file.write("")
        csv_file.close()
    return


if __name__ == '__main__':

    app.run()