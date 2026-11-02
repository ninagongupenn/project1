from web3 import Web3
from eth_account.messages import encode_defunct
import eth_account
import os

def sign_message(challenge, filename="secret_key.txt"):
    with open(filename, "r") as f:
        private_key = f.read().strip()

    assert private_key, "Your secret_key.txt is empty"

    account = eth_account.Account.from_key(private_key)
    eth_addr = Web3.to_checksum_address(account.address)

    message = encode_defunct(challenge)

    signed_message = eth_account.Account.sign_message(
        message,
        private_key=private_key
    )

    assert eth_account.Account.recover_message(
        message,
        signature=signed_message.signature.hex()
    ) == eth_addr, "Failed to sign message properly"

    return signed_message, eth_addr


if __name__ == "__main__":
    for i in range(4):
        challenge = os.urandom(64)
        sig, addr= sign_message(challenge=challenge)
        print( addr )
