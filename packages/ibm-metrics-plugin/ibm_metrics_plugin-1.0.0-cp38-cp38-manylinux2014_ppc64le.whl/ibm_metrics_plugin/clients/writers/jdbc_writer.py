# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2021
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

class JdbcWriter:

    def __init__(self, credentials) -> None:
        self.credentials = credentials

    def write(self, data) -> None:
        print(data)
        # TODO: Implement JDBC writer