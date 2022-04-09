from AgentBasedModel.exchange import ExchangeAgent


class Simulator:
    """
    Simulator is responsible for launching agents' actions and executing scenarios
    """
    def __init__(self, exchange: ExchangeAgent = None, traders: list = None):
        self.exchange = exchange
        self.traders = traders

    def simulate(self, n_iter):

