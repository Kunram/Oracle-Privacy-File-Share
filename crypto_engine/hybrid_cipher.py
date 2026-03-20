
import os
from typing import Dict
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

class HybridCipher:
    """
    Handles payload encryption via AES-256-GCM.
    Session keys are secured using RSA-OAEP.
    """

    @staticmethod
    def encrypt_payload(data: bytes, recipient_pub_key: bytes) -> Dict[str, bytes]:
        if not data or not recipient_pub_key:
            raise ValueError("Invalid payload or recipient public key")

        # Generate 32-byte (256-bit) session key
        session_key = os.urandom(32)
        
        # AES-GCM encryption
        aes_cipher = AES.new(session_key, AES.MODE_GCM)
        ciphertext, tag = aes_cipher.encrypt_and_digest(data)
        
        # RSA-OAEP key wrapping
        try:
            rsa_key = RSA.import_key(recipient_pub_key)
            rsa_cipher = PKCS1_OAEP.new(rsa_key)
            enc_session_key = rsa_cipher.encrypt(session_key)
        except ValueError as e:
            raise RuntimeError(f"RSA key import or encryption failed: {e}")
        
        return {
            "enc_session_key": enc_session_key,
            "nonce": aes_cipher.nonce,
            "tag": tag,
            "ciphertext": ciphertext
        }
