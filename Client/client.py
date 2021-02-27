"""
Client that sends the file (uploads)
"""
import socket
import os
import argparse


class Client:
    SEPARATOR = "<sep>"
    BUFFER_SIZE = 1024

    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__socket = socket.socket()

    def __send_file_header(self, filename):
        filesize = os.path.getsize(filename)
        payload = f"{filename}{Client.SEPARATOR}{filesize}"
        self.__socket.send(payload.encode())

    def send_file(self, filename):
        print(f"[+] Connecting to {host}:{port}")
        self.__socket.connect((host, port))
        print("[+] Connected.")
        self.__send_file_header(filename)
        # start sending the file
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(Client.BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                self.__socket.sendall(bytes_read)
        self.__socket.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple File Sender")
    parser.add_argument("file", help="File name to send")
    parser.add_argument("host", help="The host/IP address of the receiver")
    parser.add_argument("-p", "--port", help="Port to use, default is 5001", default=5001)
    args = parser.parse_args()
    filename = args.file
    host = args.host
    port = args.port

    client = Client(host, port)
    client.send_file(filename)