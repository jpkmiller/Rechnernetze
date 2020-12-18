import socket
import struct
import json
from sys import argv
import time

message_types = ['register', 'deregister', 'send']


# sus schhhhhhhhhhhhapelt

# json.loads(...) # decode
# json.dumps(...) # encode


# address = clients[nickname]
# udp_port.sendTo(address, "connect to me at 1234"
# tcp_port.accept()

class Client:

    def __init__(self, nickname: str = 'shitass', SERVER_IP: str = '127.0.0.1'):
        self.nickname = nickname
        self.socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socketUDP.bind(('', 0))
        self.socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = self.socketUDP.getsockname()
        self.SERVER = SERVER_IP, 2000
        self.clients = {}

        self.register()

    @staticmethod
    def convertToBytes(json_string: str) -> bytes:
        payload_msg = bytearray(json_string, 'utf-8')
        print(len(payload_msg))
        msg = bytearray(len(payload_msg).to_bytes(length=4, byteorder='big', signed=False))
        print(msg)
        msg.extend(payload_msg)
        print(msg)
        return bytes(msg)

    @staticmethod
    def sendOverTCP(sock, addr, jsonMessage: str, keepAlive: bool = False):
        sock.settimeout(10)
        try:
            sock.connect((addr[0], addr[1]))
        except OSError:
            print("already connected")
        bytesMessage = Client.convertToBytes(jsonMessage)  # or bytes(byteMessageSize) or byteMessageSize.to_bytes()
        sock.send(bytesMessage)

        if not keepAlive:
            print("closing socket")
            sock.close()

    def register(self):
        registerDict = {'type': 'register', 'nickname': self.nickname, 'ip': self.ip, 'port': self.port}
        self.sendOverTCP(self.serverSocket, self.SERVER, json.dumps(registerDict), True)
        response = Client.receiveMessage(self.serverSocket)
        for user in response['users']['added']:
            self.clients[user['nickname']] = (user['ip'], user['port'])

    def unregister(self):
        unregisterDict = {'type': 'unregister', 'nickname': self.nickname}
        self.sendOverTCP(self.serverSocket, self.SERVER, json.dumps(unregisterDict), True)

    def sendMessage(self, message: str, nickname: str):
        c = self.clients[nickname]  # ip, port

        # TODO: check if client already has a connection to other client
        connectToClientMessage = 'Please talk to me baby on {} one more time.'.format(self.socketTCP.getsockname()[1])
        bytesMessageRequest = Client.convertToBytes(connectToClientMessage)
        self.socketUDP.sendto(bytesMessageRequest, c['address'])
        self.socketTCP.accept()

        messageRequest = {'type': 'message', 'message': message}
        bytesMessage = Client.convertToBytes(json.dumps(messageRequest))
        self.socketTCP.send(bytesMessage)

    @staticmethod
    def receiveMessage(sock: socket):
        try:
            data = sock.recv(1024)
            size = int.from_bytes(bytes=data[:4], byteorder='big', signed=False)
            payload = data[4:].decode('utf-8')
            print("expected size is " + str(size) + " actual size is " + str(len(payload)))
            print(len(payload) < size)
            while len(payload) < size:
                data = sock.recv(1024)
                # print("data chunk received")
                payload += data.decode('utf-8')

            print("data received")
            # TODO: check if this is needed
            # json.dumps(payload)
            # -----------------------------
            payload_dict = json.loads(payload)
            return payload_dict
        except socket.timeout:
            print('Socket timed out')
            sock.close()


if __name__ == '__main__':
    client = Client(argv[1])
