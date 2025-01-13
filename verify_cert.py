from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# Verify the device certificate against the CA certificate
def verify_certificate(common_name):
    # Load the CA certificate
    with open("certs/ca_certificate.pem", "rb") as cert_file:
        ca_certificate = load_pem_x509_certificate(cert_file.read())

    # Load the device certificate
    with open(f"certs/{common_name}_certificate.pem", "rb") as cert_file:
        device_certificate = load_pem_x509_certificate(cert_file.read())

    # Get the CA public key
    ca_public_key = ca_certificate.public_key()

    # Verify the device certificate
    try:
        ca_public_key.verify(
            device_certificate.signature,
            device_certificate.tbs_certificate_bytes,
            padding.PKCS1v15(),
            device_certificate.signature_hash_algorithm,
        )
        print(f"Certificate for {common_name} is valid and verified.")
    except Exception as e:
        print(f"Certificate verification failed: {e}")

# Run the script
if __name__ == "__main__":
    common_name = input("Enter the device name (e.g., LightSensor): ").strip()
    verify_certificate(common_name)
