import pytest
from phe import paillier
from crypto_engine.paillier_aggregator import PaillierAggregator

@pytest.fixture
def keys():
    return paillier.generate_paillier_keypair(n_length=1024)

def test_homomorphic_addition(keys):
    pub_key, priv_key = keys
    
    # Oracle context (no priv_key)
    oracle = PaillierAggregator(pub_key=pub_key)
    
    enc_10 = oracle.encrypt_value(10)
    enc_25 = oracle.encrypt_value(25)
    enc_sum = oracle.aggregate(enc_10, enc_25)
    
    # Platform context (with priv_key)
    platform = PaillierAggregator(pub_key=pub_key, priv_key=priv_key)
    
    assert platform.decrypt_total(enc_sum) == 35

def test_oracle_cannot_decrypt(keys):
    pub_key, _ = keys
    oracle = PaillierAggregator(pub_key=pub_key)
    
    enc_val = oracle.encrypt_value(100)
    
    with pytest.raises(PermissionError):
        oracle.decrypt_total(enc_val)
