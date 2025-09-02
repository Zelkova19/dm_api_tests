from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class UserRole(str, Enum):
    GUEST = 'Guest'
    PLAYER = 'Player'
    ADMINISTRATOR = 'Administrator'
    NANNY_MODERATOR = 'NannyModerator'
    REGULAR_MODERATOR = 'RegularModerator'
    SENIOR_MODERATOR = 'SeniorModerator'


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class User(BaseModel):
    login: str
    roles: List[UserRole]
    medium_picture_url: str = Field(None, alias='mediumPictureUrl')
    small_picture_url: str = Field(None, alias='smallPictureUrl')
    status: str = Field(None, alias='status')
    rating: Rating
    online: datetime = Field(None, alias='online')
    name: str = Field(None, alias='name')
    location: str = Field(None, alias='location')
    registration: datetime = Field(None, alias='registration')


class UserEnvelop(BaseModel):
    model_config = ConfigDict(extra='forbid')
    resource: Optional[User] = None
    metadata: Optional[dict] = None
