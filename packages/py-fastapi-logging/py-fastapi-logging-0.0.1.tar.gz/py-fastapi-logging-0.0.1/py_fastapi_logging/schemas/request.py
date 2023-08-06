from pydantic import BaseModel
from typing import Optional


class RequestPayload(BaseModel):
    method: str
    path: str
    host: str
    subject_type: Optional[str]
    subject_id: Optional[str]
    params: Optional[dict]
    body: str


class RequestJsonLogSchema(BaseModel):
    payload: RequestPayload
