import socket
import sys
import time


# Create Server's Socket
def create_socket():
    try:
        global svr
        svr = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        print("Server socket created.")
    except socket.error as errmsg:
        print("Create Socket error: " + str(errmsg))
        sys.exit(1)


# Bind Server's Socket to Port & Listen to Port for new connection
def bind_n_listen():
    try:
        global host
        global port
        host = ""
        '# "" represents INADDR_ANY'
        port = 80
        svr.bind((host, port))
        print("Binding Socket to Port...")
        svr.listen(5)
        print("Listening for new conn...")
        '#Backlog = 5, num of unacceptable conn before system refuse new conn'
    except socket.error as errmsg:
        print("Binding/Listening Socket error: " + str(errmsg))
        sys.exit(1)


# Accept connection with Client
def accept_conn():
    try:
        global conn
        global address
        (conn, address) = svr.accept()
        print("Client connected| IP:" + str(address[0]) + "| Port:" + str(address[1]))
    except socket.error as errmsg:
        print("Accept Connection error: " + str(errmsg))
        sys.exit(1)


# Perform file sending function
def send_file(filename, persistent):
    try:
        fd = open("./Data/" + filename, 'rb')
    except IOError:
        print("File location incorrect!")
        sys.exit(1)

    data = fd.read(924)
    '#100bytes for HTTP header'
    while data:
        d_len = str(len(data))
        if persistent:
            data = str.encode("HTTP/1.1 200 OK\r\n Content-Length: " + d_len
                              + "\r\n Connection: Keep-Alive\r\n\r\n") + data
        else:
            data = str.encode("HTTP/1.0 200 OK\r\n Content-Length: " + d_len
                              + "\r\n Connection: Keep-Alive\r\n\r\n") + data
        send_data(data)
        ack = rec_data(1024)
        if str.encode("GET") not in ack:
            print("Server only accepts GET request!")
            fd.close()
            return
        data = fd.read(924)
    print("Sending Complete")
    if persistent:
        send_data(str.encode("HTTP/1.1 200 OK\r\n Content-Length: 0\r\n Connection: Keep-Alive\r\n\r\n End-Of-File"))
    else:
        send_data(str.encode("HTTP/1.0 200 OK\r\n Content-Length: 0\r\n Connection: close\r\n\r\n End-Of-File"))
    fd.close()


# Sends MAX 4096 bytes of data to Client
def send_data(data):
    try:
        conn.send(data)
    except socket.error as errmsg:
        print("Send data error: " + str(errmsg))
        sys.exit(1)


# Receives MAX 4096 bytes of data from Client
def rec_data(size):
    try:
        data = conn.recv(size)
    except socket.error as errmsg:
        print("Send data error: " + str(errmsg))
        sys.exit(1)
    return data


def main():
    files = ("a.jpg", "b.mp3", "c.txt")

    create_socket()
    bind_n_listen()

    while 1:
        accept_conn()

        data = rec_data(1024)
        filename = bytes.decode(data[5:10])
        while 1:
            '#Performs Persistent HTTP'
            if str.encode("HTTP/1.1") in data:
                print("Sending " + filename + "...")
                send_file(filename, 1)
                data = rec_data(1024)
                filename = bytes.decode(data[5:10])
                if filename not in files:
                    break
            else:
                print("Sending " + filename + "...")
                send_file(filename, 0)
                break
        conn.close()
        print("Client disconnected. Connection Closed")


if __name__ == '__main__':
    main()
