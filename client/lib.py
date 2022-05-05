class Client:
    def __init__(self, host, port):
        import socket as __socket
        self.host = host
        self.port = port
        self.__s = __socket.socket()
        self.__s.connect((host, port))

    def play(self, url):
        self.__s.send(b'play ' + url.encode() + b'\n')

    def stop(self):
        self.__s.send(b'stop\n')

    def pause(self):
        self.__s.send(b'pause\n')

    def resume(self):
        self.__s.send(b'resume\n')

    def ls(self):
        self.__s.send(b'ls\n')
        out = self.__s.recv(1024**2).decode().splitlines()
        out.pop()
        out.sort()
        return out

    def vol(self, vol):
        self.__s.send(b'vol ' + str(int(vol)).encode() + b'\n')
