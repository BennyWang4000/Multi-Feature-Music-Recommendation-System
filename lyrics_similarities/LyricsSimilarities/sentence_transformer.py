from sentence_transformers import SentenceTransformer, util
from sklearn.preprocessing import MinMaxScaler

import os
import numpy as np
import pandas as pd
from tqdm import tqdm

model = SentenceTransformer('distiluse-base-multilingual-cased-v1', device='cuda')

def getLyrics(directory_path):
    list = []
    file_list = os.listdir(directory_path)
    for filename in file_list:
        filepath = os.path.join(directory_path, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                sentences = content.split('\n')
            obj = {
                "lyrics": sentences,
                "id": filename.split('.')[0]
            }
            list.append(obj)
    return list

blues = getLyrics("blues_lyrics")
rap = getLyrics("rap_lyrics")
all_songs = blues+rap

score_json = {}
all_embeddings = {}
print("embedding:")
for song in tqdm(all_songs):
    all_embeddings[song["id"]] = model.encode(song["lyrics"], convert_to_tensor=True)
    score_json[song["id"]] = {}

# print(all_embeddings)

def computeCosineSimilarity(id1, id2):
    cosine_scores = util.cos_sim(all_embeddings[id1].cpu().numpy(), all_embeddings[id2].cpu().numpy())
    score = np.array(cosine_scores)
    score[score<0] = 0
    mean_rows = np.mean(score, axis=1)
    final_score = np.mean(mean_rows)
    return final_score

def compute_similarity(song_id1, song_id2):
    score = float(computeCosineSimilarity(song_id1, song_id2))
    return score

print("compute similarity:")
size = len(all_songs)
scores = np.ones((size,size))
flatten_scores = []
columns = []
for i in tqdm(range(size-1)):
    columns.append(all_songs[i]["id"])
    for j in range(i+1,size):
        song1 = all_songs[i]
        song2 = all_songs[j]
        score = compute_similarity(song1["id"], song2["id"])
        flatten_scores.append(score)
        scores[i][j] = score
        scores[j][i] = score
columns.append(all_songs[size-1]["id"])

scaler = MinMaxScaler()
np_flatten_scores = np.array(flatten_scores).reshape(-1, 1)
scaler.fit(np_flatten_scores)
scaled_scores = scaler.transform(np_flatten_scores)

index = 0
for i in range(size-1):
    for j in range(i+1,size):
        scores[i][j] = scaled_scores[index][0]
        scores[j][i] = scaled_scores[index][0]
        index+=1

df = pd.DataFrame(scores, columns=columns, index=columns)
df.to_csv("matrix.csv")
        
