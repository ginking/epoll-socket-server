#!/bin/env python3
import socket
import threading
from time import sleep
import time
import ESocketS
import selectors


host = socket.gethostbyname(socket.gethostname())
port = 1234

server = ESocketS.Socket(selector=selectors.PollSelector())
server.run_in_subthread('all', True)
server.start()

conections = 20000

def connect(clients):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    conn.connect((host, port))
    clients.append(conn)

try:
    clients = []
    t1 = time.time()
    for i in range(conections):
        threading.Thread(target=connect, args=(clients,)).start()
       # sleep(0.001)
    t2 = time.time()

    print('Connect time: ', t2-t1)


    message = b'hello from a client'
    length = len(message)
    t1 = time.time()
    for i in clients:
        x = i.send(message)
        if x != length:
            raise ValueError('Did not send entire package')

    t2 = time.time()
    print('Total send time: ', t2-t1)

#    while True:
#        sleep(10)

except KeyboardInterrupt:
    print('Disconnecting clients')
    for i in clients:
        i.shutdown(socket.SHUT_RDWR)
        i.close()
    print('Clients disconnected')



