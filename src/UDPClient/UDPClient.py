import socket

import UDPFunctions
from UDPSettings import UDPSettings


class UDPClient:
    def __init__(self, client_settings: UDPSettings):
        self.client_settings = client_settings
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiving = False
        self.the_data = 1
        self.packets_sent = 0
        self.packets_received = 0

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        self.client_socket.bind((self.client_settings.server_address, self.client_settings.receive_from_port))
        self.receiving = True
        print("Opened socket connection")
        return self

    def close(self):
        self.receiving = False
        self.client_socket.close()
        print("Closed socket connection")

    async def update(self):
        self.the_data += 1
        await UDPFunctions.send_message(self.client_socket, self.the_data,
                                        self.client_settings.server_address, self.client_settings.send_to_port)
        self.packets_sent += 1

    async def server_update(self):
        print("server_update - start")
        await UDPFunctions.receive_message(self.client_socket, 1024)
        self.packets_received += 1
        print("server_update - finish")
