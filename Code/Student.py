class Student: # every student object has a
    def __init__(self,nm,id):
        self.__name = nm # name
        self.__firstName= nm.split(' ', 4)[0]
        self.__lastName= nm.split(' ', 4)[3]

        self.__ID = id # id
        self.__AttList = []  # attendance list ( contains attendance information for all the lectures )
        self.__PaList = []  # participation list ( contains participation information for all the lectures )

    def get_name(self):  # setters and  getters
        return self.__name

    def get_firstName(self):
        return self.__firstName

    def get_lastName(self):
        return self.__lastName

    def set_name(self, nm):
        self.__name = nm
        self.__firstName= nm.split(' ', 4)[0]
        self.__lastName= nm.split(' ', 4)[3]

    def get_ID(self):
        return self.__ID

    def set_ID(self, id):
        self.__ID = id

    def get_AttList(self):
        return self.__AttList

    def set_AttList(self, val, i):
        self.__AttList[i] = val

    def append_AttList(self, val):  # append an element to the attendance list
        self.__AttList.append(val)

    def get_PaList(self):
        return self.__PaList

    def set_PaList(self, val, i):
        self.__PaList[i] = val

    def append_PaList(self, val):  # append an element to the attendance list
        self.__PaList.append(val)