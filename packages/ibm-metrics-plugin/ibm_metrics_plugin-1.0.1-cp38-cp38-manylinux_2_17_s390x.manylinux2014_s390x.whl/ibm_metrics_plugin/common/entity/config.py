# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

class DataSource():

    def __init__(self, data_source, jdbc_conn_props=None):
        self.type = data_source.get("type")
        self.connection = data_source.get("connection") or {}
        self.location_type = self.connection.get("location_type")
        self.credentials = data_source.get("credentials")
        self.jdbc_conn_props = jdbc_conn_props


class DataTable():

    def __init__(self, tables, table_type):
        table = next((t for t in tables if t.get("type") == table_type), {})
        self.db = table.get("database")
        self.schema = table.get("schema")
        self.table = table.get("table")
        parameters = table.get("parameters", {})
        self.partition_column = parameters.get("partition_column")
        self.num_partitions = parameters.get("num_partitions")
        self.lower_bound = parameters.get("lower_bound")
        self.upper_bound = parameters.get("upper_bound")
