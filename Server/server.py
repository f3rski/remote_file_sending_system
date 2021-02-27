import socket
import os
import signal


def sigint_signal_handler(sig, frame):
    print('\nSIGINT catched, closing server')
    Server.BREAK_FLAG = True
    exit(1)


class Server:
    """Websocket server component"""
    BREAK_FLAG = False
    SEPARATOR = "<sep>"
    BUFFER_SIZE = 1024

    def __init__(self):
        signal.signal(signal.SIGINT, sigint_signal_handler)
        self.__ip = "0.0.0.0"
        self.__port = 5001
        self.__buffer_size = Server.BUFFER_SIZE
        self.__socket = None

        self.__initialize()

    def __initialize(self):
        self.__socket = socket.socket()
        self.__socket.bind((self.__ip, self.__port))

    def __start_listening(self):
        self.__socket.listen(5)
        print(f"Listening as {self.__ip}:{self.__port}")

    def start(self):
        self.__start_listening()
        while not Server.BREAK_FLAG:
            connection, address = self.__socket.accept()
            print(f"[+] {address} is connected.")

            received = connection.recv(self.__buffer_size).decode()
            filename, filesize = received.split(Server.SEPARATOR)

            # remove absolute path if there is
            filename = os.path.basename(filename)
            print(f"Receiving: {filename}, with size: {filesize}")

            # start receiving the file from the socket
            # and writing to the file stream
            with open(filename, "wb") as f:
                while True:
                    # read 1024 bytes from the socket (receive)
                    bytes_read = connection.recv(self.__buffer_size)
                    if not bytes_read:
                        print("Nothing to read, transmission done")
                        break
                    # write to the file the bytes we just received
                    f.write(bytes_read)
        self.close(connection)

    def close(self, client_socket):
        Server.BREAK_FLAG = True
        client_socket.close()
        self.__socket.close()


if __name__ == "__main__":
    server = Server()
    server.start()