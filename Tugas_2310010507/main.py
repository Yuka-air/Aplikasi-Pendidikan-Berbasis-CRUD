# main.py
# -*- coding: utf-8 -*-
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6 import QtUiTools
import database
import buku
import anggota
import petugas
import peminjaman


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loader = QtUiTools.QUiLoader()
        ui = loader.load("form.ui")
        self.setCentralWidget(ui)
        self.ui = ui

        self.setWindowTitle("Aplikasi Sistem Informasi Perpustakaan Sekolah")
        self.resize(500, 400)
        self.move(400, 200)


        try:
            conn = database.get_connection()
            conn.close()
            print("[OK] Koneksi ke database MySQL berhasil.")
        except Exception as e:
            QMessageBox.critical(self, "Koneksi Gagal", f"Tidak dapat terhubung ke MySQL:\n{e}")
            sys.exit(1)

        # Tombol navigasi
        self.ui.pushButton.clicked.connect(self.open_buku)
        self.ui.pushButton_2.clicked.connect(self.open_anggota)
        self.ui.pushButton_3.clicked.connect(self.open_petugas)
        self.ui.pushButton_4.clicked.connect(self.open_peminjaman)
        self.ui.pushButton_5.clicked.connect(self.keluar)

    def open_buku(self):
        self.window = buku.BukuWindow()
        self.window.show()

    def open_anggota(self):
        self.window = anggota.AnggotaWindow()
        self.window.show()

    def open_petugas(self):
        self.window = petugas.PetugasWindow()
        self.window.show()

    def open_peminjaman(self):
        self.window = peminjaman.PeminjamanWindow()
        self.window.show()

    def keluar(self):
        confirm = QMessageBox.question(
            self,
            "Konfirmasi Keluar",
            "Yakin ingin keluar dari aplikasi?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
