import socket
import threading
import json
from concurrent.futures.thread import ThreadPoolExecutor
from sys import argv
import re

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
        self.socketUDP.bind(('127.0.0.1', 0))
        self.socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketTCP.bind(('127.0.0.1', 0))
        self.socketTCP.listen(1)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = self.socketUDP.getsockname()
        self.SERVER = SERVER_IP, 2000
        self.CLIENTS_LOCK = threading.Lock()
        self.clients = {}
        self.client_processor = ThreadPoolExecutor(max_workers=3)
        self.connection_processor = ThreadPoolExecutor(max_workers=3)

        threading.Thread(target=self.receive_server_messages).start()
        threading.Thread(target=self.receive_client_messages).start()
        threading.Thread(target=self.handle_connection_requests).start()
        self.register()

    def update_user_list(self, users):
        to_remove = users['removed']
        to_add = users['added']
        try:
            self.CLIENTS_LOCK.acquire()
            for user in to_add:
                self.clients[user['nickname']] = [
                    user['ip'], user['port'], socket.socket(socket.AF_INET, socket.SOCK_STREAM)]
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
                try:
                    type = data['type']
                    if type == 'user-list':
                        self.update_user_list(data['users'])
                    elif type == 'message':
                        print("broadcast message:\n" + data['message'])
                    else:
                        print("unknown message type")
                except KeyError:
                    print('FATAL: SERVER SEND MALFORMED MESSAGE')
                    continue

    def process_connection_requests(self, data, addr):
        data = data.decode('utf-8')
        print("data in process_connection_requests: " + data)
        try:
            searchPort = re.match(r'^Please talk to me baby on (?P<port>\d+) one more time.$', data)
            groupDict = searchPort.groupdict()
            if groupDict is not None:
                port = groupDict.get('port')
                if port is None:
                    return
            else:
                return
            """
            #port = int(re.search(r'\d+', data).group())
            # re.findall(r'\d+', data)[0]
            print(data)
            ohne_prefix = data.removeprefix('Please talk to me baby on ')
            print(ohne_prefix)
            ohne_suffix = ohne_prefix.removesuffix(' one more time.')
            print(ohne_suffix)
            print(data.removeprefix('Please talk to me baby on ').removesuffix(' one more time.'))
            port = int(data.removeprefix('Please talk to me baby on ').removesuffix(' one more time.'))
            """
        except ValueError:
            return
        print("port in process_connection_requests: " + str(port))

        try:
            self.CLIENTS_LOCK.acquire()
            client_list_copy = self.clients.copy()
        finally:
            self.CLIENTS_LOCK.release()
        print(addr[0])
        for nickname, client in client_list_copy.items():
            # search for ip and udp port
            if client[0] == addr[0] and client[1] == addr[1]:
                print("found address")
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    to = (addr[0], int(port))
                    print("try to connect to " + str(to))
                    client_socket.connect(to)  # connect to tcp port
                except socket.timeout:
                    print('remote tcp socket not valid')
                    return
                print('connected')
                try:
                    self.CLIENTS_LOCK.acquire()
                    self.clients[nickname][2] = client_socket
                finally:
                    self.CLIENTS_LOCK.release()
                print('connection successfully achieved')
                break

    def handle_connection_requests(self):
        data, addr = self.socketUDP.recvfrom(64)
        print("data in handle_connection_requests: " + str(data))

        self.connection_processor.submit(self.process_connection_requests, data, addr)

    # this method processes request through opened tcp connections (aka. registered clients)
    def receive_client_messages(self):
        timeout = 2
        while True:
            try:
                self.CLIENTS_LOCK.acquire()
                # copy the list! it is likely that the request will change the client list
                clientList_copy = self.clients.copy()
            finally:
                self.CLIENTS_LOCK.release()
            if len(clientList_copy) == 0:
                continue
            # get all connections of the clientList
            connections = [c for ip, port, c in clientList_copy.values()]
            # select filters all connections ready to read (arg1), ready to write (arg2), or 'exceptional?' state (arg3)
            # the last argument is the timeout, how long this call should wait if no connection is ready.
            ready_sockets = select.select(connections, [], [], timeout)
            # go through all connections which are ready to read (open and a message is present)
            for conn in ready_sockets[0]:
                # start a thread which executes the request.
                self.client_processor.submit(self.process_client_msgs, conn)

    def process_client_msgs(self, conn: socket):
        msg = Client.receive_message(conn)
        print(msg)
        try:
            if msg['type'] == 'message':
                print('received message: \n' + msg['message'])
        except KeyError:
            return

    def print_message(self, origin, msg):
        try:
            print('received message from ' + origin + ': \n' + msg['message'])
        except KeyError:
            return

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

    def connect_to_client(self, ip: str, port: int):
        connectToClientMessage = 'Please talk to me baby on {} one more time.'.format(
            str(self.socketTCP.getsockname()[1]))
        self.socketUDP.sendto(bytes(connectToClientMessage, 'utf-8'), (ip, port))
        self.socketTCP.settimeout(10)
        try:
            print("waiting for connection on " + str(self.socketTCP))
            conn, _ = self.socketTCP.accept()
        except socket.timeout:
            # TODO: think about better handling
            print("das hat nicht geklappt")
        return conn

    def sendMessage(self, message: str, nickname: str):
        try:
            self.CLIENTS_LOCK.acquire()
            user = self.clients[nickname]
        finally:
            self.CLIENTS_LOCK.release()

        messageRequest = {'type': 'message', 'message': message}
        bytesMessage = Client.convertToBytes(json.dumps(messageRequest))
        # TODO: think about what could happen
        try:
            user[2].send(bytesMessage)
        except socket.timeout:
            # might be a bad idea. WARNING: not delete this because socket.timeout is a subtype of OSError
            self.sendMessage(message, nickname)
        except OSError:
            conn = self.connect_to_client(user[0], user[1])
            try:
                self.CLIENTS_LOCK.acquire()
                self.clients[nickname][2] = conn
            except KeyError:
                print("client not found")
            finally:
                self.CLIENTS_LOCK.release()
            self.sendMessage(message, nickname)

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
