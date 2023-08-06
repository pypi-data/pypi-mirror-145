from __future__ import annotations
from typing import TYPE_CHECKING, List

from loguru import logger

from beez.transaction.TransactionType import TransactionType

if TYPE_CHECKING:
    from beez.transaction.Transaction import Transaction
    from beez.Types import PublicKeyString
    from beez.wallet.Wallet import Wallet

from beez.block.Block import Block
from beez.BeezUtils import BeezUtils
from beez.state.AccountStateModel import AccountStateModel
from beez.consensus.ProofOfStake import ProofOfStake

class Blockchain():
    """
    A Blockchain is a linked list of blocks
    """
    def __init__(self):
        self.blocks: List[Block] = [Block.genesis()] 
        self.accountStateModel = AccountStateModel()
        self.pos = ProofOfStake()

    def addBlock(self, block: Block):
        self.executeTransactions(block.transactions)
        self.blocks.append(block)

    def toJson(self):
        jsonBlockchain = {}
        jsonBloks = []
        for block in self.blocks:
            jsonBloks.append(block.toJson())
        jsonBlockchain['blocks'] = jsonBloks

        return jsonBlockchain

    def blockCountValid(self, block: Block):
        if self.blocks[-1].blockCount == block.blockCount - 1:
            return True
        else:
            return False

    def lastBlockHashValid(self, block: Block):
        latestBlockainBlockHash = BeezUtils.hash(self.blocks[-1].payload()).hexdigest()
        if latestBlockainBlockHash == block.lastHash:
            return True
        else:
            return False
    

    def getCoveredTransactionSet(self, transactions: List[Transaction]) -> List[Transaction]:
        coveredTransactions: List[Transaction] = []
        for tx in transactions:
            if self.transactionCovered(tx):
                coveredTransactions.append(tx)
            else:
                logger.info(f"This transaction {tx.id} is not covered [no enogh tokes ({tx.amount}) into account {tx.receiverPublicKey}]")
        
        return coveredTransactions


    # check that there is enogh money into the account
    def transactionCovered(self, transaction: Transaction):
        """
        check if a transaction is covered (knowed) by the AccountStateModel

        if the transaction is coming from the Exchange we do not check if it covered
        """
        if transaction.type == TransactionType.EXCHANGE.name:
            return True

        senderBalance = self.accountStateModel.getBalance(transaction.senderPublicKey)

        if senderBalance >= transaction.amount:
            return True
        else:
            return False

    def executeTransactions(self, transactions: List[Transaction]):
        for transaction in transactions:
            self.executeTransaction(transaction)

    def executeTransaction(self, transaction: Transaction):
        if transaction.type == TransactionType.STAKE.name:
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            if sender == receiver:
                amount = transaction.amount
                self.pos.update(sender, amount)
                self.accountStateModel.updateBalance(sender, -amount)
        else:
            sender  = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            amount: int = transaction.amount
            # first update the sender balance
            self.accountStateModel.updateBalance(sender, -amount)
            # second update the receiver balance
            self.accountStateModel.updateBalance(receiver, amount)

    def nextForger(self):
        lastBlockHash = BeezUtils.hash(self.blocks[-1].payload()).hexdigest()
        nextForger = self.pos.forger(lastBlockHash)
    
        return nextForger

    def createBlock(self, transactionsFromPool: List[Transaction], forgerWallet: Wallet) -> Block:
        coveredTransactions = self.getCoveredTransactionSet(transactionsFromPool)
        self.executeTransactions(coveredTransactions)

        newBlock = forgerWallet.createBlock(coveredTransactions, BeezUtils.hash(self.blocks[-1].payload()).hexdigest(), len(self.blocks))

        self.blocks.append(newBlock)

        return newBlock        


    def transactionExist(self, transaction: Transaction):
        #TODO: Find a better solution to check if a transactio is alreay into the blockchain!
        for block in self.blocks:
            for blockTransaction in block.transactions:
                if transaction.equals(blockTransaction):
                    return True
        return False

    def forgerValid(self, block: Block):
        forgerPublicKey = str(self.pos.forger(block.lastHash)).strip()
        proposedBlockForger = str(block.forger).strip()

        if forgerPublicKey == proposedBlockForger:
            return True
        else:
            return False

    def transactionValid(self, transactions: List[Transaction]):
        coveredTransactions = self.getCoveredTransactionSet(transactions)
        # if the lenght are equal than nodes are not cheating
        if len(coveredTransactions) == len(transactions):
            return True
        else:
            return False
