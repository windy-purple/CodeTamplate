from PyQt5 import QtCore
import SQLMethod
import sqlite3
import os
import sys
import time
import pyperclip

class selectThread(QtCore.QThread):
    table = ''
    function = ''
    code = ''
    mark = -1

    def __init__(self,tn,fu,cd,flag):
        super(selectThread,self).__init__()
        self.table = tn
        self.function = fu
        self.code = cd
        self.mark = flag

    mainSignal = QtCore.pyqtSignal(int,str,str)

    def run(self):
        if self.mark == 0:
            self.getCode()
        elif self.mark == 1:
            self.toJQB()
        elif self.mark == 2:
            self.removeLog()
        else:
            print('[-] error')

    def getCode(self):
        filename = str(os.path.join(sys.path[0])) + '\\code.db'
        conn = sqlite3.connect(filename)
        sm = SQLMethod.SqlMethod(conn)
        log = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))) + '==>' + '语言为' + self.table + ';模板描述为' + self.function + '获取完毕'
        self.mainSignal.emit(0,log,str(sm.inquiryCode(self.table,self.function)))
        conn.close()

    def removeLog(self):
        filename = str(os.path.join(sys.path[0])) + '\\code.db'
        conn = sqlite3.connect(filename)
        sm = SQLMethod.SqlMethod(conn)
        sm.deleteAllLog()
        log = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))) + '==>日志清除完毕'
        self.mainSignal.emit(2,log,'')
        conn.close()

    def toJQB(self):
        pyperclip.copy(self.code)
        spam = pyperclip.paste()
        log = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))) + '==>代码复制到剪切板完毕'
        self.mainSignal.emit(1,log,'')