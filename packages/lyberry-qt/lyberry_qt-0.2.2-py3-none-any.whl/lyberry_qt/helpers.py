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

IMAGE_DIR = relative_path('./images/')

thumb_path = os.path.join(tempfile.gettempdir(), 'lyberry_thumbs')
if not os.path.isdir(thumb_path):
    os.mkdir(thumb_path)

def fix_markdown(text):
    # most people use a single newline, not two
    text = text.replace('\n', '\n\n')
    # replace '@name' with markdown link '[@name](lbry://@name)'
    text = re.sub(r'(\s)(@[^\s]*)', r'\1[\2](lbry://\2)', text)
    # make lbry://link to <lbry://link>
    text = re.sub(r'(\s)(lbry://[^\s]*)', r'\1<\2>', text)
    return text

class FeedUpdater(QObject):
    finished = pyqtSignal(list)
    progress = pyqtSignal(object)
    error = pyqtSignal(Exception)

    def set_feed(self, feed):
        self.feed = feed

    def run(self):
        items = []
        for i in range(20):
            try:
                next_item = next(self.feed)
            except StopIteration:
                break
            except KeyError:
                continue
            except ValueError:
                continue
            except Exception as err:
                self.error.emit(err)
                break
            else:
                self.progress.emit(next_item)
                items.append(next_item)
        self.finished.emit(items)

def download_file(url):
    urlhash = hashlib.md5(url.encode()).hexdigest()
    local_filename = os.path.join(thumb_path,urlhash)
    if os.path.isfile(local_filename):
        return local_filename
    try:
        download_file_to(url, local_filename)
        return local_filename
    except Exception as err:
        print(f'Error loading image: {err}')
        return os.path.join(IMAGE_DIR, 'NotFound.png')

def download_file_to(url: str, local_filename: str):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)

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

class Loader(QObject):
    finished = pyqtSignal(object)
    def set_func(self, func):
        self.func = func
    def run(self):
        obj = self.func()
        self.finished.emit(obj)

def odysee_to_lbry_link(url):
    return re.sub(r'^(https?://)?(odysee.com|lbry.tv|open.lbry.com)/', 'lbry://', url)

