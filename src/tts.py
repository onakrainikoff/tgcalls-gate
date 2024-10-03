import os,  torch, torchaudio, logging
from IPython.display import Audio, display
from envyaml import EnvYAML
import hashlib
import shutil
from models import *

log = logging.getLogger()

class TtsSileroProvider:
    def __init__(self, lang: str, model_dir:str, model_file:str,  model_url: str, speaker:str, rate:int) -> None:
        log.info("Initialize TtsSileroProvider for lang={lang}")
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
    

    def process(self, text:str, audio_file_path:str):
        self.model.save_wav(text=text, speaker=self.speaker, sample_rate=self.rate, audio_path = audio_file_path)



class TtsService:
    def __init__(self, config:EnvYAML) -> None:
        log.info("Initialize TtsService")
        self.config = config
        torch.set_num_threads(self.config['tts.torch_threads'])
        self.data_dir = self.config['tts.data_dir']
        os.makedirs(self.data_dir, exist_ok=True)
        self.data_audios_dir = os.path.join(self.data_dir, 'audios/')
        os.makedirs(self.data_audios_dir, exist_ok=True)
        if self.config.get('tts.use_cache'):     
            self.data_audios_cache_dir = os.path.join(self.data_dir, 'audios_cache/')
            os.makedirs(self.data_audios_cache_dir, exist_ok=True)
        else:
             self.data_audios_cache_dir = None
        self.data_models_dir = os.path.join(self.data_dir, 'models/')
        os.makedirs(self.data_models_dir, exist_ok=True)   
        self.providers = {}
        for lang_name in self.config['tts.langs']:
            lang = f"tts.langs.{lang_name}"
            provider = self.config[f"{lang}.provider"]
            if provider == 'silero':
                    self.providers[lang_name] = TtsSileroProvider(
                       lang_name,
                       os.path.join(self.data_models_dir, lang_name, provider),
                       self.config[f"{lang}.model_file"],
                       self.config[f"{lang}.model_url"],
                       self.config[f"{lang}.speaker"],
                       self.config[f"{lang}.rate"],
                    )
            else:
                raise RuntimeError(f"Unsupported tts provider={provider}")


    def process(self, text_to_speach: TextToSpeach, audio_id:str) -> str:
        log.info(f"Process text_to_speach={text_to_speach}, audio_id={audio_id}")
        audio_file_path = os.path.join(self.data_audios_dir, f"{audio_id}.wav")
        if self._copy_from_cache(text_to_speach, audio_file_path):
            return audio_file_path
        provider = self.providers.get(text_to_speach.lang)
        if not provider:
            raise RuntimeError(f"Unsupported lang={text_to_speach.lang}")
        provider.process(text_to_speach.text, audio_file_path)
        self._save_to_cache(text_to_speach,audio_file_path)
        return audio_file_path

        
    

    def _copy_from_cache(self, text_to_speach:TextToSpeach, copy_to_path:str) -> bool:
        if self.config.get('tts.use_cache'):
           file_path = self._get_file_path_in_cache(text_to_speach)
           if not os.path.isfile(file_path):
               log.info(f"Copy audio from cache: from={file_path}, to={copy_to_path}")
               shutil.copyfile(file_path, copy_to_path)
               return True               
        return False
              
    
    def _save_to_cache(self, text_to_speach:TextToSpeach, save_from_path:str) -> None:
        if self.config.get('tts.use_cache'):
            file_path = self._get_file_path_in_cache(text_to_speach)
            if not os.path.isfile(file_path):
                shutil.copyfile(save_from_path, file_path)
    

    def _get_file_path_in_cache(self, text_to_speach:TextToSpeach) -> str:
        file_name = f"{text_to_speach.lang}-{hashlib.md5(text_to_speach.text).hexdigest()}.wav"
        file_path = os.path.join(self.data_audios_cache_dir, file_name)
        return file_path