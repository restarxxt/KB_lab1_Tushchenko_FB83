import sys
from cx_Freeze import setup,Executable
import getpass
import os, platform, psutil
from win32api import *
import hashlib
import winreg

def sys32_64():
	system32 = os.path.join(os.environ['SystemRoot'], 'SysNative' if 
	platform.architecture()[0] == '32bit' else 'System32')
	listtest_path = os.path.join(system32, 'ListTest.exe')

	sysWOW64 = os.path.join(os.environ['SystemRoot'], 'SysNative' if 
	platform.architecture()[0] == '32bit' else 'SysWOW64')
	listtest_path = os.path.join(sysWOW64, 'ListTest.exe')

	return str(system32 + "\n" + sysWOW64)
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

#запис до реєстру
REG_PATH = r"SOFTWARE"

def set_reg(name, value):
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, 
                                       winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False

set_reg('Tushchenko', datahash)

#інсталятор
PYTHON_INSTALL_DIR = os.path.dirname(sys.executable)
#PYTHON_INSTALL_DIR = str(input("Enter where the program will be installed: "))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')

include_files = [(os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),os.path.join('lib','tk86.dll')),
(os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'), os.path.join('lib', 'tcl86.dll'))]

base = None

if sys.platform == 'win64':
	base = 'Win64GUI'

executables = [Executable('project.py', base = base, icon = r"D:\KB\lab2\key.icon",
	shortcutName = 'SomeProgram', shortcutDir = "DesktopFolder")]

setup(name = 'LoginRegisterSystem Installer',
	version = '1.0',
	author = 'restar-xx-t',
	description = 'Installer for LAB2',
	options = {'build_exe':{'include_files':include_files}},
	executables = executables)