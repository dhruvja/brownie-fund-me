pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public addressToAmountFunded;

    address owner;
    address[] funders;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function pay() public payable {
        uint256 minAmount = 50 * 10**18;
        require(
            getConversionRate(msg.value) >= minAmount,
            "Spend More Eth u mofo"
        );
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getEntranceFee() public view returns(uint256){
        uint256 minUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minUSD * precision)/price;
    }

    function getVersion() external view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getConversionRate(uint256 eth) public view returns (uint256) {
        uint256 price = getPrice();
        uint256 ethAmountInUSD = (price * eth) / 1000000000000000000;
        return ethAmountInUSD;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable {
        require(msg.sender == owner);
        payable(msg.sender).transfer(address(this).balance);
        for (
            uint256 fundersIndex = 0;
            fundersIndex < funders.length;
            fundersIndex++
        ) {
            address funder = funders[fundersIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }
}
