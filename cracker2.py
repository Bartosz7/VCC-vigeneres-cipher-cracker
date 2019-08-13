# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'cracker2.ui'
# Created by: PyQt5 UI code generator 5.12.1
# WARNING! All changes made in this file will be lost!
# SPECIAL THANKS TO: stackoverflow user: https://stackoverflow.com/users/840947/heike
# for fixing my gui communication problem
#########################################LIBRARIES########################################
import os, traceback, sys, time, string
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from datetime import datetime, timedelta
from collections import Counter, OrderedDict
from funcs import divisors, GCD, find_distance, transformer
from itertools import product
import time # for TESTING only
#########################################CONSTANTS############################################

# Language and version
version = "1.9.0."
app_language = "English"

# Local time / Start time of format: day-month-year hour-minute-second
time_local = time.strftime("%d-%m-%Y %H-%M-%S ", time.localtime())

# Alphabets
alphabet_capital_eng = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"     # English Capital Alphabet
alphabet_lowercase_eng = alphabet_capital_eng.lower()   # English Small Letters
digits = "0123456789"                                   # Digits
punctuation_marks = ",.?!()[]{}:;-"                     # Punctuation marks

# statistical percentage of use of chars in Polish
# according to https://pl.wikipedia.org/wiki/Alfabet_polski
char_stats_pol = [0.0891, 0.0099, 0.0147, 0.0396, 0.0040, 0.0325, 0.0766,# A Ą B C Ć D E
                  0.0111, 0.0030, 0.0142, 0.0108, 0.0821, 0.0228, 0.0351,# Ę F G H I J K
                  0.0210, 0.0182, 0.0280, 0.0552, 0.0020, 0.0775, 0.0085,# L Ł M N Ń O Ó
                  0.0313, 0.0014, 0.0469, 0.0432, 0.0066, 0.0398, 0.0250,# P Q R S Ś T U
                  0.0004, 0.0465, 0.0002, 0.0376, 0.0564, 0.0006, 0.0083]# V W X Y Z Ź Ż

# statistical percentage of use of chars in English
# according to Wikipedia: https://en.wikipedia.org/wiki/Letter_frequency
char_stats_eng = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228,  # A B C D E F
                  0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025,  # G H I J K L
                  0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987,  # M N O P Q R
                  0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,  # S T U V W X
                  0.01974, 0.00074]                                      # Y Z

###################################GUI AND MAIN CLASS####################################

