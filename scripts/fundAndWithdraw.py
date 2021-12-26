from brownie import FundMe
from scripts.helpfulScripts import getAccounts


def fund():
    fund_me = FundMe[-1]
    account = getAccounts()
    fee = fund_me.getEntranceFee()
    print("The entrance fee is " + str(fee))
    fund_me.pay({"from" : account,"value": fee})

def withdraw():
    fund_me = FundMe[-1]
    account = getAccounts()
    fund_me.withdraw({"from": account})

def main():
    withdraw()