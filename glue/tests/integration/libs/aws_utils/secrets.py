import sys
import os

ROOT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)
sys.path.append(ROOT_DIR)

from libs.aws_utils.secrets import get_secret_value


SECRET_ID = "ticketmaster-api-key-demo"

if __name__ == "__main__":

    secret = get_secret_value(SECRET_ID)
    print(secret)
