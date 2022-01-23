#!/usr/bin/env python3
import json, sys, argparse, os, logging, pathlib

from modules import transaction
from modules import config
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

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
    parser.add_argument('--chain')
    parser.add_argument('--unit', default='gwei')
    parser.add_argument('--config', default=pathlib.Path(os.getenv('HOME')).joinpath('.ethsmart/ethsmart.yaml'))
    args = parser.parse_args()

    ethsmart_config = config.EthsmartConfig(args)

    logger.info(f"Using http endpoint {ethsmart_config.endpoint}")
    w3 = initialize_web3(ethsmart_config.endpoint)

    txn = transaction.EthereumTxn(args)

    match args.cmd:
        case "calculate":
          transaction.calculate_txn_fee(w3, txn, logger)

if __name__ == '__main__':
    log_format = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(stream=sys.stdout, format=log_format)

    logger = logging.getLogger(__name__)
    logger.setLevel("INFO")
    if "BASE_FEE_CALCULATION_LOG_LEVEL" in os.environ:
        logger.setLevel(os.getenv("ETHSMART_LOG_LEVEL"))

    sys.exit(main(logger))
