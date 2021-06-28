from bitcoinutils.setup import setup
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, Sequence
from bitcoinutils.keys import P2pkhAddress, P2shAddress, PrivateKey
from bitcoinutils.script import Script
from bitcoinutils.constants import TYPE_RELATIVE_TIMELOCK
import sys


def main():
    setup('testnet')

    relative_blocks = 20
    seq = Sequence(TYPE_RELATIVE_TIMELOCK, relative_blocks)

    # p2pkh_sk = PrivateKey(
    #     'cRvyLwCPLU88jsyj94L7iJjQX5C2f8koG4G2gevN4BeSGcEvfKe9')

    # p2pkh_addr = p2pkh_sk.get_public_key().get_address()
    # get address from command line
    p2pkh_addr = sys.argv[1]
    redeem_script = Script([seq.for_script(), 'OP_CHECKSEQUENCEVERIFY', 'OP_DROP',
                           'OP_DUP', 'OP_HASH160', p2pkh_addr, 'OP_EQUALVERIFY', 'OP_CHECKSIG'])

    addr = P2shAddress.from_script(redeem_script)
    print(f"block before unlock: {relative_blocks}")
    print(f"p2sh address: {addr.to_string()}")


if __name__ == "__main__":
    main()
