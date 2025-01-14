import ssl
import socket
import logging

# Configure logging
logging.basicConfig(filename="client.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def connect_to_secure_server():
    # Create an SSL context
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    
    # Load CA's certificate to verify the server's authenticity
    try:
        context.load_verify_locations("certs/ca_certificate.pem")
        logging.info("CA certificate loaded successfully.")
    except ssl.SSLError as e:
        logging.error(f"Error loading CA certificate: {e}")
        return
    
    # Create a socket and wrap it with SSL
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_socket = context.wrap_socket(client_socket, server_hostname="localhost")
    
    # Connect to the server
    try:
        secure_socket.connect(("localhost", 8443))
        logging.info("Connection to the secure server established.")
    except ssl.SSLError as e:
        logging.error(f"SSL connection error: {e}")
        return
    
    # Send data to the server
    try:
        secure_socket.send(b"Hello from Secure Client!")
        logging.info("Message sent to server.")
    except Exception as e:
        logging.error(f"Error sending data: {e}")
    
    # Receive response from the server
    try:
        response = secure_socket.recv(1024).decode()
        logging.info(f"Received from server: {response}")
    except Exception as e:
        logging.error(f"Error receiving data: {e}")
    
    secure_socket.close()

if __name__ == "__main__":
    connect_to_secure_server()
