from flask import Flask, render_template
import pyvisa
from datetime import datetime


app = Flask(__name__)

ergebnis = None
verbindung = None
scanlist = None
zeit = None

@app.route('/',methods = ['POST', 'GET'])


def home():

    return render_template('index.html', ergebnis1 = messung(), verbindung = verbindung(), scanlist = scanlistconf(), zeit = time())

def messung():




    rm = pyvisa.ResourceManager('@py')
    dmm = rm.open_resource('TCPIP0::192.168.178.101::inst0::INSTR')

    verbindung()


    dmm.timeout = 5000
    dmm.write("*CLS")
    dmm.write("*RST")

    scanlist = scanlistconf()


    dmm.write("CONF:TEMP RTD,85, " + scanlist)


    dmm.write("ROUTE:SCAN " + scanlist)

    temp = {}
    dmm.write("MEAS:TEMP? " + scanlist)
    temp['value'] = float(dmm.read())
    qq = temp['value']
    print("%.2f" % qq)

    ergebnis = "%.2f" % qq + "°"
    return str(ergebnis)

def verbindung():

    rm = pyvisa.ResourceManager('@py')
    dmm = rm.open_resource('TCPIP0::192.168.178.101::inst0::INSTR')
    list2 = str(dmm.query('*IDN?'))
    con = "%.38s" % list2
    return str(con)

def scanlistconf():
    scanlist = "(@101)"
    return str(scanlist)

def time():
    ptime = datetime.now().strftime('%H:%M:%S')
    return ptime


if __name__ == '__main__':

    app.run()