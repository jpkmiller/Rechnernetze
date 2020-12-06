import socket
import struct

VPN_IP = '141.37.206.9'
# Server_IP = '127.0.0.1'
Server_IP = VPN_IP
Server_PORT = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(10)

def calculate(operator, operands):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(10)
    id = 0
    operands_size = len(operands)
    payload = struct.pack('>I64sB' + str(operands_size) + 'i',
                          id,
                          operator.encode('utf-8'),
                          operands_size,
                          *operands
                          )
    print('Sending message', payload)
    sock.sendto(payload, (Server_IP, Server_PORT))
    try:
        data, addr = sock.recvfrom(1024)
        (id, result) = struct.unpack('>Ii', data)
        print(str(id) + ': ' + str(result))
    except socket.timeout:
        print('Socket timed out')
        close()

def close():
    sock.close()


def shutdown_server():
    sock.send('quit'.encode('utf-8'))
    sock.close()
