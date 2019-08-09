# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'cracker1.ui'
# Created by: PyQt5 UI code generator 5.12.1
# WARNING! All changes made in this file will be lost!
#########################################LIBRARIES########################################
import os, traceback, sys, time, string
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from datetime import datetime, timedelta
from collections import Counter, OrderedDict
from funcs import divisors, GCD, find_distance, transformer
#########################################CONSTANTS############################################
# Language and version
version = "1.8.0"
language = "English"

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
        MainWindow.resize(639, 343)
        MainWindow.setMaximumSize(639, 343)
        MainWindow.setMinimumSize(639, 343)
        MainWindow.setWindowTitle("Vigenere's Cipher Cracker")

        # Main GUI Look
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 251, 16))
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 30, 401, 241))
        self.textBrowser.setReadOnly(False)
        self.textBrowser.setOverwriteMode(False)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setFontPointSize(8)
        self.groupBox_Control_Panel = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Control_Panel.setGeometry(QtCore.QRect(420, 20, 211, 251))
        self.groupBox_Control_Panel.setObjectName("groupBox_Control_Panel")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_Control_Panel)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 22, 199, 227))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(5, 0, 5, 0)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_2.addWidget(self.line_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_open = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btn_open.setObjectName("btn_open")
        self.horizontalLayout_2.addWidget(self.btn_open)
        self.btn_save = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout_2.addWidget(self.btn_save)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.line_3 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.spinBox = QtWidgets.QSpinBox(self.verticalLayoutWidget_2)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.spin_label_1 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.spin_label_1.setObjectName("spin_label_1")
        self.horizontalLayout.addWidget(self.spin_label_1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.spinBox_2 = QtWidgets.QSpinBox(self.verticalLayoutWidget_2)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout_3.addWidget(self.spinBox_2)
        self.spin_label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.spin_label_2.setObjectName("spin_label_2")
        self.horizontalLayout_3.addWidget(self.spin_label_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout.addWidget(self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox_3.setObjectName("checkBox_3")
        self.verticalLayout.addWidget(self.checkBox_3)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.btn_start = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.btn_start.setObjectName("btn_start")
        self.verticalLayout.addWidget(self.btn_start)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.progressbar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressbar.setGeometry(QtCore.QRect(10, 280, 621, 21))
        self.progressbar.setProperty("value", 0)
        self.progressbar.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.progressbar.setTextVisible(False)
        self.progressbar.setObjectName("progressbar")
        self.progressbar.hide()
        self.progress_label = QtWidgets.QLabel(self.centralwidget)
        self.progress_label.setGeometry(QtCore.QRect(10, 280, 621, 21))
        self.progress_label.setText("")
        self.progress_label.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_label.setObjectName("progress_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 639, 21))
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

        # Test
        self.button_new = QtWidgets.QPushButton(MainWindow)
        self.button_new.setText("Try me!")

        # Styling
        # TODO: play with style
        normal_style = "color: white; background-color: gray"

        # Icon and window title
        icon = QtGui.QIcon("wasp.png")
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowTitle("VCC Vigenere's Cipher Cracker v.1.8.0")

        # Button for clearing
        self.btn_clear = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clear.setGeometry(QtCore.QRect(360, 9, 51, 21))
        self.btn_clear.setObjectName("btn_clear")
        self.btn_clear.raise_()

        # Font size label
        self.label_fs = QtWidgets.QLabel(MainWindow)
        self.label_fs.setText("Font size: 8")
        self.label_fs.move(180, 24)
        self.label_fs.show()

        # New slider for Font size
        self.slider = QtWidgets.QSlider(MainWindow)
        self.slider.setFixedWidth(100)
        self.slider.setFixedHeight(17)
        self.slider.setMaximum(30)
        self.slider.setMinimum(8)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.move(250, 32)
        self.slider.show()

        # Spinboxes default values
        self.spinBox.setMinimum(2)
        self.spinBox_2.setMinimum(2)
        self.spinBox.setValue(3)        # MINLEN
        self.spinBox_2.setValue(2)      # MINCNT

        # Retranslation and connecting SIGNALS
        self.retranslateUi(MainWindow)
        self.actionExit.triggered.connect(MainWindow.close)
        self.btn_start.clicked.connect(self.start_cracking)
        self.btn_save.clicked.connect(self.save_text)
        self.btn_open.clicked.connect(self.open_text)
        self.btn_clear.clicked.connect(self.textBrowser.clear)
        self.slider.valueChanged.connect(self.change_font_size)
        self.button_new.clicked.connect(self.new_func)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Upload or type the ciphergram"))
        self.groupBox_Control_Panel.setTitle(_translate("MainWindow", "Control Panel"))
        self.btn_open.setText(_translate("MainWindow", "Open"))
        self.btn_save.setText(_translate("MainWindow", "Save"))
        self.btn_clear.setText (_translate ("MainWindow", "Clear"))
        self.label_3.setText(_translate("MainWindow", "Settings:"))
        self.spin_label_1.setToolTip(_translate("MainWindow", "# minimal length of repeating fragments to find"))
        self.spin_label_1.setText(_translate("MainWindow", "MIN_LEN"))
        self.spin_label_2.setToolTip(_translate("MainWindow", "# minimal number of appearings of repeating fragments to find"))
        self.spin_label_2.setText(_translate("MainWindow", "MIN_CNT"))
        self.checkBox.setText(_translate("MainWindow", "Table"))
        self.checkBox_2.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_3.setText(_translate("MainWindow", "CheckBox"))
        self.btn_start.setText(_translate("MainWindow", "Crack"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionGuide_to_Vigenere_s_Cipher.setText(_translate("MainWindow", "Guide to Vigenere\'s Cipher"))
        self.actionAuthor_License.setText(_translate("MainWindow", "Author/License"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Esc"))

    def start_cracking(self):
        # TODO: add documentation
        """
        :return:
        """

        # Disabling input
        self.textBrowser.setDisabled(True)
        self.btn_open.setDisabled(True)
        self.btn_save.setDisabled(True)
        self.btn_start.setDisabled(True)
        self.spinBox.setDisabled(True)
        self.spinBox_2.setDisabled(True)
        self.checkBox.setDisabled(True)
        self.checkBox_2.setDisabled(True)
        self.checkBox_3.setDisabled(True)

        # Set progressbar
        self.progressbar.show()
        self.progress_label.setText("Cracking...")

        # Get inputed options
        MINLEN = self.spinBox.value()           # minimal length of repeating fragments
        MINCNT = self.spinBox_2.value()         # minimal number of appearings of repeating fragments
        show_table = self.checkBox.isChecked()

        # Get text for analysis
        ciphergram = self.textBrowser.toPlainText()

        # Ciphergram preprocessing: making text uppercase and only letters
        # eg. "Today is Sunday!" --> "TODAYISSUNDAY"
        ciphergram_upper = ciphergram.upper()
        new_ciphergram = ""
        for el in ciphergram_upper:
            if el in alphabet_capital_eng:
                new_ciphergram += el

        # Search for repeating fragments of chars
        try:
            repeat_result = self.subfind(new_ciphergram, MINLEN, MINCNT) # Returns a dict with repeating fragments and number of their appearings
            key_length = self.create_table(new_ciphergram, repeat_result, show_table)
        except Exception as e:
            print(e)
        # error if wrong value is given

        # Real cracking: statistical analysis using least-squares method
        key_word = self.decoder(key_length, new_ciphergram) # decoder -> mono_crack --> password letter by letter

        # Decoding whole text using cracked password
        try:
            new_text = "Password: "+str(key_word) + "\n"
            new_text += self.decrypt(ciphergram, key_word)
            self.textBrowser.setText(new_text)
            MainWindow.showMaximized()

        except Exception as e:
            print(e)

        # Re-enabling input
        self.textBrowser.setDisabled(False)
        self.btn_open.setDisabled(False)
        self.btn_save.setDisabled(False)
        self.btn_start.setDisabled(False)
        self.spinBox.setDisabled(False)
        self.spinBox_2.setDisabled(False)
        self.checkBox.setDisabled(False)
        self.checkBox_2.setDisabled(False)
        self.checkBox_3.setDisabled(False)

        # Closing progressbar
        self.progressbar.hide()
        self.progress_label.clear()
        return

    def create_table(self, ciphergram, repeat_result, show_table):
        """

        :param ciphergram: ciphered text
        :param repeat_result: result of subfind
        :param show_table:
        :return: create calculation table, Dialog for key input and return key_length imput
        """

        # Basics
        new_ciphergram = ciphergram
        repeat_keys = list(repeat_result.keys())  # list of repeating fragments
        repeat_values = list(repeat_result.values())  # list of their appearings

        # FIXME: there is a problem with creating table for small texts
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
        except Exception as e:
            print ("Error occured while creating a table :" + "\n", e)
            print ("CODE: 261-268")

        # Check whether to show table
        if show_table == True:
            self.tableWidget.show()

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
                self.tableWidget.setItem (X, Y + 3, QTableWidgetItem(str(list_1[Y])))

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

        # Checking for option
        if show_table == True:
            self.tableWidget.showMaximized()

        # Counting divisors and sorting from largest number of appearings to smallest
        x = Counter(list_of_divisors)
        x = sorted(x.items(), key=lambda x: x[1], reverse=True)

        # Message to give probable key length values
        message_text = ""
        message_text = "Programme suggests 5 most probable values of key length: " + "\n"
        for i in range(5):
            message_text += str(x[i][0])
            if i != 4:
                message_text += ", "
        message_text += "\n\n" + "Remember: keys of length 3 or less are rarely chosen"
        message_text += "\n\n" + "Enter probable key length:"

        dialog = QtWidgets.QInputDialog(MainWindow)
        key_length, ok = dialog.getInt(self.tableWidget, 'Probable key length: ', message_text)
        if ok:
            # add number or list of numbers with spacing " "
            key_length = int(key_length)

        return key_length

    def subfind(self, text, MINLEN, MINCNT):
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

    def crack_mono(self, file):
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

        # Sorting and calculating the smallest difference and nearest key
        # Finding best mono position transformation
        best_fit = (sorted(results))[0]
        best_fit = results.index(best_fit)
        # Decoding letter of key_word
        key_char = alphabet_capital_eng[(26 - best_fit) % 26]
        return key_char

    def decoder(self, key_length, ciphergram):
        """

        :param key_length:
        :param ciphergram:
        :return:
        """
        lengths = []
        key_word = ""
        for i in range(0, int(key_length)):
            what_to_crack = ""
            for i2 in range(i, int(len(ciphergram)), int(key_length)):
                what_to_crack += ciphergram[i2]
            key_word += str(self.crack_mono(what_to_crack))

        return key_word

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

    def new_func(self):
        print(self.textBrowser.isBackwardAvailable())
        self.textBrowser.backward()
####################################FILE EXECUTION###################################################
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

"""
DRAFTS
"""