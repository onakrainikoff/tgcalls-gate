from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum
import uuid


get_id = lambda: str(uuid.uuid4())


class Status(Enum):
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    ERROR = 'ERROR'


class TextToSpeech(BaseModel):
    text: str
    lang: str
    audio_file_path: Optional[str] = None


class MessageRequest(BaseModel):
    id: str = Field(default_factory=get_id)
    created_at: datetime = Field(default_factory=datetime.now)
    chat_id: int
    text: Optional[str]


class MessageResponse(BaseModel):
    message_request: MessageRequest
    status: Optional[Status] = Field(default=None, validate_default=True)
    status_details: Optional[str] = None
    model_config = ConfigDict(use_enum_values=True)


class CallRequest(BaseModel):
    id: str = Field(default_factory=get_id) 
    created_at: datetime = Field(default_factory=datetime.now)
    chat_id: int
    audio_url: Optional[str] = None 
    text_to_speech: Optional[TextToSpeech] = None
    message_before: Optional[MessageRequest] = None
    message_after: Optional[MessageRequest] = None
    send_audio_after_call: bool = True


class CallResponse(BaseModel):    
    call_request: CallRequest
    status: Optional[Status] = Field(default=None, validate_default=True)
    status_details: Optional[str] = None
    model_config = ConfigDict(use_enum_values=True)


__all__ = [
        'Status',
        'TextToSpeech',
        'CallRequest',
        'CallResponse',
        'MessageRequest',
        'MessageResponse',
        'get_id'
]
