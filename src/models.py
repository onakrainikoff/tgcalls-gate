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


class MessageContent(BaseModel):
    text: Optional[str]


class MessageEntity(BaseModel):
    id: str = Field(default_factory=get_id, validate_default=True)
    created_at: datetime = Field(default_factory=datetime.now, validate_default=True)
    chat_id: int
    content: MessageContent
    status: Optional[Status] = Field(default=None, validate_default=True)
    status_details: Optional[str] = None
    model_config = ConfigDict(use_enum_values=True)


class CallContent(BaseModel):    
    text_to_speech: Optional[TextToSpeech] = None
    audio_url: Optional[str] = None 
    message_before: Optional[MessageContent] = None
    message_after: Optional[MessageContent] = None
    send_audio_after_call: bool = True


class CallEntity(BaseModel):
    id: str = Field(default_factory=get_id, validate_default=True)
    created_at: datetime = Field(default_factory=datetime.now, validate_default=True)
    chat_id: int
    content: CallContent
    status: Optional[Status] = Field(default=None, validate_default=True)
    status_details: Optional[str] = None
    model_config = ConfigDict(use_enum_values=True)


__all__ = [
        'get_id',
        'Status',
        'TextToSpeech',
        'CallContent',
        'CallEntity',
        'MessageContent',
        'MessageEntity',
]
