import asyncio
import json

from UDPServer import UDPServer
from UDPSettings import UDPSettings


async def run_send_messages(udp_server: UDPServer):
    try:
        while True:
            await udp_server.send_messages()  # might need to 'queue up' messages for smoothness
    except Exception as ex:
        print(f"'run_send_messages' : {ex}")
        raise ex


async def run_receive_messages(udp_server: UDPServer):
    try:
        while True:
            await udp_server.receive_messages()
    except Exception as ex:
        print(f"'run_receive_messages' : {ex}")
        raise ex


async def main():
    with open("..\\appsettings.json") as config:
        data = json.load(config)

    server_settings = UDPSettings(data["UDPServer"]["Address"],
                                  int(data["UDPServer"]["SendToPort"]),
                                  int(data["UDPServer"]["ReceiveFromPort"]))

    print("Ctrl-C to end the program...")

    with UDPServer(server_settings) as udp_server:
        try:
            tasks = [
                run_send_messages(udp_server),
                run_receive_messages(udp_server)
            ]
            await asyncio.gather(*tasks)
        except Exception as appFailure:
            print(f"Application failure. Reason: {appFailure}")
        finally:
            print("Program shutting down...")


asyncio.run(main())
