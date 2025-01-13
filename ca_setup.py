from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.x509 import Name, NameAttribute, CertificateBuilder
from cryptography.x509.oid import NameOID
import datetime

# Create CA's Private Key and Certificate
def generate_ca():
    # Generate CA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Build CA certificate
    subject = issuer = Name([
        NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        NameAttribute(NameOID.ORGANIZATION_NAME, u"My CA"),
        NameAttribute(NameOID.COMMON_NAME, u"MyIoTCA"),
    ])
    certificate = CertificateBuilder() \
        .subject_name(subject) \
        .issuer_name(issuer) \
        .public_key(private_key.public_key()) \
        .serial_number(1000) \
        .not_valid_before(datetime.datetime.utcnow()) \
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365)) \
        .sign(private_key, hashes.SHA256())

    # Save private key and certificate
    with open("certs/ca_private_key.pem", "wb") as key_file:
        key_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))
    with open("certs/ca_certificate.pem", "wb") as cert_file:
        cert_file.write(certificate.public_bytes(serialization.Encoding.PEM))

    print("CA setup complete! Files saved in the 'certs' folder.")

# Run the script
if __name__ == "__main__":
    generate_ca()
