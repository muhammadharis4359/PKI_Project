import ssl
import socket
import logging

# Configure logging for the client
logging.basicConfig(filename="client.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def connect_to_secure_server():
    """ Connects to a secure server using SSL/TLS. """
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

    # Load CA certificate to verify server
    context.load_verify_locations("certs/ca_certificate.pem")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_socket = context.wrap_socket(client_socket, server_hostname="localhost")

    try:
        secure_socket.connect(("localhost", 8443))
        logging.info("Connection to the secure server established.")
        print("Connection to the secure server established.")

        secure_socket.send(b"Hello from Secure Client!")
        logging.info("Data sent to the server: Hello from Secure Client!")

        response = secure_socket.recv(1024).decode()
        print(f"Received from server: {response}")
        logging.info(f"Received from server: {response}")

    except ssl.SSLError as ssl_error:
        logging.error(f"SSL error occurred: {ssl_error}")
        print(f"SSL error occurred: {ssl_error}")
    except socket.error as socket_error:
        logging.error(f"Socket error occurred: {socket_error}")
        print(f"Socket error occurred: {socket_error}")
    finally:
        secure_socket.close()
        logging.info("Connection closed.")

if __name__ == "__main__":
    connect_to_secure_server()
