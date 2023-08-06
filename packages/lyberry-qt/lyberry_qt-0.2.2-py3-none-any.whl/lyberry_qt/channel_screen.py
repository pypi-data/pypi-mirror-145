from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal
from lyberry_qt import helpers
from lyberry_qt.comment_screen import CommentScreen
from lyberry_qt.feed_screen import FeedScreen

class ChannelScreen(QtWidgets.QDialog):
    change_url = pyqtSignal(str)
    def __init__(self, window, channel):
        super(ChannelScreen, self).__init__()
        self.title = channel.title
        self.channel = channel
        self._window = window
        self.title = channel.title
        self.url = channel.url
        uic.loadUi(helpers.relative_path('designer/channel.ui'), self)
        self.name_label.setText(self.channel.name)
        self.description_label.setText(helpers.fix_markdown(self.channel.description))
        self.description_label.linkActivated.connect(self.change_url.emit)
        if channel.is_followed:
            self.set_to_unfollow()
        else:
            self.set_to_follow()
        self.finished.connect(self.channel.refresh_feed)
        self.title_label.setText(self.title)

        feed_screen = FeedScreen(self._window, self.channel.pubs_feed)
        feed_screen.title_label.deleteLater()
        self.tabWidget.insertTab(1, feed_screen, "Publications")
        feed_screen.change_url.connect(self.change_url.emit)
        self.tabWidget.setCurrentIndex(1)

        comment_screen = CommentScreen(window, channel)
        self.tabWidget.insertTab(2, comment_screen, "Comments")
        comment_screen.change_url.connect(self.change_url.emit)

        self.search_line_edit.returnPressed.connect(self.search_for_search_line)

    def search_for_search_line(self):
        self.search_for(self.search_line_edit.text().strip())
        self.search_line_edit.setText('')

    def search_for(self, text: str):
        search_feed = self.channel.search(text)
        search_title = f"Search - {text}"
        search_screen = FeedScreen(self._window, search_feed, search_title)
        search_screen.change_url.connect(self.change_url.emit)
        self.tabWidget.insertTab(2, search_screen, search_title)
        self.tabWidget.setCurrentIndex(2)

    def follow(self):
        self.channel.follow()
        self.set_to_unfollow()
    
    def set_to_follow(self):
        self.follow_button.clicked.connect(self.follow)
        self.follow_button.setText('Follow')
    
    def set_to_unfollow(self):
        self.follow_button.clicked.connect(self.unfollow)
        self.follow_button.setText('Following')

    def unfollow(self):
        self.channel.unfollow()
        self.set_to_follow()

