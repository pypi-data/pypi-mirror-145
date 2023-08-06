from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal
from lyberry_qt import helpers
import lyberry_api.channel
from datetime import datetime

class FeedScreen(QtWidgets.QDialog):
    change_url = pyqtSignal(str)
    def __init__(self, window, feed, title: str = '', url: str = ''):
        super(FeedScreen, self).__init__()
        uic.loadUi(helpers.relative_path('designer/following.ui'), self)
        self._window = window
        self.feed = feed
        self.title = title
        self.url = url
        if self.title == '':
            self.title_layout.deleteLater()
        else:
            self.title_label.setText(self.title)
        self.load_more_button.clicked.connect(self.more)
        self.amt = 2
        self.width = 2
        self.items = []
        self.more()

    def new_pub(self, pub):
        item = PubWidget(pub)
        item.change_url.connect(self.change_url.emit)
        self._window.img_url_to_label(pub.thumbnail, item.thumbnail)
        self.items.append(item)
        self.pub_thumb_grid_layout.addWidget(item, self.amt // self.width, self.amt % self.width, 1, 1)
        self.amt += 1
        return item.pub_grid
    
    def fix_button(self):
        self.pub_thumb_grid_layout.addWidget(self.load_more_button, self.amt // self.width +1, 0, 1, 2)
        self.load_more_button.setEnabled(True)

    def more(self):
        self.load_more_button.setEnabled(False)
        self.worker = helpers.FeedUpdater()
        self.worker.set_feed(self.feed)
        self.worker.moveToThread(self._window.load_thread)
        self._window.load_thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.new_pub)
        self.worker.error.connect(self._window.show_connecting_screen)
        self.worker.error.connect(print)
        self.worker.finished.connect(self.fix_button)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self._window.load_thread.quit)
        self.scroll_area.ensureWidgetVisible(self.load_more_button)
        self._window.load_thread.start()

class PubWidget(QtWidgets.QDialog):
    change_url = pyqtSignal(str)
    def __init__(self, pub):
        super(PubWidget, self).__init__()
        uic.loadUi(helpers.relative_path('designer/pub_thumb.ui'), self)
        self.loaders = []
        self.pub = pub
        self.title.setText(pub.title)
        info = str(datetime.fromtimestamp(pub.timestamp))
        if pub.is_repost:
            info += f'\nreposted by {pub.reposter.name}'
        self.info_label.setText(info)
        if type(pub) == lyberry_api.channel.LBRY_Channel:
            self.channel.setText(pub.name)
            self.channel.pressed.connect(lambda: self.change_url.emit(self.pub.url))
        else:
            self.channel.setText(pub.channel.name)
            self.channel.pressed.connect(lambda: self.change_url.emit(self.pub.channel.url))

    # the _ takes the mouse click event, but it doesn't matter
    def mousePressEvent(self, _):
        self.change_url.emit(self.pub.url)
