from scripts.deploy import deployFundMe
from scripts.helpfulScripts import getAccounts, LOCAL_BLOCKCHAIN_NETWORKS
import pytest
from brownie import accounts, network, exceptions

def test_fund_me():
    fund_me = deployFundMe()
    account = getAccounts()

    minPrice = fund_me.getEntranceFee() + 100
    tx1 = fund_me.pay({"from":account,"value":minPrice})
    tx1.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == minPrice

    tx2 = fund_me.withdraw({"from":account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0

def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORKS:
        pytest.skip("Only for development networks")
    fund_me = deployFundMe()
    account = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": account})
