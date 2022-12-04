
from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from collections import Counter
from konlpy.tag import * 

def cal_index(df, mine, col):
    idx = 0
    # 요구되는 사항 중 내가 가지고 있는 사항하고 겹치는 개수 세기 
    for c in col:
        idx += len(set(mine) & set(df[f'{c}'].split(', ')))

    return idx

# https://medium.com/analytics-vidhya/text-summarization-using-a-wordcloud-deployed-on-streamlit-cbce2f411c24
# https://blog.naver.com/PostView.nhn?blogId=vi_football&logNo=221775297963&parentCategoryNo=&categoryNo=1&viewDate=&isShowPopularPosts=true&from=search

def word_count(cluster_df, col_name):
    if col_name == '업종':
        cluster_col = []
        for sub_cat in cluster_df[col_name]:
            cluster_col.append(sub_cat)
    else:
        cluster_col = []
        for sub_cat in cluster_df[col_name]:
            cluster_col.extend(list(sub_cat))
            
    count = Counter(cluster_col).most_common()  # 카운트 후 빈도순 정렬
    count = pd.DataFrame(count)       # df형태로 만들기
    count.columns = ['word','count'] 
    
    words = []
    for i in range(len(count)):
        word = dict()
        word['text'] = count.iloc[i]['word']
        word['value'] = int(count.iloc[i]['count'])
        words.append(word)
    return words