#*-------------------------------------------*
# Project 1:- SFS
#
# Group members:- Chanpreet and Gurbani
#*-------------------------------------------*

import os
import sqlite3
import time

readUsers = []
writeUsers = []



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
    at_end_encrypt_these_paths = []

    connection = sqlite3.connect("SFS.db")
    cursor = connection.cursor()


    while(True):
        
        command = input(sfs).strip()

        try:
            
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

            elif(command.find("setpermission")!=-1):    # setpermission path username permission   (setpermission groupA/user1/test.txt gb12 rw) r - read only ; w - write only; rw - read write both
                given_path = command.split(" ")[1]
                temp_lis = given_path.split("/")
                file_name =temp_lis[len(temp_lis)-1]     
                given_user = command.split(" ")[2]
                permission = command.split(" ")[3]

                if (permission == "r"):
                    cursor.execute("SELECT (readPermission) FROM sfsFiles WHERE fileName = ?", (file_name,))
                    if (cursor.fetchone()[0]!=None):
                        read_result = cursor.fetchone()[0]
                        u = read_result + "," + given_user
                    else:
                        u = given_user
                    cursor.execute('UPDATE sfsFiles SET readPermission = ? WHERE fileName = ?', (u, file_name))
                    connection.commit()

                elif (permission == "w"):
                    cursor.execute("SELECT (writePermission) FROM sfsFiles WHERE fileName = ?", (file_name,))
                    if (cursor.fetchone()[0]!=None):
                        write_result = cursor.fetchone()[0]
                        u = write_result + "," + given_user
                    else:
                        u = given_user
                    cursor.execute('UPDATE sfsFiles SET writePermission = ? WHERE fileName = ?', (u, file_name))
                    connection.commit()

                elif (permission == "rw"):
                    cursor.execute("SELECT (readPermission) FROM sfsFiles WHERE fileName = ?", (file_name,))
                    if (cursor.fetchone()[0]!=None):
                        read_result = cursor.fetchone()[0]
                        u1 = read_result + "," + given_user
                    else:
                        u1 = given_user
                
                    cursor.execute("SELECT (writePermission) FROM sfsFiles WHERE fileName = ?", (file_name,))
                    if (cursor.fetchone()[0]!=None):
                        write_result = cursor.fetchone()[0]
                        u2 = write_result + "," + given_user
                    else:
                        u2 = given_user
                    
                    cursor.execute('UPDATE sfsFiles SET readPermission = ? WHERE fileName = ?', (u1, file_name))
                    cursor.execute('UPDATE sfsFiles SET writePermission = ? WHERE fileName = ?', (u2, file_name))
                    connection.commit()
                

            elif(command.find("login")!=-1): # login username password
                command= command.split(" ")
                username = command[1]
                password = command[2]

                if(username == "external"):
                    currentUser = "external"
                    break

                if(username != "admin"):
                    root_path=sfsDirectory
                    rawPaths = []
                    #we get all the encrypted paths
                    for root, dirs, files in os.walk(root_path):
                        for name in files:
                            rawPaths.append(os.path.join(root, name))
                        for name in dirs:
                            rawPaths.append(os.path.join(root, name))
                    #we decrupt them all
                    for path in reversed(rawPaths):
                        fileName = path.split('/')[-1]
                        if not (fileName.startswith('.')):
                            directoryOfFile = path.replace("/"+fileName,"")
                            shift = 3
                            decryptedFileName = cipher_decrypt(fileName, shift)
                            newpath = directoryOfFile+"/"+decryptedFileName
                            if os.path.exists(path):
                                os.rename(path,newpath)


                    #we get all the decrupted paths
                    rawPaths = []
                    for root, dirs, files in os.walk(root_path):
                        for name in files:
                            rawPaths.append(os.path.join(root, name))
                        for name in dirs:
                            rawPaths.append(os.path.join(root, name))
                    #print(rawPaths)

                    #paths - all that we dont want
                    paths = []
                    #path2 - all that we want
                    at_end_encrypt_these_paths=[]
                    for path in rawPaths:
                        if username not in path:
                            paths.append(path)
                        else:   
                            at_end_encrypt_these_paths.append(path)

                    path_t = at_end_encrypt_these_paths[0]
                    result = path_t.split('SFsystem/', 1)[1]
                    result = result.split('/', 1)
                    groupName = (result[0])

                    #we encrypt all those we dont want
                    for path in reversed(paths):
                        fileName = path.split('/')[-1]
                        if not (fileName.startswith('.')):
                            directoryOfFile = path.replace("/"+fileName,"")
                            shift = 3
                            encryptedFileName = cipher_encrypt(fileName, shift)
                            newpath = directoryOfFile+"/"+encryptedFileName
                            os.rename(path, newpath)


                    shift = 3
                    encryptedGroupName = cipher_encrypt(groupName, shift)
                    path1 = sfsDirectory+"/"+groupName
                    path2 = sfsDirectory+"/"+encryptedGroupName
                    if os.path.exists(path2):
                        os.rename(path2,path1)

                    at_end_encrypt_these_paths.append(path1)

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
                if(currentUser=="external"):
                    break

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

                #to encode everything
                # root_path=sfsDirectory
                # paths = []
                # for root, dirs, files in os.walk(root_path):
                #     for name in files:
                #         paths.append(os.path.join(root, name))
                #     for name in dirs:
                #         paths.append(os.path.join(root, name))
                # print(paths)

                if(currentUser=="admin"):
                    root_path=sfsDirectory
                    paths = []
                    for root, dirs, files in os.walk(root_path):
                        for name in files:
                            paths.append(os.path.join(root, name))
                        for name in dirs:
                            paths.append(os.path.join(root, name))

                    for path in reversed(paths):
                        fileName = path.split('/')[-1]
                        if not (fileName.startswith('.')):
                            directoryOfFile = path.replace("/"+fileName,"")
                            shift = 3
                            encryptedFileName = cipher_encrypt(fileName, shift)
                            newpath = directoryOfFile+"/"+encryptedFileName
                            os.rename(path, newpath)


                sorted_array = sorted(at_end_encrypt_these_paths, key=len)
                for path in reversed(sorted_array):
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

                shift = 3
                decChangeToDir = cipher_decrypt(changeToDir, shift)

                if(currentDir.find(changeToDir)!=-1 or currentDir.find(decChangeToDir)!=-1):
                    altDir = command[1].replace(changeToDir,decChangeToDir)
                    print("entered dir - "+command[1])
                    print("altDir - "+ altDir)
                    if(os.path.exists(command[1])):
                        os.chdir(command[1])
                    elif(os.path.exists(altDir)):
                        os.chdir(altDir)
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
                shift = 3
                enc_fileName = cipher_encrypt(command[1], shift)
                fullpath = os.path.abspath(command[1])
                at_end_encrypt_these_paths.append(fullpath)
                cursor.execute("INSERT INTO sfsFiles VALUES(\""+ currentDir+ "\",\""+command[1] +"\",\""+ str(enc_fileName)  +"\",\""+  "" +"\",\""+ currentUser +"\",\""+ m_ti +"\",\""+currentUser+"\",\""+currentUser+"\")")
                connection.commit()

            elif(command.find("cat")!=-1): #cat user.txt - user to read a file
                command= command.split(" ",1)
                currentDir = os.getcwd()

                #GURBANI'S Permissions Implementation
                cursor.execute("SELECT (readPermission) FROM sfsFiles WHERE fileName = ? OR fileEncryptedName =?", (command[1],command[1]))
                result = cursor.fetchone()

                if ((len(result)>0) and (result[0] != None)):
                    readers = (result[0]).split(",")
                    if username in readers:
                        #CHANPREET'S Cat Implementation
                        with open(command[1],'rb') as f:
                            encoded_content = f.read()
                            if(currentDir.find(currentUser)!=-1):
                                decoded_content = encoded_content.decode(encoding='cp037',errors='strict')
                                print(decoded_content)
                            else:
                                print("You do now belong to this directory, thus you cannot read the file.")
                        f.close()
                    
                    else:
                        print("Sorry you don't have permission to read this file!")
                    
                else: 
                    print("Sorry you don't have permission to read this file!")


            elif(command.find("echo")!=-1): #echo user.txt Hi we are programing 
                command= command.split(" ",2)
                print(command[2])

                #GURBANI'S Permissions Implementation
                cursor.execute("SELECT (writePermission) FROM sfsFiles WHERE fileName = ?", (command[1],))
                result = cursor.fetchone()

                if ((len(result)>0) and (result[0] != None)):
                    writers = (result[0]).split(",")
                    if username in writers:
                        #CHANPREET'S Echo Implementation
                        str_enc = command[2].encode(encoding='cp037')
                        fileDir = os.getcwd()+"/"+command[1]
                        ti_m = os.path.getmtime(fileDir)
                        m_ti = time.ctime(ti_m)
                        with open(command[1],'wb') as f:
                            f.write(str_enc)
                            cursor.execute("UPDATE sfsFiles SET fileContent=\""+str(str_enc)+"\", fileLastModified=\""+m_ti+"\" WHERE fileDirectory=\""+fileDir+"\"")
                            connection.commit()
                            f.close()
                    else:
                        print("Sorry you don't have permission to write to this file!")
                    
                else: 
                    print("Sorry you don't have permission to write to this file!")

            elif(command.find("rename")!=-1): #rename oldName newName
                command= command.split(" ",2)
                old_name = os.getcwd()+"/"+command[1]
                new_name = os.getcwd()+"/"+command[2]
                # Renaming the file
                os.rename(old_name, new_name)   

            elif(command.find("exit")!=-1): # exit
                break

            elif(command.find("help")!=-1):
                print("* To Login - login <username> <password>")
                print("* To Logout - logout")
                print("* To make a group - mkgroup <group name>")
                print("* To make a user - mkuser <group name> <username> <password>")
                print("* To change directory - cd <file path>")
                print("* To see the files/directories - ls")
                print("* To see the path - pwd")
                print("* To create a new file - touch <file name>")
                print("* To read a file - cat <file name>")
                print("* To write a file - echo <file name> <content/text>")
                print("* To rename a file - rename <old path with name> <new path with name>")
                print("* To set permission of a file - setpermission <file path> <username> <command(r-read, w-write, rw-read and write)>")
                print("* exit - exit")

            else:
                print("Invalid command, use 'help' for list of valid commands")

        
        except:
            print("Error")
            #continue



            

