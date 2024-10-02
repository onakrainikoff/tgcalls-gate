from typing import Union, Annotated, Optional
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
from models import *


class Api:
    def __init__(self, config) -> None:
        self.config = config
        self.tts = None
        self.tgcalls = None

        # !todo configuration
        self.app = FastAPI()

        class JWTBearer(HTTPBearer):
            def __init__(self, auto_error: bool = True):
                super(JWTBearer, self).__init__(auto_error=auto_error)

            async def __call__(self, request: Request) -> Optional[str]:
                credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
                if credentials:
                    if not credentials.scheme == "Bearer":
                        raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
                    token = credentials.credentials
                    if not self.verify_jwt(token):
                        raise HTTPException(status_code=403, detail="Invalid token or expired token.")
                    return token
                else:
                    raise HTTPException(status_code=403, detail="Invalid authorization code.")

            def verify_jwt(self, token: str) -> bool:
                return '12345' == token

        @self.app.post("/call")
        async def call(call_request: CallRequest):
            return "Not implemented"
        
        @self.app.get("/health", dependencies=[Depends(JWTBearer())])
        @self.app.get("/")
        async def health_check():
            return {"health": "OK"}

    def run(self):    
        uvicorn.run(self.app, host=self.config['api.host'], port=self.config['api.port'])


# https://gist.github.com/alexpearce/73700474d8be770c0e5448cb09d885cb