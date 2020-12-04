import socket as s
import threading

#Idle while waiting for 'finish' signal, then send a message to this computer at port
#@param port telling it to finish
def handle_full_players(finisher, port):
    answer = ""
    print("Type 'finish' once all players have connected")
    while answer != "finish":
        answer = input("")
    
    r = s.socket()
    r.connect((s.gethostname(), port))
    r.send(bytes(finisher, 'utf-8'))

class Net_Connection:
    def __init__(self, socket, IP, port):
        self.socket = socket
        self.IP = IP
        self.port = port
    
    def send(self, bytesToSend):
        self.socket.send(bytesToSend)
    
    def recv(self, bufferSize):
        return self.socket.recv(bufferSize)

#Returns list of Net_Connections and list of names of the connections
def get_connections():
    listener = s.socket()
    host_IP = s.gethostname()
    port = int(input("What port do you want to host on (10000 -> 20000 preferably):\n\t"))

    print("Hosted by",host_IP,"on port",port)
    listener.bind(('', port))
    listener.listen()
    waiting_for_players = True

    connections = []
    names = []

    finish_message = 'finish looking'

    #This thread finishing is a requirement for the main one to continue, so there is no need
    #to save a reference to it. It is going to have to finish
    threading._start_new_thread(handle_full_players, (finish_message, port,))

    while waiting_for_players:
        #Gets an IP
        connection, address = listener.accept()
        #Wait for their response
        reply = connection.recv(1024)

        #If their response is the finisher, 
        if reply.decode('utf-8') != finish_message:
            print(reply.decode(), "has joined the lobby from",address,"!")
            connections.append(Net_Connection(connection, address[0], address[1]))
            names.append(reply.decode())
            message = "You have connected to host as player " + str(len(connections))
            connection.send(bytes(message, 'utf-8'))
        else:
            waiting_for_players = False
    
    print("All the players have joined the lobby")
    return connections, names

#Returns a connection to the server
def get_host():
    connection = s.socket()
    address = input("Please enter the target address\n\t")
    port = int(input("Please enter the port\n\t"))
    connection.connect((address, port))
    name = input("\n\nWhat is your name?\n\t")

    connection.send(bytes(name,'utf-8'))
    print()
    print(connection.recv(1024).decode())
    
    return Net_Connection(connection, address, port)