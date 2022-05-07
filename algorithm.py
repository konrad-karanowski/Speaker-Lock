from typing import Dict, List
import requests
import json

import numpy as np


class Algorithm:

    def __init__(
            self,
            target_sr: int,
            target_num_samples: int,
            speaker_threshold: float,
            label_threshold: float
    ) -> None:
        """Class for connecting to model, getting predictions and returning it.
        Args:
            target_sr (int): Desired audio's sample rate.
            target_num_samples (int): Desired number of samples in audio.
            speaker_threshold (float): Threshold for classifing speaker as correct.
            label_threshold (float): Threshold for classifing label as correct. 
        """
        self.target_sr: int = target_sr
        self.target_num_samples: int = target_num_samples
        self.speaker_threshold: float = speaker_threshold
        self.label_threshold: float = label_threshold

    def _get_prediction(self, audio_samples: List[np.ndarray], sr: int) -> Dict[str, List[float]]:
        """Gets predictions from the model using API.
        Args:
            audio_samples (List[np.ndarray]): List of audio samples to classify.
            sr (int): Sample rate for audio.
        Returns:
            Dict[str, List[float]]: Model's responses (probability of speaker and label).
        """
        response = requests.post(
                url='http://127.0.0.1:5000/predict',
                json={
                    'query': [(slide.tolist(), sr) for slide in audio_samples],
                })
        return json.loads(response.text)

    def _handle_result(self, predictions: Dict[str, List[float]]) -> Dict[str, float]:
        """Handle results from model using thresholds and returns full response from algorithm.
        Args:
            predictions (Dict[str, List[float]]): Predictions from the model.
        Returns:
            Dict[str, float]: Final predictions and probabilities from the model.
        """
        label, speaker = np.array(predictions['label_proba']), np.array(predictions['speaker_proba'])
        label_pred = int(label[:, 1].item() > self.label_threshold)
        speaker_pred = int(speaker[:, 1].item() > self.speaker_threshold)
        verdict = {
            'label_pred': label_pred,
            'speaker_pred': speaker_pred,
            'label_proba': label[:, 1],
            'speaker_proba': speaker[:, 1]
        }
        return verdict

    def try_unlock(self, audio: np.ndarray, sr: int) -> Dict[str, float]:
        """Gets predictions from the model using audio sample and returns it to the system.
        Args:
            audio (np.ndarray): Audio signal to classify.
            sr (int): Sampling rate of the audio.
        Returns:
            Dict[str, float]: Final predictions and probabilities from the model.
        """
        predictions = self._get_prediction([audio], sr)
        result = self._handle_result(predictions)
        return result

