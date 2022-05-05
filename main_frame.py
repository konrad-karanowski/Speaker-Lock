from typing import *
import tkinter as tk
from tkinter import messagebox
import sounddevice as sd

import numpy as np
import pandas as pd
from PIL import Image, ImageTk

from recorder import Recorder
from algorithm import Algorithm


class MainFrame(tk.Frame):
    audio: Optional[np.ndarray] = None
    audio_sr: Optional[int] = 22050
    latence: int = 3
    recording_duration: int = 2
    recorder = Recorder()
    algorithm = Algorithm(22050, 22050, 11050, 0.5, 0.5)

    def __init__(self, container, **kwargs) -> None:
        super(MainFrame, self).__init__(container, **kwargs)

        # widgets 
        self.record_button = tk.Button(self, text='Record', command=self.record_audio, height=1, width=7)
        self.record_button.grid(row=0, column=0)

        self.play_button = tk.Button(
            self,
            text='Play',
            command=self.play_audio,
            height=1,
            width=7,
            state=tk.DISABLED
        )
        self.play_button.grid(row=0, column=1)

        self.unlock_button = tk.Button(
            self,
            text='Unlock',
            command=self.unlock,
            height=1, width=7,
            state=tk.DISABLED
        )
        self.unlock_button.grid(row=0, column=2)

        self.message_label = tk.Label(self)
        self.message_label.grid(row=1, column=0, columnspan=3)

        self.image = ImageTk.PhotoImage(file='img/lock.png')
        self.image_label = tk.Label(self, image=self.image)
        self.image_label.grid(row=2, column=0, columnspan=3, rowspan=3)

    def record_audio(self) -> None:
        for i in range(self.latence, 0, -1):
            self.record_button['text'] = str(i)
            self.update()
            self.after(1000)
        self.record_button['text'] = 'Recording...'
        self.update()

        self.audio = self.recorder.record_audio(self.recording_duration)

        if self.audio is not None:
            self.play_button['state'] = tk.ACTIVE
            self.unlock_button['state'] = tk.ACTIVE
        self.record_button['text'] = 'Record'
        self.update()

    def play_audio(self) -> None:
        if self.audio is not None:
            sd.play(self.audio, self.audio_sr)

    def unlock(self) -> None:
        if self.audio is not None:
            result = self.algorithm.try_unlock(self.audio, self.audio_sr)
            print(result)
            if result['label_pred'] and result['speaker_pred']:
                verdict = 'Granted'
                self.grant_permission(result)
            else:
                verdict = 'Denied'
                self.deny_permission(result)
            messagebox.showinfo(f'''
            {verdict} permission to system. 
            Distance between audio and speaker: {result["speaker_distance"]}
            Distance between audio and word: {result["label_distance"]}
            ''')

    def grant_permission(self, result: Dict[str, float]) -> None:
        self.message_label['text'] = 'Welcome back, Konrad!'
        self.image = ImageTk.PhotoImage(file='img/unlock.png')
        self.image_label['image'] = self.image
        self.image_label['bg'] = 'lightgreen'

    def deny_permission(self, result: Dict[str, float]) -> None:
        msg = ''
        if not result['label_pred']:
            msg += ' This is not correct password.'
        if not result['speaker_pred']:
            msg += ' You are an intruder'
        self.message_label['text'] = f'Permission denied.{msg}'
        self.image = ImageTk.PhotoImage(file='img/lock.png')
        self.image_label['image'] = self.image
        self.image_label['bg'] = 'red'
