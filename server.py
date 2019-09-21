import socket
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor
import time

class Server:
    def __init__(self, m):
        self.sock = socket.socket()
        self.m = m

    def run(self):
        self.sock.bind(("127.0.0.1", 10001))
        self.sock.listen(socket.SOMAXCONN)

    def worker(self):
        while True:
            conn, address = self.sock.accept()
            conn.settimeout(10)
            self.thread_maker(conn)

    def thread_maker(self, conn):
        with ThreadPoolExecutor() as pool:
            pool.submit(self.servicing(conn))

    def servicing(self, conn):
        with conn:
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        print("WHY??")
                        break
                except socket.timeout:
                    print("Connection closed by timeout")
                    break
                if type(data) != str:
                    data = data.decode("utf-8")
                if data == "1":
                    data_to_send = self.hour()
                    conn.send(data_to_send.encode("utf-8"))
                elif data == "2":
                    data_to_send = self.minutes()
                    conn.send(data_to_send.encode("utf-8"))
                elif data == "3":
                    data_to_send = self.seconds()
                    conn.send(data_to_send.encode("utf-8"))
                elif data == "4":
                    conn.close()
                    break
                else:
                    data_to_send = self.error(data)
                    conn.send(data_to_send.encode("utf-8"))

    def hour(self):
        hour = time.asctime().split()[3][:2]
        return hour

    def minutes(self):
        minutes = time.asctime().split()[3][3:5]
        return minutes

    def seconds(self):
        seconds = time.asctime().split()[3][6:]
        return seconds

    def stop(self):
        self.sock.close()

    def error(self, data):
        return "Вы ввели недоступную комманду: "


def main():
    list_of_processes = []
    server = Server(4)
    server.run()

    for i in range(server.m):
        process = Process(target=server.worker())
        list_of_processes.append(process)
    for i in list_of_processes:
        i.start()
    for i in list_of_processes:
        i.join()






if __name__ == "__main__":
    main()
