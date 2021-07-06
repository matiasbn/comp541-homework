# Bitcoin Assignment

For this assignment you will need to implement two scripts using Python 3 and any additional library of your choice.

The first one will create a P2SH Bitcoin address where all funds sent to it should be locked until a specific time, specified by block height; other than the time locking the redeem script should be equivalent to P2PKH.

The second program will allow someone to spend all funds from this address.

Both programs should:

use testnet (or regtest)

assume a local Bitcoin testnet/regtest node is running


* The first program should:

accept a public key for the P2PKH part of the redeem script

accept a future time expressed in block height

display the P2SH address


* The second program should:

accept a future time (expressed in block height) and a private key; to recreate the redeem script as above and also use to unlock the P2PKH part

accept a P2SH address to get the funds from (the one created by the first script - this could be recreated but we want to pass to double check it!)

check if the P2SH address has any UTXOs to get funds from

accept a P2PKH address to send the funds to

calculate the appropriate fees with respect to the size of the transaction

send all funds that the P2SH address received to the P2PKH address provided

display the raw unsigned transaction

sign the transaction

display the raw signed transaction

display the transaction id

verify that the transaction is valid and will be accepted by the Bitcoin nodes

if the transaction is valid, send it to the blockchain


## Notes:

* there is some repetition between the 2 programs; this is fine

* you will of course need to send some funds (manually) to the P2SH address that script one creates so that script two has something to spent

* the P2SH address might have received funds from multiple transactions. Create an initial version of your script where it handles a single known transaction. Expand it to using multiple unknown transactions later.

* when dealing with multiple inputs, you will need to sign all of them

* you will submit a single compressed file (ZIP or TGZ) that contains the Python source code. It should include a text file with detailed instructions on how to run your programs

* Also include a requirements.txt file that will specify any extra Python libraries you have used. You can easily create such a file using the following command in your Python virtual environment: ```$ pip freeze > requirements.txt```

* the source code is your main submission and it should contain everything you want to share. It should include detailed comments and everything else you think we should be aware of

* you are expected to manually construct the Bitcoin locking/unlocking script for the timelock transactions, using the appropriate OP_codes. If the programming libraries you are using have functionality to automatically create timelock transactions do not use them (it will be penalized)

# How to use
## First program (first-program.py)

This program creates the P2SH address. You should complete the next data inside the program:
1. toPublicKey: the receiver public key
2. block height: amount of blocks elapsed until funds are unlocked

The output P2SH address is "p2sh address:".

Run: 
```
python first-program.py
```
Output:
````
redeem script:
[10, 'OP_CHECKSEQUENCEVERIFY', 'OP_DROP', 'OP_DUP', 'OP_HASH160', '7cb019fab8fc75633a07cf753ff8089367b58aa2', 'OP_EQUALVERIFY', 'OP_CHECKSIG']
public address: mrtF3ay8XUPtJGCUbdK9mEDma45KBxVcSU
hash160 address: 7cb019fab8fc75633a07cf753ff8089367b58aa2
block height: 10
p2sh address: 2N6RCyV7TnhyfLWzsSAKtzJniTkhmACRXZr
p2sh hash160 address: 907cf2d4a7a9f61d06013365bc310281e01bb1c8
````
## Spend witness tx (spend_witness_tx.py)

This program creates an UTXO for the P2SH address. Assumes that you are using regtest with segwit enabled:
1. fromPrivateKey = source of the UTXO
2. txId = tx id of the "from" UTXO
3. txVout = tx vout

4. toPublicKey = who to send the funds
5. block_height = how much blocks to wait

6. rpcuser = btc node rpc user
7. rpcpass = btc node rpc pass

Run: 
```
python spend_witness_tx.py
```
Output:
````
{'bestblock': '7b8fc8a9eee798e49c4196a88471e48bec3c20f7fbc76a560cb4a6c00e32b4fc',
 'coinbase': True,
 'confirmations': 536,
 'scriptPubKey': {'addresses': ['bcrt1qtcw9xsen5fnmh7xhx5yaf56k09s5wy83uvup68'],
                  'asm': '0 5e1c534333a267bbf8d73509d4d35679614710f1',
                  'hex': '00145e1c534333a267bbf8d73509d4d35679614710f1',
                  'reqSigs': 1,
                  'type': 'witness_v0_keyhash'},
 'value': Decimal('50.00000000')}

Raw transaction:
02000000000101cf61b70e05c91dcf21ad3d501e34a0cc75b895a6a883b878b783f19b8760ef980000000000ffffffff01606b042a0100000017a914907cf2d4a7a9f61d06013365bc310281e01bb1c887024730440220710eed0b6e797bb4d368449037fd0b403a670a490c932b51dda18ab2248cb7d3022045bce58083f0d77a11550b2191f242dadf6c3a5a73d3e47327b3e7d8a7874fa2012102d3eef90768939bcc5d11376f94c704a435b0709bb0343b751741c0104bc2dc3000000000

Raw signed transaction:
02000000000101cf61b70e05c91dcf21ad3d501e34a0cc75b895a6a883b878b783f19b8760ef980000000000ffffffff01606b042a0100000017a914907cf2d4a7a9f61d06013365bc310281e01bb1c887024730440220710eed0b6e797bb4d368449037fd0b403a670a490c932b51dda18ab2248cb7d3022045bce58083f0d77a11550b2191f242dadf6c3a5a73d3e47327b3e7d8a7874fa2012102d3eef90768939bcc5d11376f94c704a435b0709bb0343b751741c0104bc2dc3000000000

TxId: 53ce3f5a38ea0f4701980ffc8ebcd865a64ea942e8262713aaaace879a68f035
````

# Second program (second-program.py)

Looks up all the UTXOs corresponding to a P2SH address and spent it in name of a user
1. rpcuser = btc node rpc user
2. rpcpass = btc node rpc pass
3. p2sh_address = generated in the first-program
4. block_height = how many block to wait
5. toPrivateKey = receiver private key

Example:
```
python second-program.py
```

Output:
```
Raw transaction:
020000000135f0689a87ceaaaa132726e842a94ea665d8bc8efc0f9801470fea385a3fce530000000088483045022100ab730479525482d813fbf7fc85474a2c8a307bbdc849d238020bc9ab5868ad4d022062cdcc6b5608c4db85846d115157474efc30029c9d40e066e5e7a2b9339b95c2012102f5dda832bf11ce1ea14e527a00881cb1979f074cfc3a2098ff4466973f10546b1c5ab27576a9147cb019fab8fc75633a07cf753ff8089367b58aa288ac0a00000001c0e4022a010000001976a9147cb019fab8fc75633a07cf753ff8089367b58aa288ac00000000

Raw signed transaction:
020000000135f0689a87ceaaaa132726e842a94ea665d8bc8efc0f9801470fea385a3fce530000000088483045022100ab730479525482d813fbf7fc85474a2c8a307bbdc849d238020bc9ab5868ad4d022062cdcc6b5608c4db85846d115157474efc30029c9d40e066e5e7a2b9339b95c2012102f5dda832bf11ce1ea14e527a00881cb1979f074cfc3a2098ff4466973f10546b1c5ab27576a9147cb019fab8fc75633a07cf753ff8089367b58aa288ac0a00000001c0e4022a010000001976a9147cb019fab8fc75633a07cf753ff8089367b58aa288ac00000000

TxId: ea47b64d877f002c472280d6e4332935e2978f06de3a438eb9cafb503fff3a21
Amount redeemed: 49.99900000 BTC
```

Remember to "mine" `block_height`blocks in order to unlock the locked BTCs.