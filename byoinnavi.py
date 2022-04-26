import requests
from bs4 import BeautifulSoup
import math
import pandas as pd 
import time
import csv

HEADER = ['name', 'tel', 'address', "link"]

base_url = "https://byoinnavi.jp/tokyo/bunkyoku/000?p="
headers = {
    'User-Agent':'Mozilla/5.0'
}
#デフォルトだと403エラーが返ってきたのでヘッダー情報を追加
res = requests.get(url=base_url, headers=headers)
res.encoding = res.apparent_encoding
soup = BeautifulSoup(res.text, 'html.parser')

#全体の病院数からページ数を算出
max_num = soup.find("span", class_="count_total").text.split("件")[0]
page_num = math.ceil(int(max_num)/15)
count = 1


#csvに書き出し
with open('hospitals.csv', 'w', encoding='utf-8') as f:
  writer = csv.writer(f)
  writer.writerow(HEADER)
  while count <= page_num:
    url = base_url + str(count)
    res = requests.get(url=url, headers=headers)
    time.sleep(2)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'html.parser')

    hospitals = soup.find_all("div", class_="corp corp_type_clinic corp_status_opened")

    for hospital in hospitals:
      name = hospital.find("a", class_="corp-title__name").text.replace('\n', '')
      tel = hospital.find("div", class_="corp_tel").text.replace('\n', '')
      add = hospital.find("div", class_="corp_address")
      add.find("span").decompose()
      address = add.text.replace('\n', '')
      hp = hospital.find("a", text="ホームページへ")
      if hp is None:
        link = 'HPはありません。'
      else:
        link = hp.get('href')

      row = [name, tel, address, link]
      writer.writerow(row)
    count += 1

df = pd.read_csv('hospitals.csv')
print(df)
  




