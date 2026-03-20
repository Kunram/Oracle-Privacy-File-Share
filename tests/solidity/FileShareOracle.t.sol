// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {Test} from "forge-std/Test.sol";
import {FileShareOracle} from "../../contracts/FileShareOracle.sol";

contract FileShareOracleTest is Test {
    FileShareOracle oracle;
    
    address admin = address(0x1);
    address node = address(0x2);
    address user = address(0x3);

    function setUp() public {
        vm.startPrank(admin);
        oracle = new FileShareOracle();
        oracle.addOracle(node);
        vm.stopPrank();
    }

    function test_updateEncryptedBilling() public {
        bytes memory payload = hex"deadbeef";

        vm.prank(node);
        oracle.updateEncryptedBilling(user, payload);

        assertEq(oracle.encryptedBilling(user), payload);
    }

    function test_RevertWhen_UnauthorizedBilling() public {
        vm.prank(user);
        vm.expectRevert(FileShareOracle.Unauthorized.selector);
        oracle.updateEncryptedBilling(user, hex"deadbeef");
    }

    function test_RevertWhen_FileIdCollision() public {
        bytes32 fileId = keccak256("file_001");
        
        oracle.uploadFile(fileId, "QmTest", hex"ff");

        vm.expectRevert(FileShareOracle.FileAlreadyExists.selector);
        oracle.uploadFile(fileId, "QmTest2", hex"ee");
    }
}
