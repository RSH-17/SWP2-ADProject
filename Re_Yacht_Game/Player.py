from PyQt5.QtCore import Qt, QObject
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from PyQt5.QtWidgets import QPushButton, QLineEdit

from dice_case_lst import dice_case_


OBJ_WIDTH = 70


class Button(QPushButton):
    def __init__(self, callback):
        super(Button, self).__init__()
        self.num = 0                    # 이 버튼이 선택된 상태인지

        self.setFixedWidth(OBJ_WIDTH)
        self.setText("0")
        self.clicked.connect(lambda: callback())


class Player(QObject):
    signal_ = pyqtSignal()

    def __init__(self):
        super(Player, self).__init__()

        self.is_get_bonus = False

        self.player_name = QLineEdit("")
        self.player_name.setFixedWidth(OBJ_WIDTH)
        self.player_name.setAlignment(Qt.AlignHCenter)
        self.player_name.returnPressed.connect(lambda: self.player_name.setReadOnly(True))

        self.num_cases = [Button(self.case_btn_clicked) for _ in range(6)]
        self.spe_cases = [Button(self.case_btn_clicked) for _ in range(6)]

        self.total = [QLineEdit('0') for _ in range(3)]    # 0 : bonus, 1 : subTotal, 2 : total

        for t in self.total:
            t.setFixedWidth(OBJ_WIDTH)
            t.setAlignment(Qt.AlignHCenter)
            t.setReadOnly(True)

        self.able_btn(False)

    def add_widget(self, grid, player_num):
        idx = 0

        grid.addWidget(self.player_name, idx, player_num)
        idx += 1

        for num in self.num_cases:
            grid.addWidget(num, idx, player_num)
            idx += 1

        for t in range(2):
            grid.addWidget(self.total[1 - t], idx, player_num)
            idx += 1

        for spe in self.spe_cases:
            grid.addWidget(spe, idx, player_num)
            idx += 1

        grid.addWidget(self.total[2], idx, player_num)

    def del_widget(self):
        self.player_name.setParent(None)

        for idx in range(6):
            self.num_cases[idx].setParent(None)
            self.spe_cases[idx].setParent(None)

        for t in self.total:
            t.setParent(None)

    def case_btn_set_num(self, dice_case):
        for idx in range(6):
            if self.num_cases[idx].num == 0:
                self.num_cases[idx].setText(str(dice_case_[idx][1](dice_case)))
            if self.spe_cases[idx].num == 0:
                self.spe_cases[idx].setText(str(dice_case_[8 + idx][1](dice_case)))

    @pyqtSlot()
    def case_btn_clicked(self):
        sender = self.sender()

        for idx in range(6):
            if id(self.num_cases[idx]) == id(sender):
                self.total[1].setText(str(int(self.total[1].text()) + int(sender.text())))
                self.total[2].setText(str(int(self.total[2].text()) + int(sender.text())))
                break

            if id(self.spe_cases[idx]) == id(sender):
                self.total[2].setText(str(int(self.total[2].text()) + int(sender.text())))
                break

        if self.is_bonus() and (not self.is_get_bonus):
            self.total[0].setText("+ 35")
            self.total[2].setText(str(int(self.total[2].text()) + 35))

        self.able_btn(False)
        sender.num = 1

        self.signal_.emit()

    def is_bonus(self):
        if int(self.total[1].text()) > 63:
            self.is_get_bonus = True
            return True

        return False

    def able_btn(self, flg):
        for idx in range(6):
            if self.num_cases[idx].num == 0:
                self.num_cases[idx].setEnabled(flg)

            if self.spe_cases[idx].num == 0:
                self.spe_cases[idx].setEnabled(flg)