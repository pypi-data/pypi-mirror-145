from __future__ import annotations
from typing import List, TYPE_CHECKING
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

if TYPE_CHECKING:
    from beez.Types import PublicKeyString

from beez.BeezUtils import BeezUtils
from beez.transaction.Transaction import Transaction
from beez.transaction.TransactionType import TransactionType
from beez.block.Block import Block

class Wallet():
    """
    The wallet is used by the clients to allow them to perform transactions into the Blockchain.
    """
    def __init__(self):
        # 1024 is the modulo that we are going to use.
        self.keyPair = RSA.generate(1024) 

    def fromKey(self, file):
        key = ''
        with open(file, 'r') as keyfile:
            key = RSA.import_key(keyfile.read())
        self.keyPair = key

    def sign(self, data):
        dataHash = BeezUtils.hash(data)
        signatureSchemeObject = PKCS1_v1_5.new(self.keyPair)
        signature = signatureSchemeObject.sign(dataHash)

        return signature.hex()

    @staticmethod
    def signatureValid(data, signature, publicKeyString: PublicKeyString) -> bool:
        signature = bytes.fromhex(signature)
        dataHash = BeezUtils.hash(data)
        publicKey = RSA.importKey(publicKeyString)
        signatureSchemeObject = PKCS1_v1_5.new(publicKey) # providing the pubKey is able to validate the signature
        signatureValid = signatureSchemeObject.verify(dataHash, signature)

        return signatureValid

    def publicKeyString(self) -> PublicKeyString:
        publicKeyString: PublicKeyString = self.keyPair.publickey().exportKey('PEM').decode('utf-8')

        return publicKeyString

    def createTransaction(self, receiver: PublicKeyString, amount, type: TransactionType) -> Transaction:
        transaction = Transaction(self.publicKeyString(), receiver, amount, type)
        signature = self.sign(transaction.payload())
        transaction.sign(signature)

        return transaction


    def createBlock(self, transactions: List[Transaction], lastHash: str, blockCounter: int) -> Block:
        block = Block(transactions, lastHash, self.publicKeyString(), blockCounter)

        signature = self.sign(block.payload())

        block.sign(signature) # sign the Block

        return block        
        




