import asyncio
import json

from UDPServer import UDPServer
from UDPSettings import UDPSettings


async def run(udp_server: UDPServer):
    running = True
    while running:
        try:
            await udp_server.update()  # when we receive data, send the update. might need to 'queue up' for smoothness
        except KeyboardInterrupt as kiex:
            print(f"Operation Cancelled. Reason: {kiex}")
            running = False


async def main():
    with open("..\\appsettings.json") as config:
        data = json.load(config)

    server_settings = UDPSettings(data["UDPServer"]["Address"],
                                  int(data["UDPServer"]["SendToPort"]),
                                  int(data["UDPServer"]["ReceiveFromPort"]))
    print("Ctrl-C to end the program...")

    with UDPServer(server_settings) as udp_server:
        try:
            await run(udp_server)
        except Exception as appFailure:
            print(f"Application failure. Reason: {appFailure}")
        finally:
            print("Program shutting down...")

asyncio.run(main())
