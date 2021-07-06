# Copyright (C) 2018-2020 The python-bitcoin-utils developers
#
# This file is part of python-bitcoin-utils
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoin-utils, including this file, may be copied,
# modified, propagated, or distributed except according to the terms contained
# in the LICENSE file.


import pprint
from decimal import Decimal
from bitcoinutils.setup import setup
from bitcoinutils.proxy import NodeProxy
from bitcoinutils.keys import P2pkhAddress, P2shAddress, PrivateKey, PublicKey, P2wpkhAddress
from bitcoinutils.script import Script
from bitcoinutils.utils import to_bytes, to_satoshis
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, Sequence
from bitcoinutils.constants import TYPE_RELATIVE_TIMELOCK

# This program assumes that regtest implements segwit


def main():
    pp = pprint.PrettyPrinter(depth=6)
    setup('regtest')
    # The spender private key, the txId and the output id to lock in the p2sh address
    fromPrivateKey = 'cPfLev7BCA48m2NKhmeYDYyTKzkCCTkWHM2JKDwPkwVUQi33krXF'
    txId = '98ef60879bf183b778b883a8a695b875cca0341e503dad21cf1dc9050eb761cf'
    txVout = 0

    # the receiver address and the block height to lock funds
    toPublicKey = PublicKey(
        '02f5dda832bf11ce1ea14e527a00881cb1979f074cfc3a2098ff4466973f10546b')
    block_height = 10

    rpcuser = 'bitcoin'
    rpcpass = 'J9JkYnPiXWqgRzg3vAA'
    proxy = NodeProxy(rpcuser, rpcpass).get_proxy()

    # Replace with the corresponding pks
    fromPrivKey = PrivateKey(fromPrivateKey)
    fromAddress = fromPrivKey.get_public_key()

    txin = TxInput(txId, 0)
    utxo = proxy.gettxout(txId, txVout)
    pp.pprint(utxo)
    minerFee = Decimal(0.001)
    amount = to_satoshis(utxo['value'] - minerFee)

    seq = Sequence(TYPE_RELATIVE_TIMELOCK, block_height)
    redeem_script = Script([seq.for_script(), 'OP_CHECKSEQUENCEVERIFY', 'OP_DROP',
                           'OP_DUP', 'OP_HASH160', toPublicKey.to_hash160(), 'OP_EQUALVERIFY', 'OP_CHECKSIG'])
    txOut = TxOutput(amount, redeem_script.to_p2sh_script_pub_key())

    tx = Transaction([txin], [txOut], has_segwit=True)

    script_code = Script(['OP_DUP', 'OP_HASH160', fromAddress.to_hash160(),
                          'OP_EQUALVERIFY', 'OP_CHECKSIG'])

    sig = fromPrivKey.sign_segwit_input(
        tx, 0, script_code, to_satoshis(utxo['value']))
    tx.witnesses.append(Script([sig, fromAddress.to_hex()]))

    print("\nRaw transaction:\n" + tx.serialize())
    print("\nRaw signed transaction:\n" + tx.serialize())
    print("\nTxId:", tx.get_txid())
    proxy.sendrawtransaction(tx.serialize())


if __name__ == "__main__":
    main()
