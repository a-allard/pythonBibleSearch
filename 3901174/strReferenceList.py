import caselessDictionary

class strReferenceList(list):
    """This allows the user to reference a list with string keys much like a dictionaryWhile still having the list feel.  Requires a dictionary with integer values though"""
    def __init__(self,dictionary,initvals=[]):
        self.dict=caselessDictionary.caselessDictionary()
        if not isinstance(dictionary,dict):
            return None
        for value in dictionary.values():
            if not isinstance(value,int):
                return None
        keys=list(dictionary.keys())
        for key in keys:
            val=dictionary[key]
            self.dict[key.lower()]=val


    def __setitem__(self,index,value):
        if isinstance(index,str):
            try:
                index=self.dict[index]
            except:
                raise('Index not found in dictionary')
        list.__setitem__(self,index,value)

    def __getitem__(self,index):
        if isinstance(index,str):
            try:
                index=self.dict[index]
            except:
                raise('Index not found in dictionary')
        return list.__getitem__(self,index)
