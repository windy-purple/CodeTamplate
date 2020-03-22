import sys
from PyQt5.QtWidgets import *
import codeStorageUi
import addCode
import SQLMethod
import sqlite3
import os
import sys
import selectCodeLogThread
from PyQt5.QtGui import QIcon
                
class Main(QMainWindow,codeStorageUi.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        codeStorageUi.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton_4.clicked.connect(self.addCodeUi)
        self.pushButton.clicked.connect(self.exitProcess)
        self.pushButton_3.clicked.connect(self.logRemove)
        self.pushButton_2.clicked.connect(self.toJQB)
        self.setMaincomboboxItem()

    def setMaincomboboxItem(self):
        filename = str(os.path.join(sys.path[0])) + '\\code.db'
        print(filename)
        conn = sqlite3.connect(filename)
        sm = SQLMethod.SqlMethod(conn)
        itemList = sm.inquiryAllTable()
        itemList.insert(0,'null')
        self.comboBox.clear()
        self.comboBox.addItems(itemList)
        conn.close()
        self.comboBox.currentIndexChanged.connect(self.setMinorcomboboxItem)

    def setMinorcomboboxItem(self):
        if self.comboBox.currentText() != 'null' and self.comboBox.currentText() != '':
            filename = str(os.path.join(sys.path[0])) + '\\code.db'
            conn = sqlite3.connect(filename)
            sm = SQLMethod.SqlMethod(conn)
            itemList = sm.inquiryFunction(self.comboBox.currentText())
            self.comboBox_2.clear()
            itemList.insert(0,'null')
            self.comboBox_2.addItems(itemList)
            conn.close()
            self.comboBox_2.currentIndexChanged.connect(self.codeToEdit)
        else:
            itemList = ['null']
            self.comboBox_2.clear()
            self.comboBox_2.addItems(itemList)

    def codeToEdit(self):
        if self.comboBox.currentText() != 'null' and self.comboBox.currentText() != '' and self.comboBox_2.currentText() != 'null' and self.comboBox_2.currentText() != '':
            table = self.comboBox.currentText()
            function = self.comboBox_2.currentText()
            self.codeThread = selectCodeLogThread.selectThread(table,function,'',0)
            self.codeThread.mainSignal.connect(self.receiveCode)
            self.codeThread.start()
            self.codeThread.exec()

    def addCodeUi(self):
        ch.show()
        ch.mySignal.connect(self.LoadLog)
        
    def exitProcess(self):
        sys.exit(0)

    def logRemove(self):
        self.logThread = selectCodeLogThread.selectThread('','','',2)
        self.logThread.mainSignal.connect(self.receiveCode)
        self.logThread.start()
        self.logThread.exec()

    def toJQB(self):
        self.JQBThread = selectCodeLogThread.selectThread('','',str(self.textBrowser.toPlainText()),1)
        self.JQBThread.mainSignal.connect(self.receiveCode)
        self.JQBThread.start()
        self.JQBThread.exec()

    def LoadLog(self,timeString,messageString):
        log = timeString + '==>' + messageString
        self.textBrowser_2.append(log)

    def receiveCode(self,flag,log,code):
        if flag == 0:
            self.textBrowser.clear()
            newcode = code.replace("(dyh)","'")
            newcode = newcode.replace("(syh)",'"')
            self.textBrowser.setText(newcode)
            self.textBrowser_2.append(log)
        if flag == 2:
            self.textBrowser_2.clear()
            self.textBrowser_2.append(log)
        if flag == 1:
            self.textBrowser_2.append(log)
        
        
if __name__=='__main__':
    app = QApplication(sys.argv)
    iconname = str(os.path.join(sys.path[0])) + '\\lib\\存储.ico'
    icon = QIcon(iconname)
    md = Main()
    md.setWindowIcon(icon)
    md.show()
    ch = addCode.addCode()
    sys.exit(app.exec_())