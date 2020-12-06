import socket
import time
import struct
import numpy

VPN_IP = '141.37.206.9'
# My_IP = '127.0.0.1'
My_IP = VPN_IP
My_PORT = 50000
server_activity_period = 30

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((My_IP, My_PORT))
print('Listening on Port ', My_PORT, ' for incoming TCP connections')

t_end = time.time() + server_activity_period  # Ende der Aktivitätsperiode

command_length = 64


functions = {
    'Summe': lambda l: numpy.copy(l).sum(initial=0),
    'Produkt': lambda l: numpy.copy(l).prod(initial=1),
    'Minimum': lambda l: numpy.copy(l).min(initial=0x7FFFFFFF),
    'Maximum': lambda l: numpy.copy(l).max(initial=0x80000000)
}

sock.listen(1)
print('Listening ...')

while time.time()<t_end:
    print("waiting for connection")
    try:
        conn, addr = sock.accept()
        print('Incoming connection accepted: ', addr)
        break
    except socket.timeout:
        print('Socket timed out listening', time.asctime())
        continue

while time.time() < t_end:
    try:
        data = conn.recv(1024)
        if not data:  # receiving empty messages means that the socket other side closed the socket
            print('Connection closed from other side')
            print('Closing ...')
            conn.close()
            break
        (id, operator, number) = struct.unpack('>I' + str(command_length) + 'sB', data[:69])
        operator = operator.decode('utf-8').strip('\x00')
        operands = struct.unpack_from('>' + str(number) + 'i', data[69:])
        result = functions[operator](operands)
        payload = struct.pack('>Ii', 1234, result)
        print(operator)
        print(operands)
        print(payload)
        conn.send(payload)
    except socket.timeout:
        print('Socket timed out at', time.asctime())

sock.close()
if conn:
    conn.close()
