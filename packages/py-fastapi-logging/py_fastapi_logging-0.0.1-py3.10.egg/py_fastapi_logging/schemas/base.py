from typing import Union, Optional

from pydantic import BaseModel, Field


class BaseJsonLogSchema(BaseModel):
    thread: Union[int, str]
    level: int
    request_id: Optional[str]
    progname: Optional[str]
    timestamp: str = Field(...)
    exceptions: Union[list[str], str] = None

    class Config:
        allow_population_by_field_name = True
