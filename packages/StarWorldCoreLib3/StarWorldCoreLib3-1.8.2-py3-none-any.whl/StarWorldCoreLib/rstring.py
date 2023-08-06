import random

"""
 ____  _           __        __         _     _  ____               _     _ _    _____       ____  ____  _        _             
/ ___|| |_ __ _ _ _\ \      / /__  _ __| | __| |/ ___|___  _ __ ___| |   (_) |__|___ /      |  _ \/ ___|| |_ _ __(_)_ __   __ _ 
\___ \| __/ _` | '__\ \ /\ / / _ \| '__| |/ _` | |   / _ \| '__/ _ \ |   | | '_ \ |_ \ _____| |_) \___ \| __| '__| | '_ \ / _` |
 ___) | || (_| | |   \ V  V / (_) | |  | | (_| | |__| (_) | | |  __/ |___| | |_) |__) |_____|  _ < ___) | |_| |  | | | | | (_| |
|____/ \__\__,_|_|    \_/\_/ \___/|_|  |_|\__,_|\____\___/|_|  \___|_____|_|_.__/____/      |_| \_\____/ \__|_|  |_|_| |_|\__, |
                                                                                                                           |___/ 
"""

def string(Any) -> str:
    """
    Convert some special characters into strings.
    """
    string = Any.__string__()
    if type(string) != str:
        raise TypeError(f"__string__() should return str, not '{type(string).__name__}'")
    else:
        return string
class rstring:
    def __init__(this,string) -> None:
        """
        The 'string' parameter is used to convert to the rstring class. You can use rstring('some texts').toString() to convert to string.
        """
        if type(string) == str:
            this.this = this
            this.__string = string
        else:
            raise TypeError(f"rstring() requires str type, not \"{type(string).__name__}\"")
    def toString(this):
        """
        Convert rstring to string.
        """
        return this.__string
    def __string__(this):
        """
        Special function created for string() function.
        """
        return this.__string
    def reverse(this) -> object:
        """
        Reverse the rstring.
        """
        i = 0
        __str__ = ""
        for i in range(len(this.__string)):
            __str__ = __str__ + this.__string[len(this.__string)-1-i]
            i = i + 1
        return rstring(__str__)
    def replace(this,old,new):
        """
        Replace the old rstring with new rstring.
        """
        this.__string:str
        old:rstring
        new:rstring
        return rstring(this.__string.replace(old.__string,new.__string))
    def split(this,__rstring__:object):
        """
        Split the rstring with the rstring.
        """
        __rstring__:rstring
        return this.__string.split(__rstring__.__string)
    def upset(this):
        """
        Disrupt rstring.
        """
        __lists__ = list(this.__string)
        __strs__ = ""
        i = 0
        random.shuffle(__lists__)
        for i in range(len(__lists__)):
            __strs__ = __strs__ + __lists__[i]
            i = i + 1
        return rstring(__strs__)
    def __add__(this,__rstring__:object):
        """
        rstring + rstring
        """
        __rstring__:rstring
        return rstring(this.__string + __rstring__.__string)
    def __mul__(this,number:int):
        """
        rstring * int
        """
        __rstring__:rstring
        return rstring(this.__string * number)
    def __repr__(self) -> str:
        """
        Repeat rstring
        """
        strings = self.__string.replace("\\","\\\\").replace("\"","\\\"")
        return f"rstring(\"{strings}\")"


class rclipboard:
    def __init__(self) -> None:
        """
        Initialize rclipboard.
        """
        self.__app = __import__("clipboard")
    def write(self,content:rstring) -> None:
        """
        write rstring to clipboard.
        """
        if type(content) != rstring:
            raise TypeError(f"rclipboard() requires rstring type, not \"{type(string).__name__}\"")
        self.__app.copy(content.toString())
    def read(self) -> rstring:
        """
        read rstring from clipboard.
        """
        return rstring(self.__app.paste())
    def __del__(self) -> None:
        """
        Delete rclipboard.
        """
        del self.__app
    def __str__(self) -> str:
        """
        rclipboard to string.
        """
        return self.read().toString()
    def __repr__(self) -> str:
        """
        Repeat rclipboard.
        """
        return "rclipboard()"
