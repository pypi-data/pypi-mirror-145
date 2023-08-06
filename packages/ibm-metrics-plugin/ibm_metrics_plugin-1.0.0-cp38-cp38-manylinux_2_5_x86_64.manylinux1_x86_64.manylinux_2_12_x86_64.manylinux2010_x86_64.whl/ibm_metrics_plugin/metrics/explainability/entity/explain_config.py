# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------
import numpy as np

from ibm_metrics_plugin.common.utils.constants import InputDataType, ProblemType, ExplainabilityMetricType


class ExplainConfig():
    """Explainability configuration containing the parameters required to generate explanation."""

    def __init__(self, input_data_type, problem_type, features, categorical_features=[], text_features=[], meta_fields=[], metric_types=[], prediction_column=None, probability_column=None, training_stats=None, training_data=None, features_schema={}, parameters={}, label_column=None, record_id_column=None):
        """
        Arguments:
            input_data_type: 
                The type of input data. Possible values are "structured", "unstructured_text", "unstructured_image".
            problem_type: 
                The problem type. Possible values are "binary", "multiclass", "regression".
            features: 
                The list of features.
            categorical_features: 
                The list of categorical features.
            text_features: 
                The list of text features.
            meta_fields:
                The list of meta fields which needs to be sent while scoring.
            metrics:
                The list of metrics to compute.
            prediction_column:
                The prediction column name
            probability_column:
                The probability column name
            training_stats: 
                A dictionary having the details of training data statistics.
            training_data: 
                Training data pandas dataframe
            features_schema: 
                The datatypes of all the features as key value pairs
            parameters: 
                The configuration parameters specific to each explainer
            label_column:
                The label column name in training data
            record_id_column:
                The record id column name in the input data
        """
        self.input_data_type = input_data_type
        self.problem_type = problem_type
        self.features = features
        self.categorical_features = categorical_features
        self.text_features = text_features
        self.meta_fields = meta_fields
        cat_text = categorical_features + text_features
        self.numeric_features = [
            f for f in features if f not in cat_text]
        self.metric_types = metric_types
        self.prediction_column = prediction_column
        self.probability_column = probability_column
        self.training_stats = training_stats
        self.training_data = training_data
        self.features_schema = features_schema
        self.parameters = parameters
        self.features_indexes = {k: v for v,
                                 k in enumerate(self.features)}
        self.label_column = label_column
        self.record_id_column = record_id_column

    @property
    def input_data_type(self):
        return self._input_data_type

    @input_data_type.setter
    def input_data_type(self, input_data_type):
        supported_types = [i.value for i in InputDataType]
        if input_data_type not in supported_types:
            raise ValueError("The input data type {0} is invalid. Valid types are {1}".format(
                input_data_type, supported_types))
        self._input_data_type = InputDataType(input_data_type)

    @property
    def problem_type(self):
        return self._problem_type

    @problem_type.setter
    def problem_type(self, problem_type):
        supported_types = [p.value for p in ProblemType]
        if problem_type not in supported_types:
            raise ValueError("The problem type {0} is invalid. Valid types are {1}".format(
                problem_type, supported_types))
        self._problem_type = ProblemType(problem_type)

    @property
    def metric_types(self):
        return self._metric_types

    @metric_types.setter
    def metric_types(self, metric_types):
        supported_types = [e.value for e in ExplainabilityMetricType]
        if not all(t in supported_types for t in metric_types):
            raise ValueError("The metric types {0} are invalid. Valid types are {1}".format(
                metric_types, supported_types))

        self._metric_types = [
            ExplainabilityMetricType(e) for e in metric_types]

    @property
    def training_stats(self):
        return self._training_stats

    @training_stats.setter
    def training_stats(self, training_stats):
        if self.input_data_type is InputDataType.STRUCTURED:
            self._training_stats = training_stats
        else:
            self._training_stats = None

    def get_stats(self, attributes):
        """Convert the required attributes in statistics dict from string to int and return"""
        updated_stats = {}

        # Convert string keys to int
        for k in attributes:
            v = self.training_stats.get(k)
            if isinstance(v, list):
                new_value = v
            else:
                new_value = {}
                for k_in_v in v:
                    new_value[int(k_in_v)] = v[k_in_v]

            updated_stats[k] = new_value

        return updated_stats

    @staticmethod
    def load(config):
        conf = config.get("configuration")
        explainability = conf.get("explainability") or {}
        parameters = explainability.get("metrics_configuration")

        # Validate before loading
        ExplainConfig.validate(conf)

        return ExplainConfig(input_data_type=conf.get("input_data_type"),
                             problem_type=conf.get("problem_type"),
                             features=conf.get("feature_columns"), categorical_features=conf.get("categorical_columns") or [],
                             training_stats=explainability.get(
                                 "training_statistics"),
                             metric_types=list(parameters.keys()),
                             label_column=conf.get("label_column"),
                             prediction_column=conf.get("prediction"),
                             probability_column=conf.get("probability"),
                             record_id_column=conf.get("record_id"),
                             parameters=parameters)

    @staticmethod
    def validate(config):
        # Adding only following as these are mandatory in init
        missing_values = []
        if(config.get("input_data_type") is None):
            missing_values.append("label_column")

        if(config.get("problem_type") is None):
            missing_values.append("prediction_column")

        feature_columns = config.get("feature_columns") or []
        if(len(feature_columns) == 0):
            missing_values.append("feature_columns")

        if(len(missing_values) > 0):
            raise AttributeError(
                "Missing inputs .Details :{}".format(missing_values))


class TrainingStats():
    def __init__(self, training_stats, feature_columns, categorical_columns):
        self.training_stats = training_stats or {}
        self.feature_columns = feature_columns
        self.categorical_columns = categorical_columns
        self.__validate_stats(training_stats)
        training_stats = self.__convert_stats(training_stats)

        self.class_labels = training_stats.get("class_labels")
        self.base_values = training_stats.get("base_values")
        self.stds = training_stats.get("stds")
        self.mins = training_stats.get("mins")
        self.maxs = training_stats.get("maxs")
        self.categorical_counts = training_stats.get("categorical_counts")

        self.cat_col_indexes = [feature_columns.index(
            c) for c in categorical_columns]
        self.cat_cols_encoding_map = training_stats.get(
            "categorical_columns_encoding_mapping")

    def get_cem_stats(self):
        """Get the statistics needed for contrastive explanation"""
        cem_stats = {}

        base_values_list, sd_list, min_list, max_list = (
            [] for i in range(4))

        for i in range(len(self.base_values)):
            base_values_list.append(self.base_values.get(i))
            sd_list.append(self.stds.get(i) if self.stds.get(i) else 0)
            min_list.append(self.mins.get(i) if self.mins.get(i) else 0)
            max_list.append(self.maxs.get(i) if self.maxs.get(i) else 1)

        cem_stats["base_values"] = np.asarray(
            base_values_list, dtype=object)
        cem_stats["stds"] = np.asarray(sd_list, dtype=float)
        cem_stats["mins"] = np.asarray(
            [min_list], dtype=float)
        cem_stats["maxs"] = np.asarray(
            [max_list], dtype=float)

        if self.categorical_counts:
            cem_stats["categorical_counts"] = self.categorical_counts
        else:
            cem_stats["categorical_counts"] = {}

        return cem_stats
