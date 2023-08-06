from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from beez.socket.MessageType import MessageType
    from beez.transaction.Transaction import Transaction
    from beez.block.Block import Block
    from beez.block.Blockchain import Blockchain
    from beez.socket.SocketConnector import SocketConnector

class Message():
    """
    Represent the message that can be trasmitted in the network
    """

    def __init__(self, 
        senderConnector: SocketConnector, 
        messageType: MessageType, 
        ownPeers: Optional[List[SocketConnector]], 
        transaction: Optional[Transaction], 
        block: Optional[Block],
        blockchain: Optional[Blockchain]
        ):
        self.senderConnector = senderConnector
        self.messageType = messageType
        self.ownPeers = ownPeers
        self.transaction = transaction
        self.block = block
        self.blockchain = blockchain