import sys
import os

# Hacky way to add root directory to Python path during local execution
ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    )
)
sys.path.append(ROOT_DIR)

from libs.ticketmaster.events.client import EventRequests
from libs.aws_utils.secrets import get_secret_value
from libs.utils import write_list_model_newline_json


SECRET_ID = "ticketmaster-api-key-demo"

if __name__ == "__main__":
    creds = get_secret_value(SECRET_ID)

    event_client = EventRequests(api_key=creds["consumer_key"])

    events, next_page_url = event_client.get_all_events()

    print(len(events))
    print(events[0].model_dump())
    print(next_page_url)

    write_list_model_newline_json(
        file_path=f"{ROOT_DIR}/../data/events.json", model_list=events
    )
