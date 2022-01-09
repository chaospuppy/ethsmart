import yaml

class EthsmartConfig:
    def __init__(self, file):
        self.parse_config(file)
    def parse_config(self, file):
        with open(file ,"r") as f:
            config_yaml = yaml.safe_load(f)
        self._chains = config_yaml["chains"]
        self._preferences = config_yaml["preferences"]
        self._unit = config_yaml["preferences"]["unit"]
    @property
    def unit(self):
        return self._unit
    @unit.setter
    def unit(self, unit):
        self._unit = unit
    @property
    def chains(self):
        return self._chains
