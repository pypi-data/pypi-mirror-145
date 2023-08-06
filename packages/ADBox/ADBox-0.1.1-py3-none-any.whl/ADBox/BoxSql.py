import sqlite3
import os
import json
import hashlib
import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return((str(z)))
        else:
            return(super().default(z))

class BoxSql(object):
    # __init__
    # - DBName: db file path
    # - MainLogger: logger object
    def __init__(self, DBName, MainLogger):
        self._ChceckDB = False
        self.__DBLogger = MainLogger
        if(not os.path.isdir(DBName)):
            if(not os.path.exists(DBName)):
                self.__DBLogger.debug("BoxSql.__init__: Create new database {0}".format(DBName))
                try:
                    self.__BoxDBObject = sqlite3.connect(DBName)
                    self.__BoxDBCursor = self.__BoxDBObject.cursor()
                except Exception as BoxExcept:
                    self.__DBLogger.error("BoxSql.__init__: Exception {0}".format(BoxExcept))
                else:
                    self.__DBLogger.info("BoxSql.__init__: Create new db {0}".format(DBName))
                try:
                    self.__BoxDBCursor.execute(
                        '''CREATE TABLE users (dn text, sAMAccountName text, RawData text)''')
                    self.__BoxDBCursor.execute(
                        '''CREATE TABLE groups (dn text, sAMAccountName text, RawData text)''')
                    self.__BoxDBCursor.execute(
                        '''CREATE TABLE pwd (sAMAccountName text, LM text, NT text, pass text)''')
                    self.__BoxDBCursor.execute(
                        '''CREATE TABLE computers (dn text, sAMAccountName text, RawData text)''')
                    self.__BoxDBCursor.execute(
                        '''CREATE TABLE settings (name text, value text)''')
                    self.__BoxDBObject.commit()
                except Exception as BoxExcept:
                    self.__DBLogger.error("BoxSql.__init__: Exception {0}".format(BoxExcept))
                else:
                    self._ChceckDB = True
            else:
                self.__DBLogger.debug("BoxSql.__init__: Open exist database {0}".format(DBName))
                try:
                    self.__BoxDBObject = sqlite3.connect(DBName)
                    self.__BoxDBCursor = self.__BoxDBObject.cursor()
                except Exception as BoxExcept:
                    self.__DBLogger.error("BoxSql.__init__: Exception {0}".format(BoxExcept))
                else:
                    self.__DBLogger.info("BoxSql.__init__: Open success {0}".format(DBName))
                    self._ChceckDB = True

    def __CheckType(self,JsonObj):
        try:
            for JsonKey in JsonObj.keys():
                if(isinstance(JsonObj[JsonKey],list)):
                    for JsonValue in JsonObj[JsonKey]:
                        if(isinstance(JsonValue,bytes)):
                            JsonObj[JsonKey] = ["HEX({0})".format(JsonValue.hex()) if item == JsonValue else item for item in JsonObj[JsonKey]]
                else:
                    if (isinstance(JsonObj[JsonKey], bytes)):
                        JsonObj[JsonKey] = "HEX({0})".format(JsonObj[JsonKey].hex()) # bytes.fromhex('deadbeef')
        except Exception as BoxExcept:
            self.__DBLogger.error("BoxSql.__CheckType: Exception {0}".format(BoxExcept))

    def _GetSettings(self):
        try:
            Return =  self.__BoxDBCursor.execute("""SELECT * FROM settings""").fetchall()
        except Exception as BoxExcept:
            self.__DBLogger.error("BoxSql._GetSettings: Exception {0}".format(BoxExcept))
        return(Return)

    # _AddSetting
    # - Name
    # - Value
    def _AddSetting(self, Name, Value):
        if ((1,) != self.__BoxDBCursor.execute("SELECT EXISTS(SELECT 1 FROM settings WHERE name='{0}')".format(Name)).fetchone()):
            self.__BoxDBCursor.execute("""INSERT INTO settings VALUES ('{0}','{1}')""".format(Name, Value))
            self.__DBLogger.debug("BoxSql._AddSetting: Add seting name - {0}".format(Name))
        else:
            self.__BoxDBCursor.execute("""UPDATE settings SET value='{1}' WHERE name='{0}'""".format(Name, Value))
            self.__DBLogger.debug("BoxSql._AddSetting: Update seting name - {0}".format(Name))
        self.__BoxDBObject.commit()


    def AddUser(self, dn, sam, raw):
        if((1, ) != self.__BoxDBCursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE sAMAccountName='{0}')".format(sam)).fetchone()):
            self.__BoxDBCursor.execute("""INSERT INTO users VALUES ('{0}','{1}','{2}')""".format(dn, sam, json.dumps(dict(raw), cls=DateTimeEncoder)))
            self.__DBLogger.debug("BoxSql.AddUser: Add new user - {0}".format(dn))
        else:
            BoxUser = self.__BoxDBCursor.execute("SELECT RawData FROM users WHERE sAMAccountName='{0}'".format(sam)).fetchone()
            TestDB = hashlib.sha256(BoxUser[0].encode('utf-8')).hexdigest()
            TestDump = hashlib.sha256(json.dumps(dict(raw), cls=DateTimeEncoder).encode('utf-8')).hexdigest()
            if(TestDB != TestDump):
                self.__BoxDBCursor.execute(
                    """UPDATE users SET RawData='{1}' WHERE sAMAccountName='{0}'""".format(
                        sam, json.dumps(dict(raw), cls=DateTimeEncoder)))
                self.__DBLogger.debug("BoxSql.AddUser: Update user info - {0}".format(dn))
            else:
                self.__DBLogger.debug("BoxSql.AddUser: User exist - {0}".format(dn))
        self.__BoxDBObject.commit()

    def AddComputer(self, dn, sam, raw):
        self.__CheckType(raw)
        if ((1,) != self.__BoxDBCursor.execute("SELECT EXISTS(SELECT 1 FROM computers WHERE sAMAccountName='{0}')".format(sam)).fetchone()):
            self.__BoxDBCursor.execute(
                """INSERT INTO computers VALUES ('{0}','{1}','{2}')""".format(dn, sam,json.dumps(dict(raw),cls=DateTimeEncoder)))
            self.__DBLogger.debug("BoxSql.AddComputers: Add new computer - {0}".format(dn))
        else:
            BoxUser = self.__BoxDBCursor.execute("SELECT RawData FROM computers WHERE sAMAccountName='{0}'".format(sam)).fetchone()
            TestDB = hashlib.sha256(BoxUser[0].encode('utf-8')).hexdigest()
            TestDump = hashlib.sha256(json.dumps(dict(raw), cls=DateTimeEncoder).encode('utf-8')).hexdigest()
            if (TestDB != TestDump):
                self.__BoxDBCursor.execute(
                    """UPDATE computers SET RawData='{1}' WHERE sAMAccountName='{0}'""".format(sam, json.dumps(dict(raw), cls=DateTimeEncoder)))
                self.__DBLogger.debug("BoxSql.AddComputers: Update computer info - {0}".format(dn))
            else:
                self.__DBLogger.debug("BoxSql.AddComputers: Computer exist - {0}".format(dn))
        self.__BoxDBObject.commit()

    def AddGroup(self, dn, sam, raw):
        if ((1,) != self.__BoxDBCursor.execute("SELECT EXISTS(SELECT 1 FROM groups WHERE sAMAccountName='{0}')".format(sam)).fetchone()):
            self.__BoxDBCursor.execute(
                """INSERT INTO groups VALUES ('{0}','{1}','{2}')""".format(dn, sam, json.dumps(dict(raw),cls=DateTimeEncoder)))
            self.__DBLogger.debug("BoxSql.AddGroup: Add new group - {0}".format(dn))
        else:
            BoxUser = self.__BoxDBCursor.execute("SELECT RawData FROM groups WHERE sAMAccountName='{0}'".format(sam)).fetchone()
            TestDB = hashlib.sha256(BoxUser[0].encode('utf-8')).hexdigest()
            TestDump = hashlib.sha256(json.dumps(dict(raw), cls=DateTimeEncoder).encode('utf-8')).hexdigest()
            if (TestDB != TestDump):
                self.__BoxDBCursor.execute(
                    """UPDATE groups SET RawData='{1}' WHERE sAMAccountName='{0}'""".format(
                        sam, json.dumps(dict(raw), cls=DateTimeEncoder)))
                self.__DBLogger.debug("BoxSql.AddGroup: Update group info - {0}".format(dn))
            else:
                self.__DBLogger.debug("BoxSql.AddGroup: Group exist - {0}".format(dn))
        self.__BoxDBObject.commit()


    def _LoadObject(self,TableName):
        try:
            Return =  self.__BoxDBCursor.execute("""SELECT * FROM {0}""".format(TableName)).fetchall()
        except Exception as BoxExcept:
            self.__DBLogger.error("BoxSql._LoadObject: Exception {0}".format(BoxExcept))
        return(Return)