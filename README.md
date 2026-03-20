# Oracle-Privacy-File-Share
Something written in 2021

# Decentralized Oracle-Based Privacy File Sharing 🛡️

A hybrid Web3 architecture for secure file sharing, leveraging **Oracle Networks** and **Privacy-Preserving Computation (Homomorphic Encryption)**.

## 🌟 Core Architecture
This project solves the "data privacy vs. blockchain transparency" dilemma by offloading heavy cryptographic operations to an off-chain oracle node, while maintaining access control and verifiable state on-chain.

### Cryptographic Modules
1. **Hybrid Encryption (AES + RSA)**:
   - Large files are symmetrically encrypted using `AES-256-GCM` before being uploaded to IPFS.
   - The AES session key is asymmetrically encrypted via `RSA-2048` using the intended recipient's public key.
2. **Additive Homomorphic Encryption (Paillier)**:
   - Used for privacy-preserving billing and download statistics. 
   - Node operators can aggregate encrypted download counts without ever decrypting the underlying data, adhering to the property: 
     $$E(m_1) \cdot E(m_2) = E(m_1 + m_2)$$

## 🛠 Tech Stack
- **On-chain**: Solidity `^0.8.19` (Data registry & Access control)
- **Off-chain Oracle**: Python (PyCryptodome for AES/RSA, `phe` for Paillier)
- **Storage**: IPFS (InterPlanetary File System)

## 💡 Engineering Highlights
Designed with gas optimization in mind. Paillier and RSA operations are extremely gas-intensive (exceeding block gas limits if executed directly on EVM). This project delegates the ciphertext generation and homomorphic aggregation to the Python off-chain engine, passing only lightweight proofs and encrypted payloads to the Solidity contract via an Oracle.
