import sys
import os

# Hacky way to add root directory to Python path during local execution
ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    )
)
sys.path.append(ROOT_DIR)

from libs.ticketmaster.venues.client import VenueRequests
from libs.aws_utils.secrets import get_secret_value
from libs.utils import write_list_model_newline_json


SECRET_ID = "ticketmaster-api-key-demo"

if __name__ == "__main__":
    creds = get_secret_value(SECRET_ID)

    venue_client = VenueRequests(api_key=creds["consumer_key"])

    venues, next_page_url = venue_client.get_all_venues()

    print(len(venues))
    print(venues[0].model_dump())
    print(next_page_url)

    write_list_model_newline_json(
        file_path=f"{ROOT_DIR}/../data/venues.json", model_list=venues
    )
