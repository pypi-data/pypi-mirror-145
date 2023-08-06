from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal

from lyberry_qt import helpers

class CommentWidget(QtWidgets.QDialog):
    change_url = pyqtSignal(str)
    def __init__(self, comment):
        super(CommentWidget, self).__init__()
        uic.loadUi(helpers.relative_path('designer/comment.ui'), self)
        self.comment = comment
        self.pub = comment.pub
        self._lbry = comment._LBRY_api
        self.message.setText(helpers.fix_markdown(self.comment.msg))
        self.message.linkActivated.connect(self.change_url.emit)
        self.channel_button.setText(comment.channel.name)
        self.show_replies_button.setText(str(comment.replies_amt) + " Replies")
        self.show_replies_button.clicked.connect(self.show_replies)
        self.show_replies_button.setEnabled(comment.replies_amt > 0)
        self.write_comment_button.clicked.connect(self.write_comment)

    def write_comment(self):
        self.writing_section = WriteCommentWidget(self, self.comment)
        self.write_comment_section.addWidget(self.writing_section)
        self.write_comment_button.setEnabled(False)
        self.writing_section.finished.connect(lambda: 
            self.write_comment_button.setEnabled(True))
    
    def show_replies(self):
        for comment in self.comment.replies:
            item = CommentWidget(comment)
            item.change_url.connect(self.change_url.emit)
            self.replies_section.addWidget(item)
        self.show_replies_button.setEnabled(False)

class WriteCommentWidget(QtWidgets.QDialog):
    def __init__(self, parent, comment=None):
        super(WriteCommentWidget, self).__init__()
        uic.loadUi(helpers.relative_path('designer/write_comment.ui'), self)
        self.create_comment_button.clicked.connect(self.create_comment)
        self.parent = parent
        self.comment = comment
        self.add_my_channels_as_comment_options()
    
    def add_my_channels_as_comment_options(self):
        my_channels = self.parent._lbry.my_channels
        for channel in my_channels:
            self.channel_select.addItem(channel.name)

    def create_comment(self):
        channel_name = self.channel_select.currentText()
        channel = self.parent._lbry.channel_from_uri(channel_name)
        message = self.comment_box.toPlainText()
        self.parent._lbry.make_comment(channel, message, self.parent.pub, self.comment)
        self.comment_box.clear()
        self.close()

class CommentScreen(QtWidgets.QWidget):
    change_url = pyqtSignal(str)
    def __init__(self, window, pub):
        super(CommentScreen, self).__init__()
        uic.loadUi(helpers.relative_path('designer/comment_screen.ui'), self)
        self.pub = pub
        self._lbry = pub._LBRY_api
        self._window = window
        self.comments = []
        self.comments_button.clicked.connect(self.more_comments)
        self.write_comment_button.clicked.connect(self.write_comment)
        self.amt = 1

    def write_comment(self):
        self.writing_section = WriteCommentWidget(self)
        self.write_comment_section.addWidget(self.writing_section)
        self.scrollArea.ensureWidgetVisible(self.writing_section.create_comment_button)
        self.write_comment_button.setEnabled(False)
        self.writing_section.finished.connect(lambda: 
            self.write_comment_button.setEnabled(True))

    def show_comment(self, comment):
        item = CommentWidget(comment)
        item.channel_button.clicked.connect(lambda: self.change_url.emit(comment.channel.url))
        item.change_url.connect(self.change_url.emit)
        self.comments.append(item)
        self.comments_section.addWidget(item, self.amt, 0, 1, 1)
        self.amt += 1
    
    def list_comments(self, comments):
        for comment in comments:
            self.show_comment(comment)
        self.fix_comment_button()

    def fix_comment_button(self):
        self.comments_section.addWidget(self.comments_button)
        self.comments_button.setEnabled(True)

    def more_comments(self):
        self.comments_button.setEnabled(False)
        self.comment_worker = helpers.FeedUpdater()
        self.comment_worker.set_feed(self.pub.comments_feed)
        self.comment_worker.moveToThread(self._window.comment_thread)
        self._window.comment_thread.started.connect(self.comment_worker.run)
        self.comment_worker.progress.connect(self.show_comment)
        self.comment_worker.error.connect(print)
        self.comment_worker.finished.connect(self.fix_comment_button)
        self.comment_worker.finished.connect(self.comment_worker.deleteLater)
        self.comment_worker.finished.connect(self._window.comment_thread.quit)
        self.scrollArea.ensureWidgetVisible(self.comments_button)
        self._window.comment_thread.start()

