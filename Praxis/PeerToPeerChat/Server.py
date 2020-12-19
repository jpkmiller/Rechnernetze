import json
import socket
import threading
import select
from concurrent.futures import ThreadPoolExecutor

register_executor = ThreadPoolExecutor(2)
My_IP = '127.0.0.1'
server_ip = [127, 0, 0, 1]
print(My_IP)
My_PORT = 2000
server_activity_period = 30
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.bind((My_IP, My_PORT))
tcp_sock.listen(1)

# Nickname -> (IPAddr, Port, connection)
CLIENTS_LOCK = threading.Lock()
clientList = {}


def pack_payload(json_string):
    payload_msg = bytearray(json_string, 'utf-8')
    msg = bytearray(len(payload_msg).to_bytes(length=4, byteorder='big', signed=False))
    msg.extend(payload_msg)
    return bytes(msg)


def register_client(nickname, ip, port: int, conn: socket) -> bool:
    try:
        CLIENTS_LOCK.acquire()
        if nickname in clientList:
            CLIENTS_LOCK.release()
            return False
        added_list = [{'nickname': key, 'ip': value[0], 'port': value[1]} for key, value in clientList.items()]
        clientList[nickname] = (ip, port, conn)
        print("client added\nnew list: " + str(clientList))
    finally:
        CLIENTS_LOCK.release()

    user_list_dict = {
        'type': 'user-list',
        'users': {
            'added': added_list,
            'removed': []
        }
    }

    client_list_response = json.dumps(user_list_dict)
    conn.send(pack_payload(client_list_response))

    update_user_list_dict = {
        'type': 'user-list',
        'users': {
            'added': [{'nickname': nickname, 'ip': ip, 'port': port}],
            'removed': []
        }
    }
    update_list_response = json.dumps(update_user_list_dict)
    broadcast_clients(pack_payload(update_list_response), exclude=nickname)

    return True


def unregister_client(nickname, addr) -> bool:
    try:
        CLIENTS_LOCK.acquire()
        if nickname not in clientList:
            CLIENTS_LOCK.release()
            return False
        removed_client = clientList.pop(nickname)
        print("client removed\nnew list: " + str(clientList))
    finally:
        CLIENTS_LOCK.release()
    removed_client[3].close()
    update_user_list_dict = {
        'type': 'user-list',
        'users': {
            'added': [],
            'removed': [{'nickname': nickname, 'ip': removed_client[0], 'port': removed_client[1]}]
        }
    }
    update_list_response = json.dumps(update_user_list_dict)
    broadcast_clients(pack_payload(update_list_response))
    return True


def broadcast_clients(msg: bytes, exclude=None):
    try:
        CLIENTS_LOCK.acquire()
        clientList_copy = clientList.copy()
    finally:
        CLIENTS_LOCK.release()
    for nickname, (ip_addr, port, conn) in clientList_copy.items():
        # exclude certain client from broadcast e.g. register
        if exclude is not None and nickname is exclude:
            continue
        conn.send(msg)


message_types = {
    'register': register_client,
    'deregister': unregister_client,
    'broadcast': broadcast_clients
}


def process_request(conn, addr):
    print("try to receive data from " + str(addr))
    data = conn.recv(1024)
    size = int.from_bytes(bytes=data[:4], byteorder='big', signed=False)
    payload = data[4:].decode('utf-8')
    print(len(payload) < size)
    while len(payload) < size:
        data = conn.recv(1024)
        # print("data chunk received")
        payload += data.decode('utf-8')
    payload_dict = json.loads(payload)
    print("data converted payload is: " + str(payload_dict))
    msg_type = payload_dict['type']
    try:
        if msg_type == 'register':
            nickname = payload_dict['nickname']
            ip = payload_dict['ip']
            port = payload_dict['port']
            print(nickname + " tries to register")
            register_client(nickname, ip, port, conn)
        elif msg_type == 'unregister':
            nickname = payload_dict['nickname']
            print(nickname + " tries to deregister")
            unregister_client(nickname, addr)
        elif msg_type == 'broadcast':
            nickname = payload_dict['nickname']
            print(nickname + " tries to broadcast")
            broadcast_msg = payload_dict['message']
            msg = bytearray(len(broadcast_msg))
            msg.extend(broadcast_msg)
            broadcast_clients(msg, nickname)
        else:
            print("unknown message type")
    except KeyError:
        # TODO: handle malformed requests
        print("invalid messagetype")


msg_executor = ThreadPoolExecutor(7)


def check_msgs():
    timeout = 2
    while True:
        try:
            CLIENTS_LOCK.acquire()
            clientList_copy = clientList.copy()
        finally:
            CLIENTS_LOCK.release()
        if len(clientList.copy()) == 0:
            continue
        ready_sockets = select.select([c for ip, port, c in clientList_copy.values()], [], [], timeout)
        for conn in ready_sockets[0]:
            print("message received")
            msg_executor.submit(process_request, conn, conn.getpeername())


if __name__ == '__main__':
    threading.Thread(target=check_msgs).start()
    while True:
        print('waiting for connection')
        try:
            conn, addr = tcp_sock.accept()
            print('Incoming connection accepted: ', addr)
            register_executor.submit(process_request, conn, addr)
        except socket.timeout:
            print('Socket timed out listening')
            continue
