import os
import numpy as np
import pandas as pd
import IPython
import librosa
import librosa.display
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.metrics import ConfusionMatrixDisplay
import sklearn.metrics as skm
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_predict
from sklearn.ensemble import RandomForestClassifier
# To clean up the notebook
import warnings
warnings.filterwarnings("ignore")
warnings.simplefilter("ignore")

def getFeatures(filePath):
    signal, sr = librosa.load(filePath)
    
    tempo = librosa.beat.tempo(y=signal)
    output = np.array(tempo)
    
    stft = np.mean(librosa.feature.melspectrogram(y=signal).T, axis=0)
    output = np.hstack((output, stft))
    
    chroma = np.mean(librosa.feature.chroma_stft(y=signal).T, axis=0)
    output = np.hstack((output, chroma))
    
    mfccs = np.mean(librosa.feature.mfcc(y=signal).T, axis=0)
    output = np.hstack((output, mfccs))
    
    return output

def modelResults(y_train, y_pred):
    ConfusionMatrixDisplay.from_predictions(y_train, y_pred)
    ConfusionMatrixDisplay.from_predictions(y_train, y_pred, normalize="true", values_format=".0%")
    print(skm.classification_report(y_train, y_pred, digits=3))
    print(skm.precision_recall_fscore_support(y_train, y_pred, average="macro"))

def get5sFeatures(filePath):
    signal, sr = librosa.load(filePath)
    #print("signal: ", signal)
    tempo = librosa.beat.tempo(y=signal)
    output = np.array(tempo)
    
    signal = signal[sr*20:sr * 25]
    print(signal.shape)
    print("signal: ", signal)
    stft = np.mean(librosa.feature.melspectrogram(y=signal).T, axis=0)
    output = np.hstack((output, stft))
    
    chroma = np.mean(librosa.feature.chroma_stft(y=signal).T, axis=0)
    output = np.hstack((output, chroma))
    
    mfccs = np.mean(librosa.feature.mfcc(y=signal).T, axis=0)
    output = np.hstack((output, mfccs))
    
    return output

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
 
    # Sample (can ignore 82-97)
    samples = []
    sr = 22050
    for mood in os.listdir(rootPath):
        sample = { "mood" : mood }
        # split to 5 moods
        moodData = data[data.mood == mood]
        
        print(mood + ":")
        IPython.display.display(IPython.display.Audio(moodData.iloc[20, 0]))
        # choose sample data to load
        signal, _ = librosa.load(moodData.iloc[30, 0], sr=sr)
        sample["signal"] = signal
        samples.append(sample)
    print(getFeatures(data.iloc[0, 0]))

    print("Extracting Features...")
    X, y = [], []
    
    for i, row in tqdm(data.iterrows()):
        label = row["mood"]
        features = getFeatures(row["filePath"])
        X.append(features)
        y.append(label)
        if i % 100 == 0:
            print("#", end="")
    print("\ndone")

    X = np.array(X)
    y = np.array(y)
    # print(X)
    # print(y)
    #split data into Test and Train set
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.2, stratify=y)
    # print(X_train.shape)
    # print(X_test.shape)
    # print(y_train.shape)
    # print(y_test.shape)

    # encoding string labels ("happy", "sad", ...) to OneHotEncoding
    ohe = OneHotEncoder()
    y_train_ohe = ohe.fit_transform(y_train.reshape(-1, 1)).toarray()
    y_test_ohe = ohe.fit_transform(y_test.reshape(-1, 1)).toarray()

    oe = OrdinalEncoder()
    y_train_oe = oe.fit_transform(y_train.reshape(-1, 1))
    y_test_oe = oe.fit_transform(y_test.reshape(-1, 1))
  
    print("y_train_oe :", y_train_oe)
    print("y_train_ohe :", y_train_ohe)
    # ------------------------LogisticRegression--------------------------------------
    scaler = StandardScaler()
    lr = LogisticRegression(max_iter=400)
    lr_pipeline = make_pipeline(scaler, lr)
    y_train_pred = cross_val_predict(lr_pipeline, X_train, y_train_oe, cv=3)
    print("y_train_pred : ",  y_train_pred)
    modelResults(y_train_oe, y_train_pred)

    # ------------------------RandomForestClassifier--------------------------------------
    randomForestClassifier = RandomForestClassifier()
    randomForestClassifier.fit(X_train, y_train_oe)
    y_train_pred = cross_val_predict(randomForestClassifier, X_train, y_train_oe, cv=3)
    print("y_train_pred : ", y_train_pred)
    modelResults(y_train_oe, y_train_pred)

    model = randomForestClassifier
    y_test_pred = model.predict(X_test)
    modelResults(y_test_oe, y_test_pred)

    # check_path = "./spotify_preview_target/traditional blues/Abraham, Martin and John-0TFPU0mrqfiUTSmzCfnvWY.mp3"
    # file_name = "Abraham, Martin and John-0TFPU0mrqfiUTSmzCfnvWY.mp3"
    # IPython.display.display(IPython.display.Audio(check_path))
    # x = get5sFeatures(check_path)
    # #print(x)
    # pred = model.predict(x.reshape(1, -1))
    # pred_transform = oe.inverse_transform(pred.reshape(1, -1))
    # print(pred_transform.item(0))
    # pred_trs_lst = []
    # pred_trs_lst.append([file_name, pred_transform.item(0), pred.item(0)])
    # print(pred_trs_lst)

    dir_path = r"C:\Users\yale\Desktop\bigdata\spotify_preview_target_non_dup"
    save_path = r"C:\Users\yale\Desktop\bigdata\prediction"
    pred_trs_lst = []
    for file_name in os.listdir(dir_path):
        check_path = dir_path + '\\' + file_name
        print(check_path)
        x = get5sFeatures(check_path)
        pred = model.predict(x.reshape(1,-1))
        pred_transform = oe.inverse_transform(pred.reshape(1, -1))
        pred_trs_lst.append([file_name, pred_transform.item(0), pred.item(0)])
    print(pred_trs_lst)
    pred_df = pd.DataFrame(pred_trs_lst)
    pred_df.columns = ['Song', 'Mood', 'Score']
    print(pred_df)
    pred_df.to_csv(r'C:\Users\yale\Desktop\bigdata\prediction\pred_trans.csv', index=False)