'''

'''
import pandas as pd
from tqdm import tqdm
import ast

TAGS_PATH = './data/tags.csv'
NON_DUP_PATH = './data/spotify_preview_target_non.csv'
TARGET_SIMI_PATH = './runs/jaccard.csv'


def to_simi():
    simi_dct = {}
    simi_df = pd.DataFrame()
    tags_dct = pd.read_csv(TAGS_PATH, sep=';')[
        ['song_spotify_id', 'tag']].groupby(['song_spotify_id']).agg({'tag': lambda x:  x}).to_dict()['tag']
    id_lst = pd.read_csv(NON_DUP_PATH).sort_values(
        by=['spotify_id'])['spotify_id'].to_list()
    for i, id in tqdm(enumerate(id_lst)):
        if id in tags_dct:
            tags = tags_dct[id]
            for i, t_id in enumerate(id_lst[i:]):
                if t_id in tags_dct:
                    t_tags = tags_dct[t_id]
                    simi = jaccard_sim(tags, t_tags)
                    simi_dct[(id, t_id)] = simi
    simi_df = pd.Series(simi_dct).unstack()
    simi_df = simi_df.combine_first(simi_df.T).fillna(1.0)
    simi_df.to_csv(TARGET_SIMI_PATH)


def jaccard_sim(tags: list[str], t_tags: list[str]):
    s1 = set(tags)
    s2 = set(t_tags)
    return 0 if len(s1.union(s2)) == 0 else float(len(s1.intersection(s2)) / len(s1.union(s2)))


if __name__ == '__main__':
    to_simi()
