#!/usr/bin/env python3

import json, sys, argparse, os, logging

from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

http_endpoints = {
      "ropsten": "https://ropsten.infura.io/v3/6b0739e915a04d5bbdac6711c72f1052",
      "rinkby": "https://rinkeby.infura.io/v3/6b0739e915a04d5bbdac6711c72f1052",
      "mainnet": "https://mainnet.infura.io/v3/6b0739e915a04d5bbdac6711c72f1052",
}

gwei_to_wei = 0.000000001

class EthereumTxn:
    def __init__(self, amount=None, from_addr=None, to_addr=None):
        self._amount = amount
        self._from_addr = from_addr
        self._to_addr = to_addr
    @property
    def amount(self):
        return self._amount
    @amount.setter
    def amount(self, amount):
        self._amount = amount
    @property
    def from_addr(self):
        return self._from_addr
    @from_addr.setter
    def from_addr(self, from_addr):
        self._from_addr = from_addr
    @property
    def to_addr(self):
        return self._to_addr
    @to_addr.setter
    def to_addr(self, to_addr):
        self._to_addr = to_addr
    def to_json(self):
        txn_json = {
                "from": f"{self._from_addr}",
                "to": f"{self._to_addr}",
                "value": f"{self._amount}",
              }
        return txn_json

def to_wei(gwei):
    return gwei/gwei_to_wei

def to_gwei(wei):
    return wei * gwei_to_wei

def initialize_web3(http_endpoint) -> Web3:
    w3 = Web3(Web3.HTTPProvider(http_endpoint))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # Check if we're connected
    if w3.isConnected():
      logger.info(f"Connected to {http_endpoint}")
    else:
      logger.critical(f"Failed to connect to {http_endpoint}!")
      sys.exit(1)

    return w3

def calculate_txn_fee(w3, txn):
    gas_estimate = w3.eth.estimate_gas(txn.to_json())
    gas_base_fee = w3.eth.get_block('latest').baseFeePerGas
    total_txn_fee = (gas_estimate * gas_base_fee) + to_wei(int(txn.amount))
    txn_cost = {
            "gas_fee": f"{to_gwei(gas_estimate * gas_base_fee)}",
            "total_cost": f"{to_gwei(total_txn_fee)}",
        }
    logger.info(f"{txn_cost}")

def main(logger):
    parser = argparse.ArgumentParser(description=f"{__file__} is used to perform rudimentary operations related to transaction execution on the ethereum blockchain")

    parser.add_argument('cmd', nargs='+', choices=['calculate'])
    parser.add_argument('--amount', help="Amount (in gwei) to transfer")
    parser.add_argument('--from_addr', help="Account to send funds from")
    parser.add_argument('--to_addr', help="Account to receive funds")
    parser.add_argument('--chain', dest='chain', default='ropsten')
    parser = parser.parse_args()

    chain = parser.chain

    match parser.cmd:
        case calculate:
            if parser.amount is None:
                logger.fatal("--amount is a required flag for the estimate command")
                sys.exit(1)
            if parser.from_addr is None:
                logger.fatal("--from_addr is a required flag for the estimate command")
                sys.exit(1)
            if parser.to_addr is None:
                logger.fatal("--to_addr is a required flag for the estimate command")
                sys.exit(1)

    txn = EthereumTxn(parser.amount, parser.from_addr, parser.to_addr)
    if chain not in http_endpoints.keys():
      logger.info(f"{chain} is not a valid chain")
      sys.exit(1)

    http_endpoint = http_endpoints[chain]
    logger.info(f"Using http endpoint {http_endpoint}")

    w3 = initialize_web3(http_endpoint)
    calculate_txn_fee(w3, txn)

if __name__ == '__main__':
    log_format = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(stream=sys.stdout, format=log_format)

    logger = logging.getLogger(__name__)
    logger.setLevel("INFO")
    if "BASE_FEE_CALCULATION_LOG_LEVEL" in os.environ:
        logger.setLevel(os.getenv("BASE_FEE_CALCULATION_LOG_LEVEL"))

    sys.exit(main(logger))
