# Secure-File-System

Group Members Name: Chanpreet Singh and Gurbani Baweja

To set SFS on Cybera:
Login to Cybera rapid cloud, create/login account, create a database instant, copy the IP address for the instance. Make sure that the instance security allow for your local IP acces. Download your private key. 
Clone the code from GitHub
git clone https://github.com/Chanpreet-Singh-UofA/Secure-File-System.git
Add SF to the cloned files base directory folder, 
cd Secure-File-System
mkdir SFsystem
Upload the code to cybera instance
scp -i path/of/sfs.pem -r path/to/Secure-File-System ubuntu@\[<instance IP adress>\]:
Now you can login into the SFS on Cybera. 


To run the SFS on Cybera:
Connect to the cynera instant using the ssh.
ssh -i path/of/sfs.pem ubuntu@2605:fd00:4:1001:f816:3eff:fe1f:f1ec
Change directory to Secure-File-System
cd Secure-File-System
Run the python script
python3 SFS.py

  
  User Guide

To Login
login <username> <password>
To logout
logout
To Create a group and/or user
login admin admin
mkgroup <groupName>
mkuser <groupName> <username> <password>
To create a file
touch <fileName>
To write content into a file
echo <fileName> <content>
To read a file
cat <fileName>
To check the current path
pwd
To check all the directories and files in current directory
ls
To change directory
cd <full new directory path>
To rename a file
rename <full current file path> <full new file path>
To set permissions
setpremission <file name> <userName to who permission is be granted> <command - r, w, rw>
To see all valid commands
help
To exit the SFS
exit
