import json
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


def register_client(nickname, ip, port: int, conn) -> bool:
    if nickname in clientList:
        return False

    added_list = [{'nickname': key, 'ip': value[0], 'port': value[1]} for key, value in clientList.items()]
    user_list_dict = {
        'type': 'user-list',
        'users': {
            'added': added_list,
            'removed': []
        }
    }

    client_list_response = json.dumps(user_list_dict)
    client_list_msg = bytearray(client_list_response, 'utf-8')
    msg = bytearray(len(client_list_msg))
    msg.extend(client_list_msg)
    conn.send(bytes(msg))

    update_user_list_dict = {
        'type': 'user-list',
        'users': {
            'added': [{'nickname': nickname, 'ip': ip, 'port': port}],
            'removed': []
        }
    }
    update_list_response = json.dumps(update_user_list_dict)
    update_list_msg = bytearray(update_list_response, 'utf-8')
    update_msg = bytearray(len(update_list_msg))
    update_msg.extend(update_list_msg)
    broadcast_clients(bytes(update_msg))

    clientList[nickname] = (ip, port, conn)
    return True


def unregister_client(nickname, addr) -> bool:
    if nickname not in clientList or clientList[nickname][0] != addr:
        return False
    removed_client = clientList.pop(nickname)
    removed_client[3].close()
    update_user_list_dict = {
        'type': 'user-list',
        'users': {
            'added': [],
            'removed': [{'nickname': nickname, 'ip': removed_client[0], 'port': removed_client[1]}]
        }
    }
    update_list_response = json.dumps(update_user_list_dict)
    update_list_msg = bytearray(update_list_response, 'utf-8')
    update_msg = bytearray(len(update_list_msg))
    update_msg.extend(update_list_msg)
    broadcast_clients(bytes(update_msg))
    return True


def broadcast_clients(msg: bytes, exclude=None):
    for nickname, (ip_addr, port, conn) in clientList.items():
        # exclude certain client from broadcast e.g. register
        if exclude is not None and nickname is exclude:
            continue
        conn.send(msg)


# deregister der form <Nickname><Port>
message_types = {
    'register': register_client,
    'deregister': unregister_client,
    'broadcast': broadcast_clients
}


def process_request(conn, addr):
    data = conn.recv(1024)
    size = int.from_bytes(bytes=data[:4], byteorder='little', signed=False)
    payload = data[4:].decode('utf-8')
    while len(payload) <= size:
        data = conn.recv(1024)
        payload += data.decode('utf-8')

    # TODO: check if this is needed
    json.dumps(payload)
    # -----------------------------

    payload_dict = json.loads(payload)
    msg_type = payload_dict['type']
    try:
        if msg_type == 'register':
            nickname = payload['nickname']
            ip = payload['ip']
            port = payload['port']
            register_client(nickname, ip, port, conn)

        elif msg_type == 'unregister':
            nickname = payload['nickname']
            unregister_client(nickname, addr)

        elif msg_type == 'broadcast':
            nickname = payload['nickname']
            broadcast_msg = payload['message']
            msg = bytearray(len(broadcast_msg))
            msg.extend(broadcast_msg)
            broadcast_clients(msg, nickname)

    except KeyError:
        # TODO: handle malformed requests
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
