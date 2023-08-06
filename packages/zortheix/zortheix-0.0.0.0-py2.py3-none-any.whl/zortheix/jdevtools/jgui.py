'''
    Allo heckc'est le mode gUI
'''
from PyQt5 import QtWidgets, uic
import sys

class gUI(QtWidgets.QMainWindow):
    '''
    c'est le mode gUI
    '''
    def __init__(self):
        super(gUI, self).__init__()
        #uic.loadUi('basic.ui', self)
        self.setWindowTitle('GUI Mode')
        self.resize(600, 400)
        self.show()
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = gUI()
    app.exec_()