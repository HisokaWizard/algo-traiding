from typing import Type

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QMainWindow

from src.sandbox.sandbox import create_account, get_accounts, add_cash_to_account, get_balance, get_ru_shares_list, \
    set_candle_price_to_share, SharesItem


def get_font():
    font = QtGui.QFont()
    font.setFamily('Courier New')
    font.setPointSize(15)
    font.setWeight(75)
    return font


class GeneralWindow(QMainWindow):
    __base_color = "color: rgb(0, 200, 53);"
    __matrix_css_style = "background-color: rgb(25, 25, 25);" + __base_color
    __button_css_style = "background-color: rgb(75, 75, 75);" + __base_color
    __list_css_style = "background-color: rgb(50, 50, 50);" + __base_color

    def __init__(self):
        super(QMainWindow, self).__init__()
        # add general geometry
        self.balance = None
        self.account = None
        self.ru_shares: [Type[SharesItem]] = []
        self.setWindowTitle('Торговый робот первого поколения')
        self.setGeometry(100, 100, 1280, 480)
        # add button to create account
        self.add_account_btn = QtWidgets.QPushButton(self)
        self.add_account_btn.setGeometry(0, 0, 1280, 40)
        self.add_account_btn.setFont(get_font())
        self.add_account_btn.setStyleSheet(self.__button_css_style)
        self.add_account_btn.setText('Добавить новый аккаунт для торгов')
        self.add_account_btn.clicked.connect(self.create_account_cb)
        # add label to see account id
        self.account_info = QtWidgets.QLabel(self)
        self.account_info.setGeometry(0, 0, 1280, 40)
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
        self.input_amount.setGeometry(0, 40, 640, 40)
        self.input_amount.setFont(get_font())
        self.input_amount.setPlaceholderText('Введите сумму...')
        self.input_amount.setStyleSheet(self.__matrix_css_style)
        self.int_validator = QIntValidator()
        self.input_amount.setValidator(self.int_validator)
        self.input_amount.setTextMargins(10, 10, 10, 10)
        # add button to add amount to balance
        self.add_amount = QtWidgets.QPushButton(self)
        self.add_amount.setGeometry(640, 40, 640, 40)
        self.add_amount.setFont(get_font())
        self.add_amount.setStyleSheet(self.__button_css_style)
        self.add_amount.setText("Добавить к балансу")
        self.add_amount.clicked.connect(self.add_amount_to_balance_cb)
        # add total amount label
        self.total_amount = QtWidgets.QLabel(self)
        self.total_amount.setGeometry(0, 80, 1280, 40)
        self.total_amount.setFont(get_font())
        self.balance = get_balance(self.account.id)
        if self.total_amount:
            self.total_amount.setText(self.get_format_balance())
        else:
            self.total_amount.setText('Мой текущий баланс: 0')
        self.total_amount.setMargin(10)
        self.total_amount.setStyleSheet(self.__matrix_css_style)
        # add button to update shares quotation
        self.update_shares_quotation = QtWidgets.QPushButton(self)
        self.update_shares_quotation.setGeometry(640, 120, 640, 40)
        self.update_shares_quotation.setFont(get_font())
        self.update_shares_quotation.setStyleSheet(self.__button_css_style)
        self.update_shares_quotation.setText("Обновить котировки акций")
        self.update_shares_quotation.clicked.connect(self.update_shares_quotation_cb)
        # list with all russian shares
        self.shares_list = QtWidgets.QListWidget(self)
        self.shares_list.setGeometry(640, 160, 640, 320)
        self.shares_list.setFont(get_font())
        self.shares_list.setStyleSheet(self.__list_css_style)
        # buttons for get all necessary days for counting
        # # year
        self.get_year_button = QtWidgets.QPushButton(self)
        self.get_year_button.setGeometry(0, 120, 128, 40)
        self.get_year_button.setFont(get_font())
        self.get_year_button.setText("Год")
        self.get_year_button.setStyleSheet(self.__button_css_style)
        self.get_year_button.clicked.connect(self.add_year_price)
        # # half year
        self.get_half_year_button = QtWidgets.QPushButton(self)
        self.get_half_year_button.setGeometry(128, 120, 128, 40)
        self.get_half_year_button.setFont(get_font())
        self.get_half_year_button.setText("Полгода")
        self.get_half_year_button.setStyleSheet(self.__button_css_style)
        self.get_half_year_button.clicked.connect(self.add_half_year_price)
        # # three months
        self.get_three_months_button = QtWidgets.QPushButton(self)
        self.get_three_months_button.setGeometry(256, 120, 128, 40)
        self.get_three_months_button.setFont(get_font())
        self.get_three_months_button.setText("3 месяца")
        self.get_three_months_button.setStyleSheet(self.__button_css_style)
        self.get_three_months_button.clicked.connect(self.add_three_months_price)
        # # month
        self.get_month_button = QtWidgets.QPushButton(self)
        self.get_month_button.setGeometry(384, 120, 128, 40)
        self.get_month_button.setFont(get_font())
        self.get_month_button.setText("Месяц")
        self.get_month_button.setStyleSheet(self.__button_css_style)
        self.get_month_button.clicked.connect(self.add_month_price)
        # # week
        self.get_week_button = QtWidgets.QPushButton(self)
        self.get_week_button.setGeometry(512, 120, 128, 40)
        self.get_week_button.setFont(get_font())
        self.get_week_button.setText("Неделя")
        self.get_week_button.setStyleSheet(self.__button_css_style)
        self.get_week_button.clicked.connect(self.add_week_price)
        # list with all data in the share
        self.example_share_fields_list = QtWidgets.QListWidget(self)
        self.example_share_fields_list.setGeometry(0, 160, 640, 320)
        self.example_share_fields_list.setFont(get_font())
        self.example_share_fields_list.setStyleSheet(self.__list_css_style)
        # Items list
        self.item1 = QtWidgets.QListWidgetItem()
        self.item2 = QtWidgets.QListWidgetItem()
        self.item3 = QtWidgets.QListWidgetItem()
        self.item4 = QtWidgets.QListWidgetItem()
        self.item5 = QtWidgets.QListWidgetItem()
        self.item6 = QtWidgets.QListWidgetItem()
        self.item7 = QtWidgets.QListWidgetItem()
        self.example_share_fields_list.addItem(self.item1)
        self.example_share_fields_list.addItem(self.item2)
        self.example_share_fields_list.addItem(self.item3)
        self.example_share_fields_list.addItem(self.item4)
        self.example_share_fields_list.addItem(self.item5)
        self.example_share_fields_list.addItem(self.item6)
        self.example_share_fields_list.addItem(self.item7)

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

    def update_shares_quotation_cb(self):
        self.ru_shares = get_ru_shares_list()
        index = 0
        for share in self.ru_shares:
            index += 1
            item = QtWidgets.QListWidgetItem()
            item.setText(str(index) + '. ' + str(share.today_price) + ' ' + share.currency + ' : ' + share.name)
            self.shares_list.addItem(item)

    def get_format_balance(self):
        return 'Мой текущий баланс: ' + str(self.balance.units) + ' ' + self.balance.currency

    def prepare_share_fields_list(self):
        share_item: SharesItem = self.ru_shares[5]
        self.item1.setText('Акция: ' + share_item.ticker + ' : ' + share_item.name)
        self.item2.setText('Цена год назад: ' + str(share_item.year_ago_price))
        self.item3.setText('Цена пол год назад: ' + str(share_item.half_year_ago_price))
        self.item4.setText('Цена 3 месяца назад: ' + str(share_item.three_month_ago_price))
        self.item5.setText('Цена месяц назад: ' + str(share_item.month_ago_price))
        self.item6.setText('Цена неделю назад: ' + str(share_item.week_ago_price))
        self.item7.setText('Цена текущая: ' + str(share_item.today_price))

    def add_year_price(self):
        for share in self.ru_shares:
            set_candle_price_to_share(share, 365)
        self.prepare_share_fields_list()

    def add_half_year_price(self):
        for share in self.ru_shares:
            set_candle_price_to_share(share, 180)
        self.prepare_share_fields_list()

    def add_three_months_price(self):
        for share in self.ru_shares:
            set_candle_price_to_share(share, 90)
        self.prepare_share_fields_list()

    def add_month_price(self):
        for share in self.ru_shares:
            set_candle_price_to_share(share, 30)
        self.prepare_share_fields_list()

    def add_week_price(self):
        for share in self.ru_shares:
            set_candle_price_to_share(share, 7)
        self.prepare_share_fields_list()
