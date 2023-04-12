// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol"; //importa lib which is stored in an isolated location in an address prevents overflow

contract fundMe {
    using SafeMathChainlink for uint256; //prevent overflow for datatype uint256
    mapping(address => uint256) public addressAmountFunded; //mapping array
    address public owner; //variable is of type address 0x34556dfg types
    address[] funders; //creates an array of address of funders for the contract

    constructor()
        public
    //constructors are executed just after the contract is deployed because function can be executed by anyone
    {
        owner = msg.sender; //address of msg.sender is made equal to owner
    }

    function fund() public payable {
        uint256 minimumethusd = 50 * 10 ** 8; //minimum eth
        require(msg.value <= minimumethusd, "You need more eth"); //if send value is lesss than min eth then a messsage gets displayed along with gas revert
        addressAmountFunded[msg.sender] += msg.value; //associates sender address with the amount that account send as funds and adds the amt if amt cxame from same account
        funders.push(msg.sender); //puts each funder in the funds array
    }

    function getVersion() public view returns (uint256) {
        //displays version no of contract of pricefeed
        AggregatorV3Interface pricefeed = AggregatorV3Interface(
            0x694AA1769357215DE4FAC081bf1f309aDC325306
        ); //this just shows the price feed contract foer eth to usd number conversion is present at the given address
        //aggregator is datatype of the price contact it contains the foll functions
        return pricefeed.version();
    }

    function getLatestPrice() public view returns (uint256) {
        //gets current rate conv between eth and ethusd
        AggregatorV3Interface pricefeed = AggregatorV3Interface(
            0x694AA1769357215DE4FAC081bf1f309aDC325306
        );
        (, int256 answer, , , ) = pricefeed.latestRoundData();
        return uint256(answer * 10000000000); //to ethusd from wei
        //1767.54000000 * 10 ** 8 = 176754000000 ethusd
    }

    function getConversionRate(uint256 ethval) public view returns (uint256) {
        //converts eth to ethusd
        uint256 ethprice = getLatestPrice();
        uint256 ethinusd = (ethprice * ethval) / 1000000000000000000; //17675400000000000000000000000000
        return ethinusd;
    }

    modifier admin() {
        //lets only the admin gain privileges of the smart contract
        _;
        require(owner == msg.sender); // checks if owner acc is the msg.sender account if it is not then gas is reverted
        _; //execute rest of the code
    }

    function withdraw() public payable admin {
        //payable function and modifier can be used anywhere in the smartcontract as a check
        //require(owner == msg.sender);
        msg.sender.transfer(address(this).balance); //transfer amt to only the admins account
        for (
            uint256 fundsindex = 0;
            fundsindex <= funders.length;
            fundsindex++
        ) {
            //iterates thru the funders array
            address funder = funders[fundsindex]; //gets the address of the funder
            addressAmountFunded[funder] = 0; //resets the address of a funder in the particular index as 0
        } //reset amount funded of an address to 0
        funders = new address[](0); //sets the funders array to 0
    }
}
