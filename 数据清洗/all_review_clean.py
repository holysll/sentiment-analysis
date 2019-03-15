# -*- coding utf-8 -*-

import re

def clean_info(info):
    '''
    清洗评论数据,包括去除数据中的数字、英文字母、或者标点等
    :param info:每一行的评论数据
    :return:清洗后的数据
    '''
    # 匹配所有不是汉字的字符,并将其换成" ",之后在将多个" "换成"，"
    info = re.sub(u'[^\u4E00-\u9FA5]', " ", info).strip()
    info = re.sub('\s+','，',info)
    return info

def regularize_data(file_input_name,file_output_name):
    '''
    提取商品评价数据,清洗数据,并写入目标文件中
    :param file_input_name: 输入文件
    :param file_output_name: 输出文件
    :return: None
    '''
    # 正则表达式匹配出时间和分数
    time_pattern = re.compile(r'\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}')
    score_pattern = re.compile(r',\d,')
    f = open(file_input_name,encoding="utf-8")
    f_output = open(file_output_name, mode='w')
    try:
        f_output.write('time,score,Info\n')
        time= score = info = ''
        for line in f:
            line = line.strip()
            if line:
                time_list = re.findall(pattern=time_pattern, string=line)
                score_list = re.findall(pattern=score_pattern, string=line)
                # 判断前两个字段是否为空
                if time_list and score_list:
                    time = time_list[0]
                    score = score_list[0]
                    info = line.replace(time,"").replace(score,"")
                    #判断原始数据中的评论是否为空
                    if info:
                        info = clean_info(info)
                        #判断清洗完后的评论数据是否为空
                        if info:
                            info = '%s,%s,%s\n' % (time,score.replace(",",""),info)
                            f_output.write(info)
    finally:
        f.close()
        f_output.close()
if __name__ == "__main__":
    regularize_data("all_reviews.csv","all_reviews_clean.csv")
