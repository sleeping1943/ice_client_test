# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Window(object):
    def setupUi(self, Window):
        Window.setObjectName("Window")
        Window.resize(1115, 843)
        Window.setAcceptDrops(True)
        Window.setAutoFillBackground(False)
        self.widget_more = QtWidgets.QWidget(Window)
        self.widget_more.setGeometry(QtCore.QRect(10, 870, 1081, 31))
        self.widget_more.setObjectName("widget_more")
        self.btn_more = QtWidgets.QPushButton(self.widget_more)
        self.btn_more.setGeometry(QtCore.QRect(480, 20, 75, 23))
        self.btn_more.setObjectName("btn_more")
        self.widget_main = QtWidgets.QWidget(Window)
        self.widget_main.setGeometry(QtCore.QRect(10, 20, 1091, 811))
        self.widget_main.setObjectName("widget_main")
        self.btn_invoke = QtWidgets.QPushButton(self.widget_main)
        self.btn_invoke.setGeometry(QtCore.QRect(1000, 770, 75, 23))
        self.btn_invoke.setObjectName("btn_invoke")
        self.btn_test_invoke = QtWidgets.QPushButton(self.widget_main)
        self.btn_test_invoke.setEnabled(True)
        self.btn_test_invoke.setGeometry(QtCore.QRect(760, 770, 75, 23))
        self.btn_test_invoke.setObjectName("btn_test_invoke")
        self.te_now = QtWidgets.QLabel(self.widget_main)
        self.te_now.setGeometry(QtCore.QRect(20, 770, 971, 21))
        self.te_now.setObjectName("te_now")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.widget_main)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 140, 1061, 611))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.text_params = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.text_params.setObjectName("text_params")
        self.verticalLayout_2.addWidget(self.text_params)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.text_result = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.text_result.setObjectName("text_result")
        self.verticalLayout_2.addWidget(self.text_result)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.func_params = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.func_params.setObjectName("func_params")
        self.horizontalLayout.addWidget(self.func_params)
        self.label_5 = QtWidgets.QLabel(self.widget_main)
        self.label_5.setGeometry(QtCore.QRect(10, 110, 71, 20))
        self.label_5.setObjectName("label_5")
        self.label_4 = QtWidgets.QLabel(self.widget_main)
        self.label_4.setGeometry(QtCore.QRect(530, 110, 71, 20))
        self.label_4.setObjectName("label_4")
        self.font_size = QtWidgets.QLabel(self.widget_main)
        self.font_size.setGeometry(QtCore.QRect(720, 20, 61, 21))
        self.font_size.setObjectName("font_size")
        self.label_ip = QtWidgets.QLabel(self.widget_main)
        self.label_ip.setGeometry(QtCore.QRect(30, 20, 31, 16))
        self.label_ip.setObjectName("label_ip")
        self.label_func = QtWidgets.QLabel(self.widget_main)
        self.label_func.setGeometry(QtCore.QRect(10, 70, 41, 16))
        self.label_func.setObjectName("label_func")
        self.lineEdit_ip = QtWidgets.QLineEdit(self.widget_main)
        self.lineEdit_ip.setGeometry(QtCore.QRect(60, 20, 161, 20))
        self.lineEdit_ip.setObjectName("lineEdit_ip")
        self.label_3 = QtWidgets.QLabel(self.widget_main)
        self.label_3.setGeometry(QtCore.QRect(670, 70, 71, 21))
        self.label_3.setObjectName("label_3")
        self.lineEdit_func = QtWidgets.QLineEdit(self.widget_main)
        self.lineEdit_func.setGeometry(QtCore.QRect(60, 70, 161, 20))
        self.lineEdit_func.setObjectName("lineEdit_func")
        self.comboBox = QtWidgets.QComboBox(self.widget_main)
        self.comboBox.setGeometry(QtCore.QRect(320, 70, 331, 22))
        self.comboBox.setObjectName("comboBox")
        self.label_port = QtWidgets.QLabel(self.widget_main)
        self.label_port.setGeometry(QtCore.QRect(300, 20, 41, 16))
        self.label_port.setObjectName("label_port")
        self.label_flag = QtWidgets.QLabel(self.widget_main)
        self.label_flag.setGeometry(QtCore.QRect(490, 20, 81, 20))
        self.label_flag.setObjectName("label_flag")
        self.lineEdit_flag = QtWidgets.QLineEdit(self.widget_main)
        self.lineEdit_flag.setGeometry(QtCore.QRect(570, 20, 113, 20))
        self.lineEdit_flag.setObjectName("lineEdit_flag")
        self.label = QtWidgets.QLabel(self.widget_main)
        self.label.setGeometry(QtCore.QRect(260, 70, 54, 21))
        self.label.setObjectName("label")
        self.font_box = QtWidgets.QSpinBox(self.widget_main)
        self.font_box.setGeometry(QtCore.QRect(800, 20, 51, 22))
        self.font_box.setObjectName("font_box")
        self.cb_func_total = QtWidgets.QComboBox(self.widget_main)
        self.cb_func_total.setGeometry(QtCore.QRect(740, 70, 331, 22))
        self.cb_func_total.setObjectName("cb_func_total")
        self.lineEdit_port = QtWidgets.QLineEdit(self.widget_main)
        self.lineEdit_port.setGeometry(QtCore.QRect(330, 20, 101, 20))
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.theme_box = QtWidgets.QGroupBox(self.widget_main)
        self.theme_box.setGeometry(QtCore.QRect(890, 10, 141, 41))
        self.theme_box.setObjectName("theme_box")
        self.theme_dark = QtWidgets.QRadioButton(self.theme_box)
        self.theme_dark.setGeometry(QtCore.QRect(10, 20, 49, 16))
        self.theme_dark.setObjectName("theme_dark")
        self.theme_light = QtWidgets.QRadioButton(self.theme_box)
        self.theme_light.setGeometry(QtCore.QRect(70, 20, 51, 16))
        self.theme_light.setObjectName("theme_light")

        self.retranslateUi(Window)
        QtCore.QMetaObject.connectSlotsByName(Window)

    def retranslateUi(self, Window):
        _translate = QtCore.QCoreApplication.translate
        Window.setWindowTitle(_translate("Window", "Ice测试"))
        self.btn_more.setText(_translate("Window", "more"))
        self.btn_invoke.setText(_translate("Window", "调用"))
        self.btn_test_invoke.setText(_translate("Window", "测试invoke"))
        self.te_now.setText(_translate("Window", "TextLabel"))
        self.label_2.setText(_translate("Window", "调用返回:"))
        self.label_5.setText(_translate("Window", "函数参数:"))
        self.label_4.setText(_translate("Window", "函数说明:"))
        self.font_size.setText(_translate("Window", "文字大小:"))
        self.label_ip.setText(_translate("Window", "IP:"))
        self.label_func.setText(_translate("Window", "函数名:"))
        self.label_3.setText(_translate("Window", "文件中函数:"))
        self.label_port.setText(_translate("Window", "port:"))
        self.label_flag.setText(_translate("Window", "Ice对象flag:"))
        self.label.setText(_translate("Window", "最近调用:"))
        self.theme_box.setTitle(_translate("Window", "主题"))
        self.theme_dark.setText(_translate("Window", "黑暗"))
        self.theme_light.setText(_translate("Window", "明亮"))
