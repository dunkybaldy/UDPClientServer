import asyncio
import json

from UDPClient import UDPClient
from UDPSettings import UDPSettings


async def run_receive_messages(udp_client: UDPClient):
    running = True

    while running:
        try:
            await udp_client.server_update()
        except KeyboardInterrupt as kiex:
            print(f"Operation Cancelled. Reason: {kiex}")
            running = False


async def run_send_messages(udp_client: UDPClient):
    running = True

    while running:
        try:
            await udp_client.update()
        except KeyboardInterrupt as kiex:
            print(f"Operation Cancelled. Reason: {kiex}")
            running = False


async def main():
    with open("..\\appsettings.json") as config:
        data = json.load(config)

    client_settings = UDPSettings(data["UDPClient"]["Address"],
                                  int(data["UDPClient"]["SendToPort"]),
                                  int(data["UDPClient"]["ReceiveFromPort"]))

    print("Ctrl-C to end the program...")

    with UDPClient(client_settings) as udp_client:
        try:
            asyncio.ensure_future(run_send_messages(udp_client))
            asyncio.(run_receive_messages(udp_client))
            asyncio.get_event_loop().run_forever()
        except Exception as appFailure:
            print(f"Application failure. Reason: {appFailure}")
        finally:
            print("Program shutting down...")

asyncio.run(main())
