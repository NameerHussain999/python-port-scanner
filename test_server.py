import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server.bind(("127.0.0.1", 9999))
server.listen(5)


print("Test server running on port 9999....")


while True:
    client, address = server.accept()


    client.sendall(
        b"PORT-SCANNER-TEST v1.0 | Python Test Service\r\n"
    )

    client.close()