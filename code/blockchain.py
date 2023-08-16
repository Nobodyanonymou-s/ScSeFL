import hashlib
from hashlib import sha256
import time
import copy
import os
status = 0
class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
    def __str__(self):
        return '%s-%s-%s-%s-%s' % (self.index, self.transactions, self.timestamp, self.previous_hash, self.nonce)
    __repr__ = __str__

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        #block_string = self.__dict__
        s_temp = copy.deepcopy(self.__str__())#.encode().decode()
        #print(s_temp)
        temp = hashlib.sha256()
        temp.update(s_temp.encode('utf-8'))
        return temp.hexdigest()


class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.temp = []
        self.chain = []
        #self.index = 0

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0,[], 0, "0")
        #genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
        #self.chain[0] = copy.deepcopy(genesis_block)
    def get_trans(self):
        #temp = self.last_block
        return self.temp
    # @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block().compute_hash()

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False
        #self.index+=1
        #block.hash = proof
        self.chain.append(block)
        #self.chain[self.index] = copy.deepcopy(block)
        return True
    
    def addblock(self,block):
        self.chain.append(block)
        #self.index+=1
        #self.chain[self.index] = copy.deepcopy(block)

    #@staticmethod
    def proof_of_work(self,block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new(self, transaction):
        self.unconfirmed_transactions.append(transaction)
    #@classmethod
    def is_valid_proof(self, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    #@classmethod
    def check_chain_validity(self, chain):
        result = True
        previous_hash = "0"

        for block in chain:
            block_hash = block.compur_hash()
            # remove the hash field to recompute the hash again
            # using `compute_hash` method.
            delattr(block, "hash")

            if not self.is_valid_proof(block, block_hash) or \
                    previous_hash != block.previous_hash:
                result = False
                break

            block.hash, previous_hash = block_hash, block_hash

        return result

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block()
        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.compute_hash())
        print(new_block.transactions)
        proof = self.proof_of_work(new_block)# 加入10个节点竞争，每轮随机拓扑，算力，能量写个函数，计算耗时并等待完耗时
        if self.add_block(new_block, proof):
            print("true")
        self.temp = self.unconfirmed_transactions
        self.unconfirmed_transactions = []

        return True

class account():
    def __init__(self,type):
        self.balance = 0
        self.type = type
    def check(self):
        return self.balance
    def change(self,benefit):
        temp = benefit
        self.balance = self.balance + temp
        return 1

class transaction():
    def __init__(self,amount,type):
        self.payer = 2
        self.amount = amount
        self.receiver = type

# app = Flask(__name__)

# the node's copy of blockchain
#blockchain = Blockchain()
#blockchain.create_genesis_block()

# endpoint to add a block mined by someone else to
# the node's chain. The block is first verified by the node
# and then added to the chain.
# @app.route('/add_block', methods=['POST'])
# def verify_and_add_block():
#     block_data = request.get_json()
#     block = Block(block_data["index"],
#                   block_data["transactions"],
#                   block_data["timestamp"],
#                   block_data["previous_hash"],
#                   block_data["nonce"])

#     proof = block_data['hash']
#     added = blockchain.add_block(block, proof)

#     if not added:
#         return "The block was discarded by the node"

#     return "Block added to the chain"

