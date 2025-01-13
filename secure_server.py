import ssl
import socket
import logging

# Configure logging for the server
logging.basicConfig(filename="server.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def check_access(role, action):
    """ Dummy access control function, modify as needed. """
    if role == "Admin" and action == "monitor_devices":
        return True
    return False

def start_secure_server():
    """ Starts the secure server with SSL/TLS encryption. """
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    # Load server certificate and private key
    context.load_cert_chain(certfile="certs/Mobile_certificate.pem", keyfile="certs/Mobile_private_key.pem")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 8443))
    server_socket.listen(5)
    print("Secure server is running and waiting for connections...")

    # Wrap the socket with SSL for secure communication
    secure_socket = context.wrap_socket(server_socket, server_side=True)

    while True:
        # Accept a new client connection
        client_socket, addr = secure_socket.accept()
        logging.info(f"Connection established with: {addr}")

        # Example role and action for testing
        role = "User"  # Change this to 'Admin' or any other role for testing
        action = "monitor_devices"

        # Check access control before proceeding
        if not check_access(role, action):
            logging.warning(f"Access denied for role: {role}, action: {action}")
            print("Access denied. Terminating connection.")
            client_socket.send(b"Access denied.")
            client_socket.close()
            continue

        # Receive data from the client
        data = client_socket.recv(1024).decode()
        logging.info(f"Data received from client {addr}: {data}")

        # Send a response to the client
        client_socket.send(b"Hello from Secure Server!")

        # Close the client connection
        client_socket.close()

if __name__ == "__main__":
    start_secure_server()
