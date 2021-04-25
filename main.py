from pynput.keyboard import Key, Listener
from functools import partial
import time
from itertools import chain
import scipy.stats, numpy
import math
from math import sqrt

DATABASE = "database.txt"

class Action():
    def __init__(self):
        self.press = time.time()
        self.release = time.time()
        self.internal_time_arr = []
        self.external_time_arr = []
        self.internal_all = []
        self.external_all = []
        self.word_arr = []

        self.a = 0.05
        self.Si_sqr = 0
        self.new_arr = []

    def on_press(self, key):
        self.release = time.time()
        self.external_time_arr.append(self.release-self.press)
        self.press = time.time()
        return self.external_time_arr

    def on_release(self, key):
        self.release = time.time()
        self.internal_time_arr.append(self.release - self.press)
        self.press = time.time()
        self.word_arr.append(str(key))

        if key == Key.esc:
            self.internal_time_arr.pop()
            self.external_time_arr.pop(0)
            self.external_time_arr.pop()
            self.word_arr.pop()
            return False

        return self.internal_time_arr, self.word_arr

    def average(self, a, n):
        sum = 0
        for i in range(n):
            sum += a[i]
        self.res = sum/n
        return self.res

    def studentCoeficient(self):
        self.Tt = abs(scipy.stats.t.ppf(self.a, len(self.external_time_arr) - 1)) 
        for i in range(len(self.external_time_arr)): 
            self.temporary = [self.external_time_arr[i] for i in range(len(self.external_time_arr))] 
            self.Yi = self.temporary.pop(i) 
            self.Mi = numpy.sum(self.temporary) / (len(self.temporary)) 
            for k in range(len(self.temporary)): 
                self.Si_sqr += pow((self.temporary[k] - self.Mi), 2)
            self.Si = sqrt(self.Si_sqr)
            self.Si_sqr = self.Si_sqr / (len(self.temporary) - 1)  
            self.Tp = abs((self.Yi - self.Mi)/self.Si) 
            if self.Tp > self.Tt: 
                self.new_arr.append(i) 
        self.external_time_arr = [i for j, i in enumerate(self.external_time_arr) if j not in self.new_arr]
        return self.external_time_arr

    def fisherCoeficient(self):
        if self.internal_time_arr_average > self.external_time_arr_average:
            self.Smax = pow(self.internal_time_arr_average, 2)
            self.Smin = pow(self.external_time_arr_average, 2)
            self.Fp = self.Smax / self.Smin
            print(self.Smax)
            print(self.Smin)
            print(self.Fp)
        elif self.internal_time_arr_average < self.external_time_arr_average:
            print("MENSHE")
            self.Smax = pow(self.external_time_arr_average, 2)
            self.Smin = pow(self.internal_time_arr_average, 2)
            self.Fp = self.Smax / self.Smin
            print(self.Smax)
            print(self.Smin)
            print(self.Fp)

        for i in range(len(self.external_time_arr)): 
            self.temporary = [self.external_time_arr[i] for i in range(len(self.external_time_arr))] 
            self.Yi = self.temporary.pop(i) 
            self.My = numpy.sum(self.temporary) / (len(self.temporary))
            self.SiY_sqr = 0 
            for k in range(len(self.temporary)): 
                self.SiY_sqr += pow((self.temporary[k] - self.My), 2)
            self.SiY_sqr = self.SiY_sqr / (len(self.temporary) - 1)  

        for i in range(len(self.external_all)):
            self.temporary = [self.external_all[i] for i in range(len(self.external_all))]
            self.Yi = self.temporary.pop(i)
            self.Mx = numpy.sum(self.temporary) / (len(self.temporary))
            self.SiX_sqr = 0
            for k in range(len(self.temporary)): 
                self.SiX_sqr += pow((self.temporary[k] - self.Mx), 2)
            self.SiX_sqr = self.SiX_sqr / (len(self.temporary) - 1)  
            self.S = sqrt((pow(self.SiX_sqr, 2) + pow(self.SiY_sqr, 2))*(len(self.temporary) - 1)) / sqrt(2*len(self.temporary) - 1)
            self.Tp = abs(self.Mx - self.My) / (self.S * sqrt(2 / len(self.temporary)))
            if self.Fp > self.Tt: 
                self.new_arr.append(i) 
        self.external_time_arr = [i for j, i in enumerate(self.external_time_arr) if j not in self.new_arr]

    def whenLogin(self):
        with Listener(
            on_press=self.on_press,
            on_release=self.on_release) as listener:
            listener.join()
        self.internal_time_arr.pop(0)
        self.word_arr.pop(0)
        self.fisherCoeficient()
        self.internal_time_arr_average = self.average(self.internal_time_arr, len(self.internal_time_arr))
        self.external_time_arr_average = self.average(self.external_time_arr, len(self.external_time_arr))
        print(*self.word_arr, sep="")

    def whenReg(self):
        i = 0
        for i in range(10): 
            with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
                listener.join()
            if i == 0:
                self.internal_time_arr.pop(0)
                self.word_arr.pop(0)
            self.studentCoeficient()
            self.internal_time_arr_average = self.average(self.internal_time_arr, len(self.internal_time_arr))
            self.external_time_arr_average = self.average(self.external_time_arr, len(self.external_time_arr))
            self.internal_all.append(self.internal_time_arr_average)
            self.external_all.append(self.external_time_arr_average)
            self.internal_time_arr.clear()
            self.external_time_arr.clear()
            print(*self.word_arr, sep="")
            self.word_arr.clear()
        
        f = open(DATABASE,'r')
        info = f.read()
        f.close()
        f = open(DATABASE,'w')
        info = info + ' ' + str(self.average(self.internal_all, len(self.internal_all))) + ' ' + str(self.average(self.external_all, len(self.external_all)))
        f.write(info)
        f.close()

