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

from decimal import Decimal
from bitcoinutils.setup import setup
from bitcoinutils.utils import to_satoshis
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, Sequence
from bitcoinutils.constants import TYPE_RELATIVE_TIMELOCK
from bitcoinutils.keys import P2pkhAddress, P2wshAddress, PrivateKey, P2shAddress
from bitcoinutils.script import Script
from bitcoinutils.proxy import NodeProxy

import sys


def main():
    setup('regtest')
    proxy = NodeProxy('bitcoin', 'J9JkYnPiXWqgRzg3vAA').get_proxy()
    toPrivKey = PrivateKey(
        'cV1BXriUYr4y45waKc1Zz8MXRUC61MdNa4NH7nXS4moPXihe4S1Q')
    toPublicKey = toPrivKey.get_public_key()
    txId = '19b4e5032ec10746efeb7299d2c1b8cdddd1b011f5e494158a43f648cf0f5206'
    txVout = 0
    txin = TxInput(txId, txVout)
    utxo = proxy.gettxout(txId, txVout)
    print(utxo)
    minerFee = Decimal(0.001)
    amount = to_satoshis(utxo['value'] - minerFee)
    txout = TxOutput(
        amount,  toPrivKey.get_public_key().get_address().to_script_pub_key())
    tx = Transaction([txin], [txout], has_segwit=True)

    relative_blocks = 10
    seq = Sequence(TYPE_RELATIVE_TIMELOCK, relative_blocks)
    redeem_script = Script([seq.for_script(), 'OP_CHECKSEQUENCEVERIFY', 'OP_DROP',
                           'OP_DUP', 'OP_HASH160', toPublicKey.get_segwit_address().to_hash(), 'OP_EQUALVERIFY', 'OP_CHECKSIG'])

    sig = toPrivKey.sign_segwit_input(
        tx, 0, redeem_script, to_satoshis(utxo['value']))
    tx.witnesses.append(
        Script([sig, redeem_script.to_hex()]))
    print("\nRaw transaction:\n" + tx.serialize())
    print("\nRaw signed transaction:\n" + tx.serialize())
    print("\nTxId:", tx.get_txid())
    proxy.sendrawtransaction(tx.serialize())


if __name__ == "__main__":
    main()
