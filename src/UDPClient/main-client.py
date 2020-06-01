import asyncio
import json

from UDPClient import UDPClient
from UDPSettings import UDPSettings


async def run_receive_messages(udp_client: UDPClient):
    try:
        while True:
            await udp_client.server_update()
    except Exception as ex:
        print(f"'run_receive_messages' : {ex}")
        raise ex


async def run_send_messages(udp_client: UDPClient):
    try:
        while True:
            await udp_client.update()
    except Exception as ex:
        print(f"'run_send_messages' : {ex}")
        raise ex


async def main():
    with open("..\\appsettings.json") as config:
        data = json.load(config)

    client_settings = UDPSettings(data["UDPClient"]["Address"],
                                  int(data["UDPClient"]["SendToPort"]),
                                  int(data["UDPClient"]["ReceiveFromPort"]))

    with UDPClient(client_settings) as udp_client:
        try:
            tasks = [
                # run_receive_messages(udp_client)
                # ,
                run_send_messages(udp_client)
            ]
            await asyncio.gather(*tasks)
        except KeyboardInterrupt as kiex:
            print(f"KeyboardInterrupt: {kiex}")
        except Exception as appFailure:
            print(f"Application failure. Reason: {appFailure}")
        finally:
            print("Program shutting down...")
            print(f"Packets sent: {udp_client.packets_sent}")
            print(f"Packets received: {udp_client.packets_received}")

asyncio.run(main())
