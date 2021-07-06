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
    rpcuser = 'bitcoin'
    rpcpass = 'J9JkYnPiXWqgRzg3vAA'
    p2sh_address = '2N6RCyV7TnhyfLWzsSAKtzJniTkhmACRXZr'
    block_height = 10
    # Corresponding to the address that has the funds locked in the p2sh address
    toPrivateKey = 'cV1BXriUYr4y45waKc1Zz8MXRUC61MdNa4NH7nXS4moPXihe4S1Q'

    proxy = NodeProxy(rpcuser, rpcpass).get_proxy()
    p2sh_address = P2shAddress(p2sh_address)
    p2sh_utxos = proxy.listunspent(0, 999999, [p2sh_address.to_string()])
    seq = Sequence(TYPE_RELATIVE_TIMELOCK, block_height)

    # Get amount and txin
    amount = 0
    txins = []
    for utxo in p2sh_utxos:
        amount += utxo['amount']
        txins.append(TxInput(utxo['txid'], utxo['vout'],
                             sequence=seq.for_input_sequence()))

    toPrivKey = PrivateKey(toPrivateKey)
    toPublicKey = toPrivKey.get_public_key()

    redeem_script = Script([seq.for_script(), 'OP_CHECKSEQUENCEVERIFY', 'OP_DROP',
                           'OP_DUP', 'OP_HASH160', toPublicKey.get_address().to_hash160(), 'OP_EQUALVERIFY', 'OP_CHECKSIG'])

    minerFee = Decimal(0.001)
    txout = TxOutput(to_satoshis(amount - minerFee),
                     toPublicKey.get_address().to_script_pub_key())
    tx = Transaction(txins, [txout])

    for index, txin in enumerate(txins):
        sig = toPrivKey.sign_input(tx, index, redeem_script)
        txin.script_sig = Script(
            [sig, toPublicKey.to_hex(), redeem_script.to_hex()])

    print("\nRaw transaction:\n" + tx.serialize())
    print("\nRaw signed transaction:\n" + tx.serialize())
    print("\nTxId:", tx.get_txid())
    print("Amount redeemed: " + str(amount) + " BTC")
    proxy.sendrawtransaction(tx.serialize())


if __name__ == "__main__":
    main()
