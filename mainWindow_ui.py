# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(575, 688)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tasksTab = QtWidgets.QWidget()
        self.tasksTab.setObjectName("tasksTab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tasksTab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.editCategoryButtonInTasks = QtWidgets.QPushButton(parent=self.tasksTab)
        self.editCategoryButtonInTasks.setObjectName("editCategoryButtonInTasks")
        self.gridLayout_3.addWidget(self.editCategoryButtonInTasks, 0, 3, 1, 2)
        self.categoriesInTasks = QtWidgets.QComboBox(parent=self.tasksTab)
        self.categoriesInTasks.setObjectName("categoriesInTasks")
        self.gridLayout_3.addWidget(self.categoriesInTasks, 0, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(parent=self.tasksTab)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.filterTasksButton = QtWidgets.QPushButton(parent=self.tasksTab)
        self.filterTasksButton.setObjectName("filterTasksButton")
        self.gridLayout_3.addWidget(self.filterTasksButton, 2, 0, 1, 5)
        self.tasksTable = QtWidgets.QTableWidget(parent=self.tasksTab)
        self.tasksTable.setObjectName("TasksTable")
        self.tasksTable.setColumnCount(0)
        self.tasksTable.setRowCount(0)
        self.gridLayout_3.addWidget(self.tasksTable, 3, 0, 1, 5)
        self.tabWidget.addTab(self.tasksTab, "")
        self.eventsTab = QtWidgets.QWidget()
        self.eventsTab.setObjectName("eventsTab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.eventsTab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.eventsTable = QtWidgets.QTableWidget(parent=self.eventsTab)
        self.eventsTable.setObjectName("eventsTable")
        self.eventsTable.setColumnCount(0)
        self.eventsTable.setRowCount(0)
        self.gridLayout_2.addWidget(self.eventsTable, 7, 0, 1, 5)
        self.editCategoryButtonInEvents = QtWidgets.QPushButton(parent=self.eventsTab)
        self.editCategoryButtonInEvents.setObjectName("editCategoryButtonInEvents")
        self.gridLayout_2.addWidget(self.editCategoryButtonInEvents, 0, 3, 1, 2)
        self.filterEventsButton = QtWidgets.QPushButton(parent=self.eventsTab)
        self.filterEventsButton.setObjectName("filterEventsButton")
        self.gridLayout_2.addWidget(self.filterEventsButton, 1, 0, 1, 5)
        self.categoriesInEvents = QtWidgets.QComboBox(parent=self.eventsTab)
        self.categoriesInEvents.setObjectName("categoriesInEvents")
        self.gridLayout_2.addWidget(self.categoriesInEvents, 0, 1, 1, 2)
        self.label = QtWidgets.QLabel(parent=self.eventsTab)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.tabWidget.addTab(self.eventsTab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.editCategoryButtonInTasks.setText(_translate("MainWindow", "Редактировать категории"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\">Категория</p></body></html>"))
        self.filterTasksButton.setText(_translate("MainWindow", "Фильтровать"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tasksTab), _translate("MainWindow", "Задачи"))
        self.editCategoryButtonInEvents.setText(_translate("MainWindow", "Редактировать категории"))
        self.filterEventsButton.setText(_translate("MainWindow", "Фильтровать"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\">Категория</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.eventsTab), _translate("MainWindow", "События"))
