from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum
import uuid

__all__ = [
        'TextToSpeach',
        'CallRequest',
        'CallResult',
        'Call',
        'get_id'
]

get_id = lambda: str(uuid.uuid4())

class TextToSpeach(BaseModel):
    text: str
    lang: str

class CallRequest(BaseModel):
    chat_id: int
    audio_url: Optional[str] = None 
    text_to_speach: Optional[TextToSpeach] = None
    message_before: Optional[dict] = None
    message_after: Optional[dict] = None
    send_audio_after_call: bool = True

class CallResult(Enum):
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    ERROR = 'ERROR'

class Call(BaseModel):
    id: str = Field(default_factory=get_id) 
    created_at: datetime = Field(default_factory=datetime.now)
    call_request: CallRequest
    result: Optional[CallResult] = Field(default=None, validate_default=True)
    result_details: Optional[str] = None
    model_config = ConfigDict(use_enum_values=True)
