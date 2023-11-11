from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field
from libs.ticketmaster.venues.models import Venue
from libs.models.common import Self, _Links


class Image(BaseModel):
    ratio: Optional[str] = None
    url: str
    width: int
    height: int
    fallback: bool


class Public(BaseModel):
    start_date_time: Optional[str] = Field(None, alias="startDateTime")
    start_tbd: bool = Field(..., alias="startTBD")
    end_date_time: Optional[str] = Field(None, alias="endDateTime")


class Sales(BaseModel):
    public: Public


class Start(BaseModel):
    local_date: str = Field(..., alias="localDate")
    date_tbd: bool = Field(..., alias="dateTBD")
    date_tba: bool = Field(..., alias="dateTBA")
    time_tba: bool = Field(..., alias="timeTBA")
    no_specific_time: bool = Field(..., alias="noSpecificTime")


class Status(BaseModel):
    code: str


class Dates(BaseModel):
    start: Start
    timezone: Optional[str] = None
    status: Status


class Segment(BaseModel):
    id: str
    name: str


class Genre(BaseModel):
    id: str
    name: str


class SubGenre(BaseModel):
    id: str
    name: str


class Classification(BaseModel):
    primary: bool
    segment: Segment
    genre: Genre
    sub_genre: Optional[SubGenre] = Field(None, alias="subGenre")


class Promoter(BaseModel):
    id: str


class Attraction(BaseModel):
    href: str


class Venue(BaseModel):
    href: str


class _Links(BaseModel):
    self: Self
    attractions: List[Attraction]
    venues: List[Venue]


class Market(BaseModel):
    id: str


class Attraction1(BaseModel):
    name: str
    type: str
    id: str
    test: bool
    locale: str
    images: List[Image]
    classifications: List[Classification]
    _links: _Links


class _Embedded(BaseModel):
    venues: List[Venue]
    attractions: List[Attraction1]


class Event(BaseModel):
    name: str
    type: str
    id: str
    test: bool
    url: str
    locale: str
    images: List[Image]
    sales: Sales
    dates: Dates
    classifications: List[Classification]
    promoter: Optional[Promoter] = None
    _links: _Links
    _embedded: _Embedded
