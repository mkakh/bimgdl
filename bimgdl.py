from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import os
import sys
import requests
import imghdr

argv = sys.argv
argc = len(argv)
if argc != 3:
    print("Usage: python", argv[0], "searchterm", "pic_num")
    exit(1)

searchterm = sys.argv[1]
pic_num = int(sys.argv[2])

url = "https://www.bing.com/images/search?q="+searchterm+""
# NEED TO DOWNLOAD CHROMEDRIVER, insert path to chromedriver inside parentheses in following line
options = webdriver.ChromeOptions()
options.add_argument("--kiosk")
browser = webdriver.Chrome(chrome_options=options)
browser.get(url)

header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
counter = 0
succounter = 0

browser.execute_script("window.scrollTo(0, document.body.scrollHeight)");

if not os.path.exists(searchterm):
    os.mkdir(searchterm)

while succounter <= pic_num:
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
            with open(os.path.join(searchterm , searchterm + "_" + str(counter) + "." + imgtype), "wb") as File :
                File.write(raw_img)
                succounter = succounter + 1
        except:
            print("can't get img")
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)");

print(succounter, "pictures succesfully downloaded")
browser.execute_script('window.alert("finish!")')
browser.close()

