import socket
import sys
import threading 

localIP     = "127.0.0.1"
localPort   = 12345
bufferSize  = 1024

 

msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)

 
def udp_server():
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, localPort))

    print("UDP server up and listening")

    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)
        print(clientMsg)
        print(clientIP)


def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Données reçues du client : {data.decode('utf-8')}")
        client_socket.send("Message bien reçu".encode('utf-8'))
    client_socket.close()

def tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((localIP, localPort))
    server_socket.listen(5)
    print(f"Serveur waiting at {localIP}:{localPort}")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established {client_address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if "__main__" == __name__:
    if sys.argv[1] == "udp":
        udp_server()
    elif sys.argv[1] == "tcp":
        tcp_server()