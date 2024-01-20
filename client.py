import time
import pyperclip

import socket
import threading
from cryptography.fernet import Fernet
import struct
import os
from dotenv import load_dotenv
import sys

load_dotenv()

HOST = os.environ['HOST']
PORT = int(os.environ['PORT'])
KEY = os.environ['KEY']
RANDOM = os.environ['RANDOM']
PREFIX_SIZE = int(os.environ['PREFIX_SIZE'])

INIT_MESSAGE = os.environ['INIT_MESSAGE']
ENCRYPTION_ENABLE = bool(os.environ['ENCRYPTION_ENABLE'])

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.sock.connect((host, port))
        except Exception as e:
            print(f"Exception raised during socket connection: {e}")
            sys.exit()

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()
        self.copy_event_thread = threading.Thread(target=self.copy_event)
        self.copy_event_thread.start()
        self.key = KEY.encode()
        self.recent_value = pyperclip.paste()

    def copy_event(self):
        self.recent_value = pyperclip.paste()
        while True:
            self.new_value = pyperclip.paste()
            if self.new_value  != self.recent_value:
                self.recent_value = self.new_value 
                print("-> Event triggered with new data copied: %s..." % str(self.recent_value)[:20])
                client.write(str(self.recent_value))
            time.sleep(0.1)

    def write(self, message):
        message = message.encode('utf-8')
        if ENCRYPTION_ENABLE:
            encrypted_message = self.encrypt(message)
            print(f'Sending: {encrypted_message}')
            self.send_all(encrypted_message)
        else:
            self.send_all(message)

    def send_all(self, message):
        message = struct.pack('>I', len(message)) + message
        self.sock.sendall(message)

    def stop(self):
        self.sock.close()

    def receive(self):
        while True:
            try:
                raw_message_length = self.receive_all(PREFIX_SIZE)
                if raw_message_length:
                    message_length = struct.unpack('>I', raw_message_length)[0]
                    data = self.receive_all(message_length)
                    raw_data = data.decode('utf-8')
                    try:
                        if raw_data != INIT_MESSAGE:
                            if ENCRYPTION_ENABLE:
                                decrypted_message = self.decrypt(bytes(data)).decode('utf-8')
                                print(f'Received value: {decrypted_message}')
                                if self.recent_value != decrypted_message:
                                    pyperclip.copy(decrypted_message)
                                # else:
                                #     print("Copy not triggered because local changes")
                            else:
                                print(f'Received value: {raw_data}')
                                pyperclip.copy(raw_data)
                        else:
                            print(raw_data)
                    except Exception as e:
                        print("Error during decryption: ", e)
                # else:
                #     print('data received without prefix length !!')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                self.kill_all_thread()
    
    def receive_all(self, n):
        data = bytearray()
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
                
    def encrypt(self, message) -> bytes:
        return Fernet(self.key).encrypt(message)

    def decrypt(self, ciphertext) -> bytes:
        return Fernet(self.key).decrypt(ciphertext)
    
    def kill_all_thread(self):
        print("Killing threads")
        self.copy_event_thread.join()
        self.receive_thread.join()


client = Client(HOST, PORT)
