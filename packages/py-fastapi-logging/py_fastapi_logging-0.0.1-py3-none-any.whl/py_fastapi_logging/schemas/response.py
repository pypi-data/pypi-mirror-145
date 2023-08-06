from pydantic import BaseModel

# from typing import Optional


# class ResponseTime(BaseModel):
#     total: str
#     db: str
#     view: str


class ResponsePayload(BaseModel):
    status: int
    # time: Optional[ResponseTime] # TODO: до выяснения обстоятельств
    response_time: str
    response_body: str


class ResponseJsonLogSchema(BaseModel):
    payload: ResponsePayload
