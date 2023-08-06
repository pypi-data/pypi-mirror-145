from __future__ import annotations
from multiprocessing.connection import wait
from typing import TYPE_CHECKING
import os
from dotenv import load_dotenv
import socket
from loguru import logger
import copy

load_dotenv() # load .env

P_2_P_PORT = int(os.getenv('P_2_P_PORT', 8122))

if TYPE_CHECKING:
    from beez.Types import Address
    from beez.transaction.Transaction import Transaction
    from beez.block.Block import Block
    

from beez.transaction.TransactionPool import TransactionPool
from beez.wallet.Wallet import Wallet
from beez.block.Blockchain import Blockchain
from beez.socket.SocketCommunication import SocketCommunication
from beez.socket.Message import Message
from beez.socket.MessageType import MessageType
from beez.BeezUtils import BeezUtils
from beez.api.NodeAPI import NodeAPI

class Node():

    def __init__(self, key=None):
        self.p2p = None
        self.ip = self.getIP()
        self.port = int(P_2_P_PORT)
        self.transactionPool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()
        if key is not None:
            self.wallet.fromKey(key)

    def getIP(self) -> Address:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 53))
            nodeAddress: Address = s.getsockname()[0]
            logger.info(f"Node IP: {nodeAddress}")

            return nodeAddress

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication(self)

    
    def startAPI(self):
        self.api = NodeAPI()
        # Inject Node to NodeAPI
        self.api.injectNode(self)
        self.api.start(self.ip)

    
    # this is coming from the NodeAPI
    def handleTransaction(self, transaction: Transaction):

        data = transaction.payload()
        signature = transaction.signature
        signaturePublicKey = transaction.senderPublicKey

        # # is valid?
        signatureValid = Wallet.signatureValid(data, signature, signaturePublicKey)

        #logger.info(f"signatureValid: {signatureValid}")        
        # # already exist in the transaction pool
        transactionExist = self.transactionPool.transactionExists(transaction)
        #logger.info(f"transactionExist: {transactionExist}")        
        transactionInBlock = self.blockchain.transactionExist(transaction)

        if not transactionExist and not transactionInBlock and signatureValid:
            #logger.info(f"add to the pool!!!")
            self.transactionPool.addTransaction(transaction)
            # Propagate the transaction to other peers
            message = Message(self.p2p.socketConnector, MessageType.TRANSACTION.name, None, transaction, None, None)
            encodedMessage = BeezUtils.encode(message)
            self.p2p.broadcast(encodedMessage)

            # check if is time to forge a new Block
            forgingRequired = self.transactionPool.forgerRequired()
            if forgingRequired == True:
                # logger.info(f"Forger required")
                self.forge()

    def handleBlock(self, block: Block):
        # logger.info(f"the Node checks the Block info")
        forger = block.forger
        blockHash = block.payload()
        signature = block.signature

        blockCountValid = self.blockchain.blockCountValid(block)
        lastBlockHashValid = self.blockchain.lastBlockHashValid(block)

        forgerValid = self.blockchain.forgerValid(block)
        transactionValid = self.blockchain.transactionValid(block.transactions)
        signatureValid = Wallet.signatureValid(blockHash, signature, forger)


        if not blockCountValid:
            # ask to other peer of their state of the blockchain
            self.requestChain()

        if lastBlockHashValid and forgerValid and transactionValid and signatureValid:
            self.blockchain.addBlock(block)
            self.transactionPool.removeFromPool(block.transactions)

            # broadcast the block message
            message = Message(self.p2p.socketConnector, MessageType.BLOCK.name, None, None, block, None)
            encodedMessage = BeezUtils.encode(message)
            self.p2p.broadcast(encodedMessage)

    def requestChain(self):
        message = Message(self.p2p.socketConnector, MessageType.BLOCKCHAINREQUEST.name, None, None, None, None)
        encodedMessage = BeezUtils.encode(message)
        self.p2p.broadcast(encodedMessage)

    def handleBlockchainRequest(self, requestingNode: Node):
        message = Message(self.p2p.socketConnector, MessageType.BLOCKCHAIN.name, None, None, None, self.blockchain)
        encodedMessage = BeezUtils.encode(message)
        self.p2p.send(requestingNode,encodedMessage)

    # sync blockchain between peers in the network
    def handleBlockchain(self, blockchain: Blockchain):
        logger.info(f"Iterate on the blockchain until to sync the local blockchain with the received one")
        localBlockchainCopy = copy.deepcopy(self.blockchain)
        localBlockCount = len(localBlockchainCopy.blocks)
        receivedChainBlockCount = len(blockchain.blocks)

        if localBlockCount <= receivedChainBlockCount:
            for blockNumber, block in enumerate(blockchain.blocks):
                # we are interested only on blocks that are not in our blockchain
                if blockNumber >= localBlockCount:
                    localBlockchainCopy.addBlock(block)
                    self.transactionPool.removeFromPool(block.transactions)
            self.blockchain = localBlockchainCopy


    def forge(self):
        forger = self.blockchain.nextForger()

        forgerString = str(forger).strip()
        thisWalletString = str(self.wallet.publicKeyString()).strip()
        
        if forgerString == thisWalletString:
            logger.info(f"I'm the next forger")
            # create a new Block
            block = self.blockchain.createBlock(self.transactionPool.transactions, self.wallet)

            # clean the transaction Pool
            self.transactionPool.removeFromPool(block.transactions)

            # bradcast the block to the network
            message = Message(self.p2p.socketConnector, MessageType.BLOCK.name, None, None, block, None)
            encodedMessage = BeezUtils.encode(message)
            self.p2p.broadcast(encodedMessage)

        else:
            logger.info(f"I'm not the forger")

