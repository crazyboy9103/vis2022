def cal_index(df, mine, col):
    idx = 0
    # 요구되는 사항 중 내가 가지고 있는 사항하고 겹치는 개수 세기 
    for c in col:
        idx += len(set(mine) & set(df[f'{c}'].split(', ')))

    return idx