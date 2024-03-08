import socket

import requests

class Server:

    def __init__(self, team_name,server_name):
        self.team_name = team_name

        if len(server_name) > 32:
            raise ValueError("Server name must be 32 characters or less.")
        self.server_name = server_name

        # Getting my own ip for easy access
        self.ip = self.get_public_ip()

        # The port in which the client will listen
        self.dest_port = "13117"

        # Here I can add statistics for later

    def start_server(self):
        pass

    def get_public_ip(self):
        """
        Gets the server's computer using the ip request, returning the public ip.
        """
        try:
            response = requests.get('https://api.ipify.org')
            if response.status_code == 200:
                return response.text
        except requests.RequestException:
            return "Error: Unable to get IP Address"

    def get_free_udp_port(self):
        """
        Return a usble udp port from the computer.
        """
        # Create a UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            # Bind the socket to any available port
            udp_socket.bind(('localhost', 0))
            # Get the port number
            port = udp_socket.getsockname()[1]
            return port
        finally:
            udp_socket.close()

    def broadcast_server_start_message(self):
        """
        Broadcasts a message to announce that the server has started and is listening
        on the specified IP address and port of the self port.
        """
        # Get a free UDP port
        port = self.get_free_udp_port()

        # Create a UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        try:
            # Broadcast the message
            message = "Server started, listening on IP address " + self.ip
            udp_socket.sendto(message.encode(), ('<broadcast>', self.dest_port))
            print(f"Broadcasted message: {message}")
        finally:
            udp_socket.close()


    def broadcast_offer(self, server_port):
        """
        Broadcasts an offer message to port 13117.
        Args:
            server_name (str): The name of the server.
            server_port (int): The TCP port on the server that the client should connect to.

        Raises:
            ValueError: If the server name is longer than 32 characters.
        """

        # Create the offer message
        magic_cookie = b'\xab\xcd\xdc\xba'
        message_type = b'\x02'
        server_name_bytes = self.server_name.encode('utf-16be')[:64]  # 32 characters, UTF-16BE encoded
        server_port_bytes = server_port.to_bytes(2, byteorder='big')

        # Construct the packet
        packet = magic_cookie + message_type + server_name_bytes + server_port_bytes

        # Create a UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        try:
            # Broadcast the offer message
            udp_socket.sendto(packet, ('<broadcast>', 13117))
            print("Offer broadcasted successfully.")
        finally:
            udp_socket.close()







# def receive_offer():
#     """
#     Listens for and reads offer messages on port 13117.
#     """
#     # Create a UDP socket
#     udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#
#     try:
#         # Bind the socket to the port
#         udp_socket.bind(('0.0.0.0', 13117))
#         print("Listening for offer messages...")
#
#         # Receive and process incoming messages
#         while True:
#             data, addr = udp_socket.recvfrom(1024)
#             if data[:4] == b'\xab\xcd\xdc\xba' and data[4] == 0x02:
#                 # Extract server name and port from the packet
#                 server_name = data[5:37].decode('utf-16be').rstrip('\0')
#                 server_port = int.from_bytes(data[37:39], byteorder='big')
#
#                 print(f"Received offer from {addr[0]}:{addr[1]}")
#                 print(f"Server Name: {server_name}")
#                 print(f"Server Port: {server_port}")
#     finally:
#         udp_socket.close()