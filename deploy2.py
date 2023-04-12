
from solcx import compile_standard # to compile code to lower level
import json
from web3 import Web3
import os

private_key = (
    load_dotenv()
)  # looks for .env script and directly imports the variable into our script
from dotenv import (
    load_dotenv,
)  # helps imports environment variables directly from .env file

with open("./simpleStorage.sol", "r") as file:  # opens .sol file
    simpleStorage = file.read()  # read and displays sol file on printing
install_solc("0.6.0")  # install solc version
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"simpleStorage.sol": {"content": simpleStorage}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)  # this compiles solidity code to lower level to abi(json format of description of functions) evm.bytecode is binary format

with open("compiled_code.json", "w") as file:
    json.dump(
        compiled_sol, file
    )  # writes file content in json format to the file named compiled_code.json
# bytecode version of code
bytecode = compiled_sol["contracts"]["simpleStorage.sol"]["simple"]["evm"]["bytecode"][
    "object"
]
# abi version of code
abi = compiled_sol["contracts"]["simpleStorage.sol"]["simple"]["abi"]
# for connecting to ganache/blockchain to deploy contact
w3 = Web3(
    Web3.HTTPProvider(
        "https://eth-sepolia.g.alchemy.com/v2/U5QMS8XYiHwuNpn_ay3sDT80g6EC25hm"
    )
)  # location of blockchain
network_id = 11155111  # the exact network/chain of blockchain to be deployed
my_address = (
    "0x50676C8A7b90E9b9Fa01797Bc7521f58b04Ad1a3"  # to deploy contract to which address
)
private_key = os.getenv(
    "PRIVATE_KEY"
)  # to sign transaction #os.getenv is used to get VALUE FROM ENVIRONMENT VARIABLE STORED IN OPERATING SYSTEM THUS os
# can create env variable by
# creating contract export PRIVATE_KEY=0x913f2331d59d73121f931b12a0b182f2e1af057ea059525d8c79ca18bb6c0c2d
# when terminal is closed this variable is washed off so you will have to create it again
simpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount()  # the number of transcation made
# deploying the contract we need to create a transcation
# Build the transcation
transcation = simpleStorage.constructor().buildTransaction(
    {"chain_id": network_id, "from": my_address, "nonce": nonce}
)
# Sign a transcation
sign_txn = w3.eth.sign_transaction(transcation, private_key=private_key)
# send a transcation
print("Deploying contract")
tx_hash = w3.eth.send_raw_transaction(sign_txn.rawTranscation)
tx_conf = w3.eth.wait_for_transaction_receipt(
    # tx_hash
)  # waits for a confirmation before our transcation can be created
print("Deployed")
# interact with the contract deployed
simple_storage = w3.eth.contract(address=tx_conf.address, abi=abi)
# we can interact in two ways
# we can call a contact not make a state change we will create contract but they wont be contract interactions even if we modified the smart contract like giving it a value we will see contract creation in transaction
print(simple_storage.functions.retrieve().call())
print(simple_storage.functions.store(15).call())

# making a state change to a smart contract
# we can transcation a contract to even view it and still it makes a state change it will show contract call in transcation in ganache
# build the transcation
print("Updating contract")
build_txn = simple_storage.functions.store(25).buildTranscation(
    {"chain_id": network_id, "from": my_address, "nonce": nonce + 1}
)  # nonce + 1 because a previous trancation was created so u need to update this

# sign the transcation
signed_txn = w3.eth.sign_transaction(build_txn, private_key=private_key)

# send/deploy the transaction like remix deployement

s_txn = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
w_txn = w3.eth.wait_for_transaction_receipt(
    s_txn
)  # wait for the transaction confirmation
print("Updated")

# see the state change
print("Here's the updated value of the Smart contract")
print(simple_storage.functions.retrieve().call())
