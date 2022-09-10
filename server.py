import socket
from _thread import *
import sys


class Server:
    def __init__(self):
        # server setup
        self.server = '192.168.50.183'
        self.port = 5555

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # catch and print out any errors when binding address to port
        try:
            self.s.bind((self.server,self.port))
        except socket.error as e:
            print(str(e))

        # set number of clientss
        self.s.listen(2)
        print('Waiting for a connection, server started')

    def threaded_client(self,conn):
        conn.send(str.encode('Connected'))
        reply = ''
        while True:
            try:
                data = conn.recv(2048)
                reply = data.decode('utf-8')

                # stop receiving from the client
                if not data:
                    print('Disconnected')
                    break
                else:
                    print(f'Recieved: {reply}')

                conn.sendall(str.encode(reply))
            except:
                break

        print('Lost connection')
        conn.close()

    def run(self):
        while True:
            # get the connected client and start new thread
            conn, addr = self.s.accept()
            print(f'Connected to: {addr}')

            start_new_thread(self.threaded_client, (conn,))

if __name__ == '__main__':
    server = Server()
    server.run()