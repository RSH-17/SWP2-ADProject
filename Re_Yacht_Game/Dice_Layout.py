from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLabel, QPushButton

from PyQt5.QtCore import pyqtSignal, pyqtSlot

import random

from Dice import DiceButton


class DiceUI(QVBoxLayout):
    dice_case_signal = pyqtSignal(dict)

    def __init__(self):
        super(DiceUI, self).__init__()

        self.dice_case_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

        # First ~ Second Line
        self.dice_select_lst = [[QLabel("미선택"), QHBoxLayout()],
                                [QLabel("선택"), QHBoxLayout()]]
        for lst in self.dice_select_lst:
            lst[1].addWidget(lst[0])

        # dice 이미지 버튼 생성
        self.dice_lst = [DiceButton(1) for _ in range(5)]
        for dice in self.dice_lst:
            dice.click_signal.connect(self.clicked_dice)
            self.dice_select_lst[0][1].addWidget(dice)

        # Third Line : point & other btn (reroll, apply)
        h_box_3 = QHBoxLayout()

        self.remain_point = [QLabel("남은 시도 횟수: 3"), 3]

        self.reroll_btn = QPushButton("재시도")
        self.reroll_btn.clicked.connect(self.clicked_reroll_btn)
        self.reroll_btn.setEnabled(False)
        self.reroll_btn.setFixedWidth(100)

        h_box_3.addWidget(self.remain_point[0])
        h_box_3.addWidget(self.reroll_btn)

        # Add Layout
        for idx in range(2):
            self.addLayout(self.dice_select_lst[1 - idx][1])
        self.addLayout(h_box_3)

    def clicked_dice(self):
        sender = self.sender()
        self.dice_select_lst[sender.selected][1].addWidget(sender)

    def clicked_reroll_btn(self):
        # 만약 주사위 이미지 버튼이 활성화 되지 않은 경우 -> 활성화
        if not self.dice_lst[0].isEnabled():
            for dice in self.dice_lst:
                dice.setEnabled(True)

        # 랜덤 숫자
        num_lst = [random.randint(1, 6) for _ in range(5)]

        for idx, dice in enumerate(self.dice_lst):
            if dice.selected == 0:                        # non-selected 에 있는 주사위만 리롤
                dice.show_icon(num_lst[idx])

        # 리롤 가능 횟수 차감
        self.remain_point[1] -= 1
        self.remain_point[0].setText(self.remain_point[0].text()[:-1] + str(self.remain_point[1]))

        # 주사위 딕셔너리 보내기
        self.send_dice_dict()

        # 리롤 가능 횟수 0 일떄 -> 리롤 버튼 비 활성화
        if self.remain_point[1] == 0:
            self.reroll_btn.setEnabled(False)

            for dice in self.dice_lst:
                dice.selected = 0
                dice.setEnabled(False)

                dice.setParent(None)
                self.dice_select_lst[0][1].addWidget(dice)

    @pyqtSlot()
    def send_dice_dict(self):
        self.dice_case_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

        for dice in self.dice_lst:
            self.dice_case_dict[dice.num] += 1

        self.dice_case_signal.emit(self.dice_case_dict)

    def if_player_write_score(self):
        for dice in self.dice_lst:
            dice.selected = 0
            dice.setEnabled(False)

            dice.show_icon(1)
            dice.setParent(None)
            self.dice_select_lst[0][1].addWidget(dice)

        self.reroll_btn.setEnabled(True)
        self.remain_point[1] = 3
        self.remain_point[0].setText(self.remain_point[0].text()[:-1] + str(self.remain_point[1]))

