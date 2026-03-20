from phe import paillier

class PaillierAggregator:
    """
    Off-chain homomorphic aggregation engine.
    In production, keys should be securely loaded from a KMS.
    """

    def __init__(self, pub_key: paillier.PaillierPublicKey, priv_key: paillier.PaillierPrivateKey = None):
        self.pub_key = pub_key
        self.priv_key = priv_key

    def encrypt_value(self, val: int) -> paillier.EncryptedNumber:
        if not isinstance(val, int):
            raise TypeError("Only integers are supported for Paillier encryption")
        return self.pub_key.encrypt(val)

    @staticmethod
    def aggregate(enc_a: paillier.EncryptedNumber, enc_b: paillier.EncryptedNumber) -> paillier.EncryptedNumber:
        # Homomorphic addition: E(a) * E(b) = E(a + b)
        return enc_a + enc_b

    def decrypt_total(self, enc_total: paillier.EncryptedNumber) -> int:
        if not self.priv_key:
            raise PermissionError("Private key not loaded. Oracle nodes should not hold private keys.")
        return self.priv_key.decrypt(enc_total)
