import socket
import time
import struct
import numpy
from concurrent.futures import ThreadPoolExecutor

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("9.9.9.9", 80))
VPN_IP = s.getsockname()[0]
s.close()
My_IP = VPN_IP
My_IP = '127.0.0.1'
print(My_IP)
My_PORT = 50000
server_activity_period = 30

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
sock.bind((My_IP, My_PORT))

t_end = time.time() + server_activity_period  # Ende der Aktivitätsperiode

command_length = 64

exec = ThreadPoolExecutor(5)

functions = {
    'Summe': lambda l: numpy.copy(l).sum(initial=0),
    'Produkt': lambda l: numpy.copy(l).prod(initial=1),
    'Minimum': lambda l: numpy.copy(l).min(initial=0x7FFFFFFF),
    'Maximum': lambda l: numpy.copy(l).max(initial=0x80000000)
}

def process_request(data, addr):
    try:
        (id, operator, number) = struct.unpack('>I' + str(command_length) + 'sB', data[:69])
        operator = operator.decode('utf-8').strip('\x00')
        operands = struct.unpack_from('>' + str(number) + 'i', data[69:])
        result = functions[operator](operands)
        payload = struct.pack('>Ii', 1234, result)
        print(operator)
        print(operands)
        print(payload)
        sock.sendto(payload, addr)
    except socket.timeout:
        print('Socket timed out at', time.asctime())

while time.time()<t_end:
    try:
        data, addr = sock.recvfrom(1024)
        exec.submit(process_request, data, addr)
    except socket.timeout:
        print('Socket timed out at', time.asctime())
        continue

exec.shutdown()
sock.close()
