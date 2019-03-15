# -*- coding utf-8 -*-

import pandas as pd

def count_rate(df,out_file,col):
    sum_list = df.sum()
    sum = sum_list[1]+sum_list[2]+sum_list[3]+sum_list[4]
    kv = {}
    for index in range(len(df)):
        key = df.loc[index,"key"]
        sum_row = df.loc[index,col].sum()
        rate = sum_row/sum
        rate = float('%.7f' % rate)
        kv[key]=rate
    # print(kv)
    with open(out_file, "w",encoding="utf-8") as f:
        f.write("key,rate\n")
        for k1,v1 in kv.items():
                f.write(k1+","+str(v1)+"\n")

if __name__ == "__main__":
    count_num_df = pd.read_csv('score_data/count_rate_data.csv', header=0, sep=',')
    count_num_16_df = count_num_df[["key","1601","1602","1603","1604"]]
    count_num_17_df = count_num_df[["key", "1701", "1702", "1703", "1704"]]
    # print(count_num_16_df.sum())
    # print(count_num_17_df.sum())
    count_rate(count_num_16_df, 'score_data/count_rate_16.csv',["1601","1602","1603","1604"])
    count_rate(count_num_17_df, 'score_data/count_rate_17.csv', ["1701", "1702", "1703", "1704"])