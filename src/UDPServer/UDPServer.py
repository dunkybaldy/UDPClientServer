import socket

from ServerResponse import ServerResponse
from UDPSettings import UDPSettings


class UDPServer:
    def __init__(self, server_settings: UDPSettings):
        self.server_settings = server_settings
        self.receiving = True
        self.the_data = 1
        self.clients = []

    def __enter__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP protocol
        self.server_socket.bind((self.server_settings.server_address, self.server_settings.receive_from_port))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server_socket.close()

    async def receive_message(self):
        if self.receiving:
            data, address = self.server_socket.recvfrom(1024)

            response = ServerResponse(address, data.decode('utf-8'))
        return response

    async def send_message(self, message):
        cs = self.server_settings
        self.server_socket.sendto(bytes(message, 'utf-8'), (cs.server_address, cs.send_to_port))
        print(f"Message {message} sent.")

    async def delegate(self, response: ServerResponse):
        self.the_data = str(response.data)
        print(self.the_data)

    async def update(self):
        await self.delegate(await self.receive_message())  # should receive messages first
        await self.send_message(f"From the Server: {self.the_data}")
