from PySide6.QtWidgets import (QTextEdit, QSplitter, QWidget, QLineEdit, QHBoxLayout, QTreeView, QAbstractItemView, QCompleter)
from PySide6.QtCore import (Qt, Slot)
from PySide6.QtGui import (QStandardItemModel, QStandardItem, QIcon)
import json
import os
from ADBox import BoxSearch

class BoxGUI(QWidget):
    def __init__(self, GUILogger, DBObject):
        super().__init__()
        if(os.name == "nt"):
            self.setWindowIcon(QIcon(".\\resources\\adbox.png"))
        else:
            self.setWindowIcon(QIcon("./resources/adbox.png"))
        self.setStyleSheet('background-color: #cdcdc0')
        self.setWindowTitle("ADBOX")
        self.__GUILogger = GUILogger
        self.__DBObject = DBObject
        self.__TextEdit = QTextEdit()
        self.__TextEdit.setReadOnly(True)
        self.__TextEdit.setStyleSheet("""
        QTextEdit {background-color: #f1f1f2; border: 2px solid #1e434c; border-radius: 6px; padding: 5px;}
        QScrollBar {background: #f1f1f2;}
        QScrollBar::handle {background: #1e434c; border-radius: 6px;}  
        QScrollBar::up-arrow, QScrollBar::down-arrow {border: 3px solid #1e434c; border-radius: 3px; background: #f1f1f2;}
        """)
        self.__TextEdit.setAlignment(Qt.AlignLeft)
        #####
        self.__Edit = QLineEdit()
        self.__Edit.setStyleSheet("background-color: #f1f1f2; border: 2px solid #1e434c; border-radius: 6px;")
        self.__Edit.setPlaceholderText("Search")
        #####
        self.HLayout = QHBoxLayout(self)
        self.__SplitterR = QSplitter(Qt.Vertical)
        self.__SplitterR.addWidget(self.__Edit)
        self.__SplitterR.addWidget(self.__TextEdit)
        #####
        self.__Splitter = QSplitter(Qt.Horizontal)
        self.__TreeView = QTreeView()
        self.__TreeView.setStyleSheet("""
        QTreeView {background-color: #f1f1f2; border: 2px solid #1e434c; border-radius: 11px; padding: 5px;}
        QTreeView::item:selected {background-color: #cdcdc0; border-radius: 5px; color: #1e434c;}
        QTreeView::branch {background-color: #f1f1f2;}
        QScrollBar {background: #f1f1f2;}
        QScrollBar::handle {background: #1e434c; border-radius: 6px;}  
        QScrollBar::up-arrow, QScrollBar::down-arrow {border: 3px solid #1e434c; border-radius: 3px; background: #f1f1f2;}
        """)
        self.__TreeView.doubleClicked.connect(self.__TreeViewDoubleClick)
        self.__TreeView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.__TreeView.setHeaderHidden(True)
        self.__Splitter.addWidget(self.__TreeView)
        self.__Splitter.addWidget(self.__SplitterR)
        self.__Splitter.setSizes([self.__Splitter.size().height() * 0.3, self.__Splitter.size().height() * 0.7])
        #####
        self.HLayout.addWidget(self.__Splitter)
        self.setLayout(self.HLayout)
        self.__Edit.returnPressed.connect(self.__SearchObjects)
        self.__UserAccountControls = {"SCRIPT": 1,
            "ACCOUNTDISABLE": 2,
            "HOMEDIR_REQUIRED": 8,
            "LOCKOUT": 16,
            "PASSWD_NOTREQD": 32,
            "PASSWD_CANT_CHANGE": 64,
            "ENCRYPTED_TEXT_PWD_ALLOWED": 128,
            "TEMP_DUPLICATE_ACCOUNT":256,
            "NORMAL_ACCOUNT": 512,
            "INTERDOMAIN_TRUST_ACCOUNT": 2048,
            "WORKSTATION_TRUST_ACCOUNT": 4096,
            "SERVER_TRUST_ACCOUNT": 8192,
            "DONT_EXPIRE_PASSWORD": 65536,
            "MNS_LOGON_ACCOUNT": 131072,
            "SMARTCARD_REQUIRED": 262144,
            "TRUSTED_FOR_DELEGATION": 524288,
            "NOT_DELEGATED": 1048576,
            "USE_DES_KEY_ONLY": 2097152,
            "DONT_REQ_PREAUTH": 4194304,
            "PASSWORD_EXPIRED ": 8388608,
            "TRUSTED_TO_AUTH_FOR_DELEGATION": 16777216,
            "PARTIAL_SECRETS_ACCOUNT": 67108864}
        self.__SamAccountType = { "SAM_DOMAIN_OBJECT": 0x0,
        "SAM_GROUP_OBJECT" : 0x10000000,
        "SAM_NON_SECURITY_GROUP_OBJECT" : 0x10000001,
        "SAM_ALIAS_OBJECT" : 0x20000000,
        "SAM_NON_SECURITY_ALIAS_OBJECT" : 0x20000001,
        #"SAM_USER_OBJECT" : 0x30000000,
        "SAM_NORMAL_USER_ACCOUNT" : 0x30000000,
        "SAM_MACHINE_ACCOUNT" : 0x30000001,
        "SAM_TRUST_ACCOUNT" : 0x30000002,
        "SAM_APP_BASIC_GROUP" : 0x40000000,
        "SAM_APP_QUERY_GROUP" : 0x40000001,
        "SAM_ACCOUNT_TYPE_MAX" : 0x7fffffff}

    def __AddObject(self,Objects, ObjType):
        # TODO: set "Domain Controllers" default icon
        if (os.name == "nt"):
            OtherIcon = QIcon("{0}\\resources\\adbox.png".format(os.path.dirname(os.path.abspath(__file__))))
            MainIcon = QIcon("{0}\\resources\\{1}.png".format(os.path.dirname(os.path.abspath(__file__)), ObjType))
        else:
            OtherIcon = QIcon("{0}/resources/adbox.png".format(os.path.dirname(os.path.abspath(__file__))))
            MainIcon = QIcon("{0}/resources/{1}.png".format(os.path.dirname(os.path.abspath(__file__)), ObjType))
        ParentItem = self.__Model.invisibleRootItem()
        if (len(Objects) != 0):
            for Obj in Objects:
                OUArray = Obj[0].split(',')
                RootDC = ""
                LevelCount = 0
                for OUStr in reversed(OUArray):
                    if ("DC=" in OUStr):
                        RootDC = "{0}.{1}".format(OUStr[3:],RootDC)
                        LevelCount+=1
                RootDC = RootDC[:-1]
                ChildRowCount = ParentItem.rowCount()
                if (ChildRowCount != 0):
                    for i in range(0, ChildRowCount):
                        TmpChild = ParentItem.child(i)
                        if (TmpChild.text() == RootDC):
                            ParentItem = TmpChild
                        else:
                            TmpItem = QStandardItem(RootDC)
                            TmpItem.setIcon(OtherIcon)
                            TmpItem.setData("root")
                            ParentItem.appendRow(TmpItem)
                            ParentItem = TmpItem
                else:
                    TmpItem = QStandardItem(RootDC)
                    TmpItem.setIcon(OtherIcon)
                    TmpItem.setData("root")
                    ParentItem.appendRow(TmpItem)
                    ParentItem = TmpItem
                for OUStr in reversed(OUArray[:-LevelCount]):
                    try:
                        TmpStr = OUStr[3:]
                        ChildRowCount = ParentItem.rowCount()
                        AddItem = True
                        if (ChildRowCount != 0):
                            for i in range(0, ChildRowCount):
                                TmpChild = ParentItem.child(i)
                                if (TmpChild.text() == TmpStr):
                                    ParentItem = TmpChild
                                    ParentItem.setIcon(OtherIcon)
                                    AddItem = False
                                    break
                    except Exception as BoxExcept:
                        self.__GUILogger.error("BoxGUI:__AddObject: Exception {0}".format(BoxExcept))

                    if (AddItem):
                        TmpItem = QStandardItem(TmpStr)
                        TmpItem.setIcon(MainIcon)
                        TmpObjData = [ObjType,Obj[2]]
                        TmpItem.setData(TmpObjData)
                        ParentItem.appendRow(TmpItem)
                        ParentItem = TmpItem
                ParentItem = self.__Model.invisibleRootItem()
        else:
            self.__GUILogger.info("BoxGUI:__AddObject: Objects not found")


    def __InitQCompleter(self):
        Settings =  self.__DBObject._GetSettings()
        for CurrentSetting in Settings:
            if(CurrentSetting[0] == "SearchAtt"):
                self.SearchAtt = CurrentSetting[1]
                self.__Completer = QCompleter(self.SearchAtt.split('|')[:-1])
                self.__Edit.setCompleter(self.__Completer)

    def _LoadObject(self):
        self.__Model = QStandardItemModel()
        Objects = self.__DBObject._LoadObject("users")
        self.__AddObject(Objects,"users")
        Objects = self.__DBObject._LoadObject("computers")
        self.__AddObject(Objects,"computers")
        Objects = self.__DBObject._LoadObject("groups")
        self.__AddObject(Objects,"groups")
        self.__InitQCompleter()
        self.__TreeView.setModel(self.__Model)

    @Slot()
    def __TreeViewDoubleClick(self, DCObj):
        StObject = self.__TreeView.model().itemFromIndex(DCObj)
        ObjValue = StObject.text()
        if(StObject.rowCount() == 0):
            self.__GUILogger.debug("BoxGUI:__TreeViewDoubleClick: Object name '{0}'".format(ObjValue))
            RawData = StObject.data()[1]
            if(RawData == None):
                self.__TextEdit.setText("Object not found '{0}'".format(ObjValue))
            else:
                PrintStr = ""
                JsonData = json.loads(RawData)
                for RawKey in JsonData.keys():
                    if (isinstance(JsonData[RawKey], list)):
                        for RawValue in JsonData[RawKey]:
                            PrintStr += "{0}: {1}\n".format(RawKey, RawValue)
                    else:
                        if(RawKey == "userAccountControl"):
                            UACStr = ""
                            for UACKey in self.__UserAccountControls.keys():
                                if(JsonData[RawKey] & self.__UserAccountControls[UACKey] != 0):
                                    UACStr += "{0} ,".format(UACKey)
                            PrintStr += "{0}: {1}\n".format(RawKey, UACStr[:-1])
                        elif(RawKey == "accountExpires"):
                            if(JsonData[RawKey] == "9999-12-31 23:59:59.999999+00:00"):
                                PrintStr += "{0}: ACCOUNT_DONT_EXPIRE\n".format(RawKey, JsonData[RawKey])
                            else:
                                PrintStr += "{0}: {1}\n".format(RawKey, JsonData[RawKey])
                        elif(RawKey == "sAMAccountType"):
                            UACStr = ""
                            for UACKey in self.__SamAccountType.keys():
                                if(JsonData[RawKey] == self.__SamAccountType[UACKey]):
                                    UACStr += "{0} ,".format(UACKey)
                                    break
                            PrintStr += "{0}: {1}\n".format(RawKey, UACStr[:-1])
                        else:
                            PrintStr += "{0}: {1}\n".format(RawKey, JsonData[RawKey])
                self.__TextEdit.setText(PrintStr)

    def __ExpandedViewObject(self, Obj, ExpType):
        self.__TreeView.setExpanded(Obj.index(), ExpType)
        if(Obj.parent() != None):
            self.__ExpandedViewObject(Obj.parent(), ExpType)

    @Slot()
    def __SearchObjects(self):
        SearchText = self.__Edit.text()
        SearchObj = BoxSearch.BoxSearch(SearchText, self.SearchAtt, self.__GUILogger)
        ParentItem = self.__Model.invisibleRootItem()
        SearchObj._Search(ParentItem, self.__TreeView)