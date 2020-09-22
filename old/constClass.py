# Constant base class used to create Constants in python
class Const: 
    """
    forbids to overwrite existing variables 
    forbids to add new values if "locked" variable exists
    """ 
    def __setattr__(self,name,value):
        if("locked" in self.__dict__):    
            raise NameError("Class is locked can not add any attributes (%s)"%name)
        if (name in self.__dict__):
            raise NameError("Can't rebind const(%s)"%name)
        self.__dict__[name]=value