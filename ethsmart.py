#!/usr/bin/env python3

import json, sys, argparse, os, logging

from modules import transaction
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

http_endpoints = {
      "ropsten": "https://ropsten.infura.io/v3/6b0739e915a04d5bbdac6711c72f1052",
      "rinkby": "https://rinkeby.infura.io/v3/6b0739e915a04d5bbdac6711c72f1052",
      "mainnet": "https://mainnet.infura.io/v3/6b0739e915a04d5bbdac6711c72f1052",
}

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

def main(logger):
    parser = argparse.ArgumentParser(description=f"{__file__} is used to perform rudimentary operations related to transaction execution on the ethereum blockchain")

    parser.add_argument('cmd', choices=['calculate'])
    parser.add_argument('--amount', help="Amount (in gwei) to transfer")
    parser.add_argument('--from_addr', help="Account to send funds from")
    parser.add_argument('--to_addr', help="Account to receive funds")
    parser.add_argument('--chain', default='ropsten')
    parser.add_argument('--units', default='gwei')
    parser = parser.parse_args()

    chain = parser.chain

    http_endpoint = http_endpoints[chain]
    logger.info(f"Using http endpoint {http_endpoint}")
    w3 = initialize_web3(http_endpoint)

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

    txn = transaction.EthereumTxn(parser.amount, parser.from_addr, parser.to_addr)
    if chain not in http_endpoints.keys():
      logger.info(f"{chain} is not a valid chain")
      sys.exit(1)

    transaction.calculate_txn_fee(w3, txn, logger)

if __name__ == '__main__':
    log_format = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(stream=sys.stdout, format=log_format)

    logger = logging.getLogger(__name__)
    logger.setLevel("INFO")
    if "BASE_FEE_CALCULATION_LOG_LEVEL" in os.environ:
        logger.setLevel(os.getenv("BASE_FEE_CALCULATION_LOG_LEVEL"))

    sys.exit(main(logger))
