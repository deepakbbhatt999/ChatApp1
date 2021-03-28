
import threading
import socket
import argparse
import os


class Server(threading.Thread):
    """
    Connection Server Class
    Attributes:
        connections ->list: A list of ServerSocket objects representing the active connections.
        host ->str: The IP address of the listening socket.
        port ->int: The port number of the listening socket.
    """
    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port
    
    def run(self):
        """
        Create a socket to listen. This socket uses SO_REUSEADDR to bind previous socket.
        For new connection, serversocket thread is started to start communications with that client
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))

        sock.listen(1)
        print('Listening at', sock.getsockname())

        while True:

            # Accept new connection
            sc, sockname = sock.accept()
            print('Accepted a new connection from {} to {}'.format(sc.getpeername(), sc.getsockname()))

            # Create new thread
            server_socket = ServerSocket(sc, sockname, self)
            
            # Start new thread
            server_socket.start()

            # Add thread to active connections
            self.connections.append(server_socket)
            print('Ready to receive messages from', sc.getpeername())

    def broadcast(self, message, source):
        """
        Sending message to all the users except the one who sends it.
        Args:
            message ->str: The message to broadcast.
            source : The socket address of the source client.
        """
        for connection in self.connections:

            # Send to all connected clients except the source client
            if connection.sockname != source:
                connection.send(message)
    
    def remove_connection(self, connection):
        """
        Removes a ServerSocket thread from the connections attribute.
        Args:
            connection (ServerSocket): The ServerSocket thread to remove.
        """
        self.connections.remove(connection)


class ServerSocket(threading.Thread):
    """
    For communicationg with a connected client.
    Attributes:
        sc : The connected socket.
        sockname: The client socket address.
        server : The parent thread.
    """
    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server
    
    def run(self):
        """
        Receives data from the connected client and broadcasts the message to all other clients.
        If the client has left the connection, closes the connected socket and removes itself.
        """
        while True:
            message = self.sc.recv(1024).decode('ascii')
            if message:
                print('{} says {!r}'.format(self.sockname, message))
                self.server.broadcast(message, self.sockname)
            else:
                # Client has closed the socket, exit the thread
                print('{} has closed the connection'.format(self.sockname))
                self.sc.close()
                server.remove_connection(self)
                return
    
    def send(self, message):
        """
        Sends a message to the connected server.
        Args:
            message ->str: The message to be sent.
        """
        self.sc.sendall(message.encode('ascii'))


def exit(server):
    """
    Allows the server administrator to shut down the server.
    Typing 'q' in the command line will close all active connections and exit the application.
    """
    while True:
        ipt = input('')
        if ipt == 'q':
            print('Closing all connections...')
            for connection in server.connections:
                connection.sc.close()
            print('Shutting down the server...')
            os._exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()

    # Create and start server thread
    server = Server(args.host, args.p)
    server.start()

    exit = threading.Thread(target = exit, args = (server,))
    exit.start()
