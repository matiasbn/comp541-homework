from bitcoinutils.setup import setup
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, Sequence
from bitcoinutils.keys import P2pkhAddress, P2shAddress, PrivateKey, PublicKey
from bitcoinutils.script import Script
from bitcoinutils.constants import TYPE_RELATIVE_TIMELOCK
import sys


def main():
    setup('testnet')

    # parameter 1, block height
    relative_blocks = int(sys.argv[1])
    seq = Sequence(TYPE_RELATIVE_TIMELOCK, relative_blocks)
    # p2pkh_sk = PrivateKey(
    #     '9269dzjLf6SVfNtiQXvcszv44rLY4ZQV24dvAikhTJmQqQpfsao')
    # p2pkh_addr = p2pkh_sk.get_public_key()
    p2pkh_addr = (PublicKey(sys.argv[2]))
    redeem_script = Script([seq.for_script(), 'OP_CHECKSEQUENCEVERIFY', 'OP_DROP',
                           'OP_DUP', 'OP_HASH160', p2pkh_addr.get_address().to_hash160(), 'OP_EQUALVERIFY', 'OP_CHECKSIG'])

    addr = P2shAddress.from_script(redeem_script)
    print(f"public address: {p2pkh_addr.get_address().to_hash160()}")
    print(f"block height: {relative_blocks}")
    print(f"p2sh address: {addr.to_string()}")


if __name__ == "__main__":
    main()
