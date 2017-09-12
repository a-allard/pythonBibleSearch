class strReferenceList(list):

    def __init__(self,dictionary,initvals=[]):
        if not isinstance(dictionary,dict):
            return None
        for value in dictionary.values():
            if not isinstance(value,int):
                return None
            
        self.dict=dictionary


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
        #return index
        return list.__getitem__(self,index)
