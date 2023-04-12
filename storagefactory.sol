// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;
import "./simpleStorage.sol"; //imports a smart contract into a smart contract

contract storagefactory is
    simple //inherits all functions of simple contract like extends a base class to another class in java
{
    simple[] public simplestorage; //creates an array that stores transcation address

    function createNewContract() public {
        simple Simple = new simple(); //deploying a smart contract
        simplestorage.push(Simple); //the trancation address is stored in simplestorage array
    }

    function sfStore(uint256 _storageindex, uint256 _storagenumber) public {
        simple(address(simplestorage[_storageindex])).store(_storagenumber);
    }

    function sfRetrieve(uint256 _storageindex) public view returns (uint256) {
        return simple(address(simplestorage[_storageindex])).retrieve();
    }
}
