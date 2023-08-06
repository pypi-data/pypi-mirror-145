from typing import Optional

from pydantic import BaseModel

MODEL_TYPE = 'montessori_certifications'


class CreateAPIMontessoriCertificationsFields(BaseModel):
    year_certified: Optional[int] = None
    certification_levels: Optional[list[str]] = None
    certifier: Optional[str] = None
    certification_status: Optional[str] = None


class APIMontessoriCertificationsFields(CreateAPIMontessoriCertificationsFields):
    full_name: Optional[str] = None
    certifier_other: Optional[str] = None
