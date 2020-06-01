import socket

from ServerResponse import ServerResponse


async def receive_message(_socket: socket, byte_buffer):
    try:
        data, address = _socket.recvfrom(byte_buffer)

        response = ServerResponse(address, data.decode('utf-8'))
        return response
    except Exception as ex:
        print(f"'UDPFunctions.receive_message' error: {ex}")


async def send_message(_socket: socket, message, address, port):
    try:
        _socket.sendto(bytes(str(message), 'utf-8'), (address, port))
    except Exception as ex:
        print(f"'UDPFunctions.send_message' error: {ex}")
