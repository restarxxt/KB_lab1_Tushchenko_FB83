import os, string, sys, getpass, random
import platform, psutil, hashlib, winreg
from win32api import *
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

DATABASE = "database.txt"
ban_status = "No"
restrictions = "No"

def pass_for_aes():
    salt = b'\xebW\xed\xaa\xeeO\xe8\xb4/\xf4jwn\x97\x12K3\x88\xa48\xf7\xa6Dh\xff\x8b\xde\x13\xbf\x06\xfc6'
    password = input("Enter your secret key: ")
    ran = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    password = password + ran
    password = str(password)
    print(password)
    hashed_password = hashlib.sha1(password.encode())
    hashed_password = str(hashed_password.hexdigest())
    key = PBKDF2(hashed_password, salt, dkLen=32)
    return key

def aes_encryptor():
    file_to_encrypt = 'database.txt'
    buffer_size = 65536 # 64kb
    key = pass_for_aes()
    input_file = open(file_to_encrypt, 'rb')
    output_file = open('encrypted.txt', 'wb')

    cipher_encrypt = AES.new(key, AES.MODE_CFB)

    output_file.write(cipher_encrypt.iv)

    buffer = input_file.read(buffer_size)
    while len(buffer) > 0:
        ciphered_bytes = cipher_encrypt.encrypt(buffer)
        output_file.write(ciphered_bytes)
        buffer = input_file.read(buffer_size)
    
    input_file.close()
    output_file.close()

def aes_decryptor():
    salt = b'\xebW\xed\xaa\xeeO\xe8\xb4/\xf4jwn\x97\x12K3\x88\xa48\xf7\xa6Dh\xff\x8b\xde\x13\xbf\x06\xfc6'
    password = input("Enter your secret key: ")
    get_hash = hashlib.sha1(password.encode())
    get_hash = str(get_hash.hexdigest())
    key = PBKDF2(get_hash, salt, dkLen=32)
    
    file_to_encrypt = 'database.txt'
    buffer_size = 65536 # 64kb
    input_file = open('encrypted.txt', 'rb')
    output_file = open(file_to_encrypt + '.temporary', 'wb')

    iv = input_file.read(16)

    cipher_encrypt = AES.new(key, AES.MODE_CFB, iv=iv)

    buffer = input_file.read(buffer_size)
    while len(buffer) > 0:
        decrypted_bytes = cipher_encrypt.decrypt(buffer)
        output_file.write(decrypted_bytes)
        buffer = input_file.read(buffer_size)

    input_file.close()
    output_file.close()

def sys32_64():
    system32 = os.path.join(os.environ['SystemRoot'], 'SysNative' if 
    platform.architecture()[0] == '32bit' else 'System32')
    listtest_path = os.path.join(system32, 'ListTest.exe')

    sysWOW64 = os.path.join(os.environ['SystemRoot'], 'SysNative' if 
    platform.architecture()[0] == '32bit' else 'SysWOW64')
    listtest_path = os.path.join(sysWOW64, 'ListTest.exe')

    return str(system32 + "\n" + sysWOW64)

def gatherData():
    #збір інформації про ПК
    username = str(getpass.getuser())
    computername = str(os.environ['ComputerName'])
    windir = str(os.environ['SystemRoot'])
    systemfiles = sys32_64()
    mouse_count = str(GetSystemMetrics(43))
    screen_width = str(GetSystemMetrics(0))
    ssd = psutil.disk_usage('/')
    memory = str(ssd.total / (2**30))

    os_type = sys.platform.lower()
    command = "wmic bios get serialnumber"
    serialnumber = str(os.popen(command).read().replace("\n","").replace("","").replace(" ",""))

    all_data = (username + computername + windir + systemfiles + mouse_count + screen_width + memory + serialnumber).encode('utf-8')
    datahash = hashlib.md5(all_data).hexdigest()
    return datahash

REG_PATH = r"SOFTWARE"
def get_reg(name):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                       winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None

def displayAdminMenu():
    print("Choose an option: ")
    print("0. AES crypto")
    print("1. Change password.")
    print("2. Show the list of users.")
    print("3. Add a new unique user.")
    print("4. Block user.")
    print("5. Turn on/off restricts for a password.")
    print("6. Exit.")

def displayUserMenu():
    print("Choose an option: ")
    print("1. Change password.")
    print("2. Exit.")

