import json
from os import path
import getpass
import threading,time,os

def write(path):
    if os.path.getsize(path) < 1073737728:  # 1073737728 is 4 bytes less than 1 Gb
        pass
    else:
        print("\nThe file size limit is 1 GB. Frist delete some records to enter new ones.\n")
        return -1
    ttl_flag=input("Would you like to create a record with Time_To_Live property? \"y\" or \"n\" : ")
    if(ttl_flag=='y'):
        seconds=int(input("Enter the life of the record in sec(s): "))
    key=input("\nEnter the key with which you want to create a record : ")
    with open(path, 'r') as json_file:
        data = {}
        data = json.load(json_file)
        if key in data.keys():
            print("This key already exists in the database.")
            return None

    data[key] = []
    data[key].append({
        'Name': input("Name : "),
        'Branch': input("Branch : "),
        'Score': input("Score : ")
    })
    with open(path, 'w') as outfile:
        json.dump(data, outfile, indent=" ")
        outfile.write('\n')
    print("Record successfully inserted !!")
    if(ttl_flag=='y'):
        event_obj = threading.Event()
        x = threading.Thread(target=delete_silent, args=(path,key,seconds,event_obj))
        x.start()

def delete_silent(path,key,seconds,event_obj):
    event_obj.wait(seconds)
    #time.sleep(seconds)
    try:
        with open(path, 'r') as json_file:
            data = {}
            data = json.load(json_file)
            data.pop(key)
        with open(path, 'w') as outfile:
            json.dump(data, outfile, indent=" ")
            outfile.write('\n')
    except KeyError:
        pass
        # print("The key is no more the records.")
    print("\n"+ key +" Timed-Out. Record auto-deleted !\n")

def read(path):
    key = input("\nEnter the key whose record you want to see : ")
    with open(path) as json_file:
        data = json.load(json_file)
        try:
            for p in data[key]:
                print('Name : ' + p['Name'])
                print('Branch : ' + p['Branch'])
                print('Score : ' + p['Score'])
                print('')
        except KeyError:
            print("Such a key does not exists in the records.")

def delete(path):
    key = input("\nEnter the key whose record is to be deleted : ")
    try:
        with open(path, 'r') as json_file:
            data = {}
            data = json.load(json_file)
            data.pop(key)
        with open(path, 'w') as outfile:
            json.dump(data, outfile, indent=" ")
            outfile.write('\n')
        print("Record successfully deleted !!")
    except KeyError:
        print("The key does not exits in the database.")

def showAll_Records(path):
    with open(path, 'r') as json_file:
        data = json.load(json_file)
        if(len(data)==0):
            print("No records found.")
            return None
        print()
        for i in data.keys():
            for p in data[i]:
                print('Key: '+ i +'  Name: ' + p['Name'] + '  Branch: ' + p['Branch'] + '  Score: ' + p['Score'])

def main(file_path):
    ch=""
    while(ch!="exit"):
        print("\nFunctional Menu : \n1. Create\n2. Read\n3. Delete\n4. See all records\n5. Exit")
        ch=input("Enter the operation number : ")
        if(ch=='1'):
            opt='y'
            while(opt!='n'):
                val=write(file_path)
                if val==-1:
                    break
                opt=input("Would you like to add more records ? y/n :")
        elif(ch=='2'):
            read(file_path)
        elif(ch=='3'):
            opt='y'
            while(opt!='n'):
                delete(file_path)
                opt = input("Would you like to delete more records ? y/n :")
        elif(ch=='4'):
            showAll_Records(file_path)
        else:
            exit()

if __name__=="__main__":
    opt=input("Do you want to provide custom path for database file? Enter \"y\" or \"n\" :")
    if(opt=='y'):
        file_path=input("Enter custom path ex. (C:\\Users\\your_database_file_name.txt) : ")
    else:
        print("Moving with the default home/root directory of your pc ... :")
        str = 'C:\\Users\\' + getpass.getuser() + '\\Desktop\\DataBase.txt'
        file_path=str

    if(path.exists(file_path)):
        print("File already exists ... ")
        main(file_path)
    else:
        file=open(file_path, "w")
        file.write("{}")
        file.close()
        print("File successfully created !!")
        main(file_path)






