from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpfulScripts import getAccounts, LOCAL_BLOCKCHAIN_NETWORKS
from web3 import Web3


def deployFundMe():
    account = getAccounts()
    if network.show_active() not in  LOCAL_BLOCKCHAIN_NETWORKS:
        price_feed_address = config['networks'][network.show_active()]['eth-usd-price']
    else:
        if len(MockV3Aggregator) <= 0:
            price_feed_address = MockV3Aggregator.deploy(8, 200000000000,{"from": account})
            price_feed_address = price_feed_address.address
        else:
            price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account}
        )
    print(fund_me)
    return fund_me

def main():
    deployFundMe()