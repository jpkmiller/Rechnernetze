import socket
import struct

message_types = ['register', 'deregister', 'send']

def register(ipAddress: str, port: int):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.settimeout(10)
    tcp_socket.connect((ipAddress, port))
    register = struct()

