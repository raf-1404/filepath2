from brownie import accounts, config, simpleStorage
# import os


def deploy_simple_storage():
    account = accounts[0] #for local ganache accounts
    simple_storage = simpleStorage.deploy({"from": account}) #the contract name . deploy from which account will be deploying it
    print(simple_storage)
    # account = accounts.load("freecodecamp-account") #safe ways for storing keys first do brownie accounts new freecodecamp-account
    #print(account)
    # account = accounts.add(os.getenv("PRIVATE_KEY")) #fetches private key from env file associated with account
    # print(account)
    #account = accounts.add(config["wallets"]["from_key"])
    #print(account)


def main():
    deploy_simple_storage()
