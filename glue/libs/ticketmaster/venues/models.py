from pydantic import BaseModel, Field
from typing import List, Optional
from libs.models.common import City, State, Country, Address, Location, Market, _Links


class Venue(BaseModel):
    name: str
    type: str
    id: str
    test: bool
    locale: str
    postal_code: str = Field(..., alias="postalCode")
    timezone: str
    city: City
    state: State
    country: Country
    address: Optional[Address] = None
    location: Optional[Location] = None
    markets: Optional[List[Market]] = None
    _links: _Links


class NextPage(BaseModel):
    """Attributes for next page in paginated response"""

    url: str
    page: int
    size: int
