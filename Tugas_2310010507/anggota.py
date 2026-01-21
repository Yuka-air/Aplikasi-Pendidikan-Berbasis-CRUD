# anggota.py
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PySide6 import QtUiTools

# ===== TAMBAHAN UNTUK PRINT =====
from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QPrinterInfo
from PySide6.QtGui import QTextDocument
# ===============================

import database
import buku
import petugas
import peminjaman


class AnggotaWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QtUiTools.QUiLoader()
        ui = loader.load("anggota.ui")
        self.setCentralWidget(ui)
        self.ui = ui

        self.setWindowTitle("Form Data Anggota")
        self.resize(self.ui.sizeHint())
        self.setMinimumSize(500, 600)
        self.move(400, 200)

        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Nama", "Alamat", "No HP"]
        )
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.ui.pushButton.clicked.connect(self.tambah_data)
        self.ui.pushButton_2.clicked.connect(self.edit_data)
        self.ui.pushButton_3.clicked.connect(self.hapus_data)
        self.ui.pushButton_4.clicked.connect(self.clear_input)

        # ===== TOMBOL PRINT =====
        self.ui.pushButton_5.clicked.connect(self.print_data)
        # =======================

        # Klik baris tabel agar bisa di-edit dan dihapus
        self.ui.tableWidget.cellClicked.connect(self.isi_form_dari_tabel)

        # --- MENU NAVIGASI ---
        try:
            self.ui.menuHome.addAction("Home").triggered.connect(self.open_home)
            self.ui.menuBuku.addAction("Buku").triggered.connect(self.open_buku)
            self.ui.menuAnggota.addAction("Anggota")
            self.ui.menuPetugas.addAction("Petugas").triggered.connect(self.open_petugas)
            self.ui.menuPeminjaman.addAction("Peminjaman").triggered.connect(self.open_peminjaman)
        except Exception as e:
            print("Gagal membuat menu navigasi:", e)
        # --- END MENU NAVIGASI ---

        self.load_data()

    # ========== FUNGSI CRUD ==========
    def load_data(self):
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM anggota")
        rows = cur.fetchall()

        self.ui.tableWidget.setRowCount(0)
        for row_data in rows:
            row = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row)
            for col, val in enumerate(row_data):
                self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(val)))
        conn.close()

    def tambah_data(self):
        if (
            not self.ui.lineEdit_2.text().strip()
            or not self.ui.lineEdit_3.text().strip()
            or not self.ui.lineEdit_4.text().strip()
        ):
            QMessageBox.warning(
                self,
                "Peringatan",
                "Semua kolom harus diisi sebelum menambah data!"
            )
            return

        data = (
            self.ui.lineEdit_2.text(),
            self.ui.lineEdit_3.text(),
            self.ui.lineEdit_4.text()
        )

        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO anggota (nama, alamat, no_hp) VALUES (%s, %s, %s)",
            data
        )
        conn.commit()
        conn.close()

        self.load_data()
        self.clear_input()
        QMessageBox.information(self, "Sukses", "Data anggota berhasil ditambahkan.")

    def isi_form_dari_tabel(self, row, column):
        self.ui.lineEdit.setText(self.ui.tableWidget.item(row, 0).text())
        self.ui.lineEdit_2.setText(self.ui.tableWidget.item(row, 1).text())
        self.ui.lineEdit_3.setText(self.ui.tableWidget.item(row, 2).text())
        self.ui.lineEdit_4.setText(self.ui.tableWidget.item(row, 3).text())

    def edit_data(self):
        id_anggota = self.ui.lineEdit.text()
        if not id_anggota:
            QMessageBox.warning(
                self,
                "Peringatan",
                "Pilih data anggota yang ingin diedit terlebih dahulu!"
            )
            return

        data = (
            self.ui.lineEdit_2.text(),
            self.ui.lineEdit_3.text(),
            self.ui.lineEdit_4.text(),
            id_anggota
        )

        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE anggota SET nama=%s, alamat=%s, no_hp=%s WHERE id_anggota=%s",
            data
        )
        conn.commit()
        conn.close()

        self.load_data()
        QMessageBox.information(self, "Sukses", "Data anggota berhasil diperbarui.")

    def hapus_data(self):
        id_anggota = self.ui.lineEdit.text()
        if not id_anggota:
            QMessageBox.warning(
                self,
                "Peringatan",
                "Pilih data anggota yang ingin dihapus terlebih dahulu!"
            )
            return

        konfirmasi = QMessageBox.question(
            self,
            "Konfirmasi Hapus",
            "Apakah Anda yakin ingin menghapus data ini?",
            QMessageBox.Yes | QMessageBox.No
        )

        if konfirmasi == QMessageBox.Yes:
            conn = database.get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM anggota WHERE id_anggota=%s", (id_anggota,))
            conn.commit()

            cur.execute("ALTER TABLE anggota AUTO_INCREMENT = 1")
            conn.commit()
            conn.close()

            self.load_data()
            self.clear_input()
            QMessageBox.information(self, "Sukses", "Data anggota berhasil dihapus.")

    def clear_input(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()

    # ========== FUNGSI PRINT (DIPERBAIKI) ==========
    def print_data(self):
        # Jika tidak ada printer
        if not QPrinterInfo.availablePrinters():
            QMessageBox.critical(
                self,
                "Printer Tidak Ditemukan",
                "Tidak ada printer yang tersedia di sistem."
            )
            return

        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec() == QPrintDialog.Accepted:
            html = """
            <h2 align="center">Data Anggota Perpustakaan</h2>
            <table border="1" cellspacing="0" cellpadding="5" width="100%">
                <tr>
                    <th>ID</th>
                    <th>Nama</th>
                    <th>Alamat</th>
                    <th>No HP</th>
                </tr>
            """

            for row in range(self.ui.tableWidget.rowCount()):
                html += "<tr>"
                for col in range(self.ui.tableWidget.columnCount()):
                    item = self.ui.tableWidget.item(row, col)
                    html += f"<td>{item.text() if item else ''}</td>"
                html += "</tr>"

            html += "</table>"

            document = QTextDocument()
            document.setHtml(html)

            try:
                document.print_(printer)  # ✅ PySide6 benar
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Gagal Mencetak",
                    f"Terjadi kesalahan saat mencetak:\n{e}"
                )

    # ========== NAVIGASI ==========
    def open_home(self):
        from form import Main
        self.window = Main()
        self.window.show()
        self.close()

    def open_buku(self):
        self.window = buku.BukuWindow()
        self.window.show()
        self.close()

    def open_petugas(self):
        self.window = petugas.PetugasWindow()
        self.window.show()
        self.close()

    def open_peminjaman(self):
        self.window = peminjaman.PeminjamanWindow()
        self.window.show()
        self.close()
