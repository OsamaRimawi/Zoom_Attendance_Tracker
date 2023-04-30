from Records import *
from Student import *
import argparse  # for the option parser
import os  # open a directory and make directory functions
import datetime  # to create time objects
import csv  # to deal with csv files related functions

# Linux Laboratory, ENCS3103
# Project 2 (Python Project)
# Osama Rihami Section (4) Student ID : 1190560
# Mahmoud Qaisi Section (3) Student ID : 1190831

def check_positive(value):
    " To check the value if it is positive (used in the input values in the option parser)"
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


def get_StudentList(path):
    " Reads the Stuudents infromation from the student sheet file and returns a list of student objects "
    file = open(path, "r")
    lines = file.readlines()
    StudentList = []
    for i in range(1, len(lines)):
        id = lines[i].split(',', 2)[0] # to separate the id from the line
        name = lines[i].split(',', 2)[1] # takes the other part of the line
        id = id.replace(" ", "")
        id = int(id)
        name = name.strip() # remove the first space from the string
        name = name.replace("\n", "")
        name = name.replace("'", "")
        name = name.replace("-", "")
        name = name.replace("õ", "") # for the name EID
        StudentList.append(Student(name, id))
    return StudentList


def get_AttendanceList(path):
    " Reads the infromation in the attendance reports file and stores them in a list of Attendance report objects(ARecords) "
    file = open(path, "r")
    lines = file.readlines()
    ARecords = []
    for i in range(1, len(lines)): # excludes the first line because it contains column labels
        str = lines[i].split(',', 2)[0]  # take the first half between the minutes and the mixture of name+id
        mint = lines[i].split(',', 2)[1] # mint stores the number of minutes a student attended
        mint = mint.strip()
        mint = mint.replace("\n", "")  # these lines will remove some special charchters that might affects comparison process remove
        str = str.replace("\n", "")
        str = str.replace("'", "")
        str = str.replace("-", "")
        str = str.replace(" ", "")
        mint = int(mint)
        A = ARecord(str, mint)
        ARecords.append(A)
    return ARecords


def get_ParticList(path):
    " Reads the infromation in the participation reports file and stores them in a list of Participation report objects(PRecords) "
    PRecords = []
    file = open(path, encoding='utf-8') # to deal with arabic language characters
    lines = file.readlines()
    for i in range(0, len(lines)):
        str = lines[i]
        if len(str) <= 3 or str[2] != ":":  # for lines that are only chat part related to the name before it
            continue

        time = lines[i].split("From")  # to seperate the time from the rest of the line
        hour = time[0].split(':', 2)[0]
        mint = time[0].split(':', 2)[1]
        sec = time[0].split(':', 2)[2]

        str = str.replace("\n", "") # these lines will remove some special charchters that might affects comparison process remove
        str = str.replace("'", "")
        str = str.replace("-", "")

        P = PRecord(str, datetime.time(int(hour), int(mint), int(sec)))
        PRecords.append(P)
    return PRecords


def Set_slimit(time, x):
    "Sets the lower limit (Tb) in the specified time interval "
    sec = time.second
    min = time.minute + x  # x is value of Tb
    hour = time.hour
    if min >= 60:
        hour += 1
        min = min - 60
    return datetime.time(hour, min, sec)


def Set_flimit(time, x):
    "Sets the lower limit (Te) in the specified time interval "
    sec = time.second
    min = time.minute - x
    hour = time.hour
    if min < 0:
        hour -= 1
        min = 60 + min
    return datetime.time(hour, min, sec)


if __name__ == '__main__':  # the following few lines are the code for the option parser
    parser = argparse.ArgumentParser()
    parser.add_argument("SLPath", help="Full Path to The Folder where the Sheet list Fill is")
    parser.add_argument("ARPath", help="Full Path to The Folder where the Attendance Records are")
    parser.add_argument("PRPath", help="Full Path to The Folder where the Attendance Records are")
    parser.add_argument("OPath", help="Full Path to The Folder where the output files will be saved")
    parser.add_argument("--P", default=0, type=check_positive, help="Minimum Attendance Minutes")
    parser.add_argument("--Tb", default=0, type=check_positive, help="Initial interval limit")
    parser.add_argument("--Te", default=0, type=check_positive, help="Final interval limit")
    args = parser.parse_args()

StudentList = []
ListFiles = os.listdir(args.SLPath)  # save the names of the files in the directory inside a list
for listfile in ListFiles:
    path = args.SLPath + "\\" + listfile  # update the path to reach the file inside the directory
    StudentList = get_StudentList(path)

