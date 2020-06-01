import socket

import UDPFunctions
from UDPSettings import UDPSettings


class UDPServer:
    def __init__(self, server_settings: UDPSettings):
        self.server_settings = server_settings
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiving = True
        self.the_data = 1
        self.clients = []

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        self.server_socket.bind((self.server_settings.server_address, self.server_settings.receive_from_port))
        print("Opened socket connection")
        return self

    def close(self):
        self.server_socket.close()
        print("Closed socket connection")

    async def send_messages(self):
        await UDPFunctions.send_message(self.server_socket, self.the_data,
                                        self.server_settings.server_address, self.server_settings.send_to_port)

    async def receive_messages(self):
        await UDPFunctions.receive_message(self.server_socket, 1024)
