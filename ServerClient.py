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


#Returns list of connections and list of names of the connections
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
            print(reply.decode(), "has joined the lobby")
            connections.append(connection)
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
    connection.connect((input("Please enter the target address\n\t"), int(input("Please enter the port\n\t"))))
    name = input("\n\nWhat is your name?\n\t")

    connection.send(bytes(name,'utf-8'))
    print()
    print(connection.recv(1024).decode())
    
    return connection