from socket import *
from multiprocessing import Process

class Server():
	def __init__(self, PORT):
		self.NAME = socket.gethostname()
		self.HOST = socket.gethostbyname(self.NAME)
		self.PORT = PORT
		self.ADDR = (self.HOST, self.PORT)
		self.SOCK = socket.socket()
		self.SOCK.bind(self.ADDR)
		self.alive = 1
	def start(self, listenNum):
		self.SOCK.listen(listenNum)
		print('Start listen...')
		while self.alive:
			clientCNNT, clientADDR = self.SOCK.accept()  #建立客户端连接
			print('client addr:', clientADDR)
			p = Process(target = self.talk, args = (clientCNNT,))
			p.start()
		self.close()
	def talk(self, clientCNNT):
		while 1:
			try:
				data = clientCNNT.recv(1024)
				if not data:
					break
				if data == b'close':
					self.close()
					return
				clientCNNT.send(b'hi, client:', data.upper())
				print(str.decode(data))
			except ConnectionResetError:
				break
		print('connection close')
		clientCNNT.close()
	def sendStr(self, clientCNNT, string):
		clientCNNT.send(str.encode(string))
		data = clientCNNT.recv(1024)
		return data
	def close(self):
		self.alive = 0
		self.SOCK.close()


class Client():
	def __init__(self, HOST, PORT):
		self.HOST = HOST
		self.PORT = PORT
		self.ADDR = (HOST, PORT)
		self.SOCK = socket.socket()
		self.alive = 1
	def connect(self):
		self.SOCK.connect(self.ADDR)
	def sendStr(self, string):
		self.SOCK.send(str.encode(string))
		data = self.SOCK.recv(1024)
		print(data)
		return data
	def listen(self):
		pass
	def close(self):
		self.alive = 0
		self.SOCK.close()


# 负责通信
def talk(conn, addr):
    while True:
        try:
            data = conn.recv(1024)
            if not data: break
            conn.send(data.upper())
        except ConnectionResetError:
            break
    conn.close()


# 建立链接
def server(host, port, listenNum = 5, target = talk):
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(listenNum)

    while True:
        conn, addr = server.accept()
        p = Process(target = target, args=(conn, addr))
        p.start()
    server.close()

# 客户端
def client(host, port):
	client = socket(AF_INET, SOCK_STREAM)
	client.connect((host, port))
	while True:
	    msg = input('>>>:').strip()
	    if not msg: continue
	    client.send(msg.encode('utf-8'))
	    data = client.recv(1024)
	    print(data.decode('utf-8'))


