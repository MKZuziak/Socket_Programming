import socket

HOST = "127.0.0.1" # # Standard loopback interface address (localhost)
PORT = 65432 # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # AF_INET is the Internet address family for IPv4.
    # SOCK_STREAM is the socket type for TCP.
    s.bind((HOST, PORT)) # the .bind() method ised to associate
    # the socket with a specific network interface and port number.
    s.listen()
    conn, addr = s.accept() # the .accept() method blocks execution
    # and waits for an incoming connection. Returns -> socket (conn, addr)
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)