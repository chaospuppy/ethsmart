from modules import eth_math

class EthereumTxn:
    def __init__(self, input):
        self._amount = input.amount
        self._from_addr = input.from_addr
        self._to_addr = input.to_addr
    @property
    def gas_price(self):
        return self._gas_price
    @gas_price.setter
    def gas_price(self, gas_price):
        self._gas_price = gas_price
    # make float
    @property
    def total_cost(self):
        return self._amount
    @total_cost.setter
    def total_cost(self, total_cost):
        self._total_cost = total_cost
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
    txn.gas_price = eth_math.convert("wei","gwei", gas_estimate * gas_base_fee)
    txn.total_cost = txn.gas_price + eth_math.convert("gwei", "gwei", float(txn.amount))
    logger.info(f"{txn.gas_price}")
    return txn.total_cost
