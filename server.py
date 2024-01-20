import socket
from _thread import *
import struct
import os
from dotenv import load_dotenv

load_dotenv()

PREFIX_SIZE = int(os.environ['PREFIX_SIZE'])

host = '127.0.0.1'
port = 9090
ThreadCount = 0

connections = {}

def client_handler(connection):
    init_message = os.environ['INIT_MESSAGE'].encode('utf-8')
    send_all(connection, init_message)
    port_origin = connection.getpeername()[1]
    connections[port_origin] = connection
    while True:
        data = []
        raw_message_length = receive_all(connection, PREFIX_SIZE)
        if raw_message_length and raw_message_length != '':
            message_length = struct.unpack('>I', raw_message_length)[0]
            data = receive_all(connection, message_length)
            message = data.decode('utf-8')
            print(f'Received and send: {message}')
            broadcast(port_origin, data)
    connection.close()


def broadcast(port_origin, message):
    for port, c in connections.items():
        if port_origin != port:
            send_all(c, message)

def accept_connections(server_socket):
    client, address = server_socket.accept()
    print('New connection to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(client_handler, (client, ))

def start_server(host, port):
    server_socket = socket.socket()
    try:
        server_socket.bind((host, port))
    except socket.error as e:
        print(str(e))
    print(f'Server is listing on the port {port}...')
    server_socket.listen()

    while True:
        accept_connections(server_socket)

def send_all(sock, message):
    message = struct.pack('>I', len(message)) + message
    sock.sendall(message)

def receive_all(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


print("Starting server...")
start_server(host, port)
