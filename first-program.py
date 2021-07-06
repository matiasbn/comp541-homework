from bitcoinutils.setup import setup
from bitcoinutils.keys import P2shAddress, PublicKey
from bitcoinutils.script import Script
import sys


def main():
    setup('testnet')
    # example "python3 first-program.py 20 0250cf95328d65b4c83e0e7b888eef21720152f17fd87e8ae5407a811b40290ba4"
    # parameter 1, block height
    relative_blocks = int(sys.argv[1])
    # p2pkh_sk = PrivateKey(
    #     '9269dzjLf6SVfNtiQXvcszv44rLY4ZQV24dvAikhTJmQqQpfsao')
    # public -> mi6EgYUUFauaMiv4pcrerkS6b97eRh1wYx
    # p2pkh_sk = PrivateKey(
    #     '91wda2o4YaqhChv7YXNSj4jLz2byHkKde4QV5tRuy4KZPHseFPX')
    # public -> mfkVbcQhuqkgFA2wqTcVxqEiAxqF3Rqd9P
    # p2pkh_addr = p2pkh_sk.get_public_key()
    # parameter 2, public key as hex
    p2pkh_addr = PublicKey(sys.argv[2])
    redeem_script = Script([relative_blocks, 'OP_CHECKSEQUENCEVERIFY', 'OP_DROP',
                           'OP_DUP', 'OP_HASH160', p2pkh_addr.get_address().to_hash160(), 'OP_EQUALVERIFY', 'OP_CHECKSIG'])
    addr = P2shAddress.from_script(redeem_script)
    print(f"public address: {p2pkh_addr.get_address().to_string()}")
    print(f"hash160 address: {p2pkh_addr.get_address().to_hash160()}")
    print(f"block height: {relative_blocks}")
    print(f"p2sh address: {addr.to_string()}")


if __name__ == "__main__":
    main()
