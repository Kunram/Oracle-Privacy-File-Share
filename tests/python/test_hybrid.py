import pytest
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from crypto_engine.hybrid_cipher import HybridCipher

@pytest.fixture
def rsa_keys():
    key = RSA.generate(2048)
    return key, key.publickey().export_key()

def test_hybrid_encryption_roundtrip(rsa_keys):
    priv_key, pub_key_bytes = rsa_keys
    payload = b"sensitive_data_block"
    
    res = HybridCipher.encrypt_payload(payload, pub_key_bytes)
    
    # Validate envelope
    assert all(k in res for k in ("enc_session_key", "nonce", "tag", "ciphertext"))
    assert len(res["nonce"]) == 16
    assert len(res["tag"]) == 16
    
    # RSA decrypt session key
    rsa_cipher = PKCS1_OAEP.new(priv_key)
    session_key = rsa_cipher.decrypt(res["enc_session_key"])
    
    # AES-GCM decrypt payload
    aes_cipher = AES.new(session_key, AES.MODE_GCM, nonce=res["nonce"])
    decrypted = aes_cipher.decrypt_and_verify(res["ciphertext"], res["tag"])
    
    assert decrypted == payload

def test_encrypt_with_invalid_key():
    with pytest.raises(RuntimeError):
        HybridCipher.encrypt_payload(b"data", b"malformed_key_bytes")
