from time import time
import json
import hashlib
from datetime import datetime

class Blockchain(object):
	def __init__(self):
		self.chain=[self.addGenesisBlock()]
		self.pendingTransactions=[]	# To be added to blockchain
		self.difficulty=3
		self.minerRewad = 100
		self.blockSize = 10;

	def addGenesisBlock(self):	#	first block of blockchain
		tArr = []
		tArr.append(Transaction("Anshul", "You", 1));
		genesis = Block(tArr,datetime.now().strftime("%m/%d/%y,%H:%M:%S"),0)
		genesis.prev="none"
		return genesis

	def getLastBlock(self):
		return self.chain[-1]

	def addBlock(self,block):
		if(len(self.chain)>0):
			block.prev=self.getLastBlock().hash
		else:
			block.prev="No Block"
		self.chain.append(block)

	def minePendingTransactions(self,miner):
		lenPT = len(self.pendingTransactions)
		if(lenPT<1):
			print("Very Less Transactions")
			return False
		else:
			for i in range(0,lenPT,self.blockSize):
				end = i + self.blockSize
				if i >= lenPT:
					end = lenPT
				transactionSlice = self.pendingTransactions[i:end]
				newBlock = Block(transactionSlice, datetime.now().strftime("%m/%d/%y, %H:%M:%S"), len(self.chain));
				hashVal = self.getLastBlock().hash
				newBlock.prev = hashVal
				newBlock.mineBlock(self.difficulty)
				self.chain.append(newBlock)
			print("Minning Successful")
			payMiner = Transaction("Rewards", miner,self.minerRewards)
			self.pendingTransactions=[payMiner]
		return True

	def chainJSONencode(self): #Print chain in nice JSON
		blockArrJSON = []
		for block in self.chain:
			blockJSON = {}
			blockJSON['index'] = block.index
			blockJSON['hash'] = block.hash
			blockJSON['prev'] = block.prev
			blockJSON['time'] = block.time
			blockJSON['nonce'] = block.nonce


			transactionsJSON = []
			tJSON = {}
			for transaction in block.transactions:
				tJSON['time'] = transaction.time
				tJSON['sender'] = transaction.sender
				tJSON['reciever'] = transaction.reciever
				tJSON['amt'] = transaction.amt
				tJSON['hash'] = transaction.hash
				transactionsJSON.append(tJSON)

			blockJSON['transactions'] = transactionsJSON

			blockArrJSON.append(blockJSON)

		return blockArrJSON

class Block(object):
	def __init__(self,transactions,time,index):
		self.index = index	 # Block Number
		self.transactions = transactions
		self.time = time	# Time of transaction
		self.prev = ''	# Previous Block Hash
		self.nonce = 0	
		self.hash = self.calculateHash()	# Current Block Hash
		# Cryptographic Nonce: Value that varies with time
	
	def mineBlock(self,difficulty):
		arr=[]
		for i in range(0,difficulty):
			arr.append(i)
		arrStr = map(str,arr)	# Convert Numbers to string
		hashPuzzle = ''.join(arrStr)	# The puzzle to solve
		while self.hash[0:difficulty] != hashPuzzle:	# Starting 0...N characters to check
			self.nonce += 1
			self.hash = self.calculateHash();
			print("Nonce",self.nonce)
			print("Hash Tried",self.hash)
			print("Hash We Want",hashPuzzle,"...")
		print("Block Mined")
		return True

	def calculateHash(self):
		hashTransactions=""
		for transaction in self.transactions:
			hashTransactions+=transaction.hash

		hashString = str(self.time)+hashTransactions+self.prev+str(self.nonce)	# Error here nonce doesn't update
		hashEncoded=json.dumps(hashString,sort_keys=True).encode()
		return hashlib.sha256(hashEncoded).hexdigest()	# SHA256 Hash Encoding

class Transaction(object):
	def __init__(self,sender,receiver,amt):
		self.sender=sender
		self.receiver=receiver
		self.amt=amt	# Amount of transaction
		self.time = datetime.now().strftime("%m/%d/%y, %H:%M:%S")# Time of transaction
		self.hash=self.calculateHash()

	def calculateHash(self):
		hashString = self.sender+self.receiver+str(self.amt)+str(self.time)
		hashEncoded=json.dumps(hashString,sort_keys=True).encode()
		return hashlib.sha256(hashEncoded).hexdigest()	
