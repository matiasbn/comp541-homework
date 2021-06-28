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