def adminPanel(username):
    name = username
    displayAdminMenu()
    choice = int(input("Your choice: "))
    if choice == 0:
        print("1. Encrypt database. ")
        print("2. Decrypt database. ")
        choicee = int(input("Your choice: "))
        if choicee == 1:
            aes_encryptor()
            adminPanel(name)
        elif choicee == 2:
            aes_decryptor()
            adminPanel(name)
        else:
            adminPanel(name)
    elif choice == 1:
        changePass(name)
        print("\n")
        adminPanel(name)
    elif choice == 2:
        printUsers()
        print("\n")
        adminPanel(name)
    elif choice == 3:
        addUniqueUser()
        print("\n")
        adminPanel(name)
    elif choice == 4:
        banUser()
        print("\n")
        adminPanel(name)
    elif choice == 5:
        name = str(input("Enter user's login: "))
        userlist = open(DATABASE).readlines()
        for user in userlist:
            login = user.split()[0]
            if login == name:
                fin = open(DATABASE, "rt")
                if user.split()[3] == "Yes":
                    turnOffRestrictions(name)
                elif user.split()[3] == "No":
                    turnOnRestrictions(name)
                fin.close()
        print("\n")
        adminPanel(name)
    elif choice == 6:
        os.rename("database.txt.temporary", "database.txt")
        aes_encryptor()
        exit(0)
    else:
        print("Wrong option.")
        print("\n")
        displayAdminMenu()

def userPanel(username):
    name = username
    displayUserMenu()
    choice = int(input("Your choice: "))
    if choice == 1: 
        userlist = open(DATABASE).readlines()
        for user in userlist:
            login = user.split()[0]
            if login == name:
                fin = open(DATABASE, "rt")
                if user.split()[3] == "Yes":
                    passRestrictions(name)
                elif user.split()[3] == "No":
                    changePass(name)
                fin.close()
        print("\n")
        userPanel(name)
    elif choice == 2:
        exit(0)
    else:
        print("Wrong option.")
        print("\n")
        displayAdminMenu()

def mainMenu():
    print("Here you can log in, register or get help.")
    print("What would you like to do?")
    print("1. Register.")
    print("2. Log in.")
    print("3. Get help.")
    print("4. Exit.")
    choice = int(input("Your choice: "))
    if choice == 1:
       return funcRegister()
    if choice == 2:
       return funcLogin()
    elif choice == 3:
        print("Тущенко Денис Михайлович, ФБ-83, варіант 18")
        print("18. Неспівпадання з ім'ям користувача, записаним в зворотному порядку.")
        mainMenu()
    elif choice == 4:
        exit(0)

def changePass(username):
    name = username
    old_pass = str(input("Old password: "))
    if is_authorized(name, old_pass):
        print("Correct, now enter your new password: ")
        new_pass = str(input("New password: "))
        new_pass_pass = str(input("Enter again: "))
        if new_pass == new_pass_pass:
            fin = open(DATABASE, "rt")
            data = fin.read()
            data = data.replace(name + ' ' + old_pass, name + ' ' + new_pass)
            fin.close()
            fin = open(DATABASE, "wt")
            fin.write(data)
            fin.close()
            print("Password changed!")
        else:
            print("Error occured.")
            if name == "admin":
                adminPanel(name)
            else:
                userPanel(name)

def passRestrictions(name):
    login = name
    old_pass = str(input("Old password: "))
    if is_authorized(name, old_pass):
        print("Correct, now enter your new password: ")
        new_pass = str(input("New password: "))
        if new_pass == login[::-1]:
            print("You can't set this password.\n")
            userPanel(login)
        else:
            new_pass_pass = str(input("Enter again: "))
            if new_pass == new_pass_pass:
                fin = open(DATABASE, "rt")
                data = fin.read()
                data = data.replace(name + ' ' + old_pass, name + ' ' + new_pass)
                fin.close()
                fin = open(DATABASE, "wt")
                fin.write(data)
                fin.close()

def printUsers():
    userlist = open(DATABASE).readlines()[1:]
    for user in userlist:
        login = user.split()[0]
        password = user.split()[1]
        ban_status = user.split()[2]
        restrictions = user.split()[3]
        print("Login: " + login + "   " + "Password: " + password + "   " + "Is banned? " + ban_status + "   " + "Restrictions: " + restrictions)

def addUniqueUser():
    const_pass = ""
    print("Add new unique user: ")
    login = str(input("Enter unique login: "))
    if user_exists(login):
        print("Name Unavailable. Please Try Again")
    else:
        f = open(DATABASE,'r')
        info = f.read()
        f.close()
        f = open(DATABASE,'w')
        info = info + "\n" + login + " " + const_pass + " " + ban_status + " " + restrictions
        f.write(info)

