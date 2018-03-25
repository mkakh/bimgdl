from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import json
import os
import sys
import requests
import imghdr

argv = sys.argv
argc = len(argv)
if argc != 2:
    print("Usage: python", argv[0], "searchterm")
    exit(1)

searchterm = sys.argv[1]
pic_num = 1000 #目安

url = "https://www.bing.com/images/search?q="+searchterm+""
# NEED TO DOWNLOAD CHROMEDRIVER, insert path to chromedriver inside parentheses in following line
options = webdriver.ChromeOptions()
options.add_argument("--kiosk")
browser = webdriver.Chrome(chrome_options=options)
browser.get(url)

header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
counter = 0
succounter = 0

# ループ回数とスリープ時間は環境依存
for _ in range(pic_num // 30 + 1):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)");
    sleep(1)

if not os.path.exists(searchterm):
    os.mkdir(searchterm)

for x in browser.find_elements_by_xpath('//a[@class="iusc"]'):
    counter = counter + 1
    print("Total Count:", counter)
    print("Succsessful Count:", succounter)
    print("URL:", json.loads(x.get_attribute('m'))['murl'])
    img = json.loads(x.get_attribute('m'))['murl']
    try:
        req = requests.get(img, params={'User-Agent': header})
        raw_img = req.content
        imgtype = imghdr.what(None, h=raw_img)
        with open(os.path.join(searchterm , searchterm + "_" + str(counter) + "." + imgtype), "wb") as f :
            f.write(raw_img)
            succounter = succounter + 1
    except:
        print("can't get img")

print(succounter, "pictures succesfully downloaded")
browser.execute_script('window.alert("finish!")')
browser.close()
