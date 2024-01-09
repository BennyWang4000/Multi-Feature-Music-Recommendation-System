import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
if __name__ == '__main__':
    filepath = r"C:\Users\yale\Desktop\bigdata\prediction\pred_trans.csv"
    mood = pd.read_csv(filepath)
    print(mood['Song'][0])
    mood_arr = mood['Score'].to_numpy()
    print(mood_arr)
    #cosine_sim_matrix = cosine_similarity(mood_arr.reshape(-1, 1), mood_arr.reshape(-1, 1))
    sim_matrix = []
    for i in range(len(mood_arr)):
        row = []
        for j in range(len(mood_arr)):
            if mood_arr[i] == mood_arr[j]:
                output = 1
            else:
                output =0
            row.append(output)
        sim_matrix.append(row)
    # sns.heatmap(pd.DataFrame(sim_matrix), annot=True, cmap="YlGnBu")
    # plt.show()
    # print(pd.DataFrame(sim_matrix))
    sim_df = pd.DataFrame(sim_matrix)
    song_id = []
    for filename in tqdm(mood['Song']):
        name = filename.split('-')[-1].replace('.mp3','')
        song_id.append(name)
    sim_df.columns = song_id
    sim_df.index = song_id
    sim_df.to_csv(r'C:\Users\yale\Desktop\bigdata\prediction\pred_sim.csv')