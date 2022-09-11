import socket
from _thread import *
import pickle
import pygame
from settings import *
from sprites import Sprites


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
        self.s.listen(PLAYER_COUNT)
        print('Waiting for a connection, server started')

        self.sprites = Sprites()

    def threaded_client(self,conn,id_num):
        conn.send(pickle.dumps(self.sprites.get_player(id_num)))
        reply = ''
        while True:
            try:
                data = pickle.loads(conn.recv(2048))
                self.sprites.update_player(id_num,data)

                # stop receiving from the client
                if not data:
                    print('Disconnected')
                    break
                else:
                    reply = self.sprites.get_sprites(id_num)

                conn.sendall(pickle.dumps(reply))
            except:
                 break

        print('Lost connection')
        conn.close()

    def run(self):
        id_num = 0
        while True:
            # get the connected client and start new thread
            conn, addr = self.s.accept()
            print(f'Connected to: {addr}')

            start_new_thread(self.threaded_client, (conn,id_num))
            id_num += 1

if __name__ == '__main__':
    server = Server()
    server.run()