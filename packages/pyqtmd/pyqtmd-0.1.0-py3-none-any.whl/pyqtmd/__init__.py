#!/usr/bin/env python3

import sys
from PyQt5 import QtWidgets
from pyqtmd.pub_screen import ArticlePage

__version__ = "0.1.0"

usage = '''
pyqtmd: a simple markdown viewer.

Usage:

    pyqtmd ( FILE | URL )
'''

def main():
    if len(sys.argv) != 2 or sys.argv[1] in ['-h', '--help', '-help', '-?']:
        print(usage)
        return
    url = sys.argv[1]
    app = QtWidgets.QApplication(sys.argv)
    window = ArticlePage(url)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
