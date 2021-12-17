from flask import Flask, render_template
import pyvisa

app = Flask(__name__)

ergebnis = None

@app.route('/',methods = ['POST', 'GET'])
def home():
    return render_template('index.html', ergebnis1 = messung())

def messung():
    print("Verbunden")
    rm = pyvisa.ResourceManager('@py')
    dmm = rm.open_resource('TCPIP0::192.168.178.101::inst0::INSTR')


    dmm.timeout = 5000
    dmm.write("*CLS")
    dmm.write("*RST")


    scanlist = "(@101)"

    dmm.write("CONF:TEMP RTD,85, " + scanlist)

    #dmm.write("ROUT:MON (@101)")
    #dmm.write("ROUT:MON:STATE ON")

    dmm.write("ROUTE:SCAN " + scanlist)

    temp = {}
    dmm.write("MEAS:TEMP? " + scanlist)
    temp['value'] = float(dmm.read())
    qq = temp['value']
    print("%.2f" % qq)

    ergebnis = "%.2f" % qq + "°"
    return str(ergebnis)

if __name__ == '__main__':

    app.run()