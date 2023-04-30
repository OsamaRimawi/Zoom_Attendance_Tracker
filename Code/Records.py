from abc import ABCMeta, abstractmethod # for the abstract methods
from re import search  # for the compare functions
import datetime  # to deal with time limitations


class Record(object, metaclass=ABCMeta):


    @abstractmethod
    def __init__(self, name):
        self._name = name # the name here is really a combination of name and or id
        self._flag = 0  # this will determine if the record is valid or not ( 0 is not valid )

    def getName(self):  # setters and getter
        return self._name

    def getFlag(self):
        return self._flag

    def setFlag(self, f):
        self._flag = f

    @abstractmethod
    def CompareToStudent(self, fname, lname):
        pass

    @abstractmethod
    def CheckTimeLimit(self, limit):
        pass


class ARecord(Record):  # Attendance Record child of Record class
    def __init__(self, name, min):
        super().__init__(name)
        self.__min = min  # the number of minutes the student attended

    def setMinuates(self, min):  # setters and getters
        self.__min = min

    def getMinuates(self):
        return self.__min

    def CompareToStudent(self, fname, lname):  # will try to approximate the given name to the name savd inside the record
        name = fname + " " + lname
        if search(name.lower(), self._name.lower()): # the function will disregard the capital letters and spaces in the name
            self._flag = 1  # if the name is found then the record is valid
            return True
        else:
            name = fname+lname # to check th given name without spaces between the first and last name
            if search(name.lower(), self._name.lower()):
                self._flag = 1
                return True
            else:
                return False

    def CheckTimeLimit(self, limit): # this function will check if the minutes are more than the set limit (in P)
        if self.__min > limit:
            return True
        else:
            return False



class PRecord(Record): # Participation Records

    def __init__(self, name, time):
        super().__init__(name)
        self.__time = time  # the time when the student participated

    def setTime(self,H,M,S): # setters and getters
        self.__time = datetime.time(H,M,S)

    def getTime(self):
        return self.__time

    def CompareToStudent(self, fname, lname): # same as above.
        name = fname + " " + lname
        if search(name.lower(), self._name.lower()):
            self.flag = 1
            return True
        else:
            name = fname+lname
            if search(name.lower(), self._name.lower()):
                self.flag = 1
                return True
            else:
                return False

    def CheckTimeLimit(self, slimit, flimit): # this limit will check if the time where the record was sent is inside the limit
        if slimit < self.__time < flimit:  # the limit is Tb and Te
            return True
        else:
            return False