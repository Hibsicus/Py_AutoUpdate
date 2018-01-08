# -*- coding: utf-8 -*-
import zipfile
import os


class ZipEdit():
    def __init__(self, path, dest=''):
        self.path = path
        self.dest = dest
    
    def package(self):
        if self.dest == '':
            zf  =zipfile.ZipFile(self.path + '.zip', mode='w')
        else:
            zf = zipfile.ZipFile(self.dest + '.zip', mode='w')
            
        os.chdir(self.path)
        
        for root, foldrs, files in os.walk('.\\'):
            for sfile in files:
                aFile = os.path.join(root, sfile)
                print(aFile)
                zf.write(aFile)
        zf.close()
        
    def unpackage(self, filePath, extraPath):
        if not os.path.exists(extraPath):
            os.makedirs(extraPath)
        
        zf = zipfile.ZipFile(filePath)
        zf.extractall(extraPath)
        

if __name__ == '__main__':
    path = r'D:\Bake'
    dest = r'D:\hello'
    extra = r'D:\BakeTest'
    
#    szip = ZipEdit(path, dest)
#    szip.package()
#    szip.unpackage(r'D:\hello.zip', extra)