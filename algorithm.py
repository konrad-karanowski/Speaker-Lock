from typing import Dict, List, Tuple
import requests
import json

import librosa
import numpy as np
import pandas as pd


class Algorithm:

    def __init__(
            self,
            target_sr: int,
            target_num_samples: int,
            speaker_threshold: float,
            label_threshold: float
    ) -> None:
        self.target_sr: int = target_sr
        self.target_num_samples: int = target_num_samples
        self.speaker_threshold: int = speaker_threshold
        self.label_threshold: int = label_threshold

    def softmax(self, x: np.ndarray) -> np.ndarray:
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=1)

    def _get_prediction(self, slides: List[np.ndarray], sr: int) -> Dict[str, np.ndarray]:
        response = requests.post(
                url='http://127.0.0.1:5000/predict',
                json={
                    'query': [(slide.tolist(), sr) for slide in slides],
                })
        print(json.loads(response.text))
        return json.loads(response.text)

    def _handle_result(self, predictions: Dict[str, np.ndarray]) -> Dict[str, float]:
        label, speaker = self.softmax(np.array(predictions['label_proba'])), self.softmax(np.array(predictions['speaker_proba']))
        label_max, speaker_max = np.argmax(label), np.argmax(speaker)
        verdict = {
            'label_pred': label_max,
            'speaker_pred': speaker_max,
            'label_proba': label[:, 1],
            'speaker_distance': speaker[:, 1]
        }
        return verdict

    def try_unlock(self, audio: np.ndarray, sr: int) -> Dict[str, float]:
        predictions = self._get_prediction([audio], sr)
        result = self._handle_result(predictions)
        return result


if __name__ == '__main__':
    algorithm = Algorithm(22050, 22050, 0.5, 0.5)
    audio, sr = librosa.load('support_set/Tree.wav')
    s = algorithm.try_unlock(audio, sr)
    print(s)
