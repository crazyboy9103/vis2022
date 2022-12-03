import pandas as pd 
import numpy as np
import json
import os 
import re
import pickle

json_path = './data/job_posting'

# load json files 
json_lists = os.listdir(json_path)
jsons = []
for j in json_lists:
    with open(os.path.join(json_path, j), 'r') as f:
        jsons.append(json.load(f))


# 스킬셋, 복지 리스트 
tools, welfares = set(), set()

for j in jsons:
    try:
        tools = tools | set(j['tools'])
    except:
        pass
    
    try:
        welfares = welfares | set([x.split('#')[1] for x in j['tags']])
    except:
        pass   


# 경력, 학력, 전공, 스킬셋, 복지 뽑아내는 전처리 함수 정의 

# 1) 항목별 키워드 정의
경력 = re.compile('\d년')
학력 = re.compile('학사|대졸|석사|박사|무관')
전공 = re.compile('무관|컴퓨터[\w|\s]*학|[\w|\s]*통계[\w|\s]*학|[\w|\s]*경영[\w|\s]*학|[\w|\s]*데이터[\w|\s]*학')

# 스킬셋, 복지: 태그에 있는 내용 활용하기 
skill_list = '|'.join(s for s in tools)
skill_list = skill_list.replace('+', '\+')
스킬셋 = re.compile(skill_list)

welfare_list = '|'.join(w for w in welfares)
복지 = re.compile(welfare_list)

# 2) 전처리 함수 정의
def ids(j):
    subs = j['id']
    return subs 
    
def sub_category(j):
    subs = j['sub_categories']
    subs = [subs[i] for i in range(len(subs)) if i % 2 ==1]  # 한국어 - 영어 중복 처리 
    subs = set(subs)
    return subs
    
def industry(j):
    subs = j['industry']
    return subs
    
def work_exp(j):
    experiences = 경력.findall(j)
    experiences = [int(x.split('년')[0]) for x in experiences]
    
    return min(experiences) if experiences else 0

def edu(j):
    edu_dict = {'무관':0, '대졸':1, '학사':1, '석사':2, '박사':3}
    educations = 학력.findall(j)
    educations = [edu_dict[x] for x in educations]
    return min(educations) if educations else 0

def major(j):
    return set(전공.findall(j))

def skill(j):
    return set(스킬셋.findall(j))

def welfare(j):
    j = j.replace(' ', '')  # 띄어쓰기 다 없애기 -> 태그 찾기 
    return set(복지.findall(j))


# json 파일 중 필요한 정보만 담고 있는 데이터 프레임 만들기  (*DF row 한개 당 공고 하나)
def json_to_dict(json_list):
    df = {'id':[],'업종':[], '세부직무':[], '경력':[], '학력':[], '전공':[], '스킬셋':[], '복지':[]}
    
    for j in json_list:
        df['id'].append(ids(j))
        df['세부직무'].append(sub_category(j))
        df['업종'].append(industry(j))
        
        j = str(j)
        df['경력'].append(work_exp(j))
        df['학력'].append(edu(j))
        df['전공'].append(major(j))
        df['스킬셋'].append(skill(j))
        df['복지'].append(welfare(j))
    
    return pd.DataFrame(df)


if __name__ == '__main__':
    wanted_df = json_to_dict(jsons)

    with open('./data/wanted_preprocessed.pickle', 'wb') as f:
        pickle.dump(wanted_df, f)