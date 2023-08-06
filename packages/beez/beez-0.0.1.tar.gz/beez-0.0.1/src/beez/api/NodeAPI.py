from __future__ import annotations
from crypt import methods
from urllib import response
from flask_classful import FlaskView, route
from flask import Flask, jsonify, request
from waitress import serve
from loguru import logger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from beez.node.Node import Node
    from beez.Types import Address
    from beez.transaction.Transaction import Transaction

from beez.BeezUtils import BeezUtils

import os
from dotenv import load_dotenv

load_dotenv() # load .env

NODE_API_PORT = os.environ.get("NODE_API_PORT", default=8176)

node = None

class NodeAPI(FlaskView):

    def __init__(self):
        self.app = Flask(__name__) # create the application


    def start(self, nodeIP: Address):
        logger.info(f"Node API started at {nodeIP}:{NODE_API_PORT}")
        NodeAPI.register(self.app, route_base="/") # register the application to routes
        serve(self.app, host=nodeIP, port=NODE_API_PORT)
        # self.app.run(host=nodeIP, port=NODE_API_PORT)

    # find a way to use the properties of the node in the nodeAPI
    def injectNode(self, incjectedNode: Node):
        global node 
        node = incjectedNode
        
    @route("/info", methods=['GET'])
    def info(self):
        logger.info(f"Provide some info about the Blockchain")
        return "This is a communication interface to node request.", 200

    @route("/blockchain", methods=['GET'])
    def blockchain(self):
        #TODO: Implement this
        logger.info(f"Blockchain called...")
        return node.blockchain.toJson(), 200

    @route("/transactionpool", methods=['GET'])
    def transactionPool(self):
        # Implement this
        logger.info(f"Send all the transactions that are on the transaction pool")
        transactions = {}

        logger.info(f"Transactions: {node.transactionPool.transactions}")

        for idx, tx in enumerate(node.transactionPool.transactions):
            logger.info(f"Transaction: {idx} : {tx.id}")
            transactions[idx] = tx.toJson()
           

        logger.info(f"Transactions to Json: {transactions}")

        return jsonify(transactions), 200

    
    @route("/transaction", methods=['POST'])
    def transaction(self):
        values = request.get_json() # we aspect that the sender use json!

        if not 'transaction' in values:
            return 'Missing transaction value', 400

        transaction: Transaction = BeezUtils.decode(values['transaction'])

        logger.info(f"Transaction to be done: {transaction.id}")

        # handle trasaction
        node.handleTransaction(transaction)

        response = {'message': 'Received transaction'}

        return jsonify(response), 201