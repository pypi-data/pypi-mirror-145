from deatool.deasolver import Tables
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sys

def run():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    tables = Tables()
    tables.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()