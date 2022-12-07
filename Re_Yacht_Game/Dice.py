from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QPushButton


class DiceImage(QIcon):
    def __init__(self, file_name):
        super(DiceImage, self).__init__()

        image_size = 134

        pixmap = QPixmap(file_name)
        pixmap = pixmap.scaled(image_size, image_size, Qt.IgnoreAspectRatio)

        self.addPixmap(pixmap)


class DiceButton(QPushButton):
    click_signal = pyqtSignal(int)

    def __init__(self, num):
        super(DiceButton, self).__init__()

        self.num = 0
        self.selected = 0       # 0 : non_select, 1 : select

        self.show_icon(num)
        self.setEnabled(False)
        self.clicked.connect(self.me_clicked)

    def change_dice(self):
        icon = DiceImage('./Dice_Image_png/dice' + str(self.num) + '.png')
        return icon

    def show_icon(self, num):
        self.num = num
        self.setIcon(self.change_dice())
        self.setIconSize(QSize(134, 134))
        self.setStyleSheet("border: 0px;")

    @pyqtSlot()
    def me_clicked(self):
        if self.parent():
            self.setParent(None)

        if self.selected == 0:
            self.selected = 1
        else:
            self.selected = 0

        self.click_signal.emit(self.selected)

