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
# 스킬셋, 복지, 기업정보 리스트 
tools = set()

for j in jsons:
    try:
        tools = tools | set(j['tools'])
    except:
        pass
    
#     try:
#         welfares = welfares | set([x.split('#')[1] for x in j['tags']])
#     except:
#         pass    

welfares = set(['#야근없음','#유연근무','#주35시간', '#주4일근무','#육아휴직','#출산휴가','#리프레시휴가',
    '#성과급','#상여금','#연말보너스','#스톡옵션',
    '#수평적조직','#스타트업','#자율복장','#워크샵','#반려동물',
    '#조식제공','#중식제공','#석식제공','#시리얼','#식비','#음료','#맥주','#커피','#와인','#샐러드','#과일','#간식',
    '#사내카페','#사내식당','#주차','#수면실','#휴게실','#헬스장','#위워크','#수유실','#안마의자',
    '#어린이집','#보육시설','#생일선물','#결혼기념일','#대출지원',
    '#택시비','#차량지원','#원격근무','#셔틀버스','#기숙사','#사택','#재택근무',
    '#건강검진','#단체보험','#의료비','#운동비','#문화비','#동호회','#복지포인트',
    '#교육비','#직무교육','#세미나참가비','#컨퍼런스참가비','#자기계발','#도서구매비','#스터디지원','#어학교육','#해외연수',
    '#산업기능요원','#전문연구요원','#인공지능','#IoT','#핀테크','#푸드테크','#Macbook','#iMac','#노트북','#통신비'])

company_infos = set(['#연봉업계평균이상', '#연봉상위1%', '#연봉상위2~5%', '#연봉상위6~10%', '#연봉상위11~20%',
    '#누적투자100억이상',
    '#인원성장', '#인원급성장',
    '#퇴사율5%이하', '#퇴사율 6~10%',
    '#50명이하', '#51~300명', '#301~1,000명','#1,001~10,000명', '#10,001명이상',
    '#설립3년이하', '#설립4~9년', '#설립10년이상'])


# 경력, 학력, 전공, 스킬셋, 복지 뽑아내는 전처리 함수 정의 

# 1) 항목별 키워드 정의
경력 = re.compile('\d년')
학력 = re.compile('학사|대졸|석사|박사|무관')
전공 = re.compile('무관|컴퓨터공학|컴퓨터과학|통계학|응용통계학|경영학|데이터사이언스|데이터과학|수학|경영과학|데이터공학|기계공학|전자공학|이공계|소프트웨어관련|IT관련')

# 스킬셋, 복지: 태그에 있는 내용 활용하기 
skill_list = '|'.join(s for s in tools)
skill_list = skill_list.replace('+', '\+')
스킬셋 = re.compile(skill_list)
welfare_list = '|'.join(w.split('#')[1] for w in welfares)
복지 = re.compile(welfare_list)
company_info_list = '|'.join(w.split('#')[1] for w in company_infos)
기업정보 = re.compile(company_info_list)

# 2) 전처리 함수 정의
def ids(j):
    subs = j['id']
    return subs
    
    
def sub_category(j):
    subs = j['sub_categories']
    subs = [subs[i] for i in range(len(subs)) if i % 2 ==1]  # 한국어 - 영어 중복 처리 
    subs = set(subs)
#         return sub_str

#     subs = subs[1] if subs else '' # 일단은 첫번째만 빼옴
    
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
    # 띄어쓰기 다 없애기 -> 전공 찾기 
    j = j.replace(' ', '')
    majors = set(전공.findall(j))
    
#     if not majors:
#         majors = set(['무관'])
        
    return majors

def skill(j):
    
    return set(스킬셋.findall(j))

def welfare(j):
    
    # 띄어쓰기 다 없애기 -> 태그 찾기 
    j = j.replace(' ', '')
    
    return set(복지.findall(j))

def company_info(j):
    
    # 띄어쓰기 다 없애기 -> 태그 찾기 
    j = j.replace(' ', '')
    
    return set(기업정보.findall(j))


# json 파일 중 필요한 정보만 담고 있는 데이터 프레임 만들기  (*DF row 한개 당 공고 하나)
def json_to_dict(json_list):
    df = {'id':[],'업종':[], '세부직무':[], '경력':[], '학력':[], '전공':[], '스킬셋':[], '복지':[], '기업정보':[]}
    
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
        df['기업정보'].append(company_info(j))
    
    return pd.DataFrame(df)


if __name__ == '__main__':
    wanted_df = json_to_dict(jsons)

    with open('./data/wanted_preprocessed.pickle', 'wb') as f:
        pickle.dump(wanted_df, f)