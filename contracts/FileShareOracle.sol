// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";

/// @title Oracle Data Layer for Privacy-Preserving File Sharing
contract FileShareOracle is AccessControl {
    bytes32 public constant ORACLE_ROLE = keccak256("ORACLE_ROLE");

    struct FileRecord {
        string ipfsHash;
        bytes encryptedAesKey; // AES key encrypted via RSA
        address uploader;
        uint256 timestamp;
    }

    mapping(bytes32 => FileRecord) public files;
    mapping(address => bytes) public encryptedBilling; // Stores Paillier ciphertext

    event FileUploaded(bytes32 indexed fileId, address indexed uploader);
    event BillingUpdated(address indexed user, bytes newEncryptedTotal);

    // Custom errors for gas optimization
    error Unauthorized();
    error InvalidAddress();
    error FileAlreadyExists();
    error EmptyPayload();

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    modifier onlyOracle() {
        if (!hasRole(ORACLE_ROLE, msg.sender)) revert Unauthorized();
        _;
    }

    function addOracle(address _oracle) external onlyRole(DEFAULT_ADMIN_ROLE) {
        if (_oracle == address(0)) revert InvalidAddress();
        grantRole(ORACLE_ROLE, _oracle);
    }

    function removeOracle(address _oracle) external onlyRole(DEFAULT_ADMIN_ROLE) {
        revokeRole(ORACLE_ROLE, _oracle);
    }

    function uploadFile(bytes32 _fileId, string calldata _ipfsHash, bytes calldata _encAesKey) external {
        if (bytes(_ipfsHash).length == 0) revert EmptyPayload();
        if (files[_fileId].timestamp != 0) revert FileAlreadyExists();

        files[_fileId] = FileRecord({
            ipfsHash: _ipfsHash,
            encryptedAesKey: _encAesKey,
            uploader: msg.sender,
            timestamp: block.timestamp
        });
        
        emit FileUploaded(_fileId, msg.sender);
    }

    function updateEncryptedBilling(address _user, bytes calldata _homomorphicSum) external onlyOracle {
        if (_user == address(0)) revert InvalidAddress();
        if (_homomorphicSum.length == 0) revert EmptyPayload();

        encryptedBilling[_user] = _homomorphicSum;
        emit BillingUpdated(_user, _homomorphicSum);
    }
}
