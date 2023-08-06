import socket
class server:
    def __init__(self,host,port,num=1):
        self.s=socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        try:
            self.s.bind((host, port))
        except:
            self.s.close()
            del self
            raise Exception('端口被占了！')
        self.s.listen(num)
    def acpt(self):
        try:
            self.c,self.addr=self.s.accept()
            return self.c
        except:
            return 0
    def send(self,content):
        try:
            self.c.send(content.encode())
            return 1
        except:
            return 0
    def recv(self):
        try:
            return (1,str(self.c.recv(1024).decode()))
        except:
            return (0,None)
    def close(self,a):
        try:
            if a=='s':
                self.c.close()
                self.s.close()
                del self
            if a=='c':
                self.c.close()
                del self.c,self.addr
            return 1
        except:
            return 0
class client:
    def __init__(self):
        self.s=socket.socket()
    def conn(self,host,port):
        try:
            self.s.connect((host, port))
            return 1
        except:
            return 0
    def send(self,content):
        try:
            self.s.send(content.encode())
            return 1
        except:
            return 0
    def recv(self):
        try:
            return (1,str(self.s.recv(1024).decode()))
        except:
            return (0,None)
    def close(self):
        self.s.close()
        del self
if __name__=='__main__':
    tt=16
    pk='0'*1024
    import random as rd
    from tb import std
    std.cls()
    if input('If you have no server task, check "s",or enter and check id from the server.\n')=='s':
        p=rd.randint(1024,65536)
        print('id:',p)
        s1=server('localhost',p)
        s1.acpt()
        print(s1.addr)
        for i in range(tt):
            print('len',len(s1.recv()[1]))
            print('data from the client!%s'%i)
            print(s1.send(pk))
        s1.close('s')
    else:
        s2=client()
        s2.conn(input('host'),int(input('Check your id:')))
        for i in range(tt):
            print(s2.send(pk))
            print('len',len(s2.recv()[1]))
            print('data from the server!%s'%i)
        s2.close()
