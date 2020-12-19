import json
import socket
import threading
import select
from concurrent.futures import ThreadPoolExecutor

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


# packs the json_string to a bytes object which can be send via tcp.
def pack_payload(json_string):
    # create a bytearray since they are mutable (bytes are not)
    payload_msg = bytearray(json_string, 'utf-8')
    # extract the length in bytes
    msg = bytearray(len(payload_msg).to_bytes(length=4, byteorder='big', signed=False))
    # append the payload to the msg size
    msg.extend(payload_msg)
    # convert bytearray to bytes and return it
    return bytes(msg)


def register_client(nickname, ip, port: int, conn: socket) -> bool:
    try:
        CLIENTS_LOCK.acquire()
        # check if client is already registered
        if nickname in clientList:
            CLIENTS_LOCK.release()
            # duplicate registration fails
            return False
        # convert local dictionary to a list following the protocols schema:
        #   [
        #       {
        #           'nickname': ...,
        #           'ip': ...,
        #           'port': ....
        #       }, ...
        #   ]
        added_list = [{'nickname': key, 'ip': value[0], 'port': value[1]} for key, value in clientList.items()]
        # add the client to the clientList.
        # This needs to be done now, otherwise another client could register without knowledge of this one
        clientList[nickname] = (ip, port, conn)
        # The client now receives updates. If a client would register now, he would be added through an update.
        print("client added\nnew list: " + str(clientList))
    finally:
        CLIENTS_LOCK.release()

    # create the initial clientList for the current client
    user_list_dict = {
        'type': 'user-list',
        'users': {
            'added': added_list,
            'removed': []
        }
    }
    # convert the dict to a json string
    client_list_response = json.dumps(user_list_dict)
    # pack the json_string and send the initial client list to the client
    conn.send(pack_payload(client_list_response))

    # now create the update message for all other clients, ...
    update_user_list_dict = {
        'type': 'user-list',
        'users': {
            'added': [{'nickname': nickname, 'ip': ip, 'port': port}],
            'removed': []
        }
    }
    # ...convert it to json ...
    update_list_response = json.dumps(update_user_list_dict)
    # ... and broadcast it to all other clients.
    broadcast_clients(pack_payload(update_list_response), exclude=nickname)
    return True


def unregister_client(nickname, addr) -> bool:
    try:
        CLIENTS_LOCK.acquire()
        # check if client exists
        # TODO: make sure a client can deregister a different client (remember: TCPport != UDP port)
        if nickname not in clientList:
            CLIENTS_LOCK.release()
            return False
        # get and remove client
        removed_client = clientList.pop(nickname)
        print("client removed\nnew list: " + str(clientList))
    finally:
        CLIENTS_LOCK.release()
    # create update message for the other users
    update_user_list_dict = {
        'type': 'user-list',
        'users': {
            'added': [],
            'removed': [{'nickname': nickname, 'ip': removed_client[0], 'port': removed_client[1]}]
        }
    }
    # convert it to json ...
    update_list_response = json.dumps(update_user_list_dict)
    # and broadcast it to all users (current user is already removed -> exclude ot needed)
    broadcast_clients(pack_payload(update_list_response))
    # finally close the connection
    removed_client[3].close()
    return True


def broadcast_clients(msg: bytes, exclude=None):
    try:
        CLIENTS_LOCK.acquire()
        # make a copy, since the list could change while broadcasting
        clientList_copy = clientList.copy()
    finally:
        CLIENTS_LOCK.release()
    # go through all clients
    for nickname, (ip_addr, port, conn) in clientList_copy.items():
        # exclude certain client from broadcast e.g. register
        if exclude is not None and nickname is exclude:
            continue
        # send the message over the TCP port
        # TODO: What happens if the connection is already closed?
        conn.send(msg)


# tries to receive the data, decodes it and delegates the request to the corresponding function
def process_request(conn, addr):
    try:
        # get the size of the message
        size = int.from_bytes(bytes=conn.recv(4), byteorder='big', signed=False)
        # get the message itself
        data = conn.recv(size)
        # decode the data
        payload = data.decode('utf-8')
        # convert the json string to a dict
        payload_dict = json.loads(payload)
    except json.decoder.JSONDecodeError:
        # TODO: handle with malformed request (Exception thrown by json.loads(payload))
        # actually those are clientside errors. For now just ignore them.
        return
    except socket.timeout:
        # close connection if socket timed out
        conn.close()
        return
    # get message type and delegate the request
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


# create a thread pool to allow parallel requests.
# Could be split: One for connection requests and one for requests through opened ports
request_processor = ThreadPoolExecutor(7)


# this method processes request through opened tcp connections (aka. registered clients)
def check_msgs():
    timeout = 2
    while True:
        try:
            CLIENTS_LOCK.acquire()
            # copy the list! it is likely that the request will change the client list
            clientList_copy = clientList.copy()
        finally:
            CLIENTS_LOCK.release()
        if len(clientList.copy()) == 0:
            continue
        # get all connections of the clientList
        connections = [c for ip, port, c in clientList_copy.values()]
        # select filters all connections ready to read (arg1), ready to write (arg2), or 'exceptional?' state (arg3)
        # the last argument is the timeout, how long this call should wait if no connection is ready.
        ready_sockets = select.select(connections, [], [], timeout)
        # go through all connections which are ready to read (open and a message is present)
        for conn in ready_sockets[0]:
            print("message received")
            # start a thread which executes the request.
            request_processor.submit(process_request, conn, conn.getpeername())


if __name__ == '__main__':
    # start the thread listening to request on opened TCP connections
    threading.Thread(target=check_msgs).start()
    # start the while loop, waiting for incoming tcp connections (either registrations or reconnects)
    while True:
        print('waiting for connection')
        try:
            conn, addr = tcp_sock.accept()
            print('Incoming connection accepted: ', addr)
            # normally after a connection is requested, a message will follow. so just process it right away.
            # mostly those requests are register requests.
            request_processor.submit(process_request, conn, addr)
        except socket.timeout:
            print('Socket timed out listening')
