"""
@version: 1.0
@author: liyao
@software: PyCharm
@time: 2017/7/5 11:36
"""

from zheye import zheye
z = zheye()


import requests
import shutil

h = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240'
}
import time

lp = []
lpp = []
s = requests.session()
web_data = s.get('http://www.zhihu.com/', headers=h).text
import re
match_obj = re.match('.*name="_xsrf" value="(.*?)"', web_data, re.DOTALL)
xsrf = ''
if match_obj:
    xsrf = (match_obj.group(1))
randomNum = str(int(time.time() * 1000))
r = s.get('https://www.zhihu.com/captcha.gif?r={}&type=login&lang=cn'.format(randomNum), headers=h,
          stream=True)
if r.status_code == 200:
    with open('pic_captcha.gif', 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

    positions = z.Recognize('pic_captcha.gif')
    print(positions)

captcha = {}
pos = positions
tmp = []
captcha['input_points'] = []
for poss in pos:
    tmp.append(float(format(poss[0] / 2, '0.2f')))
    tmp.append(float(format(poss[1] / 2, '0.2f')))
    captcha['input_points'].append(tmp)
    tmp = []

# print str(captcha)
params = {
    '_xsrf': xsrf,
    'password': 'admin321',
    'captcha': '{"img_size": [200, 44], "input_points": [[%.2f, %f], [%.2f, %f]]}' % (
        pos[0][1] / 2, pos[0][0] / 2, pos[1][1] / 2, pos[1][0] / 2),
    # 'captcha': str(captcha),
    'captcha_type': 'cn',
    'phone_num': '2222222222'
}
print (params)
r = s.post('https://www.zhihu.com/login/phone_num', headers=h, params=params)
import json
re_text = json.loads(r.text)
print (r.text)
