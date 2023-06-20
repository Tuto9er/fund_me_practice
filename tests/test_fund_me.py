from scripts.deploy import deploy_FundMe
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import network, accounts, exceptions
import pytest


def test_fund():
    account = get_account()
    fund_me = deploy_FundMe()
    entranceFee = fund_me.getEntranceFee()
    tx = fund_me.fund({"from": account, "value": entranceFee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entranceFee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me = deploy_FundMe()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
