# -*- coding: utf-8 -*-
import win32api, win32con
import os

#root
REG_ROOT = win32con.HKEY_CURRENT_USER

#path
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\run"

#flag
REG_FLAGS = win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS


class RegEdit():
    def __init__(self, root, path, flag):
        self.root = root
        self.path = path
        self.flag = flag
        
    def __getKey(self):
        key = win32api.RegOpenKeyEx(self.root, self.path, 0, self.flag)
        return key
    
    def checkKey(self):
        try:
            key = self.__getKey()
            key.close()
            return True
        except Exception as e:
            print(e)
            return False
        
    def getAllValues(self):
        key = self.__getKey()
        
        try:
            i = 0
            while True:
                yield win32api.RegEnumValue(key, i)
                i += 1
        except Exception as e:
            pass
        finally:
            key.close()
    
    def checkValueByname(self, name):
        key = self.__getKey()
        
        try:
            i = 0
            valueList = []
            while True:
                valueList.append(win32api.RegEnumValue(key, i))
                i += 1
        except Exception as e:
            pass
        finally:
            key.close()
            
        for n in valueList:
            if n[0] == name:
                return True
        return False
    
    def getValueByName(self, name):
        key = self.__getKey()
        value, value_type = win32api.RegQueryValueEx(key, name)
        return value, value_type
    
    def createValue(self, name, value_value='', value_type=win32con.REG_SZ):
        key = self.__getKey()
        win32api.RegSetValueEx(key, name, 0, value_type, value_value)
        
        key.close()
    
    def deleteValue(self, name):
        key = self.__getKey()
        win32api.RegDeleteValue(key, name)
        
        key.close()
        
    
    
if __name__ == '__main__':
    reg = RegEdit(REG_ROOT, REG_PATH, REG_FLAGS)
    print(os.path.realpath(__file__))
#    lis = list(reg.getAllValues())
    print(reg.checkValueByname('Steam'))
#   
#    for row in lis:
#        print(row[0])
#    print(list(reg.getAllValues()))