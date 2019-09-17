# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'blackjackBotMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 601)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_pause = QtWidgets.QToolButton(self.centralwidget)
        self.btn_pause.setObjectName("btn_pause")
        self.horizontalLayout.addWidget(self.btn_pause)
        self.btn_step = QtWidgets.QToolButton(self.centralwidget)
        self.btn_step.setObjectName("btn_step")
        self.horizontalLayout.addWidget(self.btn_step)
        self.btn_step_round = QtWidgets.QToolButton(self.centralwidget)
        self.btn_step_round.setObjectName("btn_step_round")
        self.horizontalLayout.addWidget(self.btn_step_round)
        self.btn_play = QtWidgets.QToolButton(self.centralwidget)
        self.btn_play.setObjectName("btn_play")
        self.horizontalLayout.addWidget(self.btn_play)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.hlayout_dealers_hand = QtWidgets.QHBoxLayout()
        self.hlayout_dealers_hand.setObjectName("hlayout_dealers_hand")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hlayout_dealers_hand.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.hlayout_dealers_hand)
        self.hlayout_players_hand = QtWidgets.QHBoxLayout()
        self.hlayout_players_hand.setObjectName("hlayout_players_hand")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hlayout_players_hand.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.hlayout_players_hand)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 25)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_2.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.form_data_0 = QtWidgets.QFormLayout()
        self.form_data_0.setObjectName("form_data_0")
        self.label_winners = QtWidgets.QLabel(self.centralwidget)
        self.label_winners.setObjectName("label_winners")
        self.form_data_0.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_winners)
        self.print_winners = QtWidgets.QLabel(self.centralwidget)
        self.print_winners.setObjectName("print_winners")
        self.form_data_0.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.print_winners)
        self.label_loosers = QtWidgets.QLabel(self.centralwidget)
        self.label_loosers.setObjectName("label_loosers")
        self.form_data_0.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_loosers)
        self.print_loosers = QtWidgets.QLabel(self.centralwidget)
        self.print_loosers.setObjectName("print_loosers")
        self.form_data_0.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.print_loosers)
        self.label_busters = QtWidgets.QLabel(self.centralwidget)
        self.label_busters.setObjectName("label_busters")
        self.form_data_0.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_busters)
        self.print_busters = QtWidgets.QLabel(self.centralwidget)
        self.print_busters.setObjectName("print_busters")
        self.form_data_0.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.print_busters)
        self.horizontalLayout_3.addLayout(self.form_data_0)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_3.addWidget(self.line)
        self.form_data_1 = QtWidgets.QFormLayout()
        self.form_data_1.setObjectName("form_data_1")
        self.label_tb = QtWidgets.QLabel(self.centralwidget)
        self.label_tb.setObjectName("label_tb")
        self.form_data_1.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_tb)
        self.print_tb = QtWidgets.QLabel(self.centralwidget)
        self.print_tb.setObjectName("print_tb")
        self.form_data_1.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.print_tb)
        self.horizontalLayout_3.addLayout(self.form_data_1)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_3.addWidget(self.line_2)
        self.form_data_2 = QtWidgets.QFormLayout()
        self.form_data_2.setObjectName("form_data_2")
        self.label_best_money = QtWidgets.QLabel(self.centralwidget)
        self.label_best_money.setObjectName("label_best_money")
        self.form_data_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_best_money)
        self.print_best_money = QtWidgets.QLabel(self.centralwidget)
        self.print_best_money.setObjectName("print_best_money")
        self.form_data_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.print_best_money)
        self.horizontalLayout_3.addLayout(self.form_data_2)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Blackjack Bot"))
        self.btn_pause.setText(_translate("MainWindow", "Pause"))
        self.btn_step.setText(_translate("MainWindow", "Step"))
        self.btn_step_round.setText(_translate("MainWindow", "Finish Game"))
        self.btn_play.setText(_translate("MainWindow", "Play"))
        self.label.setText(_translate("MainWindow", "Bots"))
        self.label_winners.setText(_translate("MainWindow", "Winners"))
        self.print_winners.setText(_translate("MainWindow", "TextLabel"))
        self.label_loosers.setText(_translate("MainWindow", "Loosers"))
        self.print_loosers.setText(_translate("MainWindow", "TextLabel"))
        self.label_busters.setText(_translate("MainWindow", "Busters"))
        self.print_busters.setText(_translate("MainWindow", "TextLabel"))
        self.label_tb.setText(_translate("MainWindow", "t/b"))
        self.print_tb.setText(_translate("MainWindow", "TextLabel"))
        self.label_best_money.setText(_translate("MainWindow", "Best Money"))
        self.print_best_money.setText(_translate("MainWindow", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
