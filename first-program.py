from bitcoinutils.setup import setup
from bitcoinutils.keys import P2shAddress, P2wshAddress, PublicKey, PrivateKey
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, Sequence
from bitcoinutils.script import Script
from bitcoinutils.constants import TYPE_RELATIVE_TIMELOCK

import sys


def main():
    setup('regtest')
    toPublicKey = PublicKey(
        '02f5dda832bf11ce1ea14e527a00881cb1979f074cfc3a2098ff4466973f10546b')
    block_height = 10
    seq = Sequence(TYPE_RELATIVE_TIMELOCK, block_height)
    redeem_script = Script([seq.for_script(), 'OP_CHECKSEQUENCEVERIFY', 'OP_DROP',
                           'OP_DUP', 'OP_HASH160', toPublicKey.to_hash160(), 'OP_EQUALVERIFY', 'OP_CHECKSIG'])
    print("redeem script:")
    print(redeem_script)
    addr = P2shAddress.from_script(redeem_script)
    print(f"public address: {toPublicKey.get_address().to_string()}")
    print(f"hash160 address: {toPublicKey.get_address().to_hash160()}")
    print(f"block height: {block_height}")
    print(f"p2sh address: {addr.to_string()}")
    print(f"p2sh hash160 address: {addr.to_hash160()}")


if __name__ == "__main__":
    main()
