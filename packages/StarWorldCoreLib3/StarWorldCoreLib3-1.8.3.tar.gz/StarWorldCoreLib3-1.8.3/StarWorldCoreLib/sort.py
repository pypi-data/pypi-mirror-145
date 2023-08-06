"""
 ____  _           __        __         _     _  ____               _     _ _    _____      ____             _   
/ ___|| |_ __ _ _ _\ \      / /__  _ __| | __| |/ ___|___  _ __ ___| |   (_) |__|___ /     / ___|  ___  _ __| |_ 
\___ \| __/ _` | '__\ \ /\ / / _ \| '__| |/ _` | |   / _ \| '__/ _ \ |   | | '_ \ |_ \ ____\___ \ / _ \| '__| __|
 ___) | || (_| | |   \ V  V / (_) | |  | | (_| | |__| (_) | | |  __/ |___| | |_) |__) |_____|__) | (_) | |  | |_ 
|____/ \__\__,_|_|    \_/\_/ \___/|_|  |_|\__,_|\____\___/|_|  \___|_____|_|_.__/____/     |____/ \___/|_|   \__|                                                                                                             
"""

class sorts:
    def __init__(self,lists:list) -> None:
        self.lists = lists
    def Bubbling(self) -> list:
        lists = self.lists
        for i in range(0, len(lists)):
            for j in range(1, len(lists) - i):
                if (lists[j] < lists[j - 1]):
                    c = lists[j]
                    lists[j] = lists[j - 1]
                    lists[j - 1] = c
        return lists
    def Diving(self) -> list:
        lists = self.lists
        for i in range(0, len(lists)):
            for j in range(1, len(lists) - i):
                if (lists[j] > lists[j - 1]):
                    c = lists[j]
                    lists[j] = lists[j - 1]
                    lists[j - 1] = c
        return lists
    def Search(self,texts="") -> list:
        __search__ = []
        lists = self.lists
        for __count__ in range(0,len(list(lists))):
            if texts in list(lists)[__count__]:
                __search__.append(list(lists)[__count__])
        return __search__
    def __str__(self) -> str:
        return str(self.lists)
    def __repr__(self) -> str:
        return str(self.lists)