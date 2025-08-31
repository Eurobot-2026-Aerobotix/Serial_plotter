import serial
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
import numpy as np
import struct

ser = serial.Serial('COM10', 115200)
win = pg.GraphicsLayoutWidget(show=True, title="Real-Time Plot", size=(800, 600))
plot = win.addPlot(title="waka waka ee ee")
curveR = plot.plot(pen='w')
plot.setYRange(-10000, 10000)

dataR = np.zeros(1000)
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
    while ser.in_waiting >= 4:
        while ser.read(1) != b'\xAA':
            ser.read(1)    
        raw = ser.read(4)
        value = struct.unpack('<f', raw)[0]
        dataR = np.roll(dataR, -1)
        dataR[-1] = value
    curveR.setData(dataR)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1)

if __name__ == '__main__':
    pg.exec()