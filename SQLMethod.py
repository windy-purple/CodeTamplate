import sqlite3
import time

class SqlMethod():

    conn = None

    def __init__(self,connsql):
        self.conn = connsql
        self.createLogTable()

    def inquiryAllTable(self):
        tableName = []
        sql = "select name from sqlite_master where type='table'"
        cur = self.conn.cursor()
        result = cur.execute(sql)
        for row in result:
            if str(row[0]) == 'sqlite_sequence' or str(row[0]) == 'Log':
                continue
            tableName.append(row[0])
        return tableName

    def AddTable(self,tableName):
        sql = "create table if not exists " + str(tableName) + " (id INTEGER PRIMARY KEY AUTOINCREMENT,function TEXT,code TEXT);"
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
        except:
            print('[-] addTable error')

    def checkTableIsExist(self,tableName):
        flag = False
        tableList = self.inquiryAllTable()
        for i in tableList:
            if i == tableName:
                flag = True
                break
        return flag

    def addCode(self,tablename,functionCode,code):
        flag = False
        cur = self.conn.cursor()
        code = code.replace("'",'(dyh)')
        code = code.replace('"','(syh)')
        cur.execute('insert into %s(function,code) values("%s","%s")'%(tablename,functionCode,code))
        self.conn.commit()
        flag = True
        return flag

    def inquiryFunction(self,table):
        functionList = []
        sql = 'select function from ' + str(table)
        cur = self.conn.cursor()
        relist = cur.execute(sql)
        for row in relist:
            functionList.append(row[0])
        return functionList

    def inquiryCode(self,table,functionName):
        strCode = ''
        sql = 'select code from ' + str(table) + ' where function=\'' + str(functionName) + '\''
        try:
            cur = self.conn.cursor()
            result = cur.execute(sql)
            for row in result:
                strCode = str(row[0])
        except:
            print('[-] select code error!')
        return strCode

    def createLogTable(self):
        sql = "create table if not exists Log (id INTEGER PRIMARY KEY AUTOINCREMENT,time TEXT,logtext TEXT);"
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
        except:
            print('[-] addLogTable error')

    def insertLog(self,text):
        flag = False
        strtime = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        sql = 'insert into Log (time,logtext) values(\'' + str(strtime) + '\',\'' + str(text) + '\')'
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            flag = True
        except:
            print('[-] addLog error!')
        return flag

    def deleteAllLog(self):
        flag = False
        sql = 'delete from Log;'
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            flag = True
        except:
            print('[-] delete Log error!')
        return flag