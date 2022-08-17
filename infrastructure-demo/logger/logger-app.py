import socket
import sys, logging
import time
from time import sleep

# Serialization/deserialization tool
import pickle


# Uncomment this to enable debugging prints
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def myLogging(name: str, quantity: int, isExisting: bool, count: int):
    f = open("/logs/ifr-demo.log", "a")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    if not isExisting:
        f.write("[" + current_time + "] " + name + " entity was created with " + str(quantity) + " quantity\n")
        logging.debug(name + " entity was created with " + str(quantity) + " quantity")
    else:
        f.write("[" + current_time + "] " + name + " entity was increased by " + str(quantity) + " to new value of " + str(count) + '\n')
        logging.debug(name + " entity was increased by " + str(quantity) + " to new value of " + str(count))
    f.close()


def await_connection():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.gethostname()
    port = 26000 #arbitrary income db port
    serverSocket.bind( ( host, port ) )
    serverSocket.listen( 0 )

    con, addr = serverSocket.accept()
    # Processing just one client at a time (backlog arg in listen is just hint
    # so we need to close server socket)
    serverSocket.close()

    logging.debug( "db-app connected to logger." )
    resolve(con)


def resolve(con: socket):
    while True:
        # receive serialized tuple from client
        serialized = con.recv( 1024 )
        if not serialized: break
        name, quantity, isExisting, count = pickle.loads(serialized)
       
        myLogging(name, quantity, isExisting, count)

    con.close()
    await_connection()

await_connection()
