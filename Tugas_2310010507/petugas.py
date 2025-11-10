# petugas.py
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PySide6 import QtUiTools
import database
import buku
import anggota
import peminjaman


class PetugasWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QtUiTools.QUiLoader()
        ui = loader.load("petugas.ui")
        self.setCentralWidget(ui)
        self.ui = ui

        self.setWindowTitle("Form Data Petugas")
        self.resize(self.ui.sizeHint())
        self.setMinimumSize(400, 600)
        self.move(400, 200)

        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(["ID", "Nama Petugas", "Jabatan", "No HP"])
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.ui.pushButton.clicked.connect(self.tambah_data)
        self.ui.pushButton_2.clicked.connect(self.edit_data)
        self.ui.pushButton_3.clicked.connect(self.hapus_data)
        self.ui.pushButton_4.clicked.connect(self.clear_input)

        # === Tambahkan klik tabel agar bisa edit/hapus ===
        self.ui.tableWidget.cellClicked.connect(self.isi_form_dari_tabel)

        # --- MENU NAVIGASI (DITAMBAHKAN TANPA UBAH FUNGSI LAIN) ---
        try:
            action_home = self.ui.menuHome.addAction("Home")
            action_home.triggered.connect(self.open_home)

            action_buku = self.ui.menuBuku.addAction("Buku")
            action_buku.triggered.connect(self.open_buku)

            action_anggota = self.ui.menuAnggota.addAction("Anggota")
            action_anggota.triggered.connect(self.open_anggota)

            action_petugas = self.ui.menuPetugas.addAction("Petugas")
            action_petugas.triggered.connect(lambda: None)  # sudah di halaman petugas

            action_peminjaman = self.ui.menuPeminjaman.addAction("Peminjaman")
            action_peminjaman.triggered.connect(self.open_peminjaman)
        except Exception as e:
            print("Gagal membuat menu navigasi:", e)
        # --- END MENU NAVIGASI ---

        self.load_data()

    # ========== FUNGSI CRUD (DIPERTAHANKAN, DITAMBAHKAN FITUR) ==========
    def load_data(self):
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM petugas")
        rows = cur.fetchall()
        self.ui.tableWidget.setRowCount(0)
        for row_data in rows:
            row = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row)
            for col, val in enumerate(row_data):
                self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(val)))
        conn.close()

    def tambah_data(self):
        # ✅ Validasi agar tidak bisa menambah jika input kosong
        if (
            not self.ui.lineEdit_2.text().strip()
            or not self.ui.lineEdit_3.text().strip()
            or not self.ui.lineEdit_4.text().strip()
        ):
            QMessageBox.warning(self, "Peringatan", "Semua kolom harus diisi sebelum menambah data!")
            return

        data = (self.ui.lineEdit_2.text(), self.ui.lineEdit_3.text(), self.ui.lineEdit_4.text())
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO petugas (nama_petugas, jabatan, no_hp) VALUES (%s, %s, %s)", data)
        conn.commit()
        conn.close()
        self.load_data()
        self.clear_input()
        QMessageBox.information(self, "Sukses", "Data petugas berhasil ditambahkan.")

    def isi_form_dari_tabel(self, row, column):
        """Klik baris tabel untuk isi form agar bisa di-edit atau dihapus"""
        self.ui.lineEdit.setText(self.ui.tableWidget.item(row, 0).text())
        self.ui.lineEdit_2.setText(self.ui.tableWidget.item(row, 1).text())
        self.ui.lineEdit_3.setText(self.ui.tableWidget.item(row, 2).text())
        self.ui.lineEdit_4.setText(self.ui.tableWidget.item(row, 3).text())

    def edit_data(self):
        id_petugas = self.ui.lineEdit.text()
        if not id_petugas:
            QMessageBox.warning(self, "Peringatan", "Pilih data petugas yang ingin diedit terlebih dahulu!")
            return

        data = (
            self.ui.lineEdit_2.text(),
            self.ui.lineEdit_3.text(),
            self.ui.lineEdit_4.text(),
            id_petugas
        )
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE petugas SET nama_petugas=%s, jabatan=%s, no_hp=%s WHERE id_petugas=%s", data)
        conn.commit()
        conn.close()
        self.load_data()
        QMessageBox.information(self, "Sukses", "Data petugas berhasil diperbarui.")

    def hapus_data(self):
        id_petugas = self.ui.lineEdit.text()
        if not id_petugas:
            QMessageBox.warning(self, "Peringatan", "Pilih data petugas yang ingin dihapus terlebih dahulu!")
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
            cur.execute("DELETE FROM petugas WHERE id_petugas=%s", (id_petugas,))
            conn.commit()
            # ✅ Reset auto increment agar ID tidak berlanjut
            cur.execute("ALTER TABLE petugas AUTO_INCREMENT = 1")
            conn.commit()
            conn.close()
            self.load_data()
            self.clear_input()
            QMessageBox.information(self, "Sukses", "Data petugas berhasil dihapus.")

    def clear_input(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()

    # ========== FUNGSI NAVIGASI (TIDAK DIUBAH) ==========
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

    def open_peminjaman(self):
        self.window = peminjaman.PeminjamanWindow()
        self.window.show()
        self.close()
