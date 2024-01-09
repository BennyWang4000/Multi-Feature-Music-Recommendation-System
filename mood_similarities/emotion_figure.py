import matplotlib.pyplot as plt
import librosa
import os
import pandas as pd
import numpy as np

if __name__ == '__main__':
    # Extracting data into dataframe
    rootPath = "./dataset"
    paths = []
    moods = []
    for mood in os.listdir(rootPath):
        for file in os.listdir(rootPath + "/" + mood):
            paths.append(rootPath + "/" + mood + "/" + file)
            moods.append(mood)
            
    data = pd.DataFrame(columns=["filePath", "mood"])
    data["filePath"] = paths
    data["mood"] = moods

    print(data)
    # Checking our input data
    # print(data["mood"].value_counts())

    samples = []
    sr = 22050
    for mood in os.listdir(rootPath):
        sample = { "mood" : mood }
        moodData = data[data.mood == mood]
        
        print(mood + ":")
        #IPython.display.display(IPython.display.Audio(moodData.iloc[20, 0]))
        signal, _ = librosa.load(moodData.iloc[30, 0], sr=sr)
        sample["signal"] = signal
        samples.append(sample)

    fig = plt.figure(figsize=(10,6))
    for i, sample in enumerate(samples):
        plt.subplot(2, 3, i + 1)
        plt.tight_layout()
        librosa.display.waveshow(sample["signal"], sr=sr, alpha=0.4, color="blue")
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.title(sample["mood"])
    plt.show()

    fig = plt.figure(figsize=(10,6))
    for i, sample in enumerate(samples):
        sample["frequencies"] = librosa.stft(sample["signal"])
        sample["frequencies_db"] = librosa.amplitude_to_db(np.abs(sample["frequencies"]), ref=np.max)
        plt.subplot(2, 3, i + 1)
        plt.tight_layout()
        #plt.figure(figsize=(10,6))
        librosa.display.specshow(sample["frequencies_db"])
        plt.xlabel("Time")
        plt.ylabel("Amplitude (db)")
        plt.title(sample["mood"])
        plt.colorbar()
    plt.show()

    fig = plt.figure(figsize=(10,6))
    for i, sample in enumerate(samples):
        plt.subplot(2, 3, i + 1)
        plt.tight_layout()
        sample["chroma"] = librosa.feature.chroma_stft(y=sample["signal"], sr=sr)
        #plt.figure(figsize=(10, 6))
        librosa.display.specshow(sample["chroma"], y_axis='chroma', x_axis='time')
        plt.title(sample["mood"])
        plt.colorbar()
    plt.show()

    fig = plt.figure(figsize=(10,6))
    for i, sample in enumerate(samples):
        plt.subplot(2, 3, i + 1)
        plt.tight_layout()
        sample["mfccs"] = librosa.feature.mfcc(y=sample["signal"], sr=sr, n_mfcc=40)
        #plt.figure(figsize=(20, 10))
        librosa.display.specshow(sample["mfccs"], x_axis='time')
        plt.title(sample["mood"])
        plt.colorbar()
    plt.show()