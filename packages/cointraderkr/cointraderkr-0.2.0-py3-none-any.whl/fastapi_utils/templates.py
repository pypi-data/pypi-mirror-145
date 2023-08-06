from enum import Enum
from pydantic import BaseModel
from typing import Any, Optional, Dict, List


# class DockerActions(str, Enum):
#     restart = 'restart'


class LogTemplate(BaseModel):
    source: Optional[str]
    ip_address: Optional[str]
    log_level: Optional[str]
    timestamp: Optional[str]
    filename: Optional[str]
    message: Optional[str]


class GetAccessTokenRequest(BaseModel):
    username: str
    password: str


class RestartContainerRequest(BaseModel):
    access_token: str
    server: int
    container: str


class DockerActionRequest(BaseModel):
    action: str
    access_token: str
    server: int
    container: str


class TaskStatusRequest(BaseModel):
    access_token: str
    task_id: str


class MetricRequest(BaseModel):
    bucket: str = 'coin-trader'
    start_from: str = '1d'
    measurement: str
    fields: Optional[List[str]] = []
    filters: Optional[Dict[str, Any]] = {}
    window: str = '1m'
    aggfunc: str = 'last'
    pivot: Optional[bool] = False