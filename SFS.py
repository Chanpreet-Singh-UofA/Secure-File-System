#*-------------------------------------------*
# Project 1:- SFS
#
# Group members:- Chanpreet and Gurbani
#*-------------------------------------------*

import os
import sqlite3

class Group:
    def __init__(self, groupName):
        self.groupName = groupName
        self.userNames = []

    def printGroup(self):
        print("groupName " + self.groupName)
        print(self.userNames)

    def AddUser(self,name):
        self.userNames.append(name)



if __name__ == '__main__':
    print("*-------------------------------------------*")
    print("The Secure File System")
    print("*-------------------------------------------*")

    directory = os.getcwd()
    print(directory)
    sfsDirectory = os.getcwd()

    groupList = []
    sfs = directory+">>SFS>>"
    sfst=">>SFS>>"

    connection = sqlite3.connect("SFS.db")
    cur = connection.cursor()
    #already in DB
    #CREATE TABLE sfsFiles( fileUserName TEXT PRIMARY KEY, fileDirectory TEXT, fileContent TEXT, fileName TEXT, filePermission TEXT, FOREIGN KEY (fileUserName) REFERENCES sfsUsers (userName) )
    #CREATE TABLE sfsUsers ( userName TEXT PRIMARY KEY, groupName TEXT, homeDirectory TEXT )
    cur.execute("SELECT * FROM sfsUsers")
    records = cur.fetchall()
    #print(type(records))
    #print(records[0][1])

    exit()

    while(True):
        
        command = input(sfs).strip()

        if (command.find("mkgroup")!=-1):      # mkgroup groupA
            groupName= command.split(" ",1)
            groupList.append(Group(groupName[1]))
            print("Group Created: "+groupName[1])
            os.chdir(sfsDirectory)
            os.mkdir(groupName[1]) 
            os.chdir(groupName[1])
            sfs = os.getcwd()+sfst


        elif(command.find("mkuser")!=-1):      # mkuser groupA user1
            userGroup= command.split(" ",2)
            
            userGroupIndex = (next(filter(lambda x: x[1].groupName == userGroup[1], enumerate(groupList)))[0])
            groupList[userGroupIndex].AddUser(userGroup[2])
            print("User Created: "+userGroup[2]+ " in group: " +userGroup[1])
            os.chdir(sfsDirectory+"/"+userGroup[1])
            os.mkdir(userGroup[2]) 
            os.chdir(userGroup[2])
            sfs = os.getcwd()+sfst

        elif(command.find("mkdir")!=-1):
            command= command.split(" ",1)
            os.mkdir(command[1]) 
            sfs = os.getcwd()+sfst

        elif(command.find("cd")!=-1):
            command= command.split(" ",1)
            sfsDirectory = os.getcwd()
            os.chdir(command[1])
            sfs = os.getcwd()+sfst
            

