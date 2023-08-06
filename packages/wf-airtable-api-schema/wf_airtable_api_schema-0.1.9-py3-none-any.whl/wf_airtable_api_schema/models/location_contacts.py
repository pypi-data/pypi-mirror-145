from typing import Optional, Union

from pydantic import BaseModel

from . import response as response_models

MODEL_TYPE = 'location_contacts'


class APILocationContactFields(BaseModel):
    location: Optional[str] = None
    location_type: Optional[str] = None
    city_radius: Optional[int] = 20
    first_contact_email: Optional[str] = None
    assigned_rse_name: Optional[str] = None
    hub_name: Optional[str] = None
    sendgrid_template_id = Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class APILocationContactRelationships(BaseModel):
    hub: Optional[response_models.APILinksAndData] = None
    assigned_rse: Optional[response_models.APILinksAndData] = None


class APILocationContactData(response_models.APIData):
    fields: APILocationContactFields


class ListAPILocationContactData(BaseModel):
    __root__: list[APILocationContactData]


class APILocationContactResponse(response_models.APIResponse):
    data: APILocationContactData


class ListAPILocationContactResponse(response_models.ListAPIResponse):
    data: list[Union[APILocationContactData, dict]]

