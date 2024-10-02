import uvicorn
from api import Api

api = Api()

if __name__ == "__main__":
    uvicorn.run(api.app, host="0.0.0.0", port=80)