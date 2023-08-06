import os
import requests
import re
import hashlib
import tempfile
from PyQt5.QtCore import QObject, pyqtSignal, Qt, pyqtSlot
from PyQt5 import QtGui
from PyQt5.Qt import QRunnable
from PyQt5.QtWidgets import QLabel

def relative_path(path):
    this_dir = os.path.dirname(__file__)
    return os.path.join(this_dir, path)

thumb_path = os.path.join(tempfile.gettempdir(), 'pyqtmd_cache')
if not os.path.isdir(thumb_path):
    os.mkdir(thumb_path)

class ImageWorker(QRunnable):
    def __init__(self, url: str, label: QLabel):
        super(ImageWorker, self).__init__()
        self.url = url
        self.label = label
        self.label_exists = True;
        self.label.destroyed.connect(self.label_deleted)

    @pyqtSlot()
    def run(self):
        pixmap = self.get_img(self.url)
        if self.label_exists:
            self.label.setPixmap(pixmap)

    def label_deleted(self):
        self.label_exists = False;

    def get_img(self, url: str):
        pixmap = QtGui.QPixmap()
        file = download_file(url)
        pixmap.load(file)
        pixmap = pixmap.scaled(720, 480, Qt.KeepAspectRatio)
        return pixmap

class Opener(QObject):
    finished = pyqtSignal(str)
    error = pyqtSignal()
    def __init__(self, url: str):
        super(Opener, self).__init__()
        self.url = url

    def run(self):
        try:
            res = get_or_open(self.url)
        except Exception as err:
            self.finished.emit("```" + str(err) + "```")
        else:
            self.finished.emit(res)

def get_or_open(uri):
    if uri.startswith('http'):
        return requests.get(uri).text
    else:
        with open(uri, 'r') as file:
            text = file.read()
        return text







