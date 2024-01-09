import librosa
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
if __name__ == '__main__':
    
    dir_path = r"C:\Users\yale\Desktop\bigdata\spotify_preview_target"
    save_path = r"C:\Users\yale\Desktop\bigdata\mp3_mfcc"
    #dir_rap_path = r""
    # all_file_name = os.listdir(dir_path)
    #all_file_name = next(os.walk(dir_path))
    for folder_name in os.listdir(dir_path):
        print(folder_name)
        folder_path = dir_path + '\\' + folder_name 
        for file_name in os.listdir(folder_path):
            mfcc = []
            wav_path = folder_path + '\\' + file_name
            # print(wav_path)
            y, sr = librosa.load(wav_path)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
            np.set_printoptions(threshold=np.inf)
            print(mfccs)
            # with open(save_path + '\\' + wav_path.split('-')[-1].replace('mp3','txt'), 'w') as f:
            #     f.write()
        
    # data, fs = librosa.load(wav_path)
    # fs is sampling frequency
    # sampling frequency nothing but how may samples present for second.
    # print(f"Sampling frequency : {fs} and Wave : {data}")
    # plt.plot(data)
    # plt.xlabel("Time")
    # plt.ylabel("Amplitude")
    # plt.show()

    # t = np.linspace(0, 0.5, 500)
    # s = np.sin(40 * 2 * np.pi * t) + 0.5 * np.sin(90 * 2 * np.pi * t)
    # # plt.ylabel("Amplitude")
    # # plt.xlabel("Time [s]")
    # # plt.plot(t, s)
    # # plt.show()

    # fft = np.fft.fft(s)
    # T = t[1] - t[0]  # sampling interval 
    # N = s.size
    # # 1/T = frequency
    # f = np.linspace(0, 1 / T, N)
    # # plt.ylabel("Amplitude")
    # # plt.xlabel("Frequency [Hz]")
    # # plt.bar(f[:N // 2], np.abs(fft)[:N // 2] * 1 / N, width=1.5)  # 1 / N is a normalization factor
    # # plt.show()

    # plt.figure(figsize=(10,4))
    # librosa.display.specshow(mfccs, x_axis="time")
    # plt.colorbar()
    # plt.title('MFCC')
    # plt.tight_layout()
    # plt.show()