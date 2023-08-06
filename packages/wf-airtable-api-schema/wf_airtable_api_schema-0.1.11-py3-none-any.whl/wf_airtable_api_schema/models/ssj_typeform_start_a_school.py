from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from . import response as response_models

MODEL_TYPE = 'ssj_typeform_start_a_school'


class CreateApiSSJTypeformStartASchoolFields(BaseModel):
    first_name: str = None
    last_name: str = None
    email: str = None
    is_montessori_certified: bool = False
    montessori_certification_year: Optional[int] = None
    montessori_certification_levels: Optional[list[str]] = []
    school_location_city: str = None
    school_location_state: str = None
    school_location_country: str = None
    school_location_community: str = None
    contact_location_city: str = None
    contact_location_state: str = None
    contact_location_country: str = None
    age_classrooms_interested_in_offering: Optional[list[str]] = []
    socio_economic_race_and_ethnicity: Optional[list[str]] = []
    socio_economic_race_and_ethnicity_other: Optional[str] = None
    socio_economic_gender: Optional[str] = None
    socio_economic_gender_other: Optional[str] = None
    socio_economic_household_income: Optional[str] = None
    socio_economic_primary_language: Optional[str] = None
    socio_economic_primary_language_other: Optional[str] = None
    message: str = None
    receive_newsletter: bool = False
    receive_event_invitations: bool = False


class ApiSSJTypeformStartASchoolFields(CreateApiSSJTypeformStartASchoolFields):
    response_id: str = None
    created_at: datetime = None


class ApiSSJTypeformStartASchoolData(response_models.APIData):
    fields: ApiSSJTypeformStartASchoolFields


class ApiSSJTypeformStartASchoolResponse(response_models.APIResponse):
    data: ApiSSJTypeformStartASchoolData
