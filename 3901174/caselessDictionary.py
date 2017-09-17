class caselessDictionary(dict):
    """Dictionary that enables case insensitive searching while preserving case sensitivity 
when keys are listed, ie, via keys() or items() methods. 

Works by storing a lowercase version of the key as the new key and stores the original key-value 
pair as the key's value (values become dictionaries)."""

    def __init__(self, initval={}):
        if isinstance(initval, dict):
            for key, value in initval.__iter__():
                self.__setitem__(key, value)
        elif isinstance(initval, list):
            for (key, value) in initval:
                self.__setitem__(key, value)
            
    def __contains__(self, key):
        return dict.__contains__(self, key.lower())
  
    def __getitem__(self, key):
        return dict.__getitem__(self, key.lower())
  
    def __setitem__(self, key, value):
        return dict.__setitem__(self, key.lower(), value)

    def get(self, key, default=None):
        try:
            v = dict.__getitem__(self, key.lower())
        except KeyError:
            return default
        else:
            return v['val']

    def has_key(self,key):
        if self.get(key):
            return True
        else:
            return False    

    def items(self):
        return [(v['key'], v['val']) for v in dict.itervalues(self)]
    
    def keys(self):
        return dict.keys(self)
    
    def values(self):
        return dict.values(self)
    
    def __iter__(self):
        for v in dict.values(self):
            yield v['key'], v['val']
        
##    def keys(self):
##        for v in dict.values(self):
##            yield v['key']
##        
##    def values(self):
##        for v in dict.values(self):
##            yield v['val']
