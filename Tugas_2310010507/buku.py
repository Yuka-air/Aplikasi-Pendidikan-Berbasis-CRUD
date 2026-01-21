# buku.py
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PySide6 import QtUiTools

# ===== TAMBAHAN UNTUK PRINT =====
from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QPrinterInfo
from PySide6.QtGui import QTextDocument
# ===============================

import database
import anggota
import petugas
import peminjaman


class BukuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QtUiTools.QUiLoader()
        ui = loader.load("buku.ui")
        self.setCentralWidget(ui)
        self.ui = ui

        # --- Pengaturan tampilan ---
        self.setWindowTitle("Form Data Buku")
        self.resize(self.ui.sizeHint())
        self.setMinimumSize(400, 600)
        self.move(400, 200)

        # --- Konfigurasi tabel ---
        self.ui.tableWidget.setColumnCount(5)
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Judul", "Pengarang", "Penerbit", "Tahun Terbit"]
        )
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)

        # --- Tombol CRUD ---
        self.ui.pushButton.clicked.connect(self.tambah_data)
        self.ui.pushButton_2.clicked.connect(self.edit_data)
        self.ui.pushButton_3.clicked.connect(self.hapus_data)
        self.ui.pushButton_4.clicked.connect(self.clear_input)

        # ===== TOMBOL PRINT (TAMBAHAN) =====
        self.ui.pushButton_5.clicked.connect(self.print_data)
        # ==================================

        # --- Klik baris tabel ---
        self.ui.tableWidget.cellClicked.connect(self.isi_form_dari_tabel)

        # --- Menu navigasi ---
        try:
            self.ui.menuHome.addAction("Home").triggered.connect(self.open_home)
            self.ui.menuBuku.addAction("Buku")
            self.ui.menuAnggota.addAction("Anggota").triggered.connect(self.open_anggota)
            self.ui.menuPetugas.addAction("Petugas").triggered.connect(self.open_petugas)
            self.ui.menuPeminjaman.addAction("Peminjaman").triggered.connect(self.open_peminjaman)
        except Exception as e:
            print("Gagal mengatur menu navigasi:", e)

        self.load_data()

    # ========== NAVIGASI ==========
    def open_home(self):
        from form import Main
        self.window = Main()
        self.window.show()
        self.close()

    def open_anggota(self):
        self.window = anggota.AnggotaWindow()
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

    # ========== CRUD ==========
    def load_data(self):
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM buku")
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
            or not self.ui.lineEdit_5.text().strip()
        ):
            QMessageBox.warning(self, "Peringatan", "Semua kolom harus diisi!")
            return

        data = (
            self.ui.lineEdit_2.text(),
            self.ui.lineEdit_3.text(),
            self.ui.lineEdit_4.text(),
            self.ui.lineEdit_5.text(),
        )

        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO buku (judul, pengarang, penerbit, tahun_terbit) VALUES (%s,%s,%s,%s)",
            data
        )
        conn.commit()
        conn.close()

        self.load_data()
        self.clear_input()
        QMessageBox.information(self, "Sukses", "Data buku berhasil ditambahkan.")

    def isi_form_dari_tabel(self, row, column):
        self.ui.lineEdit.setText(self.ui.tableWidget.item(row, 0).text())
        self.ui.lineEdit_2.setText(self.ui.tableWidget.item(row, 1).text())
        self.ui.lineEdit_3.setText(self.ui.tableWidget.item(row, 2).text())
        self.ui.lineEdit_4.setText(self.ui.tableWidget.item(row, 3).text())
        self.ui.lineEdit_5.setText(self.ui.tableWidget.item(row, 4).text())

    def edit_data(self):
        id_buku = self.ui.lineEdit.text()
        if not id_buku:
            QMessageBox.warning(self, "Peringatan", "Pilih data terlebih dahulu!")
            return

        data = (
            self.ui.lineEdit_2.text(),
            self.ui.lineEdit_3.text(),
            self.ui.lineEdit_4.text(),
            self.ui.lineEdit_5.text(),
            id_buku,
        )

        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE buku SET judul=%s, pengarang=%s, penerbit=%s, tahun_terbit=%s WHERE id_buku=%s",
            data
        )
        conn.commit()
        conn.close()

        self.load_data()
        QMessageBox.information(self, "Sukses", "Data buku berhasil diperbarui.")

    def hapus_data(self):
        id_buku = self.ui.lineEdit.text()
        if not id_buku:
            QMessageBox.warning(self, "Peringatan", "Pilih data terlebih dahulu!")
            return

        if QMessageBox.question(
            self,
            "Konfirmasi Hapus",
            "Yakin ingin menghapus data ini?",
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:

            conn = database.get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM buku WHERE id_buku=%s", (id_buku,))
            conn.commit()

            cur.execute("ALTER TABLE buku AUTO_INCREMENT = 1")
            conn.commit()
            conn.close()

            self.load_data()
            self.clear_input()
            QMessageBox.information(self, "Sukses", "Data buku berhasil dihapus.")

    def clear_input(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_5.clear()

    # ========== FUNGSI PRINT (TAMBAHAN SAJA) ==========
    def print_data(self):
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
            <h2 align="center">Data Buku Perpustakaan</h2>
            <table border="1" cellspacing="0" cellpadding="5" width="100%">
                <tr>
                    <th>ID</th>
                    <th>Judul</th>
                    <th>Pengarang</th>
                    <th>Penerbit</th>
                    <th>Tahun Terbit</th>
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
                document.print_(printer)  # PySide6 ✔
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Gagal Mencetak",
                    f"Terjadi kesalahan saat mencetak:\n{e}"
                )
