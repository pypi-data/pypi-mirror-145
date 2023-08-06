# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------
from abc import abstractmethod

from ibm_metrics_plugin.metrics.explainability.entity.explain_config import ExplainConfig


class BaseExplainer():

    def __init__(self, explain_config: ExplainConfig):
        self.config = explain_config

    @abstractmethod
    def is_supported(self):
        pass

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def explain_data(self, data, **kwargs):
        pass

    @abstractmethod
    def get_data_to_accumulate(self, response):
        pass

    def explain(self, data, **kwargs):
        self.initialize()
        return self.explain_data(data=data, **kwargs)