def banUser():
    name = str(input("Ban user: "))
    userlist = open(DATABASE).readlines()
    for user in userlist:
        login = user.split()[0]
        if login == name:
            fin = open(DATABASE, "rt")
            data = fin.read()
            new_ban_status = "Yes"
            data = data.replace(name + ' ' + user.split()[1] + ' ' + ban_status, name + ' ' + user.split()[1] + ' ' + new_ban_status)
            fin.close()
            fin = open(DATABASE, "wt")
            fin.write(data)
            fin.close()

def turnOnRestrictions(username):
    name = username
    userlist = open(DATABASE).readlines()
    for user in userlist:
        login = user.split()[0]
        if login == name:
            fin = open(DATABASE, "rt")
            data = fin.read()
            new_restrictions = "Yes"
            data = data.replace(name + ' ' + user.split()[1] + ' ' + user.split()[2] + ' ' + user.split()[3], name + ' ' + user.split()[1] + ' ' + user.split()[2] + ' ' + new_restrictions)
            fin.close()
            fin = open(DATABASE, "wt")
            fin.write(data)
            fin.close()

def turnOffRestrictions(username):
    name = username
    userlist = open(DATABASE).readlines()
    for user in userlist:
        login = user.split()[0]
        if login == name:
            fin = open(DATABASE, "rt")
            data = fin.read()
            new_restrictions = "No"
            data = data.replace(name + ' ' + user.split()[1] + ' ' + user.split()[2] + ' ' + user.split()[3], name + ' ' + user.split()[1] + ' ' + user.split()[2] + ' ' + new_restrictions)
            fin.close()
            fin = open(DATABASE, "wt")
            fin.write(data)
            fin.close()

def isBanned(name):
    userlist = open(DATABASE).readlines()
    for user in userlist:
        login = user.split()[0]
        ban_status = user.split()[2]
        if login == name:
            return ban_status

def get_existing_users():
    with open(DATABASE, "r") as fp:
        for line in fp.readlines():
            username = line.split()[0]
            password = line.split()[1]
            ban_status = line.split()[2]
            restrictions = line.split()[3]
            yield username, password

def is_authorized(name, password):
    return any((user == (name, password)) for user in get_existing_users())

def user_exists(name):
    return any((usr_name == name) for usr_name, _ in get_existing_users())

def ask_user_credentials():
    print("Enter your data:")
    name = str(input("Login: "))
    password = str(input("Password: "))
    #password = getpass("Password: ")
    if password is None:
        return name, ''
    else:
        return name, password


def funcLogin():
    name, password = ask_user_credentials()
    ban_status = isBanned(name)
    if ban_status == "Yes":
        print("Your account is banned.")
        mainMenu()
    elif name == "admin" and is_authorized(name, password):
        print("Welcome to admin panel.")
        adminPanel(name)
    elif is_authorized(name, password):
        print("Welcome to user panel, " + name)
        userPanel(name)
    elif user_exists(name):
        print("Wrong password! Try again: ")
        print("Login: " + name)
        password = str(input("Password: "))
        #password = getpass("Password: ")
        if name == "admin" and is_authorized(name, password):
            print("Welcome to admin panel.")
            adminPanel(name)
        elif is_authorized(name, password):
            print("Welcome to user panel, " + name)
            userPanel(name)
        elif user_exists(name):
            print("Wrong password! Try again: ")
            print("Login: " + name)
            password = str(input("Password: "))
            #password = getpass("Password: ")
            if name == "admin" and is_authorized(name, password):
                print("Welcome to admin panel.")
                adminPanel(name)
            elif is_authorized(name, password):
                print("Welcome to user panel, " + name)
                userPanel(name)
            elif user_exists(name):
                print("Out of tries! Exiting...")
                exit(0)
    else:
        print("This user does not exist.")
        mainMenu()


def funcRegister():
    name, password = ask_user_credentials()
    if user_exists(name):
        print("This user already exists. Pick another name.\n")
        mainMenu()
    else:
        f = open(DATABASE,'r')
        info = f.read()
        f.close()
        f = open(DATABASE,'w')
        info = info + "\n" + name + " " + password + ' ' + ban_status + ' ' + restrictions
        f.write(info)
        f.close()
        print("Your account has been created!\n")
        mainMenu()

def main():
    datahash = gatherData()
    checkhash = get_reg('Tushchenko')
    if datahash != checkhash:
        exit(0)
    else:
        file = open("database.txt", "w")
        file.write("admin admin No No")
        file.close()
        mainMenu()

if __name__ == "__main__":
    main()


