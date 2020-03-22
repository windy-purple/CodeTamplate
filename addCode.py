import sys
from PyQt5.QtWidgets import *
import addCodeUi
import threading
import SQLMethod
import os
import sqlite3
from PyQt5 import QtCore
import time
import addCodeThread
                
class addCode(QDialog,addCodeUi.Ui_Dialog):

    mySignal = QtCore.pyqtSignal(str,str)

    def __init__(self):
        QDialog.__init__(self)
        addCodeUi.Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.reset)
        self.pushButton_2.clicked.connect(self.insertCode)

    def insertCode(self):
        table = str(self.lineEdit.text())
        function = str(self.lineEdit_2.text())
        code = str(self.textEdit.toPlainText())
        self.thread = addCodeThread.addCodeThread(table,function,code)
        self.thread.signalThread.connect(self.threadToDialog)
        self.thread.start()
        self.thread.exec()

    def threadToDialog(self,timeString,informationString):
        self.mySignal.emit(timeString,informationString)
        self.reset()

    def reset(self):
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.textEdit.setText('')