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
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("9.9.9.9", 80))
        VPN_IP = s.getsockname()[0]
        s.close()
        self.nickname = nickname
        self.socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socketUDP.bind((VPN_IP, 0))
        self.socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketTCP.bind((VPN_IP, 0))
        self.socketTCP.listen(1)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = self.socketUDP.getsockname()
        self.SERVER = SERVER_IP, 50010
        self.CLIENTS_LOCK = threading.Lock()
        self.clients = {}
        self.tcp_to_nick = {}
        self.udp_to_nick = {}
        self.client_processor = ThreadPoolExecutor(max_workers=3)
        self.connection_processor = ThreadPoolExecutor(max_workers=3)
        self.server_thread = threading.Thread(target=self.receive_server_messages)
        self.client_thread = threading.Thread(target=self.receive_client_messages)
        self.connection_thread = threading.Thread(target=self.handle_connection_requests)
        self.stop_requested = False
        self.register()

    def start_thread(self):
        self.stop_requested = False
        self.client_processor = ThreadPoolExecutor(max_workers=3)
        self.connection_processor = ThreadPoolExecutor(max_workers=3)
        self.server_thread = threading.Thread(target=self.receive_server_messages)
        self.client_thread = threading.Thread(target=self.receive_client_messages)
        self.connection_thread = threading.Thread(target=self.handle_connection_requests)
        self.server_thread.start()
        self.client_thread.start()
        self.connection_thread.start()

    def stop_thread(self):
        self.stop_requested = True
        self.client_processor.shutdown()
        self.connection_processor.shutdown()
        self.client_thread.join()
        self.connection_thread.join()

    def update_user_list(self, users):
        to_remove = users['removed']
        to_add = users['added']
        try:
            self.CLIENTS_LOCK.acquire()
            for user in to_add:
                self.clients[user['nickname']] = [
                    user['ip'], user['port'], socket.socket(socket.AF_INET, socket.SOCK_STREAM)]
                self.udp_to_nick[(user['ip'], user['port'])] = user['nickname']
            for user in to_remove:
                self.clients.pop(user['nickname'])
                self.udp_to_nick.pop((user['ip'], user['port']))
        except KeyError:
            # TODO: handling malformed requests
            return
        finally:
            self.CLIENTS_LOCK.release()

    def receive_server_messages(self):
        while not self.stop_requested:
            # check if server has sent something
            try:
                ready_sockets, _, _ = select.select([self.serverSocket], [], [], 10)
            except ValueError:
                continue
            if ready_sockets:
                # receive data
                data = self.receive_message(self.serverSocket)
                print(data)
                if data is None:
                    break
                # process the message
                try:
                    msg_type = data['type']
                    if msg_type == 'user-list':
                        self.update_user_list(data['users'])
                    elif msg_type == 'message':
                        print("broadcast message:\n" + data['message'])
                    else:
                        print("unknown message type")
                except KeyError:
                    print(str(data))
                    print('FATAL: SERVER SEND MALFORMED MESSAGE')
                    continue
        self.stop_thread()

    def process_connection_requests(self, data, udp_addr: tuple):
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
        except ValueError:
            return
        print("port in process_connection_requests: " + str(port))

        try:
            with self.CLIENTS_LOCK:
                nickname = self.udp_to_nick[udp_addr]
        except KeyError:
            print("address not found")
            return

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            to = (udp_addr[0], int(port))
            print("try to connect to " + str(to))
            client_socket.connect(to)  # connect to tcp port
        except socket.timeout:
            print('remote tcp socket not valid')
            return
        print('connected')

        with self.CLIENTS_LOCK:
            self.clients[nickname][2] = client_socket
            self.tcp_to_nick[to] = nickname

        print('connection successfully achieved')

    def handle_connection_requests(self):
        self.socketUDP.settimeout(10)
        while not self.stop_requested:
            try:
                data, addr = self.socketUDP.recvfrom(64)
            except socket.timeout:
                continue
            print("data in handle_connection_requests: " + str(data))
            self.process_connection_requests(data, addr)
            # self.connection_processor.submit(self.process_connection_requests, data, addr)

    # this method processes request through opened tcp connections (aka. registered clients)
    def receive_client_messages(self):
        t = 2
        while not self.stop_requested:
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
            # the last argument is the t, how long this call should wait if no connection is ready.
            ready_sockets = select.select(connections, [], [], t)
            # go through all connections which are ready to read (open and a message is present)
            for conn in ready_sockets[0]:
                # start a thread which executes the request.
                self.process_client_msgs(conn)
                # self.client_processor.submit(self.process_client_msgs, conn)

    def process_client_msgs(self, conn: socket):
        msg = Client.receive_message(conn)
        print('received msg:')
        print(msg)
        with self.CLIENTS_LOCK:
            print(self.socketTCP)
            print(conn)
            print(conn.getpeername())
            print(self.tcp_to_nick)
            nickname = self.tcp_to_nick[conn.getpeername()]
        try:
            if msg['type'] == 'message':
                print('received message from ' + nickname + ':\n' + msg['message'])
        except KeyError:
            return

    @staticmethod
    def print_message(origin, msg):
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
        msg = bytearray(len(payload_msg).to_bytes(length=4, byteorder='little', signed=False))
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
            sock.close()

    def register(self):
        # (re)open socket
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # start threads
        self.start_thread()
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
        # stop threads

    def broadcast(self, message):
        msg = {
            'type': 'broadcast',
            'message': message
        }
        Client.sendOverTCP(self.serverSocket, self.SERVER, json.dumps(msg), True)

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

    def send_message(self, message: str, nickname: str):
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
            self.send_message(message, nickname)
        except OSError:
            conn = self.connect_to_client(user[0], user[1])
            try:
                self.CLIENTS_LOCK.acquire()
                self.clients[nickname][2] = conn
                self.tcp_to_nick[conn.getpeername()] = nickname
            except KeyError:
                print("client not found")
            finally:
                self.CLIENTS_LOCK.release()
            self.send_message(message, nickname)

    @staticmethod
    def receive_message(sock: socket):
        try:
            # get the size of the message
            # print("processing_request")
            b = sock.recv(4)
            # print("check for closed connection")
            if not b:
                # socket closed by Server
                print("Socket closed by Server. Do a register!")
                sock.close()
                return None
            size = int.from_bytes(bytes=b, byteorder='big', signed=False)
            # get the message itself
            data = sock.recv(size)
            # decode the data
            payload = data.decode('utf-8')
            # convert the json string to a dict
            payload_dict = json.loads(payload)
            return payload_dict
        except ConnectionResetError:
            sock.close()
        except json.decoder.JSONDecodeError:
            # TODO: handle with malformed request (Exception thrown by json.loads(payload))
            # one possible failure occurs if the size is wrong.
            # The client is not able to receive any message, because it will not get the right size.
            print("RECEIVED MSG WAS MALFORMED")
        except socket.timeout:
            # close connection if socket timed out
            sock.close()
        return {}


def test_wrong_size():
    pass


if __name__ == '__main__':
    client = Client(argv[1])
