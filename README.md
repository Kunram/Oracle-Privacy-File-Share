# Oracle-Privacy-File-Share
Something written during University


A proof-of-concept (PoC) architecture for privacy-preserving file sharing. It leverages an off-chain oracle network to handle heavy cryptographic computations (Homomorphic Encryption & RSA), keeping the on-chain EVM footprint minimal and Gas-efficient.

## Architecture Design

The system decouples data storage, key distribution, and billing aggregation:

1. **Hybrid Cipher (AES + RSA):** Payloads are symmetrically encrypted via `AES-256-GCM`. The ephemeral session keys are then wrapped using `RSA-OAEP` (2048-bit) against the recipient's public key.
2. **Homomorphic Billing (Paillier):** Download metrics and billing data are encrypted using the Paillier cryptosystem. Oracle nodes perform additive homomorphic aggregation (`E(a) * E(b) = E(a + b)`) off-chain without accessing the private key.
3. **On-chain State (Solidity):** A gas-optimized EVM contract utilizes `AccessControl` for Oracle node authorization and state machine enforcement (preventing CID collisions and unauthorized mutations).

## Repository Structure

- `contracts/`: EVM smart contracts (Solidity).
- `crypto_engine/`: Off-chain cryptographic primitives (Python).
- `tests/`: Dual-environment test suites (Foundry & Pytest).

## Quick Start

### 1. Off-chain Cryptographic Engine
Requires Python 3.10+.

```bash
cd crypto_engine
pip install -r requirements.txt
cd ..
pytest tests/python/ -v
```

### 2. On-chain Oracle Contract
Requires [Foundry](https://getfoundry.sh/).

```bash
forge build
forge test -vvv
```

## Security Notice

This repository is a PoC demonstrating cryptographic architectural patterns. The Paillier off-chain aggregation is implemented to bypass EVM block gas limits on heavy mathematical operations. For production, the Python engine should be replaced with a secure enclave (TEE) or a Rust-based node implementation.
