import socket as __socket

__s = __socket.socket()
__s.connect(('0.0.0.0', 12345))


def play(url):
    __s.send(b'play ' + url.encode() + b'\n')


def stop():
    __s.send(b'stop\n')


def pause():
    __s.send(b'pause\n')


def resume():
    __s.send(b'resume\n')


def ls():
    __s.send(b'ls\n')
    out = __s.recv(1024**2).decode().splitlines()
    out.sort()
    return out

def vol(vol):
    __s.send(b'vol ' + str(int(vol)).encode() + b'\n')