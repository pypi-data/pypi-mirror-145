
import pytest
from secretsmanager.secretsmanager import SecretsManager

@pytest.fixture(scope="class")
def awssecrets_connection():
    return SecretsManager("arn:aws:secretsmanager:us-west-2:860100747351:secret:RDSConfig-JMVgcU")