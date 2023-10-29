from pydantic import BaseModel, Field
from typing import List
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
    address: Address
    location: Location
    markets: List[Market]
    _links: _Links
