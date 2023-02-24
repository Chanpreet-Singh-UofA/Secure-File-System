#*-------------------------------------------*
# Project 1:- SFS
#
# Group members:- Chanpreet and Gurbani
#*-------------------------------------------*

import os
import sqlite3
import time




class Group:
    def __init__(self, groupName):
        self.groupName = groupName
        self.userNames = []

    def printGroup(self):
        print("groupName " + self.groupName)
        print(self.userNames)

    def AddUser(self,name):
        self.userNames.append(name)

#https://likegeeks.com/python-caesar-cipher/
def cipher_encrypt(plain_text, key):
    encrypted = ""
    for c in plain_text:
        if c.isupper(): #check if it's an uppercase character
            c_index = ord(c) - ord('A')
            # shift the current character by key positions
            c_shifted = (c_index + key) % 26 + ord('A')
            c_new = chr(c_shifted)
            encrypted += c_new
        elif c.islower(): #check if its a lowecase character
            # subtract the unicode of 'a' to get index in [0-25) range
            c_index = ord(c) - ord('a') 
            c_shifted = (c_index + key) % 26 + ord('a')
            c_new = chr(c_shifted)
            encrypted += c_new
        elif c.isdigit():
            # if it's a number,shift its actual value 
            c_new = (int(c) + key) % 10
            encrypted += str(c_new)
        else:
            # if its neither alphabetical nor a number, just leave it like that
            encrypted += c
    return encrypted

# The Decryption Function #https://likegeeks.com/python-caesar-cipher/
def cipher_decrypt(ciphertext, key):
    decrypted = ""
    for c in ciphertext:
        if c.isupper(): 
            c_index = ord(c) - ord('A')
            # shift the current character to left by key positions to get its original position
            c_og_pos = (c_index - key) % 26 + ord('A')
            c_og = chr(c_og_pos)
            decrypted += c_og
        elif c.islower(): 
            c_index = ord(c) - ord('a') 
            c_og_pos = (c_index - key) % 26 + ord('a')
            c_og = chr(c_og_pos)
            decrypted += c_og
        elif c.isdigit():
            # if it's a number,shift its actual value 
            c_og = (int(c) - key) % 10
            decrypted += str(c_og)
        else:
            # if its neither alphabetical nor a number, just leave it like that
            decrypted += c
    return decrypted





