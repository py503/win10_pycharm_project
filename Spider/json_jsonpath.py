import requests
import json
import jsonpath

url = "https://www.lagou.com/lbs/getAllCitySearchLabels.json"
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        }
response = requests.get(url, headers=headers)
html = response.text
# 把json形式的字符串转换成python形式的Unicode字符串
unicodestr = json.loads(html)
# 通过jsonpath找出所有"name"的内容,是python形式的列表
city_list = jsonpath.jsonpath(unicodestr, "$..name")

# for item in city_list:
#     print(item)

# dumps()默认中文为ascii编码格式,ensure_ascill默认为Ture
# 禁用ascii编码格式,返回的Unicode字符串,方便使用
array = json.dumps(city_list, ensure_ascii=False)
print(array)
# 以json保存,且是utf-8
with open("lagoucity.json", "w",encoding="utf-8") as f:
    f.write(array)
    print("保存完成")