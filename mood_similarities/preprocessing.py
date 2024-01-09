import numpy as np
import pandas as pd
import os 
import filecmp
if __name__ == '__main__':
    # blue_filepath = r"C:\Users\yale\Desktop\bigdata\blues_non_duplicated.csv"
    # rap_filepath = r"C:\Users\yale\Desktop\bigdata\rap_non_duplicated.csv"

    # blue_new_file = pd.read_csv(blue_filepath, sep=',')
    # rap_new_file = pd.read_csv(rap_filepath, sep=',')
    # new_file = pd.concat([blue_new_file, rap_new_file])
    # print(new_file)
    # file_new_name = new_file['name']
    # print(file_new_name)
    check_path = r"C:\Users\yale\Desktop\bigdata\spotify_preview_target_test"
    file_list = []
    count=0
    for folder_name in os.listdir(check_path):
        folder_path = check_path + '\\' + folder_name 
        for i in os.listdir(folder_path):
            file_name = folder_path + '\\' +i
            file_list.append(file_name)
    #print(file_list)
    for x in file_list:
        for y in file_list:
            if x!=y and os.path.exists(x) and os.path.exists(y):
                if(filecmp.cmp(x,y)):
                    os.remove(y)
                    count+=1
    print("刪除", count)