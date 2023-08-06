from __future__ import annotations
from typing import TYPE_CHECKING, List
import threading
import time
from loguru import logger

from beez.socket.SocketConnector import SocketConnector

if TYPE_CHECKING:
    from beez.socket.SocketCommunication import SocketCommunication
    from p2pnetwork.node import Node

from beez.socket.MessageType import MessageType
from beez.socket.Message import Message
from beez.BeezUtils import BeezUtils

class PeerDiscoveryHandler():
    """
    A Socket Communication submodule that frequently checks if there are new peers in the network.
    """

    def __init__(self, socketCommunication: SocketCommunication):
        self.socketCommunication = socketCommunication

    
    def start(self):
        statusThread = threading.Thread(target=self.status, args={})
        statusThread.start()

        discoveryThread = threading.Thread(target=self.discovery,args={})
        discoveryThread.start()

    """
    Display the nodes that are connected to a node
    """
    def status(self):
        while True:
            logger.info(f"Current connections:")
            for peer in self.socketCommunication.peers:
                logger.info(f"Peer: {str(peer.ip)}: {str(peer.port)}")

            time.sleep(10)

    def discovery(self):
        while True:
            # logger.info(f"Discovery")
            handshakeMessage = self.handshakeMessage()
            self.socketCommunication.broadcast(handshakeMessage)
            time.sleep(10)

    def handshake(self, connect_node: Node):
        """
        exchange of information between nodes.
        """
        handshakeMessage = self.handshakeMessage()
        self.socketCommunication.send(connect_node, handshakeMessage)
    
    def handshakeMessage(self):
        """
        Define the content of the message that will be shared between peers.
        Here, what is important is to share the knowed peers
        """
        # TODO: based on the business logic of the blockchain update those information
        ownConnector = self.socketCommunication.socketConnector
        ownPeers = self.socketCommunication.peers
        messageType = MessageType.DISCOVERY.name
        message = Message(ownConnector, messageType, ownPeers, None, None, None)

        # Encode the message since peers communicate with bytes!
        encodedMessage = BeezUtils.encode(message)

        return encodedMessage


    def handleMessage(self, message: Message):
        # logger.info(f"handling message {message}")
        peerSocketConnector = message.senderConnector
        peersPeerList: List[SocketConnector] = message.ownPeers
        newPeer = True

        for peer in self.socketCommunication.peers:
            if peer.equals(peerSocketConnector):
                # the node is itself
                newPeer = False
        
        if newPeer == True:
            # if is not itself add to the list of peers
            self.socketCommunication.peers.append(peerSocketConnector)

        # Check if in the peersPeerList there are new peers and connect to them
        for peersPeer in peersPeerList:
            peerKnow = False
            for peer in self.socketCommunication.peers:
                if peer.equals(peersPeer):
                    peerKnow = True
            if not peerKnow and not peersPeer.equals(self.socketCommunication.socketConnector):
                self.socketCommunication.connect_with_node(peersPeer.ip, peersPeer.port)