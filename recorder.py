from typing import *
from dataclasses import dataclass, asdict

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
        self.stream_params = StreamParams()
        self.stream = None
        self.pyaudio = None


    def record_audio(self, duration: int) -> np.ndarray:
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
        return sound


if __name__ == '__main__':
    recorder = Recorder()
    recorder.record_audio(duration=5)