class Person():
    def __init__(self):
        self.action = Action()
    
    def get_internal(self, name):
        userlist = open(DATABASE).readlines()
        for user in userlist:
            self.login = user.split()[0]
            self.internal = user.split()[1]
            if self.login == name:
                return self.internal
    
    def get_external(self, name):
        userlist = open(DATABASE).readlines()
        for user in userlist:
            self.login = user.split()[0]
            self.external = user.split()[2]
            if self.login == name:
                return self.external

    def mainMenu(self):
        print("What would you like to do?")
        print("1. Register.")
        print("2. Log in.")
        choice = int(input("Your choice: "))
        if choice == 1:
           return self.funcRegister()
        if choice == 2:
           return self.funcLogin()
        else:
            return

    def get_existing_users(self):
        with open(DATABASE, "r") as fp:
            for line in fp.readlines():
                self.username = line.split()[0]
                self.internal =  line.split()[1]
                self.external = line.split()[2]
                yield self.username

    def user_exists(self, name):
        return any((self.usr_name == self.name) for self.usr_name in self.get_existing_users())

    def ask_user_credentials(self):
        print("Enter your data:")
        self.name = str(input("Login: "))
        if self.name is None:
            return
        else:
            return self.name

    def funcLogin(self):
        self.name = self.ask_user_credentials()
        self.const_internal = self.get_internal(self.name)
        self.const_external = self.get_external(self.name)
        if self.user_exists(self.name):
            print("Enter password: \n")
            self.action.whenLogin()
            if (float(self.action.internal_time_arr_average) >= float(self.const_internal) - 0.01 and float(self.action.internal_time_arr_average) <= float(self.const_internal) + 0.01
                and float(self.action.external_time_arr_average) >= float(self.const_external) - 0.01 and float(self.action.external_time_arr_average) <= float(self.const_external) + 0.01):
                print("Welcome back!\n")
            else: 
                print("Hacking detected!\n")
                return
        else:
            print("This user does not exist.")

    def funcRegister(self):
        self.name = self.ask_user_credentials()
        if self.user_exists(self.name):
            print("This user already exists. Pick another name.\n")
        else:
            self.f = open(DATABASE,'r')
            self.info = self.f.read()
            self.f.close()
            self.f = open(DATABASE,'w')
            self.info = self.info + '\n' + self.name
            self.f.write(self.info)
            self.f.close()
            print("Your account has been created!\n")
            print("Now enter a key phrase: \n")
            self.action.whenReg()
           

def main():
    action = Action()
    person = Person()
    
    person.mainMenu()


if __name__ == "__main__":
    main()

