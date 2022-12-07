from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout

from PyQt5.QtWidgets import QStatusBar, QPushButton, QLabel

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtCore import Qt

from Dice_Layout import DiceUI
from Player_Layout import PlayersUI


class GameWindow(QWidget):
    round_signal = pyqtSignal()

    def __init__(self):
        super(GameWindow, self).__init__()

        # Player UI
        self.players_ui = PlayersUI()
        self.players_ui.signal_.connect(self.receive_signal_add_btn)

        # Dice UI
        self.dice_ui = DiceUI()
        self.dice_ui.dice_case_signal.connect(self.receive_signal_dice)

        # Set Main Layout
        window = QHBoxLayout()

        window.addStretch(1)
        window.addLayout(self.players_ui)
        window.addStretch(1)
        window.addLayout(self.dice_ui)
        window.addStretch(1)

        # Set Window
        self.setLayout(window)

    @pyqtSlot(dict)
    def receive_signal_dice(self, dice_dict):
        self.players_ui.if_signal_from_dice(dice_dict)

    @pyqtSlot(int)
    def receive_signal_add_btn(self, idx):
        if idx >= 0:
            self.players_ui.players[idx].signal_.connect(self.receive_signal_player)

    @pyqtSlot()
    def receive_signal_player(self):
        self.players_ui.this_turn_player += 1

        if self.players_ui.this_turn_player >= len(self.players_ui.players):
            self.players_ui.this_turn_player = 0
            self.send_next_round()

        self.dice_ui.if_player_write_score()

    @pyqtSlot()
    def send_next_round(self):
        self.round_signal.emit()


class GameEnd(QWidget):
    restart_signal = pyqtSignal()

    def __init__(self, name):
        super(GameEnd, self).__init__()

        winner = QLabel("승자는 " + name + "입니다.")
        self.restart_btn = QPushButton("재시작")
        self.restart_btn.clicked.connect(self.restart_btn_clicked)

        v_box = QVBoxLayout()
        v_box.setAlignment(Qt.AlignHCenter)

        self.v_box.addWidget(winner)
        self.v_box.addWidget(self.restart_btn)

        self.setLayout(self.v_box)

        self.show()

    @pyqtSlot()
    def restart_btn_clicked(self):
        self.restart_signal.emit()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # QWidget
        self.wg = GameWindow()
        self.wg.round_signal.connect(self.next_round)
        self.setCentralWidget(self.wg)

        # Set StatusBar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.start_btn = QPushButton("게임 시작!")
        self.statusbar.addPermanentWidget(self.start_btn)
        self.start_btn.clicked.connect(self.clicked_start)

        self.round_num = 1
        self.round = QLabel("현재 라운드: " + str(self.round_num) + " / 12")
        self.statusbar.addWidget(self.round)

        # Normal Setting
        self.setGeometry(10, 100, 500, 500)
        # self.setFixedSize(1200, 700)
        self.setWindowTitle("Yacht Dice")

        self.show()

    def clicked_start(self):
        if len(self.wg.players_ui.players) > 0:
            self.start_btn.setEnabled(False)
            self.wg.players_ui.add_ply_btn.setEnabled(False)
            self.wg.players_ui.del_ply_btn.setEnabled(False)
            self.wg.dice_ui.reroll_btn.setEnabled(True)

    @pyqtSlot()
    def next_round(self):
        if self.round_num == 12:
            self.end = GameEnd(self.wg.players_ui.show_winner())
            self.end.restart_signal.connect(self.restart)
            # 게임이 끝난 경우 total이 높은 사람이 승리
            return None
        self.round_num += 1
        self.round.setText("현재 라운드: " + str(self.round_num) + " / 12")
        self.statusbar.repaint()

    @pyqtSlot()
    def restart(self):
        # QWidget
        self.wg = GameWindow()
        self.wg.round_signal.connect(self.next_round)
        self.setCentralWidget(self.wg)

        # Set StatusBar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.start_btn = QPushButton("게임 시작!")
        self.statusbar.addPermanentWidget(self.start_btn)
        self.start_btn.clicked.connect(self.clicked_start)

        self.round_num = 1
        self.round = QLabel("현재 라운드: " + str(self.round_num) + " / 12")
        self.statusbar.addWidget(self.round)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    game = MainWindow()
    sys.exit(app.exec_())
