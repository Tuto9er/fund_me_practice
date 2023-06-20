from brownie import network, accounts, config, MockV3Aggregator

# Static variables
DECIMALS = 18
STARTING_PRICE = 2000000000000000000000

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    if len(MockV3Aggregator) <= 0:
        print(f"The active network is {network.show_active()}")
        print("Deploying mocks...")
        mock_aggregator = MockV3Aggregator.deploy(
            DECIMALS, STARTING_PRICE, {"from": get_account()}
        )
        print("Mocks deployed!")
        return mock_aggregator.address
    else:
        print("Mocks already deployed!")
        return MockV3Aggregator[-1].address
