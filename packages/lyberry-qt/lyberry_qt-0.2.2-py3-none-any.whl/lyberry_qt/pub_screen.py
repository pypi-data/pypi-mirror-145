
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QFont

from lyberry_qt import helpers
from lyberry_qt.comment_screen import CommentScreen
import requests

from datetime import datetime
import re

class PubScreen(QtWidgets.QDialog):
    change_url = pyqtSignal(str)
    def __init__(self, window, pub):
        super(PubScreen, self).__init__()
        uic.loadUi(helpers.relative_path('designer/pub.ui'), self)
        self._window = window
        self.pub = pub
        self._lbry = pub._LBRY_api
        self.title_label.setText(self.pub.title)
        self.url = pub.url
        self.license_label.setText(f"License: {pub.license}")
        timestamp = datetime.fromtimestamp(pub.timestamp)
        self.date_label.setText(f"Date: {timestamp}")
        desc = helpers.fix_markdown(self.pub.description)
        self.description_label.setText(desc)
        self.description_label.linkActivated.connect(self.change_url.emit)
        self.channel_button.setText(self.pub.channel.name)
        self.channel_button.clicked.connect(lambda: self.change_url.emit(self.pub.channel.url))
        self.open_button.clicked.connect(self.open)
        self.play_thread = QThread()
        comment_screen = CommentScreen(window, pub)
        self.tabWidget.insertTab(1, comment_screen, "Comments")
        comment_screen.change_url.connect(self.change_url.emit)

    def add_article(self, widget):
        self.tabWidget.insertTab(0, widget, "Article")
        self.tabWidget.setCurrentIndex(0)
        widget.change_url.connect(self.change_url)

    def open(self):
        file_type = self.pub.media_type.split('/')[0]
        if file_type == 'video' or file_type == 'audio':
            self.opener = helpers.Loader()
            self.opener.set_func(lambda:
                self.pub.open_external())
            self.opener.moveToThread(self.play_thread)
            self.play_thread.started.connect(self.opener.run)
            self.opener.finished.connect(self.opener.deleteLater)
            self.opener.finished.connect(self.play_thread.quit)
            self.play_thread.start()
        elif file_type == 'text':
            article = ArticlePage(self._window, self.pub)
            self.add_article(article)
            article.load()

class ArticlePage(QWidget):
    change_url = pyqtSignal(str)

    def __init__(self, window, pub):
        super(ArticlePage, self).__init__()
        uic.loadUi(helpers.relative_path('designer/article.ui'), self)
        self.pub = pub
        self._window = window

        self.load_thread = QThread()

    def load(self):
        self.opener = helpers.Loader()
        self.opener.set_func(lambda:
            requests.get(self.pub.streaming_url))
        self.opener.moveToThread(self.load_thread)
        self.load_thread.started.connect(self.opener.run)
        self.opener.finished.connect(self.process_response)
        self.opener.finished.connect(self.opener.deleteLater)
        self.opener.finished.connect(self.load_thread.quit)
        self.load_thread.start()

    def process_response(self, res):
        text_format = self.pub.media_type.split('/')[1]
        res.encoding = 'utf-8'
        if text_format == 'html':
            self.add_html_article(res.text)
        else:
            self.add_markdown_article(res.text)

    def add_markdown_article(self, article):
        self.loading_label.deleteLater()

        # markdown images look like: ![alt text](image link)
        # they may be encased in a hyperlink: [image](hyperlink)

        # this regex must not have capturing groups, or it makes extra splits.
        splitter = re.compile(r'(?:\[)?\!\[[^\]]*\]\([^\)]*\)(?:\]\([^\)]*\))?')
        text_parts = splitter.split(article)

        # this regex uses capturing groups to get the image metadata
        finder = re.compile(r'\[?\!\[([^\]]*)\]\(([^)]+)\)(?:\]\(([^)]*)\))?')
        img_groups = finder.findall(article)

        # there will always be one more text part than image:
        # text ![](image) text
        # so pop off the last piece of text and add the rest in pairs.
        final_text = text_parts.pop()
        for text_part, img_group in zip(text_parts, img_groups):
            self.add_label(text_part)
            [alt_text, img_link, ext_link] = img_group
            self.add_img(alt_text, img_link, ext_link)
        self.add_label(final_text)

    def add_label(self, text: str):
        label = QLabel()
        label.setText(text)
        label.setTextFormat(Qt.MarkdownText)
        label.linkActivated.connect(self.change_url.emit)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.LinksAccessibleByMouse | Qt.TextSelectableByMouse)
        font = QFont()
        font.setPointSize(14)
        label.setFont(font)
        self.article_layout.addWidget(label)

    def add_img(self, alt_text: str, img_link: str, ext_link: str):
        img_label = Image(img_link, ext_link)
        img_label.change_url.connect(self.change_url.emit)
        self._window.img_url_to_label(img_link, img_label)
        img_label.setText(alt_text)
        self.article_layout.addWidget(img_label)

    def add_html_article(self, article: str):
        # may as well reuse this label
        self.loading_label.setText(article)
        self.loading_label.setTextFormat(Qt.RichText)

class Image(QLabel):
    change_url = pyqtSignal(str)
    def __init__(self, img_url, link_url):
        super(Image, self).__init__()
        self.setToolTip(link_url)
        self.mousePressEvent = lambda _: self.change_url.emit(link_url)
        self.setCursor(Qt.PointingHandCursor)
