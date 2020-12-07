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

sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def scanUDP(port: int):
    sockUDP.settimeout(10)
    try:
        sockUDP.sendto(MESSAGE.encode('utf-8'), (Server_IP, port))
        sockUDP.recvfrom(1024)
        UDPPortsOpened.add(port)
    except socket.error:
        UDPPortsClosed.add(port)


def scanTCP(port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    try:
        sock.connect((Server_IP, port))
        sock.send(MESSAGE.encode('utf-8'))
        sock.recv(1024).decode('utf-8')
        TCPPortsOpened.add(port)
    except socket.error:
        TCPPortsClosed.add(port)
    sock.close()

threads = []


def startScan(socketType: int):
    if socketType == socket.SOCK_DGRAM:
        scan = scanUDP
    elif socketType == socket.SOCK_STREAM:
        scan = scanTCP
    for i in range(1, 51):
        t = Thread(target=scan, args=(i,), daemon=True)
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
    startScan(socket.SOCK_STREAM)
    while time.time() - startTCP <= 30:
        ...
    Continue = False
    stopScan()
    print("Stopped TCP Port Scan")

    # UDP
    Continue = True
    startUDP = time.time()
    print("Started UDP Port Scan")
    startScan(socket.SOCK_DGRAM)
    while time.time() - startUDP <= 30:
        ...
    Continue = False
    stopScan()
    sockUDP.close()
    print("Stopped UDP Port Scan")

    print("Opened TCP Ports: {}".format(TCPPortsOpened))
    print("Closed TCP Ports: {}".format(TCPPortsClosed))
    print("Opened UDP Ports: {}".format(UDPPortsOpened))
    print("Closed UDP Ports: {}".format(UDPPortsClosed))
