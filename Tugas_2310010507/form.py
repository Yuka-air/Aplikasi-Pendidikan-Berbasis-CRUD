# form.py
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, uic
import sys
import anggota
import buku


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi("form.ui", self)

        # Tombol navigasi
        self.pushButton.clicked.connect(self.open_buku)
        self.pushButton_2.clicked.connect(self.open_anggota)
        self.pushButton_5.clicked.connect(self.close)

    def open_buku(self):
        self.window = buku.BukuWindow()
        self.window.show()

    def open_anggota(self):
        self.window = anggota.AnggotaWindow()
        self.window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
