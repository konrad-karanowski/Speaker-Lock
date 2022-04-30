from typing import Dict

import pandas as pd


class Algorithm:

    def __init__(self) -> None:
        pass

    def try_unlock(self, support_set: pd.DataFrame) -> Dict[str, float]:
        return {
            'label_pred': 1,
            'speaker_pred': 1,
            'label_distance': 0.24,
            'speaker_distance': 0.24745784573
        }