if __name__ == '__main__':
    print("*-------------------------------------------*")
    print("The Secure File System")
    print("*-------------------------------------------*")

    directory = os.getcwd()+"/SFsystem"
    print(directory)
    sfsDirectory = os.getcwd()+"/SFsystem"

    groupList = []
    sfs = directory+">>SFS>>"
    sfst=">>SFS>>"

    authenticated = 0
    currentUser=""

    connection = sqlite3.connect("SFS.db")
    cursor = connection.cursor()
    #already in DB
    #CREATE TABLE sfsFiles( fileDirectory TEXT PRIMARY KEY, fileName TEXT, fileEncryptedName TEXT, fileContent TEXT,  fileUserName TEXT, filePermission TEXT, fileLastModified TEXT, FOREIGN KEY (fileUserName) REFERENCES sfsUsers (userName) )
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

                #setpermission <filepath> <username> <r-rw-w>

        elif(command.find("mkdir")!=-1):
            if(authenticated == 111):
                command= command.split(" ",1)
                os.mkdir(command[1]) 
                sfs = os.getcwd()+sfst
            else:
                print("You do not have permission to create a directory, please reach out to admin user.")

        elif(command.find("login")!=-1): # login username password
            username = command[1]
            if(username != "admin"):
                root_path=sfsDirectory
                paths = []
                for root, dirs, files in os.walk(root_path):
                    for name in files:
                        paths.append(os.path.join(root, name))
                    for name in dirs:
                        paths.append(os.path.join(root, name))
                print(paths)

                for path in reversed(paths):
                    print(path)
                    fileName = path.split('/')[-1]
                    print("fileName - " +fileName)
                    if not (fileName.startswith('.')):
                        directoryOfFile = path.replace("/"+fileName,"")
                        print("directoryOfFile - " + directoryOfFile)
                        shift = 3
                        print("fileName - " +fileName)
                        decryptedFileName = cipher_decrypt(fileName, shift)
                        print("decryptedFileName - "+decryptedFileName)
                        newpath = directoryOfFile+"/"+decryptedFileName
                        print(newpath)
                        print(path)
                        if os.path.exists(path):
                            os.rename(path,newpath)
                       


            command= command.split(" ")
            username = command[1]
            password = command[2]
            fileUserName = username
            cursor.execute("SELECT COUNT(userName),homeDirectory from sfsUsers WHERE userName=\""+username+ "\" AND userPassword=\""+password+"\"")
            records = cursor.fetchall()
            cursor.execute("SELECT fileName,fileLastModified,fileDirectory from sfsFiles WHERE fileUserName=\""+fileUserName+"\"")
            allRecords = cursor.fetchall()

            
            for record in allRecords:
                storedModifiedTime = record[1]
                actualModifiedTimeRaw = os.path.getmtime(record[2])
                actualModifiedTime = time.ctime(actualModifiedTimeRaw)
                if(storedModifiedTime != actualModifiedTime):
                    print("ALEART: "+record[0]+" was modfied by an external user")

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

            cursor.execute("SELECT fileName,fileLastModified,fileDirectory from sfsFiles WHERE fileUserName=\""+currentUser+"\"")
            allRecords = cursor.fetchall()
            for record in allRecords:
                actualModifiedTimeRaw = os.path.getmtime(record[2])
                actualModifiedTime = time.ctime(actualModifiedTimeRaw)
                cursor.execute("UPDATE sfsFiles SET fileLastModified=\""+actualModifiedTime+"\" WHERE fileDirectory=\""+record[2]+"\"")
                connection.commit()

            root_path=sfsDirectory
            paths = []
            for root, dirs, files in os.walk(root_path):
                for name in files:
                    paths.append(os.path.join(root, name))
                for name in dirs:
                    paths.append(os.path.join(root, name))
            print(paths)



            for path in reversed(paths):
                fileName = path.split('/')[-1]
                if not (fileName.startswith('.')):
                    directoryOfFile = path.replace("/"+fileName,"")
                    shift = 3
                    encryptedFileName = cipher_encrypt(fileName, shift)
                    newpath = directoryOfFile+"/"+encryptedFileName
                    os.rename(path, newpath)







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
            currentDir = os.getcwd() +"/"+ command[1]
            print(currentDir)
            ti_m = os.path.getmtime(currentDir)
            m_ti = time.ctime(ti_m)
            enc_fileName = command[1].encode(encoding='cp037')
            cursor.execute("INSERT INTO sfsFiles VALUES(\""+ currentDir+ "\",\""+command[1] +"\",\""+ str(enc_fileName)  +"\",\""+  "" +"\",\""+ currentUser +"\",\""+ "rwa" +"\",\""+m_ti+"\")")
            connection.commit()
            #old_name = os.getcwd()+"/"+command[1]
            #new_name = os.getcwd()+"/"+str(enc_fileName)+".txt"
            # Renaming the file
            #os.rename(old_name, new_name)  

        elif(command.find("cat")!=-1): #cat user.txt - user to read a file
            command= command.split(" ",1)
            currentDir = os.getcwd()
            print(command[1])
            with open(command[1],'rb') as f:
                encoded_content = f.read()
                if(currentDir.find(currentUser)!=-1):
                    decoded_content = encoded_content.decode(encoding='cp037',errors='strict')
                    print(decoded_content)
                else:
                    print("You do now belong to this directory, thus you cannot read the file.")
                f.close()

        elif(command.find("echo")!=-1): #echo user.txt Hi we are programing 
            command= command.split(" ",2)
            print(command[2])
            str_enc = command[2].encode(encoding='cp037')
            fileDir = os.getcwd()+"/"+command[1]
            ti_m = os.path.getmtime(fileDir)
            m_ti = time.ctime(ti_m)
            with open(command[1],'wb') as f:
                f.write(str_enc)
                cursor.execute("UPDATE sfsFiles SET fileContent=\""+str(str_enc)+"\", fileLastModified=\""+m_ti+"\" WHERE fileDirectory=\""+fileDir+"\"")
                connection.commit()
                f.close()

        elif(command.find("rename")!=-1): #rename oldName newName
            command= command.split(" ",2)
            old_name = os.getcwd()+"/"+command[1]
            new_name = os.getcwd()+"/"+command[2]
            # Renaming the file
            os.rename(old_name, new_name)   

        elif(command.find("exit")!=-1): # exit
            exit()




            

