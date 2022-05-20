# Speaker-Lock
This repository is a part of the final project of Artifical Intelligence course led by bsc. Julita Bielaniewicz. Project's goal was to create the application for voice unlocking. System should detect not only the spoken word (password), but also the speaker (system's owner). The assumption of the project was to create a network from scratch, which is why I didn't use conformer and other more complicated and more computationally expensive methods.
This repository consists of a simple tkinter's application which allows a user to record a password, play the recording and try to unlock a system. After trying to open the system, application returns a feedback with probabilities and final decisions. 
Another part, repository for model's training is located [here](https://github.com/konrad-karanowski/Speech-And-Speaker-Detection). 

# About the unlocking stage
The algorithm sends an audio as a list with it's sampling rate using predict_api from another repository (linked above). Next, after getting model's logits calculate probabilities using a softmax function. After this step, the decision (based on thresholds) is made.
The best hyperparameters for me was: speaker threshold = 0.85, word threshold = 0.5.
