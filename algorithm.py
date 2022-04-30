from typing import Dict, List

import librosa
import numpy as np
import pandas as pd


class Algorithm:

    def __init__(
        self, 
        support_set: str, 
        target_sr: int, 
        target_num_samples: int, 
        sliding_window_size: int) -> None:
        self.target_sr: int = target_sr
        self.target_num_samples: int = target_num_samples
        self.sliding_window_size: int = sliding_window_size
        self.support_set: np.ndarray = self._gather_support(support_set)

    def _create_slides(self, audio: np.ndarray) -> List[np.ndarray]:
        slides = []
        i = 0
        for i in range(0, audio.shape[0] - self.target_num_samples, self.sliding_window_size):
            slide = audio[i : i + self.target_num_samples]
            slides.append(slide)
        slides.append(audio[-self.target_num_samples:])
        return slides

    def _gather_support(self, support_set: pd.DataFrame) -> np.ndarray:
        audio, sr = librosa.load(support_set)
        assert sr == self.target_sr, f'Audio sr must be equal to target sr, but got sr: {sr} and target sr: {self.target_sr}'
        return audio
        

    def _get_prediction(self, slides: List[np.ndarray]) -> Dict[str, np.ndarray]:
        return {
            'label_dist': 0.456,
            'speaker_dist': None
        }

    def _handle_result(self, predictions: Dict[str, np.ndarray]) -> Dict[str, float]:
        pass

    def try_unlock(self, audio: np.ndarray) -> Dict[str, float]:
        slides = self._create_slides(audio)
        predictions = self._get_prediction(slides)
        result = self._handle_result(predictions)
        return result

if __name__ == '__main__':
    algorithm = Algorithm('support_set/Marvin.wav', 10, 5, 3)
    audio = np.array([i for i in range(5)])
    s = algorithm._create_slides(audio)
    print(f'Audio: {audio}')
    print(s)
