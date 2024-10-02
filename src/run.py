
from api import Api
from config import Config

api = Api()

if __name__ == "__main__":
    config = Config.load()
    print(config["api"]['port'])
    print(config["api"]['host'])
    # api.run()