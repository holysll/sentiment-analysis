# -*- coding:utf-8 -*-

import urllib
import json
import time
import re
import pandas as pd
import sys

reload(sys)
sys.setdefaultencoding('GBK')

#伪装成登陆
headers ={
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
	'Cookie':'unick=holysll; _pst=holysll_m; ipLoc-djd=1-72-4137-0; ipLocation=%u5317%u4EAC; areaId=1; unpl=V2_ZzNtbURfRRd0DkZVchhfB2IGRVwRVxZFJQ4TA3NNCAVuBBNeclRCFXIURlRnGFwUZwsZX0dcRxVFCHZUehhdBGYBFV5GZxpFKwhFVidSbDVkAyJVcldGEXEJTldyEVo1VwQibXJWcxRFCXYfFRgRBWIHFlxKVEodczhHZHg%3d; CCC_SE=ADC_FZq9mJ4sEkaxhxOqVHCZbz0Erz5Ndv7vQfklm8yoYpT5hKg4VvU7%2b18sytPB%2fVQKRWztAUWfQP8xE9z4y%2fa%2b2vt54NS%2bfiS9D1tpNn2Yk%2fev9C8UnPNjNMeNjUk4wo29ADxfI9EvCsZRKUXb2uiMifg5AzNbE1ZqFQZZmoy5PwKzXoNbR4vXe9tT15nX0oE8O46LnJp2f%2bmsPbKvqruY%2brR%2f%2bLWqSR1tZ%2fokP40KZZRkGupZzV6p1wgU706y4Sz54qnpF7jIPkmOmJyNG3bmxccMkbmTlzNRzjGmvhXkM9gjBbHt%2bnXi%2bFV0Hkg8RaHu0T%2brooLWSdVrVz1xebZqLQxmsTex1xXGz2RFx8XnKAskRJ%2fOEoSyBV4n3gO0aavMXXdDlbi5hAd52wyFS7ZenVQN%2bA%2fyQerBMIJffhJcay8%2fMvbZAsVE7KadTIwum7tO; __jdv=122270672|www.hao123.com|t_1000003625_hao123mz|tuiguang|79730710802344f0b1daa7df9ee18602|1478000091571; user-key=bca5c199-c103-427d-8cfd-fe90488cc461; cn=11; __jda=122270672.1455092897.1477990349.1477999077.1478000092.3; __jdb=122270672.8.1455092897|3.1478000092; __jdc=122270672; atw=798.647948.123|6223.10491603368.9|1047.10571396873.-1|1105.1466274.-64; thor=907C9238B6B1D8BC1D8128767A19410CEC56C91B0E3B8EED476AE61FCAD5E60CB6A2A7D1A1FD2B4B7133CAA8A23A580FCB26A65BDBDD86C0D816300393B55891E4F244A51E27CFF2D6ACF17DEE30E07247FFEDED7B1AD6D5A72068FA12FD2D5B5603D3A02321C5C7797E4F4F5EAC36DE67DF83793269834D389E6EA415F3E788BC7D9D5101E3F3D8506711464F3543A7; __jdu=1455092897',
}

d_datetime, d_score, d_review = [], [], []

#输入商品的ID和页码
pid = "5174523"
pages = 10

#进入json评论数据库
for page in range(1, pages + 1):
	print "page %i ..." % page    #输出页码
	url = 'http://s.club.jd.com/productpage/p-'+ pid +'-s-0-t-0-p-'+str(page)+'.html?'
	html = urllib.urlopen(url).read()  #读取json数据
	data = json.loads(html.decode('gbk','ignore'))  #json数据解码
	time.sleep(2)  #自动休眠
	comment_txt = data['comments']
	for x in comment_txt: #根据关键词取评论时间,评论内容和得分
		d_datetime.append(x['creationTime'])
		d_score.append(x['score'])
		d_review.append(x['content'])

#保存数据为csv格式
import csv
df = pd.DataFrame({"datetime": d_datetime,
				   "score": d_score,
				   "review": d_review})
df.to_csv('5174523.csv', index=False)

print "done.."

#已完成，声音提示
import winsound
winsound.Beep(600, 2000)