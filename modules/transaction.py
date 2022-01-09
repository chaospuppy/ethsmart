from modules import eth_math

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

def calculate_txn_fee(w3, txn, logger):
    gas_estimate = w3.eth.estimate_gas(txn.to_json())
    gas_base_fee = w3.eth.get_block('latest').baseFeePerGas
    gas_fee = eth_math.convert("wei","gwei", gas_estimate * gas_base_fee)
    total_txn_fee = gas_fee + eth_math.convert("gwei", "gwei", float(txn.amount))
    txn_cost = {
            "gas_fee": f"{gas_fee}",
            "total_cost": f"{total_txn_fee}",
        }
    logger.info(f"{txn_cost}")

