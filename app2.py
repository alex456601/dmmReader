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

    scanIntervals = 5
    numberScans = 2
    channelDelay = 0.1
    points = 0
    scanlist = "(@101:102)"

    dmm.write("CONF:TEMP TC,T,(@101:102)")

    dmm.write("ROUTE:SCAN " + scanlist)
    dmm.write("ROUTE:SCAN:SIZE?")
    numberChannels = int(dmm.read()) + 1
    dmm.write("FORMAT:READING:CHAN ON")
    dmm.write("FORMAT:READING:TIME ON")
    dmm.write("ROUT:CHAN:DELAY " + str(channelDelay)+","+scanlist)
    dmm.write("TRIG:COUNT " + str(numberScans))
    dmm.write("TRIG:SOUR TIMER")
    dmm.write("TRIG:TIMER " + str(scanIntervals))
    dmm.write("INIT;:SYSTEM:TIME:SCAN?")


    sleep(11)


    dmm.read()
    '''wait until there is a data available'''
    points = 0
    while (points == 0):
        dmm.write("DATA:POINTS?")
        points = int(dmm.read())
    '''
    The data points are printed 
    data, time, channel
    '''
    print()


    for chan in range(1, numberChannels):
        dmm.write("DATA:REMOVE? 1")
        ergebnis = dmm.read()
        print(ergebnis)
        points = 0
        # wait for data
        while (points == 0):
            dmm.write("DATA:POINTS?")
            points = str(dmm.read())

    return str(ergebnis + "\n")







if __name__ == '__main__':

    app.run()