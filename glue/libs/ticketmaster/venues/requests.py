import requests
from libs.ticketmaster.venues.models import Venue
from typing import List


class VenueRequests:
    def __init__(self, api_key: str) -> None:
        self.params = {"apikey": api_key}
        self.url = "/discovery/v2/venues"

    def get_venue(self, id: str) -> Venue:
        """Gets venue details
        Args:
            id - the venue ID
        """
        url = f"{self.url}/{id}"

        response = requests.get(url=url, params=self.params)

        return response.json()

    def get_all_venues(self) -> List[Venue]:
        """Get all venues"""
        response = requests.get(url=self.url, params=self.params)


if __name__ == "__main__":
    venue_client = VenueRequests(api_key="fake")
