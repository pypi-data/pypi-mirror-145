
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.uic import loadUi
from lyberry_qt.helpers import relative_path

class Connector(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(dict)
    offline = pyqtSignal()

    def __init__(self, lbry):
        self._lbry = lbry
        super().__init__()

    def run(self):
        for i,code in enumerate(self._lbry.connect()):
            if code == 0:
                self.finished.emit()
                break
            elif code == 1:
                self.offline.emit()
                break
            elif code == 2:
                self.progress.emit(self._lbry.status)

class ConnectingWidget(QtWidgets.QDialog):
    change_url = pyqtSignal(str)
    url = 'about:connecting'

    def __init__(self, lbry):
        super(ConnectingWidget, self).__init__()
        loadUi(relative_path('designer/connecting.ui'), self)
        self._lbry = lbry
        self.reconnect_button.clicked.connect(self.reconnect)
        self.thread = QThread()
        self.label.linkActivated.connect(self.change_url.emit)
        self.showEvent = lambda _: self.reconnect()

    def reconnect(self):
        if self._lbry.online():
            self.close()
        elif self._lbry.initialising():
            status = self._lbry.status
            self.update_init_msg(status)
            self.reconnect_button.setEnabled(False)
            self.worker = Connector(self._lbry)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.progress.connect(self.update_init_msg)
            self.worker.offline.connect(self.reconnect)
            self.worker.offline.connect(self.worker.deleteLater)
            self.worker.offline.connect(self.thread.quit)
            self.worker.finished.connect(self.close)
            self.worker.finished.connect(self.worker.deleteLater)
            self.worker.finished.connect(self.thread.quit)
            self.thread.start()
        else:
            self.label.setText('''# lbrynet could not be reached.

Are you sure it is running?
You can run it by opening the LBRY desktop app, or by entering into a terminal:

```
lbrynet start
```

also ensure that lbrynet_api is set correctly in your [settings](about:settings)
''')
            self.reconnect_button.setEnabled(True)

    def update_init_msg(self, status):
        message = '# lbrynet is starting.\n'
        if "startup_status" in status:
            for key in status["startup_status"]:
                message += f'- {key}: {"✓" if status["startup_status"][key] else "❌"}\n'
        self.label.setText(message)