ADirPath = args.OPath + '\\' + 'Nonvalid Meeting Attendance reports'
if not os.path.exists(ADirPath):  # create a directory with the path value if it doesn't exist
    os.mkdir(ADirPath)

ARecords = []
AttenFiles = os.listdir(args.ARPath)
for attenReport in AttenFiles:
    path = args.ARPath + "\\" + attenReport
    ARecords = get_AttendanceList(path)
    for x in StudentList:  # for every student in the list search for his name in the attendance list
        flag = 0
        for y in ARecords: # it will look for the name if it was found it will check the time limit according to P
            if y.CompareToStudent(x.get_firstName(), x.get_lastName()) and y.CheckTimeLimit(args.P):
                flag = 1 # this flag will change to one if the student was found and will be registered as present
        if flag == 1:
            x.append_AttList('x')
        else:  # if the student name wasn't found the flag will still be at zero and the stidnent will be registred as absent
            x.append_AttList('a')
    attenReport = attenReport.split('.')  # this line will remove the file extension
    ANonpath = ADirPath + '\\' + attenReport[0] + '-NV.csv'  # add a new part to the name and the new extension
    open(ANonpath, 'a').close() # create a new file with the specified path for non valid attendance reports
    file = open(ANonpath, "w")
    firstRow = ['Name (Original Name)', 'Total Duration (Minutes)'] # the first line in the fine (column labels)
    writer = csv.writer(file)  # writer object that writes in csv files
    writer.writerow(firstRow)  # this function allows the writer to write one row in a csv file
    for i in ARecords:  # this loop will check records with flag zero (non valid) and prints them
        if i.getFlag() == 0:
            RowList = []
            # this list will be filled with the row information
            RowList.append(i.getName())
            RowList.append(i.getMinuates())
            writer.writerow(RowList)

PDirPath = args.OPath + '\\' + 'Nonvalid Meeting Participation Reports'
if not os.path.exists(PDirPath): # as mentioned before ...
    os.mkdir(PDirPath)
PRecords = []
PartFiles = os.listdir(args.PRPath)
for PartReport in PartFiles:
    path = args.PRPath + "\\" + PartReport
    PRecords = get_ParticList(path)

    slimit = Set_slimit(PRecords[0].getTime(), args.Tb) # sets the lower limit
    flimit = Set_flimit(PRecords[len(PRecords) - 1].getTime(), args.Te) # sets the upper limit

    for x in StudentList: # this loop will count the number of times a student participated in one lecture
        c = 0  # the counter
        for y in PRecords: # checks the name and the time interval
            if y.CompareToStudent(x.get_firstName(), x.get_lastName()) and y.CheckTimeLimit(slimit, flimit):
                c += 1
        x.append_PaList(c)

    PartReport = PartReport.split('.')  # these lines will handle the naming convention fro the non valid participation reports
    PNonpath = PDirPath + '\\' + PartReport[0] + '-NV.txt'
    open(PNonpath, 'a').close()
    file = open(PNonpath, "w", encoding='utf-8') # the encoding is to print arabic characters
    for i in PRecords:
        if i.getFlag() == 0:
            file.write(i.getName() + '\n')

AttOut = args.OPath + '\\' + 'Class Attendance Sheet.csv'
PartOut = args.OPath + '\\' + 'Class Score sheet.csv'

open(AttOut, 'a').close()
open(PartOut, 'a').close()

FileA = open(AttOut, "w")
firstRow = []
# the first row in the Attendance output file
firstRow.append('student ID')
firstRow.append('Student Name')

for i in AttenFiles:  # to write the dates of the lectures in the first row
    a = i.split('-')
    a = a[1] + '-' + a[2] + '-' + a[3]
    firstRow.append(a)

writer = csv.writer(FileA)
writer.writerow(firstRow)
for i in StudentList: # this loop will print a line that contains the id the full name and the attendance list
    RowList = []
    RowList.append(i.get_ID())
    RowList.append(i.get_name())
    for y in i.get_AttList():
        RowList.append(y)
    writer.writerow(RowList)

FileP = open(PartOut, "w")

writer1 = csv.writer(FileP)
writer1.writerow(firstRow)
for i in StudentList: # this loop will print a line that contains the id the full name and the participation list
    RowList = []
    RowList.append(i.get_ID())
    RowList.append(i.get_name())
    for y in i.get_PaList():
        RowList.append(y)
    writer1.writerow(RowList)

# Before you run the file you must remove the previous output files first in order to change them
# we did write a code that will remove the files if they existed but it requires administrative access so we removed it