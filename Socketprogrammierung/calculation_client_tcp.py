import socket
import struct

Server_IP = '127.0.0.1'
Server_PORT = 50000
MESSAGE = 'Hello, World!'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)


def connect():
    print('Connecting to TCP server with IP ', Server_IP, ' on Port ', Server_PORT)
    sock.connect((Server_IP, Server_PORT))


def calculate(operator, operands):
    id = 0
    operands_size = len(operands)
    payload = struct.pack('>I64sB' + str(operands_size) + 'i',
                          id,
                          operator.encode('utf-8'),
                          operands_size,
                          *operands
                          )
    print('Sending message', payload)
    sock.send(payload)
    try:
        (id, result) = struct.unpack('>Ii', sock.recv(8))
        print(str(id) + ': ' + str(result))
    except socket.timeout:
        print('Socket timed out')
        close()


def close():
    sock.close()


def shutdown_server():
    sock.send('quit'.encode('utf-8'))
    sock.close()
