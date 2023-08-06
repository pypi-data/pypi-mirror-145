from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

import pyqtgraph as pg
# Change pyqtgraph plots to be black on white
pg.setConfigOption('background', (255, 255, 255))  # Do before any widgets drawn
pg.setConfigOption('foreground', 'k')  # Do before any widgets drawn
pg.setConfigOptions(imageAxisOrder='row-major')

QApplication.setStyle('fusion')

Form, Window = uic.loadUiType('pyote.ui')

app = QApplication([])
window = Window()
form = Form()

form.setupUi(window)
print(form.markDzone)


def myPrint():
    print('Somebody called my print')


form.setDataLimits.clicked.connect(myPrint)

myPrint()


window.show()
app.exec()
