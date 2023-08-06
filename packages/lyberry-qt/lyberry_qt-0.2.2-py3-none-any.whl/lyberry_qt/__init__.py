#!/usr/bin/env python3

from lyberry_api import LBRY_Api
import sys
from PyQt5 import QtWidgets
from lyberry_qt.qt_window import MainWindow

__version__ = "0.2.2"

def main(wallet = None, start_url = None):
    if '--version' in sys.argv:
        print(__version__)
        exit()

    wallet = None
    if '--wallet' in sys.argv:
        wallet_index = sys.argv.index('--wallet') + 1
        if wallet_index < len(sys.argv):
            wallet = sys.argv[wallet_index]
            del sys.argv[wallet_index-1]
            del sys.argv[wallet_index-1]

    url = None
    if len(sys.argv) > 1:
        url = sys.argv[-1]

    lbry = LBRY_Api(wallet_id=wallet)
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(lbry, start_url = start_url)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
