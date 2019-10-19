from blockchain import *
from time import time
import pprint

pp = pprint.PrettyPrinter(indent=3)
blockchain=Blockchain()
transaction=[]

block=Block(transaction,time(),0)
blockchain.addBlock(block)

block=Block(transaction,time(),1)
blockchain.addBlock(block)

block=Block(transaction,time(),2)
blockchain.addBlock(block)

pp.pprint(blockchain.chainJSONencode())
print("LENGTH:",len(blockchain.chain))
