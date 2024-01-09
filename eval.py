# %%

import matplotlib.pyplot as plt
import pandas as pd
import os
from tqdm import tqdm
import os
import numpy as np
# %%
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, FloatType
import ast
# %%
tags_df_path = './data/id_target_jaccard.csv'
mood_df_path = './data/id_mood_simi.csv'
lyrics_df_path = './data/id_lyrics_simi.csv'
genre_df_path = './data/id_genre_simi.csv'
inst_df_path = './data/id_instruments_simi.csv'


def map_keys(row: Row):
    '''get all 
    args:
        row: Row
    '''
    dct = row.asDict()
    return dct.pop('id')


def map_id(row: Row):
    dct = row.asDict()
    id = dct.pop('id')
    dct.pop(id)
    dct.pop('_c0')
    return (id, dct)


def reduce_to_sum(row0_dct: dict, row1_dct: dict) -> dict:
    res = dict()
    for key in set(list(row0_dct.keys()) + list(row1_dct.keys())):
        sc0, sc1 = row0_dct.get(key, 0.0), row1_dct.get(key, 0.0)
        res[key] = float(sc0) + float(sc1)
    return res


def rm_zero_and_sorted(row_dct: dict) -> list:
    '''remove score zero and return nested list
    nested list means the same value
    '''
    sorted_lst = [(key, score) for key, score in row_dct.items() if score > 0]
    sorted_lst = sorted(sorted_lst, key=lambda x: x[1], reverse=True)
    res = []
    for key, score in sorted_lst:
        if len(res) < 1:
            res.append([(key, score)])
            continue
        if res[-1][-1][1] != score:
            res.append([(key, score)])
        else:
            res[-1].append((key, score))
    return res


def rm_score(row_lst: list) -> list:
    res = []
    for s_lst in row_lst:
        l = []
        for key, _ in s_lst:
            l.append(key)
        res.append(l)
    return res


def hits_at_k(k: int, tar_lst_of_tuple, hat_lst_of_tuple):
    '''readability 0 :)
    args
        k: int, hits at k
        tar_lst_of_tuple: list[tuple[str, lst[lst[str]]]]
            list, each of tuple represent each spo id
            tuple, spo id and its list of sorted similarity spo id
            list, list of sorted similarity spo id
            list, same value will be in the same bracket
        hat_lst_of_tuple: list[tuple[str, lst[lst[str]]]]
            as same as the top

    returns
        float, accuracy of hits at k
    '''
    hits_lst = []
    for spo_id, tar_ids in tar_lst_of_tuple:
        for h_spo_id, hat_ids in hat_lst_of_tuple:
            if spo_id != h_spo_id:
                continue
            target_y = []
            for id_lst in tar_ids:
                if len(target_y) > k:
                    break
                target_y.extend(id_lst)
            print('target_y', len(target_y))
            if len(target_y) > 0:
                hits = 0
                cur_k = 0
                for id_lst in hat_ids:
                    for h_y in id_lst:
                        if h_y in target_y:
                            hits += 1
                            print(h_y)
                    cur_k += len(id_lst)
                    if cur_k > k:
                        print(cur_k)
                        break
                hits_lst.append(hits)
                break
    return 0.0 if len(hits_lst) == 0 else sum(hits_lst) / len(hits_lst)


if __name__ == '__main__':
    conf = SparkConf()
    conf.setMaster(
        'local[8]').setAppName('Evalation')
    sc = SparkContext(conf=conf)
    sc.setLogLevel("ERROR")
    spark = SparkSession(sc)
    tags_rdd = spark.read.csv(tags_df_path, sep=',', header=True).rdd
    mood_df = spark.read.csv(mood_df_path, sep=',', header=True)
    inst_df = spark.read.csv(inst_df_path, sep=',', header=True)
    genre_df = spark.read.csv(genre_df_path, sep=',', header=True)
    lyrics_df = spark.read.csv(lyrics_df_path, sep=',', header=True)

    #! the type of cell is str
    # for field in mood_df.schema.fields:
    #     if str(field.dataType) in ['DoubleType', 'FloatType', 'LongType', 'IntegerType', 'DecimalType']:
    #         name = str(field.name)
    #         mood_df = mood_df.withColumn(name, col(name) * 2)

    all_rdd = mood_df.unionByName(genre_df, allowMissingColumns=True)\
        .unionByName(inst_df, allowMissingColumns=True)\
        .unionByName(lyrics_df, allowMissingColumns=True)\
        .fillna('0')

    del mood_df
    del inst_df
    del genre_df
    del lyrics_df

    keys = tags_rdd.map(lambda row: map_keys(row)).collect()
    print(len(keys))
    print(type(keys))
    print(keys[0])
    print(type(keys[0]))

    print(all_rdd.count())
    print(len(all_rdd.columns))

    all_simi = all_rdd.rdd\
        .map(lambda row: map_id(row))\
        .filter(lambda row: row[0] in keys)\
        .map(lambda row: (row[0], {k: v for k, v in row[1].items() if k in keys}))\
        .reduceByKey(lambda simis0, simis1: reduce_to_sum(simis0, simis1))\
        .mapValues(lambda simis: rm_zero_and_sorted(simis))\
        .mapValues(lambda lst: rm_score(lst))\
        .collect()

    print(len(all_simi))
    print(len(all_simi[0][1]))

    tags_simi = tags_rdd.map(lambda row: map_id(row))\
        .map(lambda row: (row[0], {k: float(v) for k, v in row[1].items()}))\
        .mapValues(lambda simis: rm_zero_and_sorted(simis))\
        .mapValues(lambda lst: rm_score(lst))\
        .collect()
# %%
ks = [1, 5, 10, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
# hits_k = [hits_at_k(k, tags_simi, all_simi)/k for k in ks]
hits_k = [0.08759124087591241, 0.04470802919708029, 0.06715328467153284, 0.13099908759124088,
          0.19432709854014596, 0.24257147201946472, 0.278654197080292, 0.30063777372262773]
hits_k = [0.0770985401459854, 0.04452554744525548, 0.0614963503649635, 0.1373859489051095,
          0.1998426094890511, 0.23799270072992704, 0.2603775091240876, 0.2800474452554744]
print(hits_k)

fig, ax = plt.subplots()
bar_colors = ['tab:orange', 'tab:orange', 'tab:orange', 'tab:orange']

ax.bar([str(k) for k in ks], hits_k,  color=bar_colors)
ax.set_ylabel('Accuracy')
ax.set_title('Number of K')

plt.show()

# %%
