import random


def string(Any) -> str:
    string = Any.__string__()
    if type(string) != str:
        raise TypeError(f"__string__() should return str, not '{type(string).__name__}'")
    else:
        return string
class rstring:
    def __init__(this,string) -> None:
        if type(string) == str:
            this.this = this
            this.__string = string

        else:
            raise TypeError(f"rstring() requires str type, not \"{type(string).__name__}\"")
    def toString(this):
        return this.__string
    def __string__(this):
        return this.__string
    def reverse(this) -> object:
        i = 0
        __str__ = ""
        for i in range(len(this.__string)):
            __str__ = __str__ + this.__string[len(this.__string)-1-i]
            i = i + 1
        return rstring(__str__)
    def replace(this,old,new):
        this.__string:str
        old:rstring
        new:rstring
        return rstring(this.__string.replace(old.__string,new.__string))
    def split(this,__rstring__:object):
        __rstring__:rstring
        return this.__string.split(__rstring__.__string)
    def upset(this):
        __lists__ = list(this.__string)
        __strs__ = ""
        i = 0
        random.shuffle(__lists__)
        for i in range(len(__lists__)):
            __strs__ = __strs__ + __lists__[i]
            i = i + 1
        return rstring(__strs__)
    def __add__(this,__rstring__:object):
        __rstring__:rstring
        return rstring(this.__string + __rstring__.__string)
    def __mul__(this,number:int):
        __rstring__:rstring
        return rstring(this.__string * number)
    def __repr__(self) -> str:
        strings = self.__string.replace("\\","\\\\").replace("\"","\\\"")
        return f"rstring(\"{strings}\")"


class rclipboard:
    def __init__(self) -> None:
        self.__app = __import__("clipboard")
    def write(self,content:rstring) -> None:
        if type(content) != rstring:
            raise TypeError(f"rclipboard() requires rstring type, not \"{type(string).__name__}\"")
        self.__app.copy(content.toString())
    def read(self) -> rstring:
        return rstring(self.__app.paste())
    def __del__(self) -> None:
        del self.__app
    def __str__(self) -> str:
        return "rclipboard()"
    def __repr__(self) -> str:
        return "rclipboard()"
