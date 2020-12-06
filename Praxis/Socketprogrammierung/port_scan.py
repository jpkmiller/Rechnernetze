import socket
from contextlib import closing
from threading import Thread
import time

Server_IP = '141.37.168.26'
MESSAGE = 'Hello, World!'

Continue = True
TCPPortsOpened = set()
TCPPortsClosed = set()
UDPPortsOpened = set()
UDPPortsClosed = set()


def scan(port: int, socketType: int):
    while True:
        with closing(socket.socket(socket.AF_INET, socketType)) as sock:
            if sock.connect_ex((Server_IP, port)) == 0:
                # print('Port {} open\n'.format(port))
                if socketType == 1:
                    TCPPortsOpened.add(port)
                else:
                    UDPPortsOpened.add(port)
                sock.sendto(MESSAGE.encode('utf-8'), (Server_IP, port))
                sock.close()
            else:
                # print('Port {} close\n'.format(port))
                if socketType == 1:
                    TCPPortsClosed.add(port)
                else:
                    UDPPortsClosed.add(port)
        if not Continue:
            break


threads = []


def startScan(socketType: int):
    for i in range(1, 51):
        t = Thread(target=scan, args=(i, socketType), daemon=True)
        threads.append(t)
        t.start()


def stopScan():
    for i in range(len(threads)):
        if threads[i].is_alive():
            threads[i].join()


if __name__ == '__main__':
    # TCP
    startTCP = time.time()
    print("Started TCP Port Scan")
    startScan(1)
    while time.time() - startTCP <= 5:
        ...
    Continue = False
    stopScan()
    print("Stopped TCP Port Scan")

    # UDP
    Continue = True
    startUCP = time.time()
    print("Started UDP Port Scan")
    startScan(2)
    while time.time() - startTCP <= 5:
        ...
    Continue = False
    stopScan()
    print("Stopped UDP Port Scan")

    print("Opened TCP Ports: {}".format(TCPPortsOpened))
    print("Closed TCP Ports: {}".format(TCPPortsClosed))
    print("Opened UDP Ports: {}".format(UDPPortsOpened))
    print("Closed UDP Ports: {}".format(UDPPortsClosed))
