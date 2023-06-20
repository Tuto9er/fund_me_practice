from brownie import accounts, config, FundMe, network, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_FundMe():
    # Account selection
    account = get_account()

    # Price Feed - Mocks deployment
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        price_feed_address = deploy_mocks()

    # Contract deployment
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )

    # Return contract address
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_FundMe()
