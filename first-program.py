from bitcoinutils.setup import setup
from bitcoinutils.keys import P2shAddress, P2wshAddress, PublicKey, PrivateKey
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, Sequence
from bitcoinutils.script import Script
from bitcoinutils.constants import TYPE_RELATIVE_TIMELOCK

import sys


def main():
    setup('regtest')
    # example "python3 first-program.py 20 0250cf95328d65b4c83e0e7b888eef21720152f17fd87e8ae5407a811b40290ba4"
    # parameter 1, block heightº
    relative_blocks = 10
    seq = Sequence(TYPE_RELATIVE_TIMELOCK, relative_blocks)
    # toPublicKey = PublicKey(sys.argv[2])
    toPrivKey = PrivateKey(
        'cV1BXriUYr4y45waKc1Zz8MXRUC61MdNa4NH7nXS4moPXihe4S1Q')
    toPublicKey = toPrivKey.get_public_key()
    redeem_script = Script([seq.for_script(), 'OP_CHECKSEQUENCEVERIFY', 'OP_DROP',
                           'OP_DUP', 'OP_HASH160', toPublicKey.get_segwit_address().to_hash(), 'OP_EQUALVERIFY', 'OP_CHECKSIG'])
    print("redeem script:")
    print(redeem_script)
    addr = P2wshAddress.from_script(redeem_script)
    print(f"public address: {toPublicKey.get_address().to_string()}")
    print(f"hash160 address: {toPublicKey.get_address().to_hash160()}")
    print(f"block height: {relative_blocks}")
    print(f"p2sh address: {addr.to_string()}")
    print(f"p2sh witness hash: {addr.to_hash()}")
    print('c8f72e3701ac1012843d750b9067465f30ba4c3b33fa29fbc1e7aa2f656c735'.__len__())


if __name__ == "__main__":
    main()
