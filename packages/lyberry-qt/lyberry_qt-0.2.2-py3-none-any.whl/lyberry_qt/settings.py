from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.uic import loadUi

from lyberry_qt.helpers import relative_path

def init_settings():
    from lyberry_api import settings

    default_settings = {
        "use_lighthouse": True,
    }

    app_settings = {
        **settings.settings,
        **default_settings,
    }

    settings.settings = app_settings
    settings.apply()
    return app_settings

app_settings = init_settings()

class SettingsScreen(QtWidgets.QDialog):
    change_url = pyqtSignal(str)

    def __init__(self, lbry):
        super(SettingsScreen, self).__init__()
        loadUi(relative_path('designer/settings.ui'), self)
        app_settings = init_settings()

        self.url = 'about:settings'
        self._lbry = lbry
        
        self.row = 0

        try:
            wallet_options = [wallet['id'] for wallet in lbry.wallets]
            wallet_select = self.make_select('default_wallet', wallet_options, lbry.wallet_id)
        except ConnectionError:
            wallet_options = ['default_wallet']
            wallet_select = self.make_select('default_wallet', wallet_options, lbry.wallet_id)
            wallet_select.setEnabled(False)
            wallet_select.setToolTip("You are not connected to LBRY")
        self.add_input('default_wallet', wallet_select)


        for key in app_settings:
            if not key in ['default_wallet']:
                inputbox = self.make_inputbox(key, app_settings[key])
                self.add_input(key, inputbox)

        self.apply_button.clicked.connect(self.apply)
        self.account_button.clicked.connect(lambda: self.change_url.emit('about:accounts'))

    def apply(self):
        from lyberry_api import settings
        settings.settings = app_settings
        settings.apply()
        self._lbry.apply_settings()

    def add_input(self, key, inputbox):
        label = QtWidgets.QLabel()
        label.setText(key)
        self.settings_form.setWidget(self.row, QtWidgets.QFormLayout.LabelRole, label)
        self.settings_form.setWidget(self.row, QtWidgets.QFormLayout.FieldRole, inputbox)
        self.row += 1

    def make_inputbox(self, key, value):
        inputbox = {}
        if type(value) == str:
            inputbox = QtWidgets.QLineEdit()
            inputbox.setText(value)
            def update_setting():
                app_settings[key] = inputbox.text()
            inputbox.editingFinished.connect(update_setting)
            inputbox.returnPressed.connect(self.apply)
        elif type(value) == int:
            inputbox = QtWidgets.QSpinBox()
            inputbox.setValue(value)
            inputbox.setMaximum(9999) # max defaults to 99
            def update_setting():
                app_settings[key] = inputbox.value()
            inputbox.editingFinished.connect(update_setting)
            inputbox.returnPressed.connect(self.apply)
        elif type(value) == bool:
            inputbox = QtWidgets.QCheckBox()
            inputbox.setCheckState(value)
            inputbox.setTristate(False)
            def update_setting():
                app_settings[key] = inputbox.isChecked()
                self.apply()
            inputbox.stateChanged.connect(update_setting)
        else:
            inputbox = QtWidgets.QLineEdit()
            inputbox.setText(str(value))
            inputbox.setEnabled(False)
            print(f'Config {key} is of unsupported type: {type(value)}')
        return inputbox

    def make_select(self, key, options: list, default_option: str) -> QtWidgets.QComboBox:
        select = QtWidgets.QComboBox()
        for option in options:
            select.addItem(option)
        select.addItem('new')
        select.setCurrentText(default_option)
        def change_value(value: str):
            if value == 'new':
                select.setEditable(True)
            app_settings[key] = value
            self.apply()
        select.currentTextChanged.connect(change_value)
        return select

class AccountsScreen(QtWidgets.QDialog):
    change_url = pyqtSignal()

    def __init__(self, lbry):
        super(AccountsScreen, self).__init__()
        loadUi(relative_path('designer/account.ui'), self)
        self._lbry = lbry
        self.url = 'about:accounts'
        for account in self._lbry.accounts:
            self._add_account_to_list(account)

        self.add_acc_button.clicked.connect(lambda: self.add_account())

    def add_account(self):
        try:
            account = self._lbry.add_account(
                self.edit_name.text(),
                self.edit_priv_key.text())
        except ValueError:
            print('invalid key!')
            return
        self._add_account_to_list(account)

    def _add_account_to_list(self, account):
        label = QtWidgets.QLabel()
        label.setText(account_to_html(account))
        self.acc_list_section.addWidget(label)
        if not account.is_default:
            default_button = QtWidgets.QPushButton()
            default_button.clicked.connect(lambda: account.set_as_default())
            default_button.setText(f'Set {account.name} as the default account')
            self.acc_list_section.addWidget(default_button)

            remove_button = QtWidgets.QPushButton()
            remove_button.clicked.connect(lambda: account.remove())
            remove_button.setText(f'Remove {account.name}')
            self.acc_list_section.addWidget(remove_button)

def account_to_html(account):
    return f'''
<h2>{account.name}{" - Default" if account.is_default else ""}</h2>
<p>
id: {account.id}
<br>
certificates: {account.certificates}
<br>
satoshis: {account.satoshis}
<br>
public key: {account.public_key}
</p>
'''

