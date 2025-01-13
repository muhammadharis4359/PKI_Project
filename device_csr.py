from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.x509 import Name, NameAttribute, CertificateSigningRequestBuilder
from cryptography.x509.oid import NameOID

# Generate CSR for a device
def generate_device_csr(common_name):
    # Generate device private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Create the CSR
    csr = CertificateSigningRequestBuilder().subject_name(Name([
        NameAttribute(NameOID.COMMON_NAME, common_name),
    ])).sign(private_key, hashes.SHA256())

    # Save private key and CSR to files
    with open(f"certs/{common_name}_private_key.pem", "wb") as key_file:
        key_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))
    with open(f"certs/{common_name}_csr.pem", "wb") as csr_file:
        csr_file.write(csr.public_bytes(serialization.Encoding.PEM))

    print(f"CSR and private key generated for {common_name}. Files saved in the 'certs' folder.")

# Run the script
if __name__ == "__main__":
    common_name = input("Enter the device name (e.g., LightSensor): ").strip()
    generate_device_csr(common_name)
