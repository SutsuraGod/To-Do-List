# Form implementation generated from reading ui file 'categoriesWindow.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(494, 359)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.categoriesLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.categoriesLabel.setObjectName("categoriesLabel")
        self.gridLayout.addWidget(self.categoriesLabel, 0, 0, 1, 1)
        self.categoriesTable = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.categoriesTable.setObjectName("categoriesTable")
        self.categoriesTable.setColumnCount(0)
        self.categoriesTable.setRowCount(0)
        self.gridLayout.addWidget(self.categoriesTable, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.categoriesLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Категории</p></body></html>"))
