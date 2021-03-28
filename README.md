This is a chat application for multiple user on the same server and it's veri simple to use and is made using Socket and Python and runs on Linux Server.
to Chat with multiple users you just need to things, first is local ip address and second is port number. Ip adress is given by the user and port number is generated randomly.
To work or start this application follow these steps:
1. Run server.py file and as it’s arguments pass the address like python3 server.py 127.0.0.1. This will start the server at this address.
2. Then run client.py file and as it’s arguments, pass the same address as above like python3 client.py 127.0.0.1. This will start the client program.
3. Then the client program will ask for the name of the user. Then by entering the name of the user, a new window will open to write the message and see the message screen.
4. This is done using tkinter. GUI is made using tkinter for the easier interaction of all the users.
5. You can create n numbers of users using Step 2 and Step 3.
6. After chatting with the users if you want to close the chat, enter “/x” this will exit that user and show it on the message screen of other users.
7. To close the server enter “q” and the server will be closed.
8. Comments are given inside the code file for easy understanding of what’s going on.

So, overall threading, sockets, and tkinter are used in this application
