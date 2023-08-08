import numpy as np
from transcriber import WhisperModel


class ModelService:
    def __init__(self, model_name="small.en", device='cuda', compute_type="float16", local_files_only=False):
        print("Loading model...")
        self.transcriber = WhisperModel(
            model_name,
            device=device,
            compute_type=compute_type,
            local_files_only=local_files_only,)
        print("Loaded.")

    def _bytes_to_float_array(self, audio_bytes):
        raw_data = np.frombuffer(
            buffer=audio_bytes, dtype=np.int16
        )
        return raw_data.astype(np.float32) / 32768.0
    
    def transcribe_wave_binary(self, binary_wave_data):
        audio_array = self._bytes_to_float_array(binary_wave_data)
        result = self.transcriber.transcribe(audio_array, initial_prompt=None, language="en", task="transcribe")
        return result