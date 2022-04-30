from typing import Dict, List, Tuple
import requests
import json

import librosa
import numpy as np
import pandas as pd


class Algorithm:

    def __init__(
            self,
            support_set: str,
            target_sr: int,
            target_num_samples: int,
            sliding_window_size: int,
            speaker_threshold: float,
            label_threshold: float
    ) -> None:
        self.target_sr: int = target_sr
        self.target_num_samples: int = target_num_samples
        self.sliding_window_size: int = sliding_window_size
        self.support_set, self.sr = self._gather_support(support_set)
        self.speaker_threshold = speaker_threshold
        self.label_threshold = label_threshold

    def _create_slides(self, audio: np.ndarray) -> List[np.ndarray]:
        slides = []
        i = 0
        for i in range(0, audio.shape[0] - self.target_num_samples, self.sliding_window_size):
            slide = audio[i: i + self.target_num_samples]
            slides.append(slide)
        slides.append(audio[-self.target_num_samples:])
        return slides

    def _gather_support(self, support_set: str) -> Tuple[np.ndarray, int]:
        audio, sr = librosa.load(support_set)
        assert sr == self.target_sr, \
            f'Audio sr must be equal to target sr, but got sr: {sr} and target sr: {self.target_sr}'
        return audio, sr

    def _get_prediction(self, slides: List[np.ndarray], sr: int) -> Dict[str, np.ndarray]:
        response = requests.post(
                url='http://127.0.0.1:5000/predict',
                json={
                    'query': [(slide.tolist(), sr) for slide in slides],
                    'support': (self.support_set.tolist(), sr)
                })
        print(json.loads(response.text))
        return json.loads(response.text)

    def _handle_result(self, predictions: Dict[str, np.ndarray]) -> Dict[str, float]:
        label, speaker = predictions['label_distances'], predictions['speaker_distances']
        label_min, speaker_min = np.min(label), np.min(speaker)
        verdict = {
            'label_pred': int(label_min < self.label_threshold),
            'speaker_pred': int(speaker_min < self.speaker_threshold),
            'label_distance': label_min,
            'speaker_distance': speaker_min
        }
        return verdict

    def try_unlock(self, audio: np.ndarray, sr: int) -> Dict[str, float]:
        slides = self._create_slides(audio)
        predictions = self._get_prediction(slides, sr)
        result = self._handle_result(predictions)
        return result


if __name__ == '__main__':
    algorithm = Algorithm('support_set/Marvin.wav', 22050, 22050, 11050, 14, 15)
    audio, sr = librosa.load('support_set/Six.wav')
    s = algorithm.try_unlock(audio, sr)
    print(s)
