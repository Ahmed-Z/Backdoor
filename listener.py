import socket


class Listener:
    def __init__(self, IP, PORT):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((IP,PORT))
        self.listener.listen(0)
        print("[+] Waiting for incoming connection on PORT: " + str(PORT))
        try:
            self.connection, address = self.listener.accept()
        except KeyboardInterrupt:
            exit("\nEXIT")
        print("[+] New connection from " + str(address))

    def r_send(self, msg):
        self.connection.send(msg.encode())
     
    def r_recv(self):
        data = ""
        while (not data.endswith("done")):
            data += self.connection.recv(1024).decode()
        return data[:-4]

    def run(self):
        while(True):
            try:
                cmd = str(input(">> "))
                self.r_send(cmd)
                result = self.r_recv()
                print(result)
            except KeyboardInterrupt:
                self.r_send("terminate")
                self.connection.close()
                exit("\nEXIT")

listener = Listener("127.0.0.1",2000)
listener.run()