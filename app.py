from flask import Flask
import pyvisa, time

app = Flask(__name__)
points = None
ergebnis = None


@app.route('/')
def hello_world():  # put application's code here
    print("C")
    rm = pyvisa.ResourceManager('@py')
    dmm = rm.open_resource('TCPIP0::192.168.178.101::inst0::INSTR')
    dmm.query('*IDN?')
    print("a")


    dmm.timeout = 5000
    dmm.write("*CLS")
    dmm.write("*RST")

    scanIntervals = 0
    numberScans = 1
    channelDelay = 0.1
    points = 2

    scanlist = "(@101)"

    dmm.write("CONF:TEMP TC,K,(@101)")
    dmm.write("ROUTE:SCAN " + scanlist)
    dmm.write("ROUTE:SCAN:SIZE?")
    numberChannels = int(dmm.read()) + 1
    dmm.write("FORMAT:READING:CHAN ON")
    dmm.write("FORMAT:READING:TIME ON")

    dmm.write("ROUT:CHAN:DELAY " + str(channelDelay) + "," + scanlist)
    dmm.write("TRIG:COUNT " + str(numberScans))
    dmm.write("TRIG:SOUR TIMER")
    dmm.write("TRIG:TIMER " + str(scanIntervals))

    dmm.write("INIT;:SYSTEM:TIME:SCAN?")
    time.sleep(5)
    ergebnis = dmm.read("TRAC:DATA?")
    return str(ergebnis)


if __name__ == '__main__':

    app.run()
