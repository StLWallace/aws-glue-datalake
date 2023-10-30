from libs.ticketmaster.events.models import Event
from libs.models.common import NextPage
import requests
from typing import List, Tuple


class EventRequestError(Exception):
    """Raised when event request fails"""

    def __init__(self, status_code: str, reason: str) -> None:
        self.status_code = status_code
        self.reason = reason

    def __str__(self) -> str:
        return f"Request failed with status code: {self.status_code}, and reason: {self.reason}"


class EventRequests:
    """Class to provide wrapper for event requests"""

    def __init__(self, api_key: str) -> None:
        self.params = {"apikey": api_key}
        self.base_url = "https://app.ticketmaster.com"
        self.path = "discovery/v2/events.json"

    def _parse_event_response(self, response: requests.Response) -> List[Event]:
        """Parses a event response into a list of Event models
        Args:
            response - a response from a events request. Expects keys "_embedded" with key "events"
        """
        data = response.json()
        events = data["_embedded"]["events"]

        event_model = [Event(**e) for e in events]
        return event_model

    def get_event_page(self, url: str, params: dict) -> Tuple[List[Event], NextPage]:
        """Parses an event response page
        Args:
            url - the url to get
            params - a dictionary of request parameters

        Returns:
            a Tuple of a list of the Events and the next page in the request
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
            events = self._parse_event_response(response)
            return (events, next_page)

        else:
            raise (EventRequestError(response.status_code, response.reason))

    def get_all_events(
        self, keyword: str = None, size: int = "200"
    ) -> Tuple[List[Event], NextPage]:
        """Get all events
        The events request is paginated, so this iterates through the request until all events are returned

        TODO: this is currently erroring after a certain number of pages for unknown reasons
        Args:
            keyword - optional search keyword to filter results
            size - number of events per page
        Returns:
            a list of event objects from the response and a NextPage object
        """
        url = f"{self.base_url}/{self.path}"
        params = self.params

        params["size"] = size
        if keyword is not None:
            params["keyword"] = keyword
        events, next_page = self.get_event_page(url, params)

        while next_page is not None:
            try:
                url = f"{self.base_url}/{next_page.url}"
                params = self.params
                params["size"] = next_page.size
                params["page"] = next_page.page
                more_events, next_page = self.get_event_page(url, params=params)
                events += more_events
            except EventRequestError as e:
                print(f"Raised error for next page: {next_page}")
                print(e)
                break

        return events, next_page
