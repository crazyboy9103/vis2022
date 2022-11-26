
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

def cloud(text, max_word=10, max_font=20, random=5):
    okt = Okt()
    noun = okt.nouns(text)
    count = Counter(noun).most_common()  # 카운트 후 빈도순 정렬
    count = pd.DataFrame(count)       # df형태로 만들기
    count.columns = ['word','count'] 
    data = dict(zip(count['word'].tolist(), count['count'].tolist()))
    stopwords = set(STOPWORDS)
    # stopwords.update(['us', 'one', 'will', 'said', 'now', 'well', 'man', 'may',
    # 'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
    # 'put', 'seem', 'asked', 'made', 'half', 'much',
    # 'certainly', 'might', 'came'])
    
    wc = WordCloud(font_path = 'C:/WINDOWS/FONTS/HMKMRHD.ttf', background_color="white", max_words=30, width=400, height=200,
    stopwords=stopwords, max_font_size=20, random_state=5)
    cloud = wc.generate_from_frequencies(data) 
    # generate word cloud
    return cloud