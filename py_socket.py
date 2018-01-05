# -*- coding: utf-8 -*-
import socket
import threading
import multiprocessing as mp
import struct

class SocketEdit():
    def __init__(self, host, port):
        self.host = host
        self.port = port
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
        s = socket.socket()
        s.connect((self.host, self.port))
        
        listenThread = threading.Thread(target=self.listenMessage, args=(s,))
        listenThread.start()
#        message = input('->')
#        while message != 'q':
#            s.send(message.encode('utf-8'))
#            data = s.recv(1024).decode('utf-8')
#            print('Received from server: ' + data)
#            message = input('-> ')
#        s.close()
        
    def listenMessage(self, socket):
        while(True):
            self.recv_msg(socket)
    
    
    def recv_msg(self, socket):
        
        raw_msglen = self.recvall(socket, 4)
        print('GetStream: ')
        print(raw_msglen)
#        print(struct.unpack('>I', raw_msglen))
        if not raw_msglen:
            return None
        
        self.data = b''
        msglen = struct.unpack('>I', raw_msglen)[0]
        
        self.recvall(socket, msglen)
        
    def recvall(self, socket, n):        
        while len(self.data) < n:
            packet = socket.recv(n - len(self.data))
            if not packet:
                return None
            self.data += packet
        print(self.data)
        
if __name__ == '__main__':
    soc = SocketEdit("127.0.0.1", 2000)
    soc.client()
#    serverThread = threading.Thread(target=soc.server, args=(1,))
#    serverThread.start()
#    soc.client()
    
#    serverMP = mp.Process(target=soc.server, args=(1,))
#    serverMP.start()
#    soc.client()
    
    
   
    