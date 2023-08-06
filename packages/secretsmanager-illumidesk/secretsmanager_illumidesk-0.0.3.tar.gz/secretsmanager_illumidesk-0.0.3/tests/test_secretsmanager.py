from secretsmanager.secretsmanager import SecretsManager

# import pytest
# import sys


# def test_output(awssecrets_connection):
#     assert awssecrets_connection.region_name == 'us-west-2'
#     assert awssecrets_connection.db_secret.__contains__('host')
#     assert awssecrets_connection.db_secret.__contains__('username')
#     assert awssecrets_connection.db_secret.__contains__('password')
#     assert awssecrets_connection.db_secret.__contains__('port')
#     assert awssecrets_connection.db_secret.__contains__('dbname')

class AWSSecretsHandler:
    def __init__(self):
        self.aws_secrets_session.Session()
        self.aws_s3_client = self.aws_secrets_session.client("secretsmanager")
    
    