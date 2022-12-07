from PyQt5.QtCore import pyqtSignal, pyqtSlot

from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel, QPushButton

from dice_case_lst import dice_case_

from Player import Player


class PlayersUI(QGridLayout):
    signal_ = pyqtSignal(int)

    def __init__(self):
        super(PlayersUI, self).__init__()

        self.players = []   # Player() list
        self.this_turn_player = 0   # 0 ~ len(self.players) - 1

        # ------ 족보 -------
        for idx, case in enumerate(list(zip(*dice_case_))[0]):
            self.addWidget(QLabel(case + " : "), idx + 1, 0)
        # -----------------------------------

        # 플레이어 추가 버튼
        self.add_ply_btn = QPushButton("Add")
        self.add_ply_btn.setFixedWidth(100)
        self.add_ply_btn.clicked.connect(self.btn_clicked)
        self.addWidget(self.add_ply_btn, 0, 1)

        # 플레이어 제거 버튼
        self.del_ply_btn = QPushButton("Del")
        self.del_ply_btn.setFixedWidth(100)
        self.del_ply_btn.clicked.connect(self.btn_clicked)
        self.addWidget(self.del_ply_btn, 1, 1)

    @pyqtSlot()
    def btn_clicked(self):
        sender = self.sender()

        self.add_ply_btn.setParent(None)
        self.del_ply_btn.setParent(None)

        if sender.text() == "Add":
            self.adjust_player(0)
            self.signal_.emit(len(self.players) - 1)
        elif sender.text() == "Del":
            self.adjust_player(1)

        self.addWidget(self.add_ply_btn, 0, 1 + len(self.players))
        self.addWidget(self.del_ply_btn, 1, 1 + len(self.players))

    def adjust_player(self, flg):
        if flg == 0:
            self.players.append(Player())
            self.players[len(self.players) - 1].add_widget(self, len(self.players))
        elif flg == 1:
            if len(self.players) > 0:
                self.players[len(self.players) - 1].del_widget()
                self.players = self.players[:-1]

    def show_winner(self):
        winner = ""
        score = 0

        for player in self.players:
            if int(player.total[2].text()) > score:
                winner = player.player_name.text()
            elif int(player.total[2].text()) == score:
                winner += " " + player.player_name.text()

        return winner

    def if_signal_from_dice(self, dice_dict):
        if len(self.players) != 0:
            self.players[self.this_turn_player].able_btn(True)
            self.players[self.this_turn_player].case_btn_set_num(dice_dict)

