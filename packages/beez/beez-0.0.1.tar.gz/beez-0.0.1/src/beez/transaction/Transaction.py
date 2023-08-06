from __future__ import annotations
from typing import TYPE_CHECKING
import uuid
import time
import copy

# Avoid circular importing
if TYPE_CHECKING:
    from . import TransactionType
    from beez.Types import PublicKeyString


class Transaction():

    def __init__(self, senderPublicKey: PublicKeyString, receiverPublicKey: PublicKeyString, amount: float, type: TransactionType):
        self.senderPublicKey = senderPublicKey
        self.receiverPublicKey = receiverPublicKey
        self.amount = amount
        self.type = type
        self.id = uuid.uuid1().hex
        self.timestamp = time.time()
        self.signature = '' # guarantee that only the owner can perform this tx

    def toJson(self):
        return self.__dict__

    def sign(self, signature):
        self.signature = signature 

    # get a consistent representation of the signed transaction
    def payload(self):
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation['signature'] = ''

        return jsonRepresentation

    def equals(self, transaction: Transaction):
        if self.id == transaction.id:
            return True
        else:
            return False