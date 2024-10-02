

class Config:
    def __init__(self, env_data:dict={}, yml_data={}) -> None:
        self._env_data = env_data
        self._yml_data = yml_data
        self.data = {
              'api': {
                  'port': self.int_env_or('TG_CALLS_API_PORT', self.int_yml_or('api.port', 8080)),
                  'host': self.str_env_or('TG_CALLS_API_HOST', self.str_yml_or('api.host', "0.0.0.0"))
              }

        }

    def int_env_or(self, key:str, defautl) -> int: 
        return int(self._env_data.get(key, defautl))
    
    def int_yml_or(self, key:str, defautl) -> int: 
        return int(self._yml_data.get(key, defautl))

    def str_env_or(self, key:str, defautl) -> str: 
        return str(self._env_data.get(key, defautl))
    
    def str_yml_or(self, key:str, defautl) -> str: 
        return str(self._yml_data.get(key, defautl))

    @classmethod
    def load(cls):
        _yml_data = {"api.port": '80'}
        _env_data = {}
        return Config(_env_data, _yml_data).data