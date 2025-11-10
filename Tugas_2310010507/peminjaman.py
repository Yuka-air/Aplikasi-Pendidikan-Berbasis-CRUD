# peminjaman.py
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PySide6 import QtUiTools
from PySide6.QtCore import QDate  # ✅ Tambahan untuk memastikan QDate bekerja
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
        self.ui.tableWidget.setHorizontalHeaderLabels(["ID", "Nama Anggota", "Judul Buku", "Tgl Pinjam", "Tgl Kembali"])
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)

        # ✅ Pastikan format tanggal QDateEdit
        self.ui.dateEdit.setDisplayFormat("yyyy-MM-dd")
        self.ui.dateEdit_2.setDisplayFormat("yyyy-MM-dd")

        self.ui.pushButton.clicked.connect(self.tambah_data)
        self.ui.pushButton_2.clicked.connect(self.edit_data)
        self.ui.pushButton_3.clicked.connect(self.hapus_data)
        self.ui.pushButton_4.clicked.connect(self.clear_input)

        # === Tambahkan klik tabel agar bisa edit/hapus ===
        self.ui.tableWidget.cellClicked.connect(self.isi_form_dari_tabel)

        # --- MENU NAVIGASI (DITAMBAHKAN, TIDAK MENGUBAH FUNGSI LAIN) ---
        try:
            action_home = self.ui.menuHome.addAction("Home")
            action_home.triggered.connect(self.open_home)

            action_buku = self.ui.menuBuku.addAction("Buku")
            action_buku.triggered.connect(self.open_buku)

            action_anggota = self.ui.menuAnggota.addAction("Anggota")
            action_anggota.triggered.connect(self.open_anggota)

            action_petugas = self.ui.menuPetugas.addAction("Petugas")
            action_petugas.triggered.connect(self.open_petugas)

            action_peminjaman = self.ui.menuPeminjaman.addAction("Peminjaman")
            action_peminjaman.triggered.connect(lambda: None)  # sudah di form ini
        except Exception as e:
            print("Gagal membuat menu navigasi:", e)
        # --- END MENU NAVIGASI ---

        self.load_combo()
        self.load_data()

    # ========== FUNGSI CRUD (ASLI, DITAMBAHKAN FITUR VALIDASI) ==========
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
        # ✅ Validasi input agar tidak kosong
        if (
            not self.ui.comboBox.currentData()
            or not self.ui.comboBox_2.currentData()
        ):
            QMessageBox.warning(self, "Peringatan", "Semua kolom harus diisi sebelum menambah data!")
            return

        # ✅ Ambil tanggal dalam format yyyy-MM-dd
        tgl_pinjam = self.ui.dateEdit.date().toString("yyyy-MM-dd")
        tgl_kembali = self.ui.dateEdit_2.date().toString("yyyy-MM-dd")

        data = (
            self.ui.comboBox.currentData(),
            self.ui.comboBox_2.currentData(),
            tgl_pinjam,
            tgl_kembali
        )
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO peminjaman (id_anggota, id_buku, tgl_pinjam, tgl_kembali) VALUES (%s, %s, %s, %s)", data)
        conn.commit()
        conn.close()
        self.load_data()
        self.clear_input()
        QMessageBox.information(self, "Sukses", "Data peminjaman berhasil ditambahkan.")

    def isi_form_dari_tabel(self, row, column):
        """Klik baris tabel untuk isi data ke kolom input"""
        self.ui.lineEdit.setText(self.ui.tableWidget.item(row, 0).text())
        self.ui.comboBox.setCurrentText(self.ui.tableWidget.item(row, 1).text())
        self.ui.comboBox_2.setCurrentText(self.ui.tableWidget.item(row, 2).text())

        # ✅ Parsing tanggal agar ditampilkan kembali ke QDateEdit
        try:
            tgl_pinjam = QDate.fromString(self.ui.tableWidget.item(row, 3).text(), "yyyy-MM-dd")
            tgl_kembali = QDate.fromString(self.ui.tableWidget.item(row, 4).text(), "yyyy-MM-dd")
            self.ui.dateEdit.setDate(tgl_pinjam)
            self.ui.dateEdit_2.setDate(tgl_kembali)
        except Exception:
            pass

    def edit_data(self):
        id_pinjam = self.ui.lineEdit.text()
        if not id_pinjam:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang ingin diedit terlebih dahulu!")
            return

        #Pastikan tanggal dikirim dengan format benar
        tgl_pinjam = self.ui.dateEdit.date().toString("yyyy-MM-dd")
        tgl_kembali = self.ui.dateEdit_2.date().toString("yyyy-MM-dd")

        data = (
            self.ui.comboBox.currentData(),
            self.ui.comboBox_2.currentData(),
            tgl_pinjam,
            tgl_kembali,
            id_pinjam
        )
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE peminjaman SET id_anggota=%s, id_buku=%s, tgl_pinjam=%s, tgl_kembali=%s WHERE id_pinjam=%s", data)
        conn.commit()
        conn.close()
        self.load_data()
        QMessageBox.information(self, "Sukses", "Data peminjaman berhasil diperbarui.")

    def hapus_data(self):
        id_pinjam = self.ui.lineEdit.text()
        if not id_pinjam:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang ingin dihapus terlebih dahulu!")
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
            cur.execute("DELETE FROM peminjaman WHERE id_pinjam=%s", (id_pinjam,))
            conn.commit()
            # Reset auto increment supaya ID tidak lanjut terus
            cur.execute("ALTER TABLE peminjaman AUTO_INCREMENT = 1")
            conn.commit()
            conn.close()
            self.load_data()
            self.clear_input()
            QMessageBox.information(self, "Sukses", "Data peminjaman berhasil dihapus.")

    def clear_input(self):
        self.ui.lineEdit.clear()

    # ========== FUNGSI NAVIGASI (ASLI) ==========
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
