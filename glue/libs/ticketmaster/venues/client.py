"""Client for making venues request, including paginated requests

TODO: Get all venues is hitting an error after 10 pages for some reason
"""

import requests
from .models import Venue, NextPage
from typing import List, Tuple


class VenueRequestError(Exception):
    """Raised when venue request fails"""

    def __init__(self, status_code: str, reason: str) -> None:
        self.status_code = status_code
        self.reason = reason

    def __str__(self) -> str:
        return f"Request failed with status code: {self.status_code}, and reason: {self.reason}"


class VenueRequests:
    def __init__(self, api_key: str) -> None:
        self.params = {"apikey": api_key}
        self.base_url = "https://app.ticketmaster.com"
        self.path = "discovery/v2/venues.json"

    def get_venue(self, id: str) -> Venue:
        """Gets venue details
        Args:
            id - the venue ID
        """
        url = f"{self.url}/{id}"

        response = requests.get(url=url, params=self.params)

        return response.json()

    def _parse_venue_response(self, response: requests.Response) -> List[Venue]:
        """Parses a venue response into a list of Venue models
        Args:
            response - a response from a venues request. Expects keys "_embedded" with key "venues"
        """
        data = response.json()
        venues = data["_embedded"]["venues"]

        venue_model = [Venue(**v) for v in venues]
        return venue_model

    def get_venue_page(self, url: str, params: dict) -> Tuple[List[Venue], NextPage]:
        """Parses a venue response page
        Args:
            url - the url to get
            params - a dictionary of request parameters

        Returns:
            a Tuple of a list of the Venues and the next page in the request
            If there isn't a next page, the second value will be None
        """
        response = requests.get(url=url, params=params)

        try:
            next_page_url = response.json()["_links"]["next"]["href"]
            next_page_base_url, next_page_params = next_page_url.split("?")
            next_page_page = next_page_params.split("&")[0].split("=")[1]
            next_page_size = next_page_params.split("&")[1].split("=")[1]
            next_page = NextPage(
                url=next_page_base_url, page=next_page_page, size=next_page_size
            )
        except:
            next_page = None

        if response.status_code == 200:
            venues = self._parse_venue_response(response)
            return (venues, next_page)

        else:
            raise (VenueRequestError(response.status_code, response.reason))

    def get_all_venues(
        self, keyword: str = None, size: int = "200"
    ) -> Tuple[List[Venue], NextPage]:
        """Get all venues
        The venues request is paginated, so this iterates through the request until all venues are returned

        TODO: this is currently erroring after a certain number of pages for unknown reasons
        Args:
            keyword - optional search keyword to filter results
            size - number of venues per page
        Returns:
            a list of Venue objects from the response and a NextPage object
        """
        url = f"{self.base_url}/{self.path}"
        params = self.params

        params["size"] = size
        if keyword is not None:
            params["keyword"] = keyword
        venues, next_page = self.get_venue_page(url, params)

        while next_page is not None:
            try:
                url = f"{self.base_url}/{next_page.url}"
                params = self.params
                params["size"] = next_page.size
                params["page"] = next_page.page
                more_venues, next_page = self.get_venue_page(url, params=params)
                venues += more_venues
            except VenueRequestError as e:
                print(f"Raised error for next page: {next_page}")
                print(e)
                break

        return venues, next_page
