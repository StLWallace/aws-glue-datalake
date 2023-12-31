import sys
import os

# Hacky way to add root directory to Python path during local execution
ROOT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)
sys.path.append(ROOT_DIR)

from libs.aws_utils.secrets import get_secret_value


SECRET_ID = "ticketmaster-api-key-demo"

if __name__ == "__main__":
    """Validate secret output format"""
    secret = get_secret_value(SECRET_ID)
    assert "consumer_secret" in secret
    print(secret)
