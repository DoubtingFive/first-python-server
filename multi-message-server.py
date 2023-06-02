import socket
import threading as th

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def Connect():
    global user_list
    while True:
        connection, address = sock.accept()
        user_list.append(connection)
        th.Thread(target=handle_connect, args=[connection,address]).start()
        print(f"[NEW CONNECTION] >> Get connection from {address}")
        for x in user_list:
            x.send(f"[NEW CONNECTION] >> Recieved new connection from {address}".encode())

def handle_connect(conn,address):
    while True:
        msg = conn.recv(1024).decode()
        if msg == "q":
            conn.close()
            user_list.remove(conn)
            print(f"[LOST CONNECTION] >> Lost connection on addres {address}")
            for x in user_list:
                x.send(f"[LOST CONNECTION] >> Lost connection on addres {address}".encode())
            break
        else:
            print(f"[{address}] >> {msg}")
            for x in user_list:
                if not x == conn:
                    x.send(f"[{address}] >> {msg}".encode())

user_list = []

sock.bind(("0.0.0.0",444))
sock.listen(5)
th.Thread(target=Connect).start()

while True:
    cmd = input("")
    for x in user_list:
        x.send(f"[SERVER] >> {cmd}".encode())