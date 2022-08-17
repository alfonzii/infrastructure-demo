import socket
import sys, logging
from time import sleep

# Dictionary in file module
import shelve

# Serialization/deserialization tool
import pickle


# Uncomment this to enable debugging prints
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def send_to_logger(name: str, quantity: int, isExisting: bool, count: int):
    clientSocket = socket.socket()
    logger_hostname = "logger"
    port = 26000 # logger port
    
    connected = False
    
    logging.debug('Trying to connect to logger')
    while not connected:
        try:
            clientSocket.connect( ( logger_hostname, port ) )
            connected = True
        except socket.error:
            sleep(2)
    logging.debug('Successfully connected. Now trying to send data.') 
    
    while True:
        try:
            clientSocket.send( pickle.dumps((name, quantity, isExisting, count)) )

        except socket.error:
            # set connection status and recreate socket
            connected = False
            clientSocket = socket.socket()
            logging.debug('Connection lost... reconnecting') 
            while not connected:
                # attempt to reconnect, otherwise sleep for 2 seconds
                try:
                    clientSocket.connect( ( logger_hostname, port ) )
                    connected = True
                    logging.debug( "re-connection successful" )
                except socket.error:
                    sleep( 2 )
        
        logging.debug("Successfully sent.")
        break
    clientSocket.close()


def await_connection():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.gethostname()
    port = 25000 #arbitrary income db port
    serverSocket.bind( ( host, port ) )
    serverSocket.listen( 0 )

    con, addr = serverSocket.accept()
    # Processing just one client at a time (backlog arg in listen is just hint
    # so we need to close server socket)
    serverSocket.close()

    logging.debug( "Client connected to db-app." )
    resolve(con)


def resolve(con: socket):
    while True:
        # receive serialized tuple from client
        serialized = con.recv( 1024 )
        if not serialized: break
        name, quantity = pickle.loads(serialized)
        quantity = int(quantity)
        
        # ------------ shelve ---------
        d = shelve.open("/data/dictfile")
        isExisting = name in d
        if not isExisting:
            d[name] = quantity
        else:
            d[name] += quantity
        
        count = d[name]
        
        d.close()
        # ------------ shelve ---------
        
        send_to_logger(name, quantity, isExisting, count)

    con.close()
    await_connection()

await_connection()
