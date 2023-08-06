from impira.tools.impira import Impira as LibImpira
from .tool import Tool


class Impira(Tool, LibImpira):
    def __init__(self, config):
        LibImpira.__init__(self, config)
        self.config = config
