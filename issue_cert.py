from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.x509 import load_pem_x509_csr, CertificateBuilder, Name, NameAttribute
from cryptography.x509.oid import NameOID
import datetime

# Issue a device certificate
def issue_device_cert(common_name):
    # Load CA private key
    with open("certs/ca_private_key.pem", "rb") as key_file:
        ca_private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    # Load CA certificate
    with open("certs/ca_certificate.pem", "rb") as cert_file:
        ca_certificate = cert_file.read()

    # Load the device CSR
    with open(f"certs/{common_name}_csr.pem", "rb") as csr_file:
        csr = load_pem_x509_csr(csr_file.read())

    # Create the device certificate
    subject = csr.subject
    issuer = Name([
        NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        NameAttribute(NameOID.ORGANIZATION_NAME, u"My CA"),
        NameAttribute(NameOID.COMMON_NAME, u"MyIoTCA"),
    ])
    certificate = CertificateBuilder() \
        .subject_name(subject) \
        .issuer_name(issuer) \
        .public_key(csr.public_key()) \
        .serial_number(1001) \
        .not_valid_before(datetime.datetime.utcnow()) \
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365)) \
        .sign(ca_private_key, hashes.SHA256())

    # Save the device certificate
    with open(f"certs/{common_name}_certificate.pem", "wb") as cert_file:
        cert_file.write(certificate.public_bytes(serialization.Encoding.PEM))

    print(f"Device certificate issued for {common_name}. Saved in the 'certs' folder.")

# Run the script
if __name__ == "__main__":
    common_name = input("Enter the device name (e.g., LightSensor): ").strip()
    issue_device_cert(common_name)
