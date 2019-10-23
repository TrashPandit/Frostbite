from blockchain import *
from time import time
import pprint

pp = pprint.PrettyPrinter(indent=3)
blockchain=Blockchain()
transaction=Transaction("Anshul","Eva",10)

blockchain.pendingTransactions.append(transaction)
blockchain.minePendingTransactions("X")

pp.pprint(blockchain.chainJSONencode())
print("LENGTH:",len(blockchain.chain))
