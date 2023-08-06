from __future__ import annotations
import json
from typing import TYPE_CHECKING, List
from loguru import logger
from p2pnetwork.node import Node

import os
from dotenv import load_dotenv

load_dotenv() # load .env

FIRST_SERVER_IP = os.getenv('FIRST_SERVER_IP', '127.0.0.1')
P_2_P_PORT = int(os.getenv('P_2_P_PORT', 8122))


if TYPE_CHECKING:
    from beez.Types import Address
    from beez.socket.SocketConnector import SocketConnector
    from beez.socket.Message import Message
    from beez.node.Node import Node as BeezNode
    
from beez.socket.PeerDiscoveryHandler import PeerDiscoveryHandler
from beez.socket.SocketConnector import SocketConnector
from beez.BeezUtils import BeezUtils
from beez.socket.MessageType import MessageType

class SocketCommunication(Node):
    """
    This class manage the P2P communication.
    """
    def __init__(self, ip: Address, port: int):
        super(SocketCommunication, self).__init__(ip, port, None)
        # TODO: move the peers to a storage!
        self.peers: List[SocketConnector] = []
        self.peerDiscoveryHandler = PeerDiscoveryHandler(self)
        self.socketConnector = SocketConnector(ip=ip, port=port)
    
    def connectToFirstNode(self):
        logger.info(f"Check to connect to first node {FIRST_SERVER_IP} at port {P_2_P_PORT}")

        if self.socketConnector.ip != FIRST_SERVER_IP or self.socketConnector.port != P_2_P_PORT:
            # connect to the first node
            self.connect_with_node(FIRST_SERVER_IP, P_2_P_PORT)

    def startSocketCommunication(self, beezNode: BeezNode):
        self.beezNode = beezNode
        self.start()
        self.peerDiscoveryHandler.start()
        self.connectToFirstNode()

    # Callback method of receiving requests from nodes
    def inbound_node_connected(self, connectedNode: Node):
        logger.info(f"inbound connection (some node wants to connect to this node)")
        self.peerDiscoveryHandler.handshake(connectedNode)

    # Callback method of sending requests to nodes
    def outbound_node_connected(self, connectedNode: Node):
        logger.info(f"outbound connection (this node wants to connect to other node)")
        self.peerDiscoveryHandler.handshake(connectedNode)

    # Once connected send a message 
    # this is automatically provided by the library
    def node_message(self, connectedNode: Node, message: Message):
        message = BeezUtils.decode(json.dumps(message))
        
        if message.messageType == MessageType.DISCOVERY.name:
            self.peerDiscoveryHandler.handleMessage(message)
        elif message.messageType == MessageType.TRANSACTION.name:
            # broadcast the transaction to all the peers
            logger.info(f"A Transaction Message will be broadcasted!!")
            transaction = message.transaction
            self.beezNode.handleTransaction(transaction)
        elif message.messageType == MessageType.BLOCK.name:
            logger.info(f"A Block will be broadcasted!!")
            block = message.block
            self.beezNode.handleBlock(block)
        elif message.messageType == MessageType.BLOCKCHAINREQUEST.name:
            logger.info(f"A request to sync the Blockchain is made")
            self.beezNode.handleBlockchainRequest(connectedNode)
        elif message.messageType == MessageType.BLOCKCHAIN.name:
            logger.info(f"Send the current version of the blockchain to the requester node")
            blockchain = message.blockchain
            self.beezNode.handleBlockchain(blockchain)


    def send(self, receiver: Node, message: str):
        self.send_to_node(receiver, message)

    def broadcast(self, message: str):
        self.send_to_nodes(message)

