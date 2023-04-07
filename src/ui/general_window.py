from PyQt6 import QtGui, QtWidgets
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QMainWindow

from src.sandbox.sandbox import create_account, get_accounts, add_cash_to_account, get_balance


def get_font():
    font = QtGui.QFont()
    font.setFamily('Courier New')
    font.setPointSize(15)
    font.setWeight(75)
    return font


class GeneralWindow(QMainWindow):
    __matrix_css_style = "background-color: rgb(22, 22, 22); color: rgb(0, 187, 53);"
    __button_css_style = "background-color: rgb(75, 75, 75); color: rgb(0, 167, 54);"

    def __init__(self):
        super(QMainWindow, self).__init__()
        # add general geometry
        self.balance = None
        self.account = None
        self.setWindowTitle('Торговый робот первого поколения')
        self.setGeometry(200, 200, 640, 480)
        # add button to create account
        self.add_account_btn = QtWidgets.QPushButton(self)
        self.add_account_btn.setGeometry(0, 0, 640, 40)
        self.add_account_btn.setFont(get_font())
        self.add_account_btn.setStyleSheet(self.__button_css_style)
        self.add_account_btn.setText('Добавить новый аккаунт для торгов')
        self.add_account_btn.clicked.connect(self.create_account_cb)
        # add label to see account id
        self.account_info = QtWidgets.QLabel(self)
        self.account_info.setGeometry(0, 0, 640, 40)
        self.account_info.setFont(get_font())
        self.account_info.setText('Мой текущий аккаунт: ')
        self.account_info.setMargin(10)
        self.account_info.setStyleSheet(self.__matrix_css_style)
        accounts = get_accounts()
        if len(accounts) == 0:
            self.account_info.setVisible(False)
        else:
            self.add_account_btn.setVisible(False)
            self.account = accounts[0]
            self.account_info.setText('Мой текущий аккаунт: ' + self.account.id + ':' + str(self.account.opened_date))

        # add input amount
        self.input_amount = QtWidgets.QLineEdit(self)
        self.input_amount.setGeometry(0, 40, 320, 40)
        self.input_amount.setFont(get_font())
        self.input_amount.setPlaceholderText('Введите сумму...')
        self.input_amount.setStyleSheet(self.__matrix_css_style)
        self.int_validator = QIntValidator()
        self.input_amount.setValidator(self.int_validator)
        self.input_amount.setTextMargins(10, 10, 10, 10)
        # add button to add amount to balance
        self.add_amount = QtWidgets.QPushButton(self)
        self.add_amount.setGeometry(320, 40, 320, 40)
        self.add_amount.setFont(get_font())
        self.add_amount.setStyleSheet(self.__button_css_style)
        self.add_amount.setText("Добавить к балансу")
        self.add_amount.clicked.connect(self.add_amount_to_balance_cb)
        # add total amount label
        self.total_amount = QtWidgets.QLabel(self)
        self.total_amount.setGeometry(0, 80, 640, 40)
        self.total_amount.setFont(get_font())
        self.balance = get_balance(self.account.id)
        if self.total_amount:
            self.total_amount.setText(self.get_format_balance())
        else:
            self.total_amount.setText('Мой текущий баланс: 0')
        self.total_amount.setMargin(10)
        self.total_amount.setStyleSheet(self.__matrix_css_style)

    def create_account_cb(self):
        create_account()
        accounts = get_accounts()
        if len(accounts) != 0:
            self.account = accounts[0]
            self.account_info.setText(self.account_info.text() + self.account.id)
            self.account_info.setVisible(True)
            self.add_account_btn.setVisible(False)

    def add_amount_to_balance_cb(self):
        balance = add_cash_to_account(self.account.id, int(self.input_amount.text()) or 0)
        self.balance = balance.balance
        if self.balance:
            self.total_amount.setText(self.get_format_balance())
            self.input_amount.setText('')

    def get_format_balance(self):
        return 'Мой текущий баланс: ' + str(self.balance.units) + ' ' + self.balance.currency
