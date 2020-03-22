from PyQt5 import QtCore
import SQLMethod
import sqlite3
import os
import sys
import time

class addCodeThread(QtCore.QThread):
    tableName = ''
    function = ''
    code = ''

    def __init__(self,table,fun,cd):
        super(addCodeThread,self).__init__()
        self.tableName = table
        self.function = fun
        self.code = cd

    signalThread = QtCore.pyqtSignal(str,str)

    def run(self):
        filename = str(os.path.join(sys.path[0])) + '\\code.db'
        conn = sqlite3.connect(filename)
        flag = self.checkTextisNull()
        sm = SQLMethod.SqlMethod(conn)
        strtime = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        if flag == 0:
            if sm.checkTableIsExist(self.tableName) == False:
                sm.AddTable(self.tableName)
            mark = sm.addCode(self.tableName,self.function,self.code)
            sm.insertLog('插入代码语言为' + str(self.tableName) + ',模板描述为' + str(self.function))
            self.signalThread.emit(strtime,'插入代码语言为' + str(self.tableName) + ',模板描述为' + str(self.function))
        elif flag == 1:
            sm.insertLog('代码语言不能为空')
            self.signalThread.emit(strtime,'代码语言不能为空')
        elif flag == 2:
            sm.insertLog('模板描述不能为空')
            self.signalThread.emit(strtime,'模板描述不能为空')
        elif flag == 3:
            sm.insertLog('代码不能为空')
            self.signalThread.emit(strtime,'代码不能为空')
        elif flag == 4:
            sm.insertLog('代码语言和模板描述不能为空')
            self.signalThread.emit(strtime,'代码语言和模板描述不能为空')
        elif flag == 5:
            sm.insertLog('代码语言和代码不能为空')
            self.signalThread.emit(strtime,'代码语言和代码不能为空')
        elif flag == 6:
            sm.insertLog('模板描述和代码不能为空')
            self.signalThread.emit(strtime,'模板描述和代码不能为空')
        else:
            sm.insertLog('代码语言、模板描述、代码均不能为空')
            self.signalThread.emit(strtime,'代码语言、模板描述、代码均不能为空')
        conn.close()

    def checkTextisNull(self):
        if self.tableName != '' and self.function != '' and self.code != '':
            return 0
        else:
            if self.tableName == '' and self.function != '' and self.code != '':
                return 1
            elif self.function == '' and self.tableName != '' and self.code != '':
                return 2
            elif self.code == '' and self.tableName != '' and self.function != '':
                return 3
            elif self.tableName == '' and self.function == '' and self.code != '':
                return 4
            elif self.tableName == '' and self.code == '' and self.function != '':
                return 5
            elif self.function == '' and self.code == '' and self.tableName != '':
                return 6
            else:
                return 7