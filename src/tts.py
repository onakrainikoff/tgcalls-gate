import os,  torch, torchaudio, logging
from IPython.display import Audio, display
from envyaml import EnvYAML
from models import *

log = logging.getLogger()
torch.set_num_threads(4)

class TtsSileroProvider:
    def __init__(self, lang: str, model_dir:str, model_file:str,  model_url: str, speaker:str, rate:int) -> None:
        self.device = torch.device('cpu')
        self.lang = lang
        self.model_dir = model_dir
        self.model_file = model_file
        self.model_url = model_url
        self.speaker = speaker
        self.rate = rate
        os.makedirs(self.model_dir, exist_ok=True)
        self.model_path = os.path.join(self.model_dir, self.model_file)
        if not os.path.isfile(self.model_path):
                log.info(f"Local model file {self.model_path} is absent and will be downloaded from {self.model_url}")
                torch.hub.download_url_to_file(self.model_url, self.model_path)
        else:
            log.info(f"Local model file {self.model_path} found")
        self.model = torch.package.PackageImporter(self.model_path).load_pickle("tts_models", "model")
        self.model.to(self.device)
    
    def process(self, text:str, audio_path:str):
        self.model.save_wav(text=text, speaker=self.speaker, sample_rate=self.rate, audio_path = audio_path)


class Tts:
    def __init__(self, config:EnvYAML=None) -> None:
        self.data_dir = './data'
        self.data_audios_dir = os.path.join(self.data_dir, 'audios/')
        os.makedirs(self.data_audios_dir, exist_ok=True)
        data_models_dir = os.path.join(self.data_dir, 'models/')
        os.makedirs(data_models_dir, exist_ok=True)   

       

    def process(self, text_to_speach: TextToSpeach) -> str:
        pass
        