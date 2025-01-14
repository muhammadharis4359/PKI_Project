import ssl
import socket
import logging
from rbac import check_access  # Import RBAC function

# Configure logging
logging.basicConfig(filename="server.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Define the port and host for the server
HOST = "localhost"
PORT = 8443

def start_secure_server():
    # Create an SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    
    # Load server's certificate and private key
    try:
        context.load_cert_chain(certfile="certs/server_certificate.pem", keyfile="certs/server_private_key.pem")
        logging.info("Server certificate and key loaded successfully.")
    except ssl.SSLError as e:
        logging.error(f"Error loading certificate or key: {e}")
        return
    
    # Create a socket and bind it to the desired address and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print("Secure server is running and waiting for connections...")
    
    # Wrap the server socket with SSL
    secure_socket = context.wrap_socket(server_socket, server_side=True)
    
    while True:
        # Accept a new client connection
        try:
            client_socket, addr = secure_socket.accept()
            logging.info(f"Connection established with: {addr}")
        except ssl.SSLError as e:
            logging.error(f"SSL error occurred while accepting connection: {e}")
            continue
        
        # Receive the data from the client
        try:
            data = client_socket.recv(1024).decode()
            logging.info(f"Received data: {data}")
        except Exception as e:
            logging.error(f"Error receiving data: {e}")
            client_socket.close()
            continue
        
        # Perform role-based access control
        role = "User"  # Example: You can modify to dynamically determine the role
        action = "monitor_devices"  # Example: Action to be performed
        
        if not check_access(role, action):
            logging.warning(f"Access denied for role: {role} to perform action: {action}")
            client_socket.send(b"Access denied.")
            client_socket.close()
            continue
        
        # Send a response back to the client
        client_socket.send(b"Hello from Secure Server!")
        client_socket.close()

if __name__ == "__main__":
    start_secure_server()
