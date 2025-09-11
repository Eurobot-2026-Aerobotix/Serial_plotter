import serial
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
import numpy as np
import struct

ser = serial.Serial('COM10', 115200)
win = pg.GraphicsLayoutWidget(show=True, title="Real-Time Plot", size=(1850, 1000))
win.setGeometry(0, 29, 1800, 840)
#win.showFullScreen()
plot = win.addPlot(title="labyedh l AA wel a5dher BB")
curveR = plot.plot(pen='w')
curveL = plot.plot(pen='g')
curveT = plot.plot(pen='r')
curveJ = plot.plot(pen='y')
plot.setYRange(-1000, 1000)

dataR = np.zeros(1000)
dataL = np.zeros(1000)
dataT = np.zeros(1000)
dataJ = np.zeros(1000)
'''
    takes float values as 4 bytes preceded by a header (0xAA)

    example:
    uint8_t header = 0xAA;
    float value = (float)current_speed_L; // your value
    uint8_t* bytes = (uint8_t*)&value;
    HAL_UART_Transmit(&huart2, &header, 1, HAL_MAX_DELAY);
    HAL_UART_Transmit(&huart2, bytes, 4, 10);
    you can add a delay for stability
'''
def update():
    global dataR
    global dataL
    global dataT
    global dataJ
    while ser.in_waiting >= 5:
        x = ser.read(1)
        while not x in {b'\xAA', b'\xAB',  b'\xAC', b'\xAD'}:
            x = ser.read(1)
        raw = ser.read(4)
        value = struct.unpack('<f', raw)[0]
        if x == b'\xAA':
            dataR = np.roll(dataR, -1)
            dataR[-1] = value
        elif x == b'\xAB':
            dataL = np.roll(dataL, -1)
            dataL[-1] = value
        elif x == b'\xAC':
            dataT = np.roll(dataT, -1)
            dataT[-1] = value
        else:
            dataJ = np.roll(dataJ, -1)
            dataJ[-1] = value
    curveR.setData(dataR)
    curveL.setData(dataL)
    curveT.setData(dataT)
    curveJ.setData(dataJ)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1)

if __name__ == '__main__':
    pg.exec()