# -*- coding: utf-8 -*-
import socket
import threading
import multiprocessing as mp
import struct
import time
import os

import py_zipedit

DIRPATH = os.getcwd()

class SocketEdit():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.dataName = b''
        self.data = b''
       
        
    def server(self, listenNum):
        s = socket.socket()
        s.bind((self.host, self.port))
        
        s.listen(listenNum)
        
        c, addr = s.accept()
        
        print('Connection from: ' + str(addr))
        
        while True:
            data = c.recv(1024).decode('utf-8')
            if not data:
                break
            print('From connected user: ' + data)
            data = data.upper()
            print('Sending: ' + data)
            c.send(data.encode('utf-8'))
            
        c.close()
        
   
    def client(self):
        #支援斷線重連
        s = socket.socket()
       
        while True:
            try:
                s.connect((self.host, self.port)) 
                break
            except socket.error as err:
                print(err)
                time.sleep(1)
                continue                              
           
        listenThread = threading.Thread(target=self.listenMessage, args=(s,))
        listenThread.start()
                
            
#       
        
    def listenMessage(self, s):
        #支援斷線重連
        isConnect = True
        while True:          
            try:
                self.recv_msg(s)
            except socket.error as err:
               print(err)
               time.sleep(1)
               isConnect = False
            try:
                if not isConnect:
                    s.close()
                    s = socket.socket()
                    s.connect((self.host, self.port))
                    isConnect = True
            except socket.error as err:
                print(err)
                time.sleep(1)
                
               
               
    
    
    def recv_msg(self, socket):
         #訊息類型(int) > 檔名長度(int) > 檔名 > 文件長度(int) > 文件內容
              
         self.dataName = b''
         self.data = b''
         
         meta_type = socket.recv(8)
         mt = int.from_bytes(meta_type, byteorder='big')
         print(mt)
         
         self.f(int(mt), socket)
                 
         
    
    def Handle_Update(self, s):       
        name_length = s.recv(8)
        nl = int.from_bytes(name_length, byteorder='big')
        print(nl)
         
        self.dataName = s.recv(int(nl))
        print(self.dataName)
         
            
        data_number = s.recv(8)
        dl = int.from_bytes(data_number, byteorder='big')
        print(dl)
            
        while len(self.data) < int(dl):
            self.data += s.recv(512)
                
        print(self.data)
        try:
            dirname = r'\%s' % str(self.dataName.decode('utf-8'))
            #寫入檔案
            with open(DIRPATH + dirname, 'wb') as in_file:
                in_file.write(self.data)
            
            #關閉主程式
            os.system("taskkill /f /im " + 'TMS_Theater.exe')
            
            #解壓縮並覆蓋檔案
            z = py_zipedit.ZipEdit(DIRPATH)
            z.unpackage(DIRPATH + dirname, DIRPATH)    
            
            #刪除壓縮包
            os.remove(DIRPATH + dirname)
            
        except Exception as err:
            print(err)
       
            
                         
             
         
    def f(self, n, socket):
        return {
                6653 : self.Handle_Update(socket)
                }[n]
    
if __name__ == '__main__':
    soc = SocketEdit("127.0.0.1", 2010)
    soc.client()
#    serverThread = threading.Thread(target=soc.server, args=(1,))
#    serverThread.start()
#    soc.client()
    
#    serverMP = mp.Process(target=soc.server, args=(1,))
#    serverMP.start()
#    soc.client()
    
    
   
    