# Form implementation generated from reading ui file 'eventWidget.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(533, 95)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.event = QtWidgets.QLabel(parent=Form)
        self.event.setText("")
        self.event.setObjectName("event")
        self.horizontalLayout.addWidget(self.event)
        self.eventsMoreInfoButton = QtWidgets.QPushButton(parent=Form)
        self.eventsMoreInfoButton.setObjectName("eventsMoreInfoButton")
        self.horizontalLayout.addWidget(self.eventsMoreInfoButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.eventsMoreInfoButton.setText(_translate("Form", "Подробнее"))
