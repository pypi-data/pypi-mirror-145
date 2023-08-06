from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt

import lyberry_api.pub as lbry_pub
import lyberry_api.channel as lbry_channel
from lyberry_api.settings import settings as app_settings
from lyberry_qt import settings, helpers
from lyberry_qt.feed_screen import FeedScreen
from lyberry_qt.channel_screen import ChannelScreen
from lyberry_qt.connect import ConnectingWidget
from lyberry_qt.pub_screen import PubScreen
from PyQt5.QtCore import QThread
from PyQt5.Qt import QThreadPool

import re
import webbrowser

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, lbry, start_url = None):
        super(MainWindow, self).__init__()
        uic.loadUi(helpers.relative_path('designer/main.ui'), self)
        self._lbry = lbry
        self.open_screens = {}
        self._start_url = start_url

        self.settings_button.clicked.connect(self.show_settings_screen)

        self.back_button.clicked.connect(self.go_back)
        self.go_button.clicked.connect(self.go_to_entered_url)
        self.url_line_edit.returnPressed.connect(self.go_to_entered_url)

        self.reload_button.clicked.connect(self.reload)

        self.thread_pool = QThreadPool()

        self.open_thread = QThread()
        self.comment_thread = QThread()
        self.load_thread = QThread()
        self.loaders = []

        self.first_screen()

    def first_screen(self):
        if not self._lbry.online():
            connecting_window = ConnectingWidget(self._lbry)
            self.open_screen(connecting_window)
            connecting_window.finished.connect(self.when_connected)
        else:
            self.when_connected()

    def when_connected(self):
        self.following_screen = FeedScreen(self, self._lbry.sub_feed, 'Following', 'about:following')
        self.following_button.clicked.connect(self.show_following_screen)
        self.add_screen(self.following_screen)
        if self._start_url:
            self.go_to_start_url()
        else:
            self.show_following_screen()

    def go_to_start_url(self):
        try:
            self.go_to_lbry_url(self._start_url)
        except ValueError:
            self.show_following_screen()
        finally:
            self._start_url = None

    def show_following_screen(self):
        self.show_screen(self.following_screen)
    
    def show_connecting_screen(self):
        self.connecting_screen = ConnectingWidget(self._lbry)
        self.open_screen(ConnectingWidget(self._lbry))
    
    def show_settings_screen(self):
        settings_screen = settings.SettingsScreen(self._lbry)
        self.open_screen(settings_screen)
    
    def show_accounts_screen(self):
        try:
            self.accounts_screen = settings.AccountsScreen(self._lbry)
        except ConnectionError:
            self.show_connecting_screen()
        else:
            self.open_screen(self.accounts_screen)

    def go_to_entered_url(self):
        entered_url = self.url_line_edit.text().strip()
        self.go_to_url(entered_url)

    def go_to_screen_at_url(self, url):
        self.go_to_index(self.open_screens[url])

    def go_to_url(self, url):
        url = helpers.odysee_to_lbry_link(url)
        if url in self.open_screens:
            self.go_to_screen_at_url(url)
        elif url.startswith('lbry://') or url.startswith('@'):
            self.go_to_lbry_url(url)
        elif url.startswith('about:'):
            self.go_to_an_about_page(url)
        elif url.startswith('http://') or url.startswith('https://'):
            webbrowser.open(url)
        else:
            self.search_for(url)
    
    def go_to_an_about_page(self, url):
        page = url.split(':')[1]
        if page in ['following', 'feed', 'subs', 'subscriptions']:
            self.show_following_screen()
        elif page == 'settings':
            self.show_settings_screen()
        elif page in ['account', 'accounts']:
            self.show_accounts_screen()

    def go_to_lbry_url(self, url):
        try:
            claim = self._lbry.resolve(url)
        except ConnectionError as err:
            print(f'connection error when resolving url: {err}')
            self.show_connecting_screen()
            self.connecting_screen.finished.connect(lambda: self.go_to_lbry_url(url))
            return
        except ValueError as err:
            print(f'value error when resolving url: {err}')
            self.search_for(url)
            return
        except Exception as err:
            print(err)
            return
        if type(claim) is lbry_pub.LBRY_Pub:
            self.show_pub(claim)
        elif type(claim) is lbry_channel.LBRY_Channel:
            self.show_channel(claim)
        else:
            print(type(claim), 'isnt supported')

    def show_channel(self, claim):
        if claim.url in self.open_screens:
            self.show_screen(claim)
        else:
            channel_screen = ChannelScreen(self, claim)
            self.open_screen(channel_screen)

    def show_pub(self, claim):
        pub_screen = PubScreen(self, claim)
        self.open_screen(pub_screen)

    def search_for(self, search_term: str):
        if app_settings['use_lighthouse']:
            claim_feed = self._lbry.lighthouse_search_feed(query = search_term)
        else:
            claim_feed = self._lbry.lbrynet_search_feed(text = search_term)
        search_screen = FeedScreen(self, claim_feed, f'Search - {search_term}', search_term)
        self.open_screen(search_screen)

    def add_screen(self, screen):
        screen.setAttribute(Qt.WA_DeleteOnClose)
        index = self.stackedWidget.addWidget(screen)
        screen.change_url.connect(self.go_to_url)
        self.open_screens[screen.url] = index
        screen.finished.connect(lambda: self.close_screen(screen))
        return index

    def open_screen(self, screen):
        index = self.add_screen(screen)
        self.go_to_index(index)

    def close_screen(self, screen):
        print('closed', screen)
        self.stackedWidget.removeWidget(screen)
        del self.open_screens[screen.url]
        self.update_url()

    def index_of(self, screen):
        return self.open_screens[screen.url]

    def show_screen(self, screen):
        self.go_to_index(self.index_of(screen))

    def go_to_index(self, index):
        self.stackedWidget.setCurrentIndex(index)
        self.update_url()
        print(self.open_screens)
        return index
    
    def go_back(self):
        top_widget = self.stackedWidget.currentWidget()
        top_widget.close()
        self.update_url()
        if len(self.open_screens) == 0:
            self.first_screen()

    def update_url(self):
        try:
            self.url_line_edit.setText(self.stackedWidget.currentWidget().url)
        except AttributeError: # if the current widget doesn't have a url
            self.url_line_edit.setText('')

    def img_url_to_label(self, url, label):
        label.setText('Loading image')
        worker = helpers.ImageWorker(url, label)
        self.thread_pool.start(worker)

    def reload(self):
        url = self.stackedWidget.currentWidget().url
        self.go_back()
        self.go_to_url(url)

