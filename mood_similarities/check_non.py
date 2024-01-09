import numpy as np
import pandas as pd
import os 
from tqdm import tqdm
from pandas import DataFrame
if __name__ == '__main__':
    dir_path = r"C:\Users\yale\Desktop\bigdata\spotify_preview_target_non_dup"
    check_blue_path = r"C:\Users\yale\Desktop\bigdata\blues_non_duplicated.csv"
    check_rap_path = r"C:\Users\yale\Desktop\bigdata\rap_non_duplicated.csv"
    check_blue = pd.read_csv(check_blue_path)
    check_rap = pd.read_csv(check_rap_path)
    check = pd.concat([check_blue, check_rap])
    #check = check['spotify_id']
    check.index = range(len(check))
    check_lst = []
    check_n = 0
    for file_name in tqdm(os.listdir(dir_path)):
        song_id = file_name.split('-')[-1].replace('.mp3','')
        for i, row in check.iterrows():
            if song_id == row['spotify_id']:
                check_lst.append({'spotify_id' : row['spotify_id'], 'name' : row['name']})
            else:
                continue
    output_df = DataFrame(check_lst)
    #output_df.columns = ['spotify','name']
    output_df.to_csv(r'C:\Users\yale\Desktop\bigdata\spotify_preview_target_non.csv')
    print(output_df)