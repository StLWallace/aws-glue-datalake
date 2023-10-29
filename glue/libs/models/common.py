from pydantic import BaseModel, Field


class City(BaseModel):
    name: str


class State(BaseModel):
    name: str
    state_code: str = Field(..., alias="stateCode")


class Country(BaseModel):
    name: str
    country_code: str = Field(..., alias="countryCode")


class Address(BaseModel):
    line1: str


class Location(BaseModel):
    longitude: str
    latitude: str


class Market(BaseModel):
    id: str


class Self(BaseModel):
    href: str


class _Links(BaseModel):
    self: Self
