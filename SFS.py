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

    authenticated = 0
    currentUser=""

    connection = sqlite3.connect("SFS.db")
    cursor = connection.cursor()
    #already in DB
    #CREATE TABLE sfsFiles( fileDirectory TEXT PRIMARY KEY, fileName TEXT, fileEncryptedName TEXT, fileContent TEXT,  fileUserName TEXT, filePermission TEXT, FOREIGN KEY (fileUserName) REFERENCES sfsUsers (userName) )
    #CREATE TABLE sfsUsers ( userName TEXT PRIMARY KEY, groupName TEXT, userPassword, homeDirectory TEXT )
    #cur.execute("SELECT * FROM sfsUsers")
    #records = cur.fetchall()
    #print(type(records))
    #print(records[0][1])


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


        elif(command.find("mkuser")!=-1):      # mkuser groupA username1 password1  
            if(authenticated == 111):
                userGroup= command.split(" ",3)
                #userGroupIndex = (next(filter(lambda x: x[1].groupName == userGroup[1], enumerate(groupList)))[0])
                #groupList[userGroupIndex].AddUser(userGroup[2])
                print("User Created: "+userGroup[2]+ " in group: " +userGroup[1])
                os.chdir(sfsDirectory+"/"+userGroup[1])
                os.mkdir(userGroup[2]) 
                os.chdir(userGroup[2])
                cursor.execute("INSERT INTO sfsUsers VALUES(\""+userGroup[2]+"\",\""+userGroup[1]+"\",\""+userGroup[3]+"\",\""+os.getcwd()+"\")")
                sfs = os.getcwd()+sfst
                connection.commit()
            else:
                print("You do not have permission to create a users, please reach out to admin user.")

        elif(command.find("mkdir")!=-1):
            if(authenticated == 111):
                command= command.split(" ",1)
                os.mkdir(command[1]) 
                sfs = os.getcwd()+sfst
            else:
                print("You do not have permission to create a directory, please reach out to admin user.")

        elif(command.find("login")!=-1): # login username password
            command= command.split(" ")
            username = command[1]
            password = command[2]
            cursor.execute("SELECT COUNT(userName),homeDirectory from sfsUsers WHERE userName=\""+username+ "\" AND userPassword=\""+password+"\"")
            records = cursor.fetchall()
            print(records[0])
            if(records[0][0] == 1):
                print("Log in Successful. Welcome "+username)
                os.chdir(records[0][1]) 
                currentUser=username
                if(username == "admin" and password == "admin"):
                    authenticated = 111
                else:
                    authenticated = 1
                sfs = os.getcwd()+sfst
            else:
                print("Log in Unsuccessful. Try again.")

        elif(command.find("logout")!=-1): # logout
            print("Log out Successful. Thank you")
            os.chdir(sfsDirectory) 
            authenticated = 0
            sfs = os.getcwd()+sfst

        elif(command.find("cd")!=-1): # need full URL - /Users/chanpreet/Desktop/SFS/Secure-File-System/groupA/user3
            command= command.split(" ",1)
            changeToDir = command[1].replace(sfsDirectory+"/","")
            changeToDir= changeToDir.split("/",1)
            changeToDir = changeToDir[0]
            currentDir = os.getcwd()

            if(currentDir.find(changeToDir)!=-1):
                os.chdir(command[1])
                sfs = os.getcwd()+sfst
            else:
                print("You do not belong to "+changeToDir+". Thus, you cannot access that directory.")

        elif(command.find("ls")!=-1):
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            for f in files:
                #if(f.find("\\x")):
                    #decoded_fileName = f.decode(encoding='cp037')
                    #print(decoded_fileName)
                #else:
                print(f)

        elif(command.find("pwd")!=-1):
            print(os.getcwd())
        
        elif(command.find("touch")!=-1): #touch user.txt - used to create a new file
            command= command.split(" ",1)
            os.close(os.open(command[1], os.O_CREAT))
            currentDir = os.getcwd()
            enc_fileName = command[1].encode(encoding='cp037')
            cursor.execute("INSERT INTO sfsFiles VALUES(\""+ (currentDir+"/"+command[1])  +"\",\""+ command[1] +"\",\""+ str(enc_fileName)  +"\",\""+  "" +"\",\""+ currentUser +"\",\""+ "rwa" +"\")")
            connection.commit()
            #old_name = os.getcwd()+"/"+command[1]
            #new_name = os.getcwd()+"/"+str(enc_fileName)+".txt"
            # Renaming the file
            #os.rename(old_name, new_name)  

        elif(command.find("cat")!=-1): #cat user.txt - user to read a file
            command= command.split(" ",1)
            currentDir = os.getcwd()
            with open(command[1],'rb') as f:
                encoded_content = f.read()
                if(currentDir.find(currentUser)!=-1):
                    decoded_content = encoded_content.decode(encoding='cp037',errors='strict')
                    print(decoded_content)
                else:
                    print("You do now belong to this directory, thus you can read the file.")
                f.close()

        elif(command.find("echo")!=-1): #echo user.txt Hi we are programing 
            command= command.split(" ",2)
            print(command[2])
            str_enc = command[2].encode(encoding='cp037')
            fileDir = os.getcwd()+"/"+command[1]
            with open(command[1],'wb') as f:
                f.write(str_enc)
                cursor.execute("UPDATE sfsFiles SET fileContent=\""+str(str_enc)+"\" WHERE fileDirectory=\""+fileDir+"\"")
                connection.commit()
                f.close()

        elif(command.find("rename")!=-1): #rename oldName newName
            command= command.split(" ",2)
            old_name = os.getcwd()+"/"+command[1]
            new_name = os.getcwd()+"/"+command[2]
            # Renaming the file
            os.rename(old_name, new_name)

        #Setting File & Directory Permissions 
        
        #authenticate user? -- pending 
        if (command.find("user")!=-1):          #user - default mode
            given_path = input("Please enter the directory or file you want to set permissions for: ")
            os.chmod(given_path, 0o600)         #set the permissions for read and write for the owner only
            
            permissions = os.stat(given_path).st_mode  #get permissions info
            #check if the permissions were successfully granted to the owner only
            if permissions & 0o600:
                print("Permissions successfully granted to the owner only!")
            
        elif (command.find("group")!=-1):       #group - all members of the group have read and write permissions
            given_path = input("Please enter the directory or file you want to set permissions for: ")
            os.chmod(given_path, 0o060)         #set the permissions for read and write for the group only
            
            permissions = os.stat(given_path).st_mode  #get permissions info
            #check if the permissions were successfully granted to the group only
            if permissions & 0o060:
                print("Permissions successfully granted to the group only!")

        elif (command.find("internal")!=-1):    #internal - all internal users have read and write permissions
            given_path = input("Please enter the directory or file you want to set permissions for: ")     #set the permissions for read and write for the internal users only
            os.chmod(given_path, 0o066)

            permissions = os.stat(given_path).st_mode  #get permissions info
            #check if the permissions were successfully granted to the internal users only
            if permissions & 0o066:
                print("Permissions successfully granted to the internal users only!")

        elif (command.find("all")!=-1):         #all - all users i.e., owner, group and internal users have read and write permissions
            given_path = input("Please enter the directory or file you want to set permissions for: ")         #set the permissions for read and write for all users i.e., owner, group and internal users
            os.chmod(given_path, 0o666)

            permissions = os.stat(given_path).st_mode  #get permissions info
            #check if the permissions were successfully granted to all users
            if permissions & 0o066:
                print("Permissions successfully granted to all users!")   

        elif(command.find("exit")!=-1): # exit
            exit()


            

