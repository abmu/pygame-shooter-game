import socket


class Network:
    def __init__(self):
        # client setup
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '192.168.50.183'
        self.port = 5555
        self.addr = (self.server,self.port)
        self.id = self.connect()

    def connect(self):
        # connect client
        try:
            self.client.connect(self.addr)
            # send back information to indicate a successful connection
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self,data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(str(e))