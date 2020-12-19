import socket
import threading
import json
from concurrent.futures.thread import ThreadPoolExecutor
from sys import argv

import select

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
        self.CLIENTS_LOCK = threading.Lock()
        self.clients = {}
        self.server_executor = ThreadPoolExecutor(max_workers=3)

        threading.Thread(target=self.receive_server_messages).start()
        self.register()

    def update_user_list(self, users):
        to_remove = users['removed']
        to_add = users['added']
        try:
            self.CLIENTS_LOCK.acquire()
            for user in to_add:
                self.clients[user['nickname']] = (user['ip'], user['port'])
            for user in to_remove:
                self.clients.pop(user['nickname'])
        except KeyError:
            # TODO: handling malformed requests
            return
        finally:
            self.CLIENTS_LOCK.release()

    def receive_server_messages(self):
        while True:
            # check if server has send something
            ready_sockets, _, _ = select.select([self.serverSocket], [], [], 10)
            if ready_sockets:
                # receive data
                data = self.receive_message(self.serverSocket)
                # process the message
                # TODO: react on a broadcast message
                if data['type'] == 'user-list':
                    self.server_executor.submit(self.update_user_list, data['users'])
                else:
                    print("unknown message type")

    # packs the json_string to a bytes object which can be send via tcp.
    @staticmethod
    def convertToBytes(json_string: str) -> bytes:
        # create a bytearray since they are mutable (bytes are not)
        payload_msg = bytearray(json_string, 'utf-8')
        # extract the length in bytes
        msg = bytearray(len(payload_msg).to_bytes(length=4, byteorder='big', signed=False))
        # append the payload to the msg size
        msg.extend(payload_msg)
        # convert bytearray to bytes and return it
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
            sock.shutdown(1)
            sock.close()

    def register(self):
        # create register message
        registerDict = {'type': 'register', 'nickname': self.nickname, 'ip': self.ip, 'port': self.port}
        # convert and send it. the response will be processed in receive_server_messages
        self.sendOverTCP(self.serverSocket, self.SERVER, json.dumps(registerDict), True)

    def unregister(self):
        # create deregister message
        unregisterDict = {'type': 'unregister', 'nickname': self.nickname}
        # convert and send it. the response will be processed in receive_server_messages
        # socket needs to be kept alive, otherwise the socket of the other clients would be closed to
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
    def receive_message(sock: socket):
        try:
            # get the size of the message
            size = int.from_bytes(bytes=sock.recv(4), byteorder='big', signed=False)
            # get the message itself
            data = sock.recv(size)
            # decode the data
            payload = data.decode('utf-8')
            # convert the json string to a dict
            payload_dict = json.loads(payload)
            return payload_dict
        except json.decoder.JSONDecodeError:
            # TODO: handle with malformed request (Exception thrown by json.loads(payload))
            # one possible failure occurs if the size is wrong.
            # The client is not able to receive any message, because it will not get the right size.
            return
        except socket.timeout:
            # close connection if socket timed out
            sock.close()


if __name__ == '__main__':
    client = Client(argv[1])