class Ui_MainWindow(object):
    """
        GUI Main Operation: setupUi; retranslateUi
        Main Process after start: start_cracking; then:
            1. create_table <-- subfind
            2. decrypt <-- crack_mono
            3. decoder
        Functions for GUI instant signals
            1. open_text
            2. save_text
            3. change_font_size
    """
    def setupUi(self, MainWindow):

        # MainWindow properties
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(680, 417)
        MainWindow.setMinimumSize(QtCore.QSize(680, 417))
        MainWindow.setMaximumSize(QtCore.QSize(680, 417))
        MainWindow.setWindowTitle("Vigenere's Cipher Cracker")

        # Icon and window title
        icon = QtGui.QIcon ("wasp.png")
        MainWindow.setWindowIcon (icon)
        MainWindow.setWindowTitle ("VCC Vigenere's Cipher Cracker v.1.8.0")

        # Main GUI look
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 16))
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 30, 401, 321))
        self.textBrowser.setReadOnly(False)
        self.textBrowser.setOverwriteMode(False)
        self.textBrowser.setObjectName("textBrowser")
        self.groupBox_Control_Panel = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Control_Panel.setGeometry(QtCore.QRect(420, 20, 251, 331))
        self.groupBox_Control_Panel.setObjectName("groupBox_Control_Panel")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_Control_Panel)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 10, 251, 324))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, -1, 10, -1)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_open = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btn_open.setObjectName("btn_open")
        self.horizontalLayout_2.addWidget(self.btn_open)
        self.btn_save = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout_2.addWidget(self.btn_save)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(10, 0, 10, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.formLayout.setItem(0, QtWidgets.QFormLayout.FieldRole, spacerItem)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.comboBox_lang = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.comboBox_lang.setObjectName("comboBox_lang")
        self.comboBox_lang.addItem("")
        self.comboBox_lang.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox_lang)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.comboBox_method = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.comboBox_method.setObjectName("comboBox_method")
        self.comboBox_method.addItem("")
        self.comboBox_method.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_method)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.formLayout.setItem(3, QtWidgets.QFormLayout.LabelRole, spacerItem1)
        self.checkBox_skip = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox_skip.setObjectName("checkBox_skip")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.checkBox_skip)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.formLayout.setItem(4, QtWidgets.QFormLayout.LabelRole, spacerItem2)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setHorizontalSpacing(10)
        self.formLayout_2.setVerticalSpacing(6)
        self.formLayout_2.setObjectName("formLayout_2")
        self.spinBox = QtWidgets.QSpinBox(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy)
        self.spinBox.setMinimumSize(QtCore.QSize(50, 0))
        self.spinBox.setMaximumSize(QtCore.QSize(75, 16777215))
        self.spinBox.setMinimum(2)
        self.spinBox.setProperty("value", 3)
        self.spinBox.setObjectName("spinBox")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.spinBox)
        self.spinBox_2 = QtWidgets.QSpinBox(self.verticalLayoutWidget_2)
        self.spinBox_2.setMinimumSize(QtCore.QSize(50, 0))
        self.spinBox_2.setMaximumSize(QtCore.QSize(75, 16777215))
        self.spinBox_2.setMinimum(2)
        self.spinBox_2.setObjectName("spinBox_2")
        self.spinBox_3 = QtWidgets.QSpinBox(self.verticalLayoutWidget_2)
        self.spinBox_3.setMinimumSize(QtCore.QSize(50,0))
        self.spinBox_3.setMaximumSize(QtCore.QSize(75, 16777215))
        self.spinBox_3.setMinimum(3)
        self.spinBox_3.setMaximum(20)
        self.spinBox_3.setObjectName("spinBox_3")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.spinBox_2)
        self.formLayout_2.setWidget (2, QtWidgets.QFormLayout.LabelRole, self.spinBox_3)
        self.spin_label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.spin_label_3.setObjectName("spin_label_3")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spin_label_3)
        self.spin_label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.spin_label_2.setObjectName("spin_label_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spin_label_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout_2.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.verticalLayout_3)
        self.spin_label_1 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.spin_label_1.setObjectName("spin_label_1")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spin_label_1)
        self.formLayout.setLayout(4, QtWidgets.QFormLayout.FieldRole, self.formLayout_2)
        self.verticalLayout.addLayout(self.formLayout)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.btn_start = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btn_start.setObjectName("btn_start")
        self.horizontalLayout.addWidget(self.btn_start)
        spacerItem4 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.progressbar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressbar.setGeometry(QtCore.QRect(10, 360, 661, 16))
        self.progressbar.setProperty("value", 0)
        self.progressbar.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.progressbar.setTextVisible(False)
        self.progressbar.setObjectName("progressbar")
        self.progress_label = QtWidgets.QLabel(self.centralwidget)
        self.progress_label.setGeometry(QtCore.QRect(10, 360, 661, 16))
        self.progress_label.setText("")
        self.progress_label.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_label.setObjectName("progress_label")
        self.btn_clear = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clear.setGeometry(QtCore.QRect(340, 10, 71, 20))
        self.btn_clear.setAutoDefault(False)
        self.btn_clear.setObjectName("btn_clear")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(160, 10, 176, 21))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_fs = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_fs.setObjectName("label_fs")
        self.gridLayout.addWidget(self.label_fs, 0, 0, 1, 1)
        self.slider = QtWidgets.QSlider(self.gridLayoutWidget)
        self.slider.setMinimum(10)
        self.slider.setMaximum(42)
        self.slider.setMinimumSize(QtCore.QSize(85, 0))
        self.slider.setMaximumSize(QtCore.QSize(50, 15))
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.gridLayout.addWidget(self.slider, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 680, 21))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionGuide_to_Vigenere_s_Cipher = QtWidgets.QAction(MainWindow)
        self.actionGuide_to_Vigenere_s_Cipher.setObjectName("actionGuide_to_Vigenere_s_Cipher")
        self.actionAuthor_License = QtWidgets.QAction(MainWindow)
        self.actionAuthor_License.setObjectName("actionAuthor_License")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuHelp.addAction(self.actionGuide_to_Vigenere_s_Cipher)
        self.menuHelp.addAction(self.actionAuthor_License)
        self.menuHelp.addAction(self.actionExit)
        self.menubar.addAction(self.menuHelp.menuAction())

        # Hiding progress bar
        self.progress_label.hide()
        self.progressbar.hide()

        # Retranslation and connecting SIGNALS
        self.retranslateUi(MainWindow)
        self.checkBox_skip.toggled['bool'].connect(self.spin_label_2.setHidden)
        self.checkBox_skip.toggled['bool'].connect(self.spinBox.setHidden)
        self.checkBox_skip.toggled['bool'].connect(self.spinBox_2.setHidden)
        self.checkBox_skip.toggled['bool'].connect(self.spin_label_1.setHidden)
        self.checkBox_skip.toggled['bool'].connect(self.spinBox_3.setHidden)
        self.checkBox_skip.toggled['bool'].connect(self.spin_label_3.setHidden)
        self.actionExit.triggered['bool'].connect(MainWindow.close)
        self.actionExit.triggered.connect(MainWindow.close)
        self.btn_start.clicked.connect(self.start_cracking)
        self.btn_save.clicked.connect(self.save_text)
        self.btn_open.clicked.connect(self.open_text)
        self.btn_clear.clicked.connect(self.textBrowser.clear)
        self.slider.valueChanged.connect(self.change_font_size)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "VCC 1.9.0. by Bartosz Grabek "))
        self.label.setText(_translate("MainWindow", "Ciphergram:"))
        self.groupBox_Control_Panel.setTitle(_translate("MainWindow", "Control Panel"))
        self.btn_open.setText(_translate("MainWindow", "Open"))
        self.btn_save.setText(_translate("MainWindow", "Save"))
        self.label_3.setText(_translate("MainWindow", "Settings:"))
        self.label_2.setText(_translate("MainWindow", "Language"))
        self.comboBox_lang.setItemText(0, _translate("MainWindow", "English"))
        self.comboBox_lang.setItemText(1, _translate("MainWindow", "Polish"))
        self.label_4.setText(_translate("MainWindow", "Method"))
        self.comboBox_method.setItemText(0, _translate("MainWindow", "Statistic (one key, simple)"))
        self.comboBox_method.setItemText(1, _translate("MainWindow", "Statistic (multiple keys)"))
        self.checkBox_skip.setText(_translate("MainWindow", "Skip key length search"))
        self.spin_label_3.setText(_translate("MainWindow", "Suggestions"))
        self.spin_label_3.setToolTip(_translate("MainWindow", "# number of suggestions of password lengths"))
        self.spin_label_2.setToolTip(_translate("MainWindow", "# minimal number of appearings of repeating fragments to find"))
        self.spin_label_2.setText(_translate("MainWindow", "MIN_CNT"))
        self.spin_label_1.setToolTip(_translate("MainWindow", "# minimal length of repeating fragments to find"))
        self.spin_label_1.setText(_translate("MainWindow", "MIN_LEN"))
        self.btn_start.setText(_translate("MainWindow", "Crack"))
        self.btn_clear.setText(_translate("MainWindow", "Clear"))
        self.label_fs.setText(_translate("MainWindow", "Font size:  10 "))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionGuide_to_Vigenere_s_Cipher.setText(_translate("MainWindow", "Guide to Vigenere\'s Cipher"))
        self.actionAuthor_License.setText(_translate("MainWindow", "Author/License"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Esc"))

    def start_cracking(self):

        # TODO: add option Handling large texts --> by dividing into smaller pieces

        # Disabling input
        self.textBrowser.setDisabled(True)
        self.btn_open.setDisabled(True)
        self.btn_save.setDisabled(True)
        self.btn_start.setDisabled(True)
        self.spinBox.setDisabled(True)
        self.spinBox_2.setDisabled(True)
        self.btn_clear.setDisabled(True)
        self.slider.setDisabled(True)
        self.label_fs.setDisabled(True)
        self.comboBox_lang.setDisabled(True)
        self.comboBox_method.setDisabled(True)
        self.checkBox_skip.setDisabled(True)
        self.spinBox_3.setDisabled(True)
        self.spin_label_1.setDisabled(True)
        self.spin_label_2.setDisabled(True)
        self.spin_label_3.setDisabled(True)

        # Set progressbar
        self.progressbar.show()
        self.progress_label.show()
        self.progress_label.setText("Cracking...")

        # Get inputed options
        MINLEN = self.spinBox.value()               # minimal length of repeating fragments
        MINCNT = self.spinBox_2.value()             # minimal number of appearings of repeating fragments
        mode = self.comboBox_method.currentIndex()  # 0: one key - auto, 1: advanced panel: multi-key
        language = self.comboBox_lang.currentText() # English / Polish
        skip = self.checkBox_skip.isChecked()       # skip key length search
        suggestions = self.spinBox_3.value()        # how many key length to suggest

        # Get text for analysis
        ciphergram = self.textBrowser.toPlainText ()

        # TESTING
        print("MINLEN: " + str(MINLEN) +"\nMINCNT: " + str(MINCNT) + "\nkey_mode: "
              + str(mode) + "\nlang: " + str(language) + "\nskip: " + str(skip))

        # Ciphergram preprocessing: making text uppercase and only letters
        # eg. "Today is Sunday!" --> "TODAYISSUNDAY"
        new_ciphergram = ""
        for el in ciphergram.upper():
            if el in alphabet_capital_eng:
                new_ciphergram += el

        # OPTION handling
        try:
            # one key mode (index: 0)
            if mode == 0:

                message_text = ""

                if skip == False:
                    # DO key_len search
                    # Returns a dict with repeating fragments and number of their appearings
                    repeat_result = self.subfind(new_ciphergram, MINLEN, MINCNT)
                    message_text = self.create_table(new_ciphergram, repeat_result, suggestions)
                    if message_text == 0: #if an error occured
                        self.reset_gui()
                        return

                # skipping key_len search
                # TODO: check for valid input / make input mask only digits, positive
                dialog = QtWidgets.QInputDialog(MainWindow)
                key_length, ok = dialog.getInt(MainWindow, 'Probable key length: ', message_text)

                # Real cracking: statistical analysis using least-squares method
                # decoder -> mono_crack --> password char by char
                key_word = self.decoder(key_length, new_ciphergram, mode)

                # Decoding whole text using cracked password
                if mode == 0:
                    try:
                        new_text = "Password: " + str (key_word) + "\n"
                        new_text += self.decrypt(ciphergram, key_word)
                        self.textBrowser.setText(new_text)
                        MainWindow.showMaximized()

                    except Exception as e:
                        print (e)

            # multi key mode (index: 1) / Advanced Panel
            else:
                if skip == False:
                    repeat_result = self.subfind(new_ciphergram, MINLEN, MINCNT)
                else:
                    None
                self.Form = QtWidgets.QWidget()
                ui = Ui_Form()
                ui.setupUi(self.Form)
                ui.create_table_2(ciphergram=new_ciphergram, repeat_result=repeat_result, suggestions=suggestions)
                self.Form.show()

        except Exception as e:
            print(e)

        self.reset_gui()
        #return

    def create_table(self, ciphergram: str, repeat_result: dict, suggestions: int):
        """

        :param ciphergram: ciphered text
        :param repeat_result: result of subfind
        :return: create calculation table, Dialog for key input and return key_length imput
        """

        # Basics
        new_ciphergram = ciphergram
        repeat_keys = list(repeat_result.keys())  # list of repeating fragments
        repeat_values = list(repeat_result.values())  # list of their appearings

        # Creating a Table - basic, headers and first 3 columns
        try:
            self.tableWidget = QTableWidget()
            self.tableWidget.setWindowTitle("TABLE")
            self.tableWidget.setRowCount(int(len(repeat_keys)))
            self.tableWidget.setColumnCount(10000)  # column count option?
            self.tableWidget.setHorizontalHeaderLabels(["Name", "Length", "Appearings"])
            self.tableWidget.setColumnWidth(0, 100)
            self.tableWidget.setColumnWidth(1, 50)
            self.tableWidget.setColumnWidth(2, 80)

            # Setting first three columns name:length:number_of_appearings
            for X in range(int(len(repeat_keys))):
                list_1 = find_distance(new_ciphergram, repeat_keys[X], repeat_values[X] - 1)
                if X == 0:
                    max_list_1_length = len(list_1)
                else:
                    if len(list_1) > max_list_1_length:
                        max_list_1_length = int(len(list_1))
                self.tableWidget.setItem(X, 0, QTableWidgetItem(str(repeat_keys[X])))
                self.tableWidget.setItem(X, 1, QTableWidgetItem(str(len(repeat_keys[X]))))
                self.tableWidget.setItem(X, 2, QTableWidgetItem(str(repeat_values[X])))
                for Y in range(len(list_1)):
                    self.tableWidget.setItem(X, Y + 3, QTableWidgetItem(str(list_1[Y])))

            # Creating place for GCD column
            max_list_1_length += 3
            self.tableWidget.setHorizontalHeaderItem(max_list_1_length, QTableWidgetItem ("GCD"))
            self.tableWidget.setColumnWidth(max_list_1_length, 50)

            # Setting factor columns
            for i in range(3, max_list_1_length):
                self.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem("Factors"))
                self.tableWidget.setColumnWidth(i, 50)

            # Calculating GCDs for each row and divisors for each row's GCD
            for row in range(0, len(repeat_keys)):
                list_2 = []
                for col in range(3, max_list_1_length):
                    try:
                        item = self.tableWidget.item (row, col).text()
                        item = int(item)
                        list_2.append(item)
                    except Exception as e:
                        item = None
                row_gcd = GCD(list_2)
                self.tableWidget.setItem(row, max_list_1_length, QTableWidgetItem(str(row_gcd)))
                self.tableWidget.setColumnWidth(max_list_1_length + 1, 500)
                self.tableWidget.setHorizontalHeaderItem(max_list_1_length + 1, QTableWidgetItem("Divisors"))

            # List for storing ALL divisors
            list_of_divisors = []
            for i in range(len(repeat_keys)):
                x = self.tableWidget.item(i, max_list_1_length).text()
                x = int(x)
                s = ""
                for el in divisors(x):
                    if int(el) != 1:
                        s += str(el) + " "
                        list_of_divisors.append(el)
                self.tableWidget.setItem(i, max_list_1_length + 1, QTableWidgetItem(s))

            # Saving memory space
            del s, x, row_gcd

            # Counting divisors and sorting from largest number of appearings to smallest
            x = Counter(list_of_divisors)
            x = sorted(x.items(), key=lambda x: x[1], reverse=True)

            # Message to give probable key length values
            message_text = ""
            message_text = "Programme suggests " +str(suggestions) +" most probable values of key length: " + "\n"
            for i in range(suggestions):
                message_text += str(x[i][0])
                if i != suggestions-1:
                    message_text += ", "
            message_text += "\n\n" + "Remember: keys of length 3 or less are rarely chosen"
            return message_text

        except Exception as e:
            msgbox = QtWidgets.QMessageBox ()
            msgbox.setIcon(QtWidgets.QMessageBox.Warning)
            msgbox.setWindowTitle('WARNING')
            msgbox.setText('Unfortunately, there is too little information to crack the ciphergram')
            msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgbox.exec_()
            self.tableWidget.hide()
            return 0

    def subfind(self, text: str, MINLEN: int, MINCNT: int):
        """
        :param text: text to be researched
        :param MINLEN: minimum length of repeating fragments in the text
        :param MINCNT: minimum number of appearings of repeating fragments in the text
        :return: dictionary list of repeating fragments and their number of appearings
        """
        message = "Cracking"
        d = {}
        c = 0
        start_time = datetime.now()
        for sublen in range(MINLEN, int(len(text) / MINCNT)):
            for i in range(0, len(text) - sublen):
                QtWidgets.QApplication.processEvents ()
                sub = text[i:i + sublen]
                cnt = text.count(sub)
                if cnt >= MINCNT and sub not in d and (" " not in sub):
                    d[sub] = cnt
                now_time = datetime.now()
                if now_time > start_time + timedelta(seconds=1) and c >= 0:
                    message += "."
                    c += 1
                    start_time = now_time
                    if c == 4:
                        c = 0
                        message = "Cracking"
                self.progress_label.setText(message)
            progress = sublen/(int(len(text)/MINCNT))*100
            self.progressbar.setValue(progress)
        return d

    def decoder(self, key_length: int, ciphergram: str, key_mode: int):
        """

        :param key_length:
        :param ciphergram:
        :param key_mode:
        :return:
        """

        password = ''
        password_list = []
        probability_list = []

        for i in range(0, int(key_length)):
            what_to_crack = ""
            for i2 in range(i, int(len(ciphergram)), int(key_length)):
                    what_to_crack += ciphergram[i2]
            new1 = self.crack_mono(what_to_crack, key_mode)
            if key_mode == 0:
                password += new1
            else: # key_mode == 1
                password_list.append(new1[0])
                probability_list.append(new1[1])

        if key_mode == 0:
            return password

        # if key_mode == 1:
        try:
            password_list = list(product(*password_list))
            probability_list = list(product(*probability_list))
            new_probability_list = []
            for el in probability_list:
                p = 1
                for el2 in el:
                    p *= el2
                new_probability_list.append(p)

            new_password_list = []
            for el in password_list:
                try:
                    new_password_list.append(("".join(el)).lower())
                except:
                    None

            newer_password_list = []
            file = open("dict_eng.txt", "r")
            data = file.read()
            for el in new_password_list:
                if el in data:
                    print("ADDING")
                    newer_password_list.append(el)
                    QtWidgets.QApplication.processEvents()

            print("Possible combinations: "+str(len(new_password_list)))
            print("Possible passwords:    "+str(len(newer_password_list)))
            print(newer_password_list)

            brand_list = []
            for el in newer_password_list:
                brand_list.append(new_probability_list[newer_password_list.index(el)])
            brand_list = sorted(brand_list)

            s = ""
            for el in brand_list:
                s += str((newer_password_list[new_probability_list.index(el)], el))+"\n"

            # TODO: add a Dialog with option choice
            msgbox2 = QtWidgets.QMessageBox()
            msgbox2.setIcon(QtWidgets.QMessageBox.Information)
            msgbox2.setWindowTitle('INFO')
            msgbox2.setText(s)
            msgbox2.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgbox2.exec_()
            self.tableWidget.hide()
            return
            #msgBox.buttonClicked.connect(msgButtonClick)


        # TODO: make a dialog with all possibilities
        # 1. show possible passwords and their probability
        # 2. let choose one / or several / or all passwords / combinations WITH WARNING OF LONG PROCESS
        # 3. let to choose if the programme should check for us the text

        except Exception as e:
            print(e)

    def crack_mono(self, file, key_mode):
        """
        Cracks mono-alphabetical ciphers using method of cryptoanalytic statistical analisys
        Statistic function finds the key by comparing frequency of chars in ciphergram to frequency of letters
        in the language (stat_chats); monoalphabetical statistic cracker with the use of least-squares regression
        :param file: sub-ciphergram (cipher encrypted with one transformation value)
        :return: transformation value
        """
        frequency = []
        for letter in alphabet_capital_eng:
            counter = 0
            for el in file:
                if el == letter:
                    counter += 1
            frequency.append(round(counter/len(file), 4))
        difference = []
        results = []
        for el in range(0, 26):
            # machine adding order
            if el != 0:
                frequency = transformer(frequency)
            for el2 in range(0, 26):
                counter_2 = 0
                counter_2 = (char_stats_eng[el2] - frequency[el2]) ** 2
                counter_2 = round(counter_2, 4)
                difference.append(counter_2)
            wynik = 0
            for ok in range(26):
                wynik = wynik + difference[ok]
            results.append(round(wynik, 6))
            difference = []

        if key_mode == 0:
            # Sorting and calculating the smallest difference and nearest key
            # Finding best mono position transformation
            best_fit = (sorted(results))[0]
            best_fit = results.index(best_fit)
            # Decoding letter of key_word
            key_char = alphabet_capital_eng[(26 - best_fit) % 26]
            return key_char

        else: # key_mode == 1
            list_3 = []
            list_4 = []
            # TODO: 4 below to be changed to variable
            for el in sorted(results)[0:4]:
                list_4.append(el)
                list_3.append(alphabet_capital_eng[(26 - results.index(el)) % 26])
            return [list_3, list_4]

    def decrypt(self, text, password):
        """

        :param text: what to decrypt
        :param password: with what password
        :return: encoded text
        """
        try:
            s = text
            list_1 = [] # list_1 for result text

            # getting the key word
            key_word = password.lower()
            key_word_len = int(len(key_word))

            # num_space for preventing non-letters from being transcribed
            num_space = 0

            # boolean for controlling upper- and lowercase
            change = False

            for index in range(0, int(len(s))):

                # number in the ASCII table
                char_ascii = ord(s[index])

                # checking if the char is a small letter
                if (char_ascii >= 65 and char_ascii <= 90) or (char_ascii >= 97 and char_ascii <= 122):

                    # if capital letter
                    if char_ascii >= 65 and char_ascii <= 90:
                        # making capitals lowercase
                        char_ascii += 32
                        change = True

                    # attributing number of password transformations to positions of prime message
                    rest = int((index - num_space)% key_word_len)

                    #shift = (ord(key_word[rest]) - 97)
                    n = char_ascii - (ord(key_word[rest]) - 97)
                    # if it doesn't fit to the alphabet
                    if not (n >= 97 and n <= 122):
                        n = 96 - n
                        n = 122 - n

                    # checking if change to lowercase was executed and converting back to uppercase
                    if change == True:
                        n -= 32
                        change = False

                    # add new transformed char to the result list
                    list_1.append(str(chr(n)))

                # if char is not a letter
                else:
                    list_1.append(str(chr(char_ascii)))
                    num_space += 1

            # saving newly transcribed message
            # connecting succesive chars to form complete ciphergram
            ciphergram = "".join(list_1)
            return ciphergram

        except Exception as e:
            print(e)

    # Buttons and GUI instant signals
    def open_text(self):
        """

        :return: opens text of chosen directory
        """
        try:
            self.filename = QtWidgets.QFileDialog.getOpenFileName(None, 'Otwórz dokument', "Users\dggt\Desktop\Vigenere's Cipher v.2.0", "*.txt;*.rtf")
            if self.filename != None:
                f = open(self.filename[0], 'r')  # New line
                data = f.read()
                f.close()

            self.textBrowser.clear()
            self.textBrowser.insertPlainText(data)
        except Exception as e:
            None

    def save_text(self):
        """

        :return: save text to chosen directory
        """
        try:
            data = self.textBrowser.toPlainText()
            name = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', ('.txt'))
            file = open(name[0] + ".txt", 'w')
            file.writelines(data)
            file.close()
        except Exception as e:
            None

    def change_font_size(self):
        """

        :return: changes instantly font size of text Browser in GUI
        """
        size = self.slider.value()
        copy = self.textBrowser.toPlainText()
        self.textBrowser.clear()
        self.textBrowser.setFontPointSize(size)
        self.textBrowser.setText(copy)
        self.label_fs.setText("Font size: "+str(size))

    def reset_gui(self):

        # Re-enabling input
        self.textBrowser.setDisabled(False)
        self.btn_open.setDisabled(False)
        self.btn_save.setDisabled(False)
        self.btn_start.setDisabled(False)
        self.spinBox.setDisabled(False)
        self.spinBox_2.setDisabled(False)
        self.btn_clear.setDisabled(False)
        self.checkBox_skip.setDisabled(False)
        self.slider.setDisabled(False)
        self.label_fs.setDisabled(False)
        self.comboBox_lang.setDisabled(False)
        self.comboBox_method.setDisabled(False)
        self.spinBox_3.setDisabled(False)
        self.spin_label_1.setDisabled(False)
        self.spin_label_2.setDisabled(False)
        self.spin_label_3.setDisabled(False)

        # Closing progressbar
        self.progressbar.hide()
        self.progress_label.clear()
        return

class Ui_Form(Ui_MainWindow):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(961, 418)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(540, 10, 411, 71))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(5, 0, 5, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line_3 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(540, 90, 181, 191))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.listwidget_lengths = QtWidgets.QListWidget(self.verticalLayoutWidget_2)
        self.listwidget_lengths.setObjectName("listwidget_lengths")
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.listwidget_lengths.addItem(item)
        self.verticalLayout_2.addWidget(self.listwidget_lengths)
        self.checkbox_use_dict = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.checkbox_use_dict.setChecked(True)
        self.checkbox_use_dict.setObjectName("checkbox_use_dict")
        self.verticalLayout_2.addWidget(self.checkbox_use_dict)
        self.btn_get_passwords = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btn_get_passwords.setObjectName("btn_get_passwords")
        self.verticalLayout_2.addWidget(self.btn_get_passwords)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(740, 90, 211, 301))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_3.setEnabled(False)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.list_passwords = QtWidgets.QListWidget(self.verticalLayoutWidget_3)
        self.list_passwords.setEnabled(False)
        self.list_passwords.setObjectName("list_passwords")
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.list_passwords.addItem(item)
        self.verticalLayout_3.addWidget(self.list_passwords)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_7.setEnabled(False)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_6.addWidget(self.label_7)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radiobtn_auto = QtWidgets.QRadioButton(self.verticalLayoutWidget_3)
        self.radiobtn_auto.setEnabled(False)
        self.radiobtn_auto.setChecked(True)
        self.radiobtn_auto.setObjectName("radiobtn_auto")
        self.horizontalLayout.addWidget(self.radiobtn_auto)
        self.radiobtn_manual = QtWidgets.QRadioButton(self.verticalLayoutWidget_3)
        self.radiobtn_manual.setEnabled(False)
        self.radiobtn_manual.setObjectName("radiobtn_manual")
        self.horizontalLayout.addWidget(self.radiobtn_manual)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_cancel = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.btn_cancel.setEnabled(False)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout_2.addWidget(self.btn_cancel)
        self.btn_check = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.btn_check.setEnabled(False)
        self.btn_check.setObjectName("btn_check")
        self.horizontalLayout_2.addWidget(self.btn_check)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_6)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 10, 371, 381))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.table_widget_calc = QtWidgets.QTableWidget(self.verticalLayoutWidget_4)
        self.table_widget_calc.setObjectName("table_widget_calc")
        self.table_widget_calc.setColumnCount(0)
        self.table_widget_calc.setRowCount(0)
        self.verticalLayout_4.addWidget(self.table_widget_calc)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(390, 10, 131, 381))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.table_widget_keys = QtWidgets.QTableWidget(self.verticalLayoutWidget_5)
        self.table_widget_keys.setObjectName("table_widget_keys")
        self.table_widget_keys.setColumnCount(0)
        self.table_widget_keys.setRowCount(0)
        self.verticalLayout_5.addWidget(self.table_widget_keys)
        #self.verticalLayoutWidget_7 = QtWidgets.QWidget(Form)
        #self.verticalLayoutWidget_7.setGeometry(QtCore.QRect(9, 11, 511, 381))
        #self.verticalLayoutWidget_7.setObjectName("verticalLayoutWidget_7")
        #self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_7)
        #self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        #self.verticalLayout_7.setObjectName("verticalLayout_7")
        #self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget_7)
        #self.label_8.setScaledContents(False)
        #self.label_8.setObjectName("label_8")
        #self.verticalLayout_7.addWidget(self.label_8)
        #self.textBrowser = QtWidgets.QTextBrowser(self.verticalLayoutWidget_7)
        #self.textBrowser.setEnabled(True)
        #self.textBrowser.setAcceptDrops(True)
        #self.textBrowser.setInputMethodHints(QtCore.Qt.ImhLatinOnly)
        #self.textBrowser.setUndoRedoEnabled(False)
        #self.textBrowser.setOpenLinks(True)
        #self.textBrowser.setObjectName("textBrowser")
        #self.verticalLayout_7.addWidget(self.textBrowser)
        self.verticalLayoutWidget_8 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_8.setGeometry(QtCore.QRect(540, 280, 181, 111))
        self.verticalLayoutWidget_8.setObjectName("verticalLayoutWidget_8")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_8)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget_8)
        self.label_9.setEnabled(False)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_8.addWidget(self.label_9)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_left = QtWidgets.QPushButton(self.verticalLayoutWidget_8)
        self.btn_left.setEnabled(False)
        self.btn_left.setObjectName("btn_left")
        self.horizontalLayout_3.addWidget(self.btn_left)
        self.btn_right = QtWidgets.QPushButton(self.verticalLayoutWidget_8)
        self.btn_right.setEnabled(False)
        self.btn_right.setObjectName("btn_right")
        self.horizontalLayout_3.addWidget(self.btn_right)
        self.verticalLayout_8.addLayout(self.horizontalLayout_3)
        self.line_password_static = QtWidgets.QLineEdit(self.verticalLayoutWidget_8)
        self.line_password_static.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.line_password_static.setFont(font)
        self.line_password_static.setToolTip("")
        self.line_password_static.setWhatsThis("")
        self.line_password_static.setAccessibleName("")
        self.line_password_static.setAccessibleDescription("")
        self.line_password_static.setInputMask("")
        self.line_password_static.setText("")
        self.line_password_static.setMaxLength(50)
        self.line_password_static.setAlignment(QtCore.Qt.AlignCenter)
        self.line_password_static.setReadOnly(True)
        self.line_password_static.setObjectName("line_password_static")
        self.verticalLayout_8.addWidget(self.line_password_static)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btn_cancel2 = QtWidgets.QPushButton(self.verticalLayoutWidget_8)
        self.btn_cancel2.setEnabled(False)
        self.btn_cancel2.setObjectName("btn_cancel2")
        self.horizontalLayout_4.addWidget(self.btn_cancel2)
        self.btn_ok2 = QtWidgets.QPushButton(self.verticalLayoutWidget_8)
        self.btn_ok2.setEnabled(False)
        self.btn_ok2.setObjectName("btn_ok2")
        self.horizontalLayout_4.addWidget(self.btn_ok2)
        self.verticalLayout_8.addLayout(self.horizontalLayout_4)

        self.progressbar_2 = QtWidgets.QProgressBar(Form)
        self.progressbar_2.setGeometry(QtCore.QRect(10, 390, 511, 16))
        self.progressbar_2.setProperty("value", 0)
        self.progressbar_2.setAlignment(QtCore.Qt.AlignCenter)
        self.progressbar_2.setObjectName("progressbar_2")

        #
        self.progressbar_2.hide()
        #self.textBrowser.hide()
        #self.label_8.hide()
        #

        self.retranslateUi(Form)
        self.btn_get_passwords.clicked['bool'].connect(self.list_passwords.setDisabled)
        self.btn_get_passwords.clicked['bool'].connect(self.radiobtn_auto.setDisabled)
        self.btn_get_passwords.clicked['bool'].connect(self.radiobtn_manual.setDisabled)
        self.btn_get_passwords.clicked['bool'].connect(self.btn_cancel.setDisabled)
        self.btn_get_passwords.clicked['bool'].connect(self.label_7.setDisabled)
        self.btn_get_passwords.clicked['bool'].connect(self.label_3.setDisabled)
        self.btn_get_passwords.clicked['bool'].connect(self.btn_check.setDisabled)
        self.btn_get_passwords.clicked['bool'].connect(self.btn_get_passwords.setEnabled)
        self.btn_cancel.clicked['bool'].connect(self.btn_get_passwords.setDisabled)
        self.btn_cancel.clicked['bool'].connect(self.radiobtn_auto.setEnabled)
        self.btn_cancel.clicked['bool'].connect(self.radiobtn_manual.setEnabled)
        self.btn_cancel.clicked['bool'].connect(self.label_3.setEnabled)
        self.btn_cancel.clicked['bool'].connect(self.label_7.setEnabled)
        self.btn_cancel.clicked['bool'].connect(self.btn_check.setEnabled)
        self.btn_cancel.clicked['bool'].connect(self.list_passwords.clear)
        self.btn_cancel.clicked['bool'].connect(self.list_passwords.setEnabled)
        self.btn_cancel.clicked['bool'].connect(self.btn_cancel.setEnabled)
        self.btn_get_passwords.clicked['bool'].connect(self.checkbox_use_dict.setEnabled)
        self.btn_get_passwords.clicked['bool'].connect(self.listwidget_lengths.setEnabled)
        self.btn_cancel.clicked['bool'].connect(self.listwidget_lengths.setDisabled)
        self.btn_cancel.clicked['bool'].connect(self.checkbox_use_dict.setDisabled)
        self.btn_cancel.clicked['bool'].connect(self.label_2.setDisabled)
        self.btn_get_passwords.clicked['bool'].connect(self.label_2.setEnabled)
        #self.btn_cancel.clicked['bool'].connect(self.textBrowser.hide)
        self.btn_get_passwords.clicked['bool'].connect(self.label_5.hide)
        self.btn_get_passwords.clicked['bool'].connect(self.table_widget_calc.hide)
        self.btn_get_passwords.clicked['bool'].connect(self.table_widget_keys.hide)
        self.btn_get_passwords.clicked['bool'].connect(self.label_4.hide)
        #self.btn_get_passwords.clicked['bool'].connect(self.textBrowser.show)
        #self.btn_get_passwords.clicked['bool'].connect(self.label_8.show)
        #self.btn_cancel.clicked['bool'].connect(self.label_8.hide)
        self.btn_cancel.clicked['bool'].connect(self.table_widget_keys.show)
        self.btn_cancel.clicked['bool'].connect(self.table_widget_calc.show)
        self.btn_cancel.clicked['bool'].connect(self.label_4.show)
        self.btn_cancel.clicked['bool'].connect(self.label_5.show)
        self.btn_check.clicked['bool'].connect(self.label_9.setDisabled)
        self.btn_check.clicked['bool'].connect(self.btn_left.setDisabled)
        self.btn_check.clicked['bool'].connect(self.btn_right.setDisabled)
        self.btn_check.clicked['bool'].connect(self.btn_cancel2.setDisabled)
        self.btn_check.clicked['bool'].connect(self.btn_ok2.setDisabled)
        self.btn_cancel.clicked['bool'].connect(self.btn_ok2.setEnabled)
        self.btn_cancel.clicked['bool'].connect(self.btn_cancel2.setEnabled)
        self.btn_cancel.clicked['bool'].connect(self.btn_left.setEnabled)
        self.btn_cancel.clicked['bool'].connect(self.btn_right.setEnabled)
        self.btn_cancel.clicked['bool'].connect(self.line_password_static.clear)
        self.btn_cancel2.clicked['bool'].connect(self.btn_left.setEnabled)
        self.btn_cancel2.clicked['bool'].connect(self.btn_right.setEnabled)
        self.btn_cancel2.clicked['bool'].connect(self.line_password_static.clear)
        self.btn_cancel2.clicked['bool'].connect(self.btn_ok2.setEnabled)
        self.btn_cancel2.clicked['bool'].connect(self.btn_cancel2.setEnabled)
        self.btn_check.clicked['bool'].connect(self.radiobtn_auto.setEnabled)
        self.btn_check.clicked['bool'].connect(self.radiobtn_manual.setEnabled)
        self.btn_check.clicked['bool'].connect(self.btn_cancel.setEnabled)
        self.btn_check.clicked['bool'].connect(self.label_7.setEnabled)
        self.btn_check.clicked['bool'].connect(self.list_passwords.setEnabled)
        self.btn_check.clicked['bool'].connect(self.label_3.setEnabled)
        self.btn_check.clicked['bool'].connect(self.btn_check.setEnabled)
        self.btn_cancel2.clicked['bool'].connect(self.btn_check.setDisabled)
        self.btn_cancel2.clicked['bool'].connect(self.btn_cancel.setDisabled)
        self.btn_cancel2.clicked['bool'].connect(self.radiobtn_auto.setDisabled)
        self.btn_cancel2.clicked['bool'].connect(self.list_passwords.setDisabled)
        self.btn_cancel2.clicked['bool'].connect(self.label_7.setDisabled)
        self.btn_cancel2.clicked['bool'].connect(self.label_3.setDisabled)
        self.btn_cancel2.clicked['bool'].connect(self.radiobtn_manual.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "INFORMATION"))
        self.label_6.setText(_translate("Form", "TextLabel"))
        self.label_2.setText(_translate("Form", "1. Choose length(s) of password:"))
        __sortingEnabled = self.listwidget_lengths.isSortingEnabled()
        self.listwidget_lengths.setSortingEnabled(False)
        item = self.listwidget_lengths.item(0)
        item.setText(_translate("Form", "Choose everything"))
        self.listwidget_lengths.setSortingEnabled(__sortingEnabled)
        self.checkbox_use_dict.setText(_translate("Form", "Search only for dictionary words"))
        self.btn_get_passwords.setText(_translate("Form", "Get probable passwords"))
        self.label_3.setText(_translate("Form", "2. Choose password(s) to check:"))
        __sortingEnabled = self.list_passwords.isSortingEnabled()
        self.list_passwords.setSortingEnabled(False)
        item = self.list_passwords.item(0)
        item.setText(_translate("Form", "Choose everything"))
        self.list_passwords.setSortingEnabled(__sortingEnabled)
        self.label_7.setText(_translate("Form", "Choose method"))
        self.radiobtn_auto.setText(_translate("Form", "Auto (recommended)"))
        self.radiobtn_manual.setText(_translate("Form", "Manual"))
        self.btn_cancel.setText(_translate("Form", "Cancel"))
        self.btn_check.setText(_translate("Form", "Check"))
        self.label_4.setText(_translate("Form", "Calculation table"))
        self.label_5.setText(_translate("Form", "Possible keys"))
        #self.label_8.setText(_translate("Form", "Ciphergram"))
        self.label_9.setText(_translate("Form", "3. Password finder"))
        self.btn_left.setText(_translate("Form", "<"))
        self.btn_right.setText(_translate("Form", ">"))
        self.line_password_static.setPlaceholderText(_translate("Form", "PASSWORD"))
        self.btn_cancel2.setText(_translate("Form", "Cancel"))
        self.btn_ok2.setText(_translate("Form", "OK"))

    def create_table_2(self, ciphergram: str, repeat_result: dict, suggestions: int):
        """

        :param ciphergram: ciphered text
        :param repeat_result: result of subfind
        :return: create calculation table, Dialog for key input and return key_length imput
        """

        # Basics
        new_ciphergram = ciphergram
        repeat_keys = list(repeat_result.keys())  # list of repeating fragments
        repeat_values = list(repeat_result.values())  # list of their appearings

        print("WORKING...")
        # Creating a Table - basic, headers and first 3 columns
        try:
            self.table_widget_calc.setWindowTitle("TABLE")
            self.table_widget_calc.setDisabled(False)
            self.table_widget_calc.setRowCount(int(len(repeat_keys)))
            self.table_widget_calc.setColumnCount(100)  # column count option?
            self.table_widget_calc.setHorizontalHeaderLabels(["Name", "Length", "Appearings"])
            self.table_widget_calc.setColumnWidth(0, 100)
            self.table_widget_calc.setColumnWidth(1, 50)
            self.table_widget_calc.setColumnWidth(2, 80)
            # Setting first three columns name:length:number_of_appearings
            for X in range(int(len(repeat_keys))):
                list_1 = find_distance(new_ciphergram, repeat_keys[X], repeat_values[X] - 1)
                if X == 0:
                    max_list_1_length = len(list_1)
                else:
                    if len(list_1) > max_list_1_length:
                        max_list_1_length = int(len(list_1))
                self.table_widget_calc.setItem(X, 0, QTableWidgetItem(str(repeat_keys[X])))
                self.table_widget_calc.setItem(X, 1, QTableWidgetItem(str(len(repeat_keys[X]))))
                self.table_widget_calc.setItem(X, 2, QTableWidgetItem(str(repeat_values[X])))
                for Y in range(len(list_1)):
                    self.table_widget_calc.setItem(X, Y + 3, QTableWidgetItem(str(list_1[Y])))

            # Creating place for GCD column
            max_list_1_length += 3
            self.table_widget_calc.setHorizontalHeaderItem(max_list_1_length, QTableWidgetItem ("GCD"))
            self.table_widget_calc.setColumnWidth(max_list_1_length, 50)

            # Setting factor columns
            for i in range(3, max_list_1_length):
                self.table_widget_calc.setHorizontalHeaderItem(i, QTableWidgetItem("Factors"))
                self.table_widget_calc.setColumnWidth(i, 50)

            # Calculating GCDs for each row and divisors for each row's GCD
            for row in range(0, len(repeat_keys)):
                list_2 = []
                for col in range(3, max_list_1_length):
                    try:
                        item = self.table_widget_calc.item (row, col).text()
                        item = int(item)
                        list_2.append(item)
                    except Exception as e:
                        item = None
                row_gcd = GCD(list_2)
                self.table_widget_calc.setItem(row, max_list_1_length, QTableWidgetItem(str(row_gcd)))
                self.table_widget_calc.setColumnWidth(max_list_1_length + 1, 500)
                self.table_widget_calc.setHorizontalHeaderItem(max_list_1_length + 1, QTableWidgetItem("Divisors"))

            # List for storing ALL divisors
            list_of_divisors = []
            for i in range(len(repeat_keys)):
                x = self.table_widget_calc.item(i, max_list_1_length).text()
                x = int(x)
                s = ""
                for el in divisors(x):
                    if int(el) != 1:
                        s += str(el) + " "
                        list_of_divisors.append(el)
                self.table_widget_calc.setItem(i, max_list_1_length + 1, QTableWidgetItem(s))

            # Saving memory space
            del s, x, row_gcd

            # Counting divisors and sorting from largest number of appearings to smallest
            x = Counter(list_of_divisors)
            x = sorted(x.items(), key=lambda x: x[1], reverse=True)

            # Message to give probable key length values
            message_text = ""
            message_text = "Programme suggests " +str(suggestions) +" most probable values of key length: " + "\n"
            for i in range(suggestions):
                item = QtWidgets.QListWidgetItem(str(x[i][0]))
                # could be Qt.Unchecked; setting it makes the check appear
                item.setCheckState(QtCore.Qt.Unchecked)
                self.listwidget_lengths.addItem(item)
                #item = QtWidgets.QListWidgetItem(self.listwidget_lengths)
                #item.setText(str(x[i][0]))
                #ch = QtWidgets.QCheckBox()
                #ch.setText(str(x[i[0]]))
                #self.listwidget_lengths.setItemWidget(ch)
                #self.listwidget_lengths.addItem(str(x[i][0]))

                message_text += str(x[i][0])
                if i != suggestions-1:
                    message_text += ", "
            message_text += "\n\n" + "Remember: keys of length 3 or less are rarely chosen"
            return message_text

        except Exception as e:
            print(e)
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Warning)
            msgbox.setWindowTitle('WARNING')
            msgbox.setText('Unfortunately, there is too little information to crack the ciphergram')
            msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgbox.exec_()

            return 0

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

# Styling
#normal_style = "color: white; background-color: gray"
