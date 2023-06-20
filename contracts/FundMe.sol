// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    address owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;

    struct Funder {
        address funderAddress;
        uint256 amountFunded;
    }

    Funder[] public funders;

    function fund() public payable {
        require(
            getConversionRate(msg.value) >= 50 * 10 ** 18,
            "You need to spend more ETH!"
        );
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(Funder(msg.sender, msg.value));
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer); //1,910.15430000_0000000000
    }

    function getDecimals() public view returns (uint8) {
        return priceFeed.decimals();
    }

    function getConversionRate(
        uint256 _ethAmount
    ) public view returns (uint256) {
        uint256 ethPriceInUSD = getPrice();
        uint256 ethAmountInUSD = (_ethAmount * ethPriceInUSD) / (10 ** 18);
        return ethAmountInUSD;
    }

    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 50 * 10 ** 18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10 ** 18;
        // return (minimumUSD * precision) / price;
        // We fixed a rounding error found in the video by adding one!
        return ((minimumUSD * precision) / price) + 1;
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);

        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address _funderAddress = funders[funderIndex].funderAddress;
            uint256 _amountFunded = funders[funderIndex].amountFunded;
            addressToAmountFunded[_funderAddress] = 0;
            _funderAddress = address(0);
            _amountFunded = 0;
        }
    }
}
