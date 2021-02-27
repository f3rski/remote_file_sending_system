"""
Client that sends the file (uploads)
"""
import socket
import os
import argparse

SEPARATOR = "<sep>"
BUFFER_SIZE = 4096


def send_file_header(socket, filename, host, port):
    filesize = os.path.getsize(filename)
    payload = f"{filename}{SEPARATOR}{filesize}"
    print(payload)
    socket.send(payload.encode())


def send_file(filename, host, port):

    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")
    send_file_header(s, filename, host, port)
    # start sending the file
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            s.sendall(bytes_read)
    s.close()


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
    send_file(filename, host, port)