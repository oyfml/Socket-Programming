import socket
import sys
import time


# Create Client's Socket
def create_socket():
    try:
        global cli
        cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        print("Client socket created.")
    except socket.error as errmsg:
        print("Create Socket error: " + str(errmsg))
        sys.exit(1)


# Connect to Server
def conn_server():
    try:
        global host
        global port
        "#User Input Server IP address as string"
        host = sys.argv[1]
        '#sys.argv(1)'
        port = 80
        cli.connect((host, port))
        print("Connected to Server| IP:" + str(host) + "| Port:" + str(port))
    except socket.error as errmsg:
        print("Connection error: " + str(errmsg))
        sys.exit(1)


# Perform file receiving function
def rec_file(filename):
    try:
        "#Opens a file for appending, creates the file if it does not exist"
        fd = open("./Received/NP/" + filename, 'wb')
    except IOError:
        print("File location incorrect!")
        sys.exit(1)

    print("Downloading " + filename)
    data = rec_data(1024)
    idx = data.find(str.encode("\r\n\r\n"))
    "#Remove HTTP header"
    data = data[idx+4:]
    while 1:
        fd.write(data)
        if ".jpg" in filename:
            send_data(str.encode("GET /" + filename +
                                 "HTTP/1.0 \r\n Host: localhost \r\n Accept: image/jpeg \r\n\r\n"))
        elif ".mp3" in filename:
            send_data(str.encode("GET /" + filename +
                                 "HTTP/1.0 \r\n Host: localhost \r\n Accept: audio/mpeg \r\n\r\n"))
        else:
            send_data(str.encode("GET /" + filename +
                                 "HTTP/1.0 \r\n Host: localhost \r\n Accept: text/txt \r\n\r\n"))
        data = rec_data(1024)
        idx = data.find(str.encode("\r\n\r\n"))
        data = data[idx + 4:]
        if str.encode('End-Of-File') in data:
            break
    fd.close()
    print("Download Complete!")


# Sends MAX 4096 bytes of data to Client
def send_data(data):
    try:
        cli.send(data)
    except socket.error as errmsg:
        print("Send data error: " + str(errmsg))
        sys.exit(1)


# Receives MAX 4096 bytes of data from Client
def rec_data(size):
    try:
        data = cli.recv(size)
    except socket.error as errmsg:
        print("Send data error: " + str(errmsg))
        sys.exit(1)
    return data


def main():

    filename = ("a.jpg", "b.mp3", "c.txt")

    if len(sys.argv[1]) == 0:
        print("Incorrect argument!")
        print("Usage: <IP Address>")
        sys.exit(1)

    start = time.time()

    for file in filename:
        create_socket()
        conn_server()
        if ".jpg" in file:
            send_data(str.encode("GET /" + file + " HTTP/1.0 \r\n Host: localhost \r\n Accept: image/jpeg \r\n\r\n"))
        elif ".mp3" in file:
            send_data(str.encode("GET /" + file + " HTTP/1.0 \r\n Host: localhost \r\n Accept: audio/mpeg \r\n\r\n"))
        else:
            send_data(str.encode("GET /" + file + " HTTP/1.0 \r\n Host: localhost \r\n Accept: text/txt \r\n\r\n"))
        rec_file(file)
        print("Received file: " + file)

        cli.close()
    end = time.time()
    print("Time Elapsed: " + str(round((end-start)*1000)) + "ms")


if __name__ == '__main__':
    main()
