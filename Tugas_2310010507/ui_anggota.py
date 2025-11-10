# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'anggota.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(489, 566)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(60, 200, 371, 291))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(170, 10, 81, 16))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(60, 40, 61, 16))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(60, 70, 51, 16))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(60, 100, 51, 16))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(60, 130, 41, 16))
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(140, 40, 171, 20))
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(140, 70, 171, 20))
        self.lineEdit_3 = QLineEdit(self.centralwidget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(140, 100, 171, 20))
        self.lineEdit_4 = QLineEdit(self.centralwidget)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setGeometry(QRect(140, 130, 171, 20))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(140, 150, 51, 18))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(200, 150, 51, 18))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(260, 150, 51, 18))
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(190, 170, 80, 18))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 489, 17))
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
        self.label.setText(QCoreApplication.translate("MainWindow", u"Form Anggota", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"ID_Anggota", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Nama", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Alamat", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"No_Hp", None))
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

