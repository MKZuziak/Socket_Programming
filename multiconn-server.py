# multiconn-server.py

import sys, socket, selectors, types

sel = selectors.DefaultSelector()

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socker.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port)) # Binding socket to host and port
lsock.listen() # Setting the socket to listening mode.
print(f"Listening on {(host, port)}")

lsock.setblocking(False) # Using .setblocking method
# to configure the socket in non-blocking mode.
# -> -> Calls made to this socket will no longer block.

sel.register(lsock, selectors.EVENT_READ, data=None)
# .register() methods register the socket to be monitored
# with sel.select() for the events that you're interested in.

# The event loop
try:
    while True:
        # .select method blocks until there are sockets
        # ready for I/O.
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()

# Listening socket was registered for the event
# by selectors.EVENT_READ, so it should be
# ready to read.
def accept_wrapper(sock):
    conn, addr = sock.accept() # Should be ready to read.
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024) # # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print("Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print(f"Echoing {data.outb!r} to {data.addr}")
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]