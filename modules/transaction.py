from modules import eth_math

class EthereumTxn:
    def __init__(self, **kwargs):
        if "amount" in kwargs.keys():
          self._amount = float(kwargs["amount"])
        if "from_addr" in kwargs.keys():
          self._from_addr = kwargs["from_addr"]
        if "to_addr" in kwargs.keys():
          self._to_addr = kwargs["to_addr"]
        if "unit" in kwargs.keys():
          self._unit = kwargs["unit"]
        if "max_priority_fee" in kwargs.keys():
          self._max_priority_fee = kwargs["max_priority_fee"]
        if "max_fee" in kwargs.keys():
          self._max_fee = kwargs["max_fee"]
    @property
    def gas_price(self):
        return self._gas_price
    @gas_price.setter
    def gas_price(self, gas_price):
        self._gas_price = gas_price
    @property
    def total_cost(self):
        return float(self._total_cost)
    @total_cost.setter
    def total_cost(self, total_cost):
        self._total_cost = float(total_cost)
    @property
    def amount(self):
        return float(self._amount)
    @amount.setter
    def amount(self, amount):
        self._amount = float(amount)
    @property
    def from_addr(self):
        return self._from_addr
    @from_addr.setter
    def from_addr(self, from_addr):
        self._from_addr = from_addr
    @property
    def unit(self):
        return self._unit
    @property
    def to_addr(self):
        return self._to_addr
    @to_addr.setter
    def to_addr(self, to_addr):
        self._to_addr = to_addr
    @property
    def max_priority_fee(self):
        return self._max_priority_fee
    @max_priority_fee.setter
    def max_priority_fee(self, max_priority_fee):
        self._max_priority_fee = max_priority_fee
    @property
    def gas_estimate(self):
        return self._gas_estimate
    @gas_estimate.setter
    def gas_estimate(self, gas_estimate):
        self._gas_estimate = gas_estimate
    def to_json(self, max_fee_per_gas=None, max_priority_fee_per_gas=None):
        txn_json = {
                "from": f"{self._from_addr}",
                "to": f"{self._to_addr}",
                "value": f"{self._amount}",
                "maxFeePerGas": f"{max_fee_per_gas}",
                "maxPriorityFeePerGas": f"{max_priority_fee_per_gas}"
              }
        return txn_json

def calculate_txn_fee(w3, txn, logger):
    txn.gas_estimate = w3.eth.estimate_gas(txn.to_json())
    gas_base_fee = w3.eth.get_block('latest').baseFeePerGas

    txn.gas_price = float(eth_math.convert("wei", txn.unit, txn.gas_estimate * gas_base_fee))
    txn.priority_fee = float(eth_math.convert("wei", txn.unit, txn.gas_estimate * txn.priority_fee_per_gas))
    txn.total_cost = txn.gas_price + txn.amount + txn.priority_fee

    logger.info(f"This transaction has a gas price of {txn.gas_price} {txn.units}, for a total cost of {txn.total_cost} {txn.units}")

    return txn.total_cost

def send(w3, txn, logger):
    executed = False
    while not executed:
        txn_fee = calculate_txn_fee(w3, txn, logger)
        max_fee_per_gas = txn.max_fee/txn.gas_estimate
        max_priority_fee_per_gas = txn.max_priority_fee/txn.gas_estimate
        if txn_fee < txn.max_fee:
            w3.eth.send_transaction(txn.to_json(max_fee_per_gas, max_priority_fee_per_gas))
            executed = True
