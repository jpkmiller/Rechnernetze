import socket
import struct
import json
from sys import argv

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
        self.socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = self.socketUDP.getsockname()  # getsockname() returns a 2-tuple (host, port)
        self.SERVER = SERVER_IP, 2000
        self.clients = {}

        self.register()

    @staticmethod
    def convertToBytes(message: str) -> bytes:
        sizeOfMessage = len(message)
        return struct.pack('>I' + str(sizeOfMessage) + 's', sizeOfMessage, message)

    @staticmethod
    def sendOverTCP(address: tuple, jsonMessage: str, keepAlive: bool = False):
        socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketTCP.settimeout(10)
        socketTCP.connect((address[0], address[1]))
        bytesMessage = Client.convertToBytes(jsonMessage)  # or bytes(byteMessageSize) or byteMessageSize.to_bytes() or
        socketTCP.send(bytesMessage)

        if not keepAlive:
            socketTCP.close()

    def register(self):
        registerDict = {'type': 'register', 'nickname': self.nickname, 'ip': self.ip, 'port': self.port}
        self.sendOverTCP(self.SERVER, json.dumps(registerDict))

    def unregister(self):
        unregisterDict = {'type': 'unregister', 'nickname': self.nickname}
        self.sendOverTCP(self.SERVER, json.dumps(unregisterDict))

    def sendMessage(self, message: str, nickname: str):
        c = self.clients[nickname]  # ip, port

        # TODO: check if client already has a connection to other client
        connectToClientMessage = 'Please talk to me baby on {} one more time.'.format(self.socketTCP.getsockname()[1])
        bytesMessageRequest = Client.convertToBytes(connectToClientMessage)
        self.socketUDP.sendto(bytesMessageRequest, c['address'])
        self.socketTCP.accept()

        # alex und walle sind geil aaaaaaaaaaaaaaaaaaaaaaa lel du geilesau josef
        messageRequest = {'type': 'message', 'message': message}
        bytesMessage = Client.convertToBytes(json.dumps(messageRequest))
        self.socketTCP.send(bytesMessage)

    @staticmethod
    def receiveMessage(sock: socket):
        try:
            receivedMessage = sock.recv(8)
            messageSize, _ = struct.unpack('>I', receivedMessage)
            _, message = struct.unpack('>I' + str(messageSize) + 's', receivedMessage)
            print(str(message))
            decodedMessage = json.loads(message)
            messageType = decodedMessage['type']
            print(str(messageType))
        except socket.timeout:
            print('Socket timed out')
            sock.close()


if __name__ == '__main__':
    client = Client(argv[1])
