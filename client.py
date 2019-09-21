import socket
import time


class Client:
    def __init__(self):
        self.sock = socket.socket()

    def start(self):
        with self.sock as socket1:
            socket1.connect(("127.0.0.1", 10001))
            while True:
                command = int(input("Введите номер одной из комманд: \n1) hour\n2) minutes\n3) seconds\n4) stop\n"))
                if command == 1:
                    socket1.send("1".encode("utf-8"))
                elif command == 2:
                    socket1.send("2".encode("utf-8"))
                elif command == 3:
                    socket1.send("3".encode("utf-8"))
                elif command == 4:
                    socket1.send("4".encode("utf-8"))
                    exit()
                else:
                    socket1.send("5".encode("utf-8"))

                data = socket1.recv(1024)
                print(data.decode("utf-8"))


def main():
    client = Client()
    client.start()


if __name__ == "__main__":
    main()

