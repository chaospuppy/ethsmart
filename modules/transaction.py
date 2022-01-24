from modules import eth_math

class EthereumTxn:
    def __init__(self, **kwargs):
        if "amount" in kwargs.keys():
          self._amount = kwargs["amount"]
        if "from_addr" in kwargs.keys():
          self._from_addr = kwargs["from_addr"]
        if "to_addr" in kwargs.keys():
          self._to_addr = kwargs["to_addr"]
        if "unit" in kwargs.keys():
          self._unit = kwargs["unit"]
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
    def unit(self):
        return self._unit
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

    txn.gas_price = eth_math.convert("wei", txn.unit, gas_estimate * gas_base_fee)
    txn.total_cost = txn.gas_price + eth_math.convert("gwei", "gwei", float(txn.amount))
    logger.info(f"This transaction has a gas price of {txn.gas_price}, for a total cost of {float(txn.total_cost)}")
    return txn.total_cost
