import yaml, os, sys, logging

log_format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(stream=sys.stdout, format=log_format)

class EthsmartConfig:
    def __init__(self, input):
        # Check if config file exists
        if os.path.exists(input.config):
          config_data = self.parse_config(input.config)

          for chain in config_data["chains"].keys():
              if "default" in config_data["chains"][chain]:
                  if config_data["chains"][chain]["default"]:
                      self._chain = chain
                      break
        # Allow user override of chain
        if input.chain:
            self._chain = input.chain

        if not hasattr(self, "_chain"):
            logging.fatal("chain must be specified with --chain or in ethsmart.yaml")
            sys.exit(1)

        self._endpoint = config_data["chains"][self._chain]["endpoint"]
        self._unit = config_data["preferences"]["unit"]
        # Allow user input of unit
        if input.unit:
            self._unit = input.unit
    def parse_config(self, file):
        with open(file ,"r") as f:
            return yaml.safe_load(f)
    @property
    def chain(self):
        return self._chain
    @chain.setter
    def chain(self, chain):
        self._chain = chain
    @property
    def unit(self):
        return self._unit
    @unit.setter
    def unit(self, unit):
        self._unit = unit
    @property
    def endpoint(self):
        return self._endpoint
    @endpoint.setter
    def endpoint(self, endpoint):
        self._endpoint = endpoint
