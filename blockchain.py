from time import time
import json
import hashlib

class Blockchain(object):
	def __init__(self):
		self.chain=[]

	def getLastBlock(self):
		return self.chain[-1]

	def addBlock(self,block):
		if(len(self.chain)>0):
			block.prev=self.getLastBlock().hash
		else:
			block.prev="No Block" 
		self.chain.append(block)

	def chainJSONencode(self): #Print chain in nice JSON
		blockArrJSON = [];
		for block in self.chain:
			blockJSON = {};
			blockJSON['index'] = block.index;
			blockJSON['hash'] = block.hash;
			blockJSON['prev'] = block.prev;
			blockJSON['time'] = block.time;


			transactionsJSON = [];
			tJSON = {};
			for transaction in block.transactions:
				tJSON['time'] = transaction.time;
				tJSON['sender'] = transaction.sender;
				tJSON['reciever'] = transaction.reciever;
				tJSON['amt'] = transaction.amt;
				tJSON['hash'] = transaction.hash;
				transactionsJSON.append(tJSON);

			blockJSON['transactions'] = transactionsJSON;

			blockArrJSON.append(blockJSON);

		return blockArrJSON;

class Block(object):
	def __init__(self,transactions,time,index):
		self.index=index	 # Block Number
		self.transactions=transactions
		self.time=time	# Time of transaction
		self.prev=''	# Previous Block Hash
		self.hash=self.calculateHash()	# Current Block Hash
	
	def calculateHash(self):
		hashTransactions=""
		for transaction in self.transactions:
			hashTransactions+=transaction.hash

		hashString = str(self.time)+hashTransactions+self.prev+str(self.index)
		hashEncoded=json.dumps(hashString,sort_keys=True).encode()
		return hashlib.sha256(hashEncoded).hexdigest()	# SHA256 Hash Encoding

class Transaction(object):
	def __init__(self,sender,receiver,amt):
		self.sender=sender
		self.receiver=receiver
		self.amt=amt	# Amount of transaction
		self.time=Time()# Time of transaction
		self.hash=self.calculateHash()

	def calculateHash(self):
		hashString = self.sender+self.receiver+str(self.amt)+str(self.time)
		hashEncoded=json.dumps(hashString,sort_keys=True).encode()
		return hashlib.sha256(hashEncoded).hexdigest()	
