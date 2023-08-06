class simpleobject(dict):
    '''Simple json serializable object'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in tuple(self.items()):
            self[key] = self.__so__(value)

    def update(self, other):
        for key, value in other.items():
            self[key] = self.__so__(value)

    def __so__(self, value):
        clazz = type(value)
        if clazz == simpleobject:
            return value
        elif issubclass(clazz, dict):
            return simpleobject(value)
        elif issubclass(clazz, list):
            return [self.__so__(v) for v in value]
        elif issubclass(clazz, tuple):
            return tuple(self.__so__(v) for v in value)
        elif issubclass(clazz, set):
            return {self.__so__(v) for v in value}
        return value

    def __str__(self):
        name_key = '__name__' if '__name__' in self else 'name' if 'name' in self else None
        name = self[name_key] if name_key in self else 'simpleobject'
        values = ', '.join(f'{k}={v!r}' for k,v in self.items() if k != name_key)
        return f'{name}({values})'

    def __repr__(self):
        return self.__str__()

    def __setattr__(self, k, v):
        self[k] = v

    def __getattr__(self, k):
        return self[k]

    def __delattr__(self, k):
        del self[k]
