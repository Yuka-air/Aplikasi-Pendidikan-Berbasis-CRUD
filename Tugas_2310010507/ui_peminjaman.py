# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'peminjaman.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTableWidget, QTableWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(510, 569)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(90, 240, 371, 271))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(220, 10, 91, 16))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(60, 40, 71, 16))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(60, 70, 71, 16))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(60, 100, 61, 16))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(60, 130, 81, 16))
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(60, 160, 71, 16))
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(160, 40, 201, 20))
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(160, 70, 201, 22))
        self.comboBox_2 = QComboBox(self.centralwidget)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(160, 100, 201, 22))
        self.dateEdit = QDateEdit(self.centralwidget)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setGeometry(QRect(160, 130, 201, 22))
        self.dateEdit_2 = QDateEdit(self.centralwidget)
        self.dateEdit_2.setObjectName(u"dateEdit_2")
        self.dateEdit_2.setGeometry(QRect(160, 160, 201, 22))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(160, 190, 61, 18))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(230, 190, 61, 18))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(300, 190, 61, 18))
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(220, 220, 80, 18))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 510, 17))
        self.menuHome = QMenu(self.menubar)
        self.menuHome.setObjectName(u"menuHome")
        self.menuBuku = QMenu(self.menubar)
        self.menuBuku.setObjectName(u"menuBuku")
        self.menuAnggota = QMenu(self.menubar)
        self.menuAnggota.setObjectName(u"menuAnggota")
        self.menuPetugas = QMenu(self.menubar)
        self.menuPetugas.setObjectName(u"menuPetugas")
        self.menuPeminjaman = QMenu(self.menubar)
        self.menuPeminjaman.setObjectName(u"menuPeminjaman")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuHome.menuAction())
        self.menubar.addAction(self.menuBuku.menuAction())
        self.menubar.addAction(self.menuAnggota.menuAction())
        self.menubar.addAction(self.menuPetugas.menuAction())
        self.menubar.addAction(self.menuPeminjaman.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Form Peminjaman", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"ID_Peminjaman", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Nama Peminjam", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Buku Pinjam", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Tanggal Pinjam", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Tanggal Kembali", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Tambah", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Hapus", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Clear Input", None))
        self.menuHome.setTitle(QCoreApplication.translate("MainWindow", u"Home", None))
        self.menuBuku.setTitle(QCoreApplication.translate("MainWindow", u"Buku", None))
        self.menuAnggota.setTitle(QCoreApplication.translate("MainWindow", u"Anggota", None))
        self.menuPetugas.setTitle(QCoreApplication.translate("MainWindow", u"Petugas", None))
        self.menuPeminjaman.setTitle(QCoreApplication.translate("MainWindow", u"Peminjaman", None))
    # retranslateUi

