import socket

from ServerResponse import ServerResponse
from UDPSettings import UDPSettings


class UDPClient():
    def __init__(self, client_settings: UDPSettings):
        self.client_settings = client_settings
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiving = True
        self.the_data = 1

    def __enter__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP protocol
        self.server_socket.bind((self.client_settings.server_address, self.client_settings.receive_from_port))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server_socket.close()

    async def send_message(self, message):
        cs = self.client_settings
        self.client_socket.sendto(bytes(message, 'utf-8'), (cs.server_address, cs.send_to_port))

    async def receive_message(self):
        if self.receiving:
            data, address = self.server_socket.recvfrom(1024)

            response = ServerResponse(address, data.decode('utf-8'))
        return response

    async def update(self):
        self.the_data += 1
        await self.send_message(self.the_data)
        print("client update")

    async def server_update(self):
        response = await self.receive_message()
        print("client server_update")

    async def wait_for_input(self):
        return

