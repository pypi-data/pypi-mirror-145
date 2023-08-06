# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2021
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------


from .hive_writer import HiveWriter
from .jdbc_writer import JdbcWriter

def get_writer(credentials):
    """
    Returns a writer object based on the credentials provided.
    """
    if credentials["type"] == "jdbc":
        return JdbcWriter(credentials)
    elif credentials["type"] == "hive":
        return HiveWriter(credentials)
    else:
        raise ValueError("Unknown writer type: {}".format(credentials["type"]))