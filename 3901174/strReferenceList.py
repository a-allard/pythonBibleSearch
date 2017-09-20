import caselessDictionary

class strReferenceList(list):
    """This allows the user to reference a list with string keys much like a dictionary
    While still having the list feel.
    Requires a dictionary with integer values though.
    Uses the caselessDictionary to simplify things.  Could be modified to use case."""
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

# setitem setup to check the dictionary for a key if the input is not an integer.
# Will still use an integer as normal if one is probvided
    def __setitem__(self,index,value):
        if isinstance(index,str):
            try:
                index=self.dict[index]
            except:
                raise('Index not found in dictionary')
        list.__setitem__(self,index,value)
# Similar to above but getitem instead of set.
    def __getitem__(self,index):
        if isinstance(index,str):
            try:
                index=self.dict[index]
            except:
                raise('Index not found in dictionary')
        return list.__getitem__(self,index)
