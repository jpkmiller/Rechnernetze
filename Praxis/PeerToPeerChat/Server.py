import socket
import struct
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(9)
server_activity_period = 30
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Nickname -> (IPAddr, Port)
clients = {}


class Server:

    def __init__(self, ip: tuple = ('127.0.0.1', 2000)):
        self.socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketTCP.bind(ip)
        self.clients = {}

    def registerClient(self, payload: bytes, addr, conn) -> bool:
        nickname, udp_port = struct.unpack('>64sH', payload)
        nickname = nickname.decode('utf-8').strip('\x00')
        if nickname in clients:
            return False

        number_of_clients = len(clients)
        response = bytearray(struct.pack('>H', number_of_clients))
        for client, (ip_addr, port) in clients.items():
            response.append(*struct.pack('>64s4cH', client.encode('utf-8'), ip_addr, port))

        conn.send(response)

        broadcast_payload = struct.pack('>32s64s4cH', 'join'.encode('utf-8'), nickname.encode('utf-8'), addr, udp_port)

        clients[nickname] = (addr, udp_port)
        return True

    def deregisterClient(self, payload: bytes, addr) -> bool:
        nickname, udp_port = struct.unpack('>64sH', payload)
        nickname = nickname.decode('utf-8').strip('\x00')

        old_ip, old_port = self.clients[nickname]
        if old_ip != addr or old_port != udp_port:
            return False
        clients.pop(nickname)
        return True

    @staticmethod
    def decode_ip(addr) -> str:
        return '.'.join(addr)

    def sendMessage(self, payload: bytes, ip_addr, port):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((Server.decode_ip(ip_addr), port))
        tcp_socket.settimeout(10)
        tcp_socket.send(payload)

    broadcast_msg = None
    isBroadcasting = False

    def broadcast_clients(self, payload: bytes, exclude=None):
        for nickname, (ip_addr, port) in clients.items():
            # exclude certain client from broadcast e.g. register
            if exclude is not None and nickname is exclude:
                continue

            connection_request = struct.pack('>32s4cH', 'connect to', self.server_ip, port)
            udp_sock.sendto()
            conn.send(payload)

    def send_broadcast(self, _, addr, conn):
        conn.send(broadcast_msg)

    # deregister der form <Nickname><Port>

    def process_request(self, conn, addr):
        data = conn.recv(1024)

        message_type = data[:64].decode('utf-8')
        message_types[message_type](data[64:], addr, conn)
        pass


if __name__ == '__main__':
    server = Server()
    while True:
        print('waiting for connection')
        try:
            conn, addr = server.accept()
            print('Incoming connection accepted: ', addr)
            executor.submit(process_request, conn, addr)
        except socket.timeout:
            print('Socket timed out listening')
            continue
