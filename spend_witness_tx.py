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


def main():
    pp = pprint.PrettyPrinter(depth=6)
    # always remember to setup the network
    setup('regtest')

    # get a node proxy using default host and port
    proxy = NodeProxy('bitcoin', 'J9JkYnPiXWqgRzg3vAA').get_proxy()

    # create transaction input from tx id of UTXO (contained 0.4 tBTC)

    # Replace with the corresponding pks
    fromPrivKey = PrivateKey(
        'cPfLev7BCA48m2NKhmeYDYyTKzkCCTkWHM2JKDwPkwVUQi33krXF')
    fromAddress = fromPrivKey.get_public_key()

    txId = '5d740508744e70618d992037735ce18c17c9be196f27be4d30bb6af434084983'
    txVout = 0
    txin = TxInput(txId, 0)
    utxo = proxy.gettxout(txId, txVout)
    pp.pprint(utxo)
    minerFee = Decimal(0.001)
    amount = to_satoshis(utxo['value'] - minerFee)

    relative_blocks = 10
    seq = Sequence(TYPE_RELATIVE_TIMELOCK, relative_blocks)
    toPrivKey = PrivateKey(
        'cV1BXriUYr4y45waKc1Zz8MXRUC61MdNa4NH7nXS4moPXihe4S1Q')
    toPublicKey = toPrivKey.get_public_key()
    redeem_script = Script([seq.for_script(), 'OP_CHECKSEQUENCEVERIFY', 'OP_DROP',
                           'OP_DUP', 'OP_HASH160', toPublicKey.to_hash160(), 'OP_EQUALVERIFY', 'OP_CHECKSIG'])
    print(redeem_script.to_p2wsh_script_pub_key())
    txOut = TxOutput(amount, redeem_script.to_p2wsh_script_pub_key())

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
