# buku.py
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PySide6 import QtUiTools
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

        # --- Klik baris tabel untuk edit / hapus ---
        self.ui.tableWidget.cellClicked.connect(self.isi_form_dari_tabel)

        # --- Menu navigasi ---
        try:
            action_home = self.ui.menuHome.addAction("Home")
            action_home.triggered.connect(self.open_home)
            action_buku = self.ui.menuBuku.addAction("Buku")
            action_buku.triggered.connect(lambda: None)
            action_anggota = self.ui.menuAnggota.addAction("Anggota")
            action_anggota.triggered.connect(self.open_anggota)
            action_petugas = self.ui.menuPetugas.addAction("Petugas")
            action_petugas.triggered.connect(self.open_petugas)
            action_peminjaman = self.ui.menuPeminjaman.addAction("Peminjaman")
            action_peminjaman.triggered.connect(self.open_peminjaman)
        except Exception as e:
            print("Gagal mengatur menu navigasi:", e)

        # --- Load data awal ---
        self.load_data()

    # ========== Navigasi Form ==========
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

    # ========== CRUD Buku ==========
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
        #Validasi: tidak boleh tambah jika input kosong
        if (
            not self.ui.lineEdit_2.text().strip()
            or not self.ui.lineEdit_3.text().strip()
            or not self.ui.lineEdit_4.text().strip()
            or not self.ui.lineEdit_5.text().strip()
        ):
            QMessageBox.warning(self, "Peringatan", "Semua kolom harus diisi sebelum menambah data!")
            return

        data = (
            self.ui.lineEdit_2.text(),
            self.ui.lineEdit_3.text(),
            self.ui.lineEdit_4.text(),
            self.ui.lineEdit_5.text(),
        )
        try:
            conn = database.get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO buku (judul, pengarang, penerbit, tahun_terbit) VALUES (%s, %s, %s, %s)",
                data
            )
            conn.commit()
            conn.close()
            self.load_data()
            self.clear_input()
            QMessageBox.information(self, "Sukses", "Data buku berhasil ditambahkan.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menambah data buku:\n{e}")

    def isi_form_dari_tabel(self, row, column):
        """Ketika user klik baris tabel, isi field input agar bisa diedit/dihapus"""
        self.ui.lineEdit.setText(self.ui.tableWidget.item(row, 0).text())
        self.ui.lineEdit_2.setText(self.ui.tableWidget.item(row, 1).text())
        self.ui.lineEdit_3.setText(self.ui.tableWidget.item(row, 2).text())
        self.ui.lineEdit_4.setText(self.ui.tableWidget.item(row, 3).text())
        self.ui.lineEdit_5.setText(self.ui.tableWidget.item(row, 4).text())

    def edit_data(self):
        id_buku = self.ui.lineEdit.text()
        if not id_buku:
            QMessageBox.warning(self, "Peringatan", "Pilih data buku yang ingin diedit terlebih dahulu!")
            return

        data = (
            self.ui.lineEdit_2.text(),
            self.ui.lineEdit_3.text(),
            self.ui.lineEdit_4.text(),
            self.ui.lineEdit_5.text(),
            id_buku,
        )
        try:
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
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal mengedit data buku:\n{e}")

    def hapus_data(self):
        id_buku = self.ui.lineEdit.text()
        if not id_buku:
            QMessageBox.warning(self, "Peringatan", "Pilih data buku yang ingin dihapus terlebih dahulu!")
            return

        konfirmasi = QMessageBox.question(
            self, "Konfirmasi Hapus",
            "Apakah Anda yakin ingin menghapus data ini?",
            QMessageBox.Yes | QMessageBox.No
        )
        if konfirmasi == QMessageBox.Yes:
            try:
                conn = database.get_connection()
                cur = conn.cursor()
                # Hapus data
                cur.execute("DELETE FROM buku WHERE id_buku=%s", (id_buku,))
                conn.commit()

                cur.execute("ALTER TABLE buku AUTO_INCREMENT = 1")
                conn.commit()
                conn.close()

                self.load_data()
                self.clear_input()
                QMessageBox.information(self, "Sukses", "Data buku berhasil dihapus.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal menghapus data buku:\n{e}")

    def clear_input(self):
        for i in range(1, 6):
            field = getattr(self.ui, f"lineEdit_{i}", self.ui.lineEdit)
            field.clear()
