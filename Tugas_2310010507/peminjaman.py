# peminjaman.py
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PySide6 import QtUiTools
from PySide6.QtCore import QDate

# ===== TAMBAHAN PRINT (SAMA DENGAN FILE LAIN) =====
from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QPrinterInfo
from PySide6.QtGui import QTextDocument
# ================================================

import database
import buku
import anggota
import petugas


class PeminjamanWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QtUiTools.QUiLoader()
        ui = loader.load("peminjaman.ui")
        self.setCentralWidget(ui)
        self.ui = ui

        self.setWindowTitle("Form Data Peminjaman")
        self.resize(self.ui.sizeHint())
        self.setMinimumSize(500, 600)
        self.move(400, 200)

        self.ui.tableWidget.setColumnCount(5)
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Nama Anggota", "Judul Buku", "Tgl Pinjam", "Tgl Kembali"]
        )
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.ui.dateEdit.setDisplayFormat("yyyy-MM-dd")
        self.ui.dateEdit_2.setDisplayFormat("yyyy-MM-dd")

        self.ui.pushButton.clicked.connect(self.tambah_data)
        self.ui.pushButton_2.clicked.connect(self.edit_data)
        self.ui.pushButton_3.clicked.connect(self.hapus_data)
        self.ui.pushButton_4.clicked.connect(self.clear_input)

        # ===== TOMBOL PRINT (SAMA POLA) =====
        self.ui.pushButton_5.clicked.connect(self.print_data)
        # ===================================

        self.ui.tableWidget.cellClicked.connect(self.isi_form_dari_tabel)

        # --- MENU NAVIGASI ---
        try:
            self.ui.menuHome.addAction("Home").triggered.connect(self.open_home)
            self.ui.menuBuku.addAction("Buku").triggered.connect(self.open_buku)
            self.ui.menuAnggota.addAction("Anggota").triggered.connect(self.open_anggota)
            self.ui.menuPetugas.addAction("Petugas").triggered.connect(self.open_petugas)
            self.ui.menuPeminjaman.addAction("Peminjaman")
        except Exception as e:
            print("Gagal membuat menu navigasi:", e)

        self.load_combo()
        self.load_data()

    # ========== CRUD ==========
    def load_combo(self):
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id_anggota, nama FROM anggota")
        for row in cur.fetchall():
            self.ui.comboBox.addItem(f"{row[1]} (ID:{row[0]})", row[0])

        cur.execute("SELECT id_buku, judul FROM buku")
        for row in cur.fetchall():
            self.ui.comboBox_2.addItem(f"{row[1]} (ID:{row[0]})", row[0])
        conn.close()

    def load_data(self):
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.id_pinjam, a.nama, b.judul, p.tgl_pinjam, p.tgl_kembali
            FROM peminjaman p
            JOIN anggota a ON p.id_anggota=a.id_anggota
            JOIN buku b ON p.id_buku=b.id_buku
        """)
        rows = cur.fetchall()
        self.ui.tableWidget.setRowCount(0)
        for row_data in rows:
            row = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row)
            for col, val in enumerate(row_data):
                self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(val)))
        conn.close()

    def tambah_data(self):
        if not self.ui.comboBox.currentData() or not self.ui.comboBox_2.currentData():
            QMessageBox.warning(self, "Peringatan", "Semua kolom harus diisi!")
            return

        data = (
            self.ui.comboBox.currentData(),
            self.ui.comboBox_2.currentData(),
            self.ui.dateEdit.date().toString("yyyy-MM-dd"),
            self.ui.dateEdit_2.date().toString("yyyy-MM-dd")
        )
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO peminjaman (id_anggota, id_buku, tgl_pinjam, tgl_kembali) "
            "VALUES (%s, %s, %s, %s)", data
        )
        conn.commit()
        conn.close()
        self.load_data()
        self.clear_input()
        QMessageBox.information(self, "Sukses", "Data peminjaman berhasil ditambahkan.")

    def isi_form_dari_tabel(self, row, _):
        self.ui.lineEdit.setText(self.ui.tableWidget.item(row, 0).text())
        self.ui.comboBox.setCurrentText(self.ui.tableWidget.item(row, 1).text())
        self.ui.comboBox_2.setCurrentText(self.ui.tableWidget.item(row, 2).text())
        self.ui.dateEdit.setDate(QDate.fromString(self.ui.tableWidget.item(row, 3).text(), "yyyy-MM-dd"))
        self.ui.dateEdit_2.setDate(QDate.fromString(self.ui.tableWidget.item(row, 4).text(), "yyyy-MM-dd"))

    def edit_data(self):
        if not self.ui.lineEdit.text():
            QMessageBox.warning(self, "Peringatan", "Pilih data terlebih dahulu!")
            return

        data = (
            self.ui.comboBox.currentData(),
            self.ui.comboBox_2.currentData(),
            self.ui.dateEdit.date().toString("yyyy-MM-dd"),
            self.ui.dateEdit_2.date().toString("yyyy-MM-dd"),
            self.ui.lineEdit.text()
        )
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE peminjaman SET id_anggota=%s, id_buku=%s,
            tgl_pinjam=%s, tgl_kembali=%s WHERE id_pinjam=%s
        """, data)
        conn.commit()
        conn.close()
        self.load_data()
        QMessageBox.information(self, "Sukses", "Data peminjaman berhasil diperbarui.")

    def hapus_data(self):
        if not self.ui.lineEdit.text():
            QMessageBox.warning(self, "Peringatan", "Pilih data terlebih dahulu!")
            return

        if QMessageBox.question(self, "Hapus", "Yakin hapus data?") == QMessageBox.Yes:
            conn = database.get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM peminjaman WHERE id_pinjam=%s", (self.ui.lineEdit.text(),))
            conn.commit()
            cur.execute("ALTER TABLE peminjaman AUTO_INCREMENT = 1")
            conn.commit()
            conn.close()
            self.load_data()
            self.clear_input()
            QMessageBox.information(self, "Sukses", "Data peminjaman berhasil dihapus.")

    def clear_input(self):
        self.ui.lineEdit.clear()

    # ========== PRINT (SAMA SEPERTI FILE LAIN) ==========
    def print_data(self):
        if not QPrinterInfo.availablePrinters():
            QMessageBox.critical(self, "Printer", "Tidak ada printer yang tersedia.")
            return

        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec() == QPrintDialog.Accepted:
            html = """
            <h3 align="center">Data Peminjaman</h3>
            <table border="1" cellspacing="0" cellpadding="5" width="100%">
            <tr>
                <th>ID</th>
                <th>Nama Anggota</th>
                <th>Judul Buku</th>
                <th>Tgl Pinjam</th>
                <th>Tgl Kembali</th>
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
            document.print_(printer)

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

    def open_anggota(self):
        self.window = anggota.AnggotaWindow()
        self.window.show()
        self.close()

    def open_petugas(self):
        self.window = petugas.PetugasWindow()
        self.window.show()
        self.close()
