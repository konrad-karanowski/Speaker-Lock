from typing import *
from dataclasses import dataclass, asdict
import wave

import pyaudio
import numpy as np


@dataclass
class StreamParams:
    format: int = pyaudio.paFloat32
    channels: int = 1
    rate: int = 22050
    frames_per_buffer: int = 1024
    input: bool = True
    output: bool = False


class Recorder:

    def __init__(self) -> None:
        """
        Audio recorder taken from: https://www.youtube.com/watch?v=e9CRZEi_feA
        """
        self.stream_params: StreamParams = StreamParams()
        self.stream: Optional[pyaudio.Stream] = None
        self.pyaudio: Optional[pyaudio.PyAudio] = None

    def record_audio(self, duration: int, save: Optional[str] = None) -> np.ndarray:
        frames = []
        self.pyaudio = pyaudio.PyAudio()
        self.stream = self.pyaudio.open(**asdict(self.stream_params))
        try:
            for _ in range(int(self.stream_params.rate * duration / self.stream_params.frames_per_buffer)):
                frame = np.frombuffer(self.stream.read(self.stream_params.frames_per_buffer), dtype=np.float32)
                frames.append(frame)
        except IOError as e:
            print(f'Exception: {e}')
        finally:
            self.stream.close()
            self.pyaudio.terminate()
        sound = np.hstack(frames)
        if save is not None:
            with wave.open(save, 'w') as obj:
                obj.setnchannels(1)
                obj.setframerate(22050)
                obj.setsampwidth(2)
                obj.writeframes(sound)
        return sound
