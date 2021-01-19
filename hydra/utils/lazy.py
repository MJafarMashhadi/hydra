class LazyLoaded():
    def __init__(self, func, name=None):
        self.func = func
        self.name = name if name is not None else func.__name__
        self.__doc__ = func.__doc__
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.get_value(instance)
    
    def get_value(self, instance):
        res = self.func(instance)
        setattr(instance, self.name, res)
        return res

