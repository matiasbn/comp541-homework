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
from bitcoinutils.keys import P2pkhAddress, PrivateKey, PublicKey, P2wpkhAddress
from bitcoinutils.script import Script
from bitcoinutils.utils import to_bytes, to_satoshis
from bitcoinutils.transactions import Transaction, TxInput, TxOutput


def main():
    pp = pprint.PrettyPrinter(depth=6)
    # always remember to setup the network
    setup('regtest')

    # get a node proxy using default host and port
    proxy = NodeProxy('bitcoin', 'J9JkYnPiXWqgRzg3vAA').get_proxy()

    # create transaction input from tx id of UTXO (contained 0.4 tBTC)
    unspent = proxy.listunspent()
    if len(unspent) == 0:
        raise ValueError('Should have at least 1 UTXO')

    for utxo in unspent:
        if utxo['amount'] > 10:
            break
    print(utxo)
    print('UTXO:')
    pp.pprint(utxo)

    # Replace with the corresponding pks
    fromPrivKey = PrivateKey(
        'cRw78AsyzshE2txeFGN3gzUaEy5GiMw6Pao1QRyARVaN1xPDFmQu')

    toPrivKey = PrivateKey(
        'cVvX26vb4Tzy8DANNL1EzoeTnE1qfHas2vKQEHKgW5Gzq1u7EQts')

    fromAddress = fromPrivKey.get_public_key()
    toAddress = toPrivKey.get_public_key()

    txin = TxInput(utxo['txid'], utxo['vout'])
    txOut = TxOutput(to_satoshis(0.009), Script(['OP_DUP', 'OP_HASH160', toAddress.to_hash160(),
                                                 'OP_EQUALVERIFY', 'OP_CHECKSIG']))
    minerFee = 0.001
    changeOut = TxOutput(to_satoshis(50-0.009 - minerFee), Script(['OP_DUP', 'OP_HASH160', fromAddress.to_hash160(),
                                                                   'OP_EQUALVERIFY', 'OP_CHECKSIG']))

    # the script code required for signing for p2wpkh is the same as p2pkh
    script_code = Script(['OP_DUP', 'OP_HASH160', fromAddress.to_hash160(),
                          'OP_EQUALVERIFY', 'OP_CHECKSIG'])
    # create transaction output

    # create transaction without change output - if at least a single input is
    # segwit we need to set has_segwit=True
    tx = Transaction([txin], [txOut, changeOut], has_segwit=True)

    sig = fromPrivKey.sign_segwit_input(tx, 0, script_code, to_satoshis(50))
    tx.witnesses.append(Script([sig, fromAddress.to_hex()]))

    # print raw signed transaction ready to be broadcasted
    print("\nRaw transaction:\n" + tx.serialize())
    print("\nRaw signed transaction:\n" + tx.serialize())
    print("\nTxId:", tx.get_txid())
    proxy.sendrawtransaction(tx.serialize())
    # txout = TxOutput(to_satoshis(
    #     utxo['amount']-Decimal(0.01)),  addr.to_script_pub_key())

    # change_addr = P2wpkhAddress(utxo['address'])
    # change_txout = TxOutput(to_satoshis(
    #     0.001), change_addr.to_script_pub_key())
    # # change_txout = TxOutput(to_satoshis(0.001), Script(['OP_DUP', 'OP_HASH160',
    # #                                                     change_addr.to_script_pub_key(),
    # #                                                     'OP_EQUALVERIFY', 'OP_CHECKSIG']))

    # # # create transaction from inputs/outputs -- default locktime is used
    # tx = Transaction([txin], [txout, change_txout])

    # # # print raw transaction
    # print("\nRaw unsigned transaction:\n" + tx.serialize())

    # # # use the private key corresponding to the address that contains the
    # # # UTXO we are trying to spend to sign the input

    # # # note that we pass the scriptPubkey as one of the inputs of sign_input
    # # # because it is used to replace the scriptSig of the UTXO we are trying to
    # # # spend when creating the transaction digest
    # from_addr = P2wpkhAddress(utxo['address'])
    # sig = sk.sign_segwit_input(tx, 0, from_addr.to_script_pub_key())
    # print(sig)

    # # # get public key as hex
    # pk = sk.get_public_key().to_hex()

    # # # set the scriptSig (unlocking script)
    # txin.script_sig = Script([sig, pk])
    # signed_tx = tx.serialize()

    # # # print raw signed transaction ready to be broadcasted
    # print("\nRaw signed transaction:\n" + signed_tx)
    # print('hola')

    # proxy.sendrawtransaction(signed_tx)


if __name__ == "__main__":
    main()
