class sort:
    def __init__(self,lists:list) -> None:
        self.lists = lists
    def Bubbling(self):
        lists = self.lists
        for i in range(0, len(lists)):
            for j in range(1, len(lists) - i):
                if (lists[j] < lists[j - 1]):
                    c = lists[j]
                    lists[j] = lists[j - 1]
                    lists[j - 1] = c
        return lists
    def Diving(self):
        lists = self.lists
        for i in range(0, len(lists)):
            for j in range(1, len(lists) - i):
                if (lists[j] > lists[j - 1]):
                    c = lists[j]
                    lists[j] = lists[j - 1]
                    lists[j - 1] = c
        return lists
    def Search(self,texts=""):
        __search__ = []
        lists = self.lists
        for __count__ in range(0,len(list(lists))):
            if texts in list(lists)[__count__]:
                __search__.append(list(lists)[__count__])
        return __search__

