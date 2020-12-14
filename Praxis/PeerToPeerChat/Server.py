import socket
import struct
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(9)
My_IP = '127.0.0.1'
server_ip = [127, 0, 0, 1]
print(My_IP)
My_PORT = 50000
server_activity_period = 30
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.bind((My_IP, My_PORT))

# Nickname -> (IPAddr, Port)
clientList = {}


def register_client(payload: bytes, addr, conn) -> bool:
    nickname, udp_port = struct.unpack('>64sH', payload)
    nickname = nickname.decode('utf-8').strip('\x00')
    if nickname in clientList:
        return False

    number_of_clients = len(clientList)
    response = bytearray(struct.pack('>H', number_of_clients))
    for client, (ip_addr, port) in clientList.items():
        response.append(*struct.pack('>64s4cH', client.encode('utf-8'), ip_addr, port))

    conn.send(response)

    broadcast_payload = struct.pack('>32s64s4cH', 'join'.encode('utf-8'), nickname.encode('utf-8'), addr, udp_port)

    clientList[nickname] = (addr, udp_port)
    return True


def deregister_client(payload: bytes, addr) -> bool:
    nickname, udp_port = struct.unpack('>64sH', payload)
    nickname = nickname.decode('utf-8').strip('\x00')

    old_ip, old_port = clientList[nickname]
    if old_ip != addr or old_port != udp_port:
        return False
    clientList.pop(nickname)
    return True


def decode_ip(addr) -> str:
    return '.'.join(addr)


def send_message(payload: bytes, ip_addr, port):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((decode_ip(ip_addr), port))
    tcp_socket.settimeout(10)
    tcp_socket.send(payload)


broadcast_msg = None
isBroadcasting = False


def broadcast_clients(payload: bytes, exclude=None):
    for nickname, (ip_addr, port) in clientList.items():
        # exclude certain client from broadcast e.g. register
        if exclude is not None and nickname is exclude:
            continue

        connection_request = struct.pack('>32s4cH', 'connect to', server_ip, port)
        udp_sock.sendto()
        conn.send(payload)


def send_broadcast(_, addr, conn):
    conn.send(broadcast_msg)


# deregister der form <Nickname><Port>
message_types = {
    'register': register_client,
    'deregister': deregister_client,
    'broadcast': broadcast_clients,
    'listening': send_broadcast
}


def process_request(conn, addr):
    data = conn.recv(1024)

    message_type = data[:64].decode('utf-8')
    message_types[message_type](data[64:], addr, conn)
    pass


if __name__ == '__main__':
    while True:
        print('waiting for connection')
        try:
            conn, addr = tcp_sock.accept()
            print('Incoming connection accepted: ', addr)
            executor.submit(process_request, conn, addr)
        except socket.timeout:
            print('Socket timed out listening')
            continue
