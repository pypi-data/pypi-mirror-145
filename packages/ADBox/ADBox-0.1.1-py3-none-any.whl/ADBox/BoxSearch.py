import re
import json

class BoxSearch(object):
    def __init__(self,SearchText, SearchAtt, Logger):
        ReRquest = "({0})\:[ ]*(.*)".format(SearchAtt[:-1])
        self.__ParseSearchResult = re.findall(ReRquest, SearchText)
        self.__SearchLogger = Logger
        self._Type = "default" # default/attribute/custom_request
        self.__SearchString = SearchText
        if(len(self.__ParseSearchResult) != 0): # AttributeSearch
            self._Type = "attribute"
            self.__SearchAttribute = self.__ParseSearchResult[0][0]
            self.__SearchString = self.__ParseSearchResult[0][1]
        else: # Custom Request
            pass
            # TODO: Custom Request
        self.__SearchLogger.debug("BoxSearch:__init__: Search type - {0}".format(self._Type))
        self.__SearchLogger.debug("BoxSearch:__init__: Search value - {0}".format(self.__SearchString))


    def __ExpandedViewObject(self, Obj, ExpType, BoxGUITreeView):
        BoxGUITreeView.setExpanded(Obj.index(), ExpType)
        if(Obj.parent() != None):
            self.__ExpandedViewObject(Obj.parent(), ExpType, BoxGUITreeView)

    def _Search(self, ParentItem, BoxGUITreeView):
        ChildRowCount = ParentItem.rowCount()
        for i in range(0, ChildRowCount):
            TmpChild = ParentItem.child(i)
            if (TmpChild.rowCount() == 0):
                if (self.__SearchString == ""):
                    BoxGUITreeView.setRowHidden(i, ParentItem.index(), False)
                    self.__ExpandedViewObject(ParentItem, False, BoxGUITreeView)
                else:
                    if(self._Type == "default"):
                        TargetText = TmpChild.text()
                    elif(self._Type == "attribute"):
                        TargetText = ""
                        JsonObj = json.loads(TmpChild.data()[1])
                        if(self.__SearchAttribute in JsonObj.keys()):
                            Target = JsonObj[self.__SearchAttribute]
                            if (isinstance(Target, list)):
                                for CurrentValue in Target:
                                    TargetText += "{0}|".format(CurrentValue)
                            elif (isinstance(Target, int)):
                                TargetText = str(Target)
                            else:
                                TargetText = Target
                    if (self.__SearchString not in TargetText):
                        BoxGUITreeView.setRowHidden(i, ParentItem.index(), True)
                    else:
                        BoxGUITreeView.setRowHidden(i, ParentItem.index(), False)
                        self.__ExpandedViewObject(ParentItem, True, BoxGUITreeView)
            else:
                self._Search(TmpChild, BoxGUITreeView)