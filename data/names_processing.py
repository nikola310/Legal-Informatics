from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os.path

browser = webdriver.Chrome(executable_path="chromedriver.exe")

url = "http://sudovi.me/odluka_prikaz.php?id="
FOLDER = "data\\"

text_file = open("names.txt", "r", encoding="UTF-16")
lines = text_file.readlines()
ids = [line for line in lines]
idsSet = set(ids)

for id in idsSet:
    id = id.rstrip()
    #id = "22256"
    browser.get(url+id)
    
    txt_path = FOLDER + "presuda_" + id + ".txt"
    if os.path.isfile(txt_path):
        continue

    f_txt = open(txt_path, "w+", encoding = "UTF-8")
    f_json = open(FOLDER + "presuda_meta_" + id + ".json","w+", encoding = "UTF-8")

    json = browser.find_elements_by_class_name('kontener')
    
    json = json[0]

    labels = browser.find_elements_by_class_name("labela")
    meta = {}
    index = 0
    for label in labels:
        key = browser.execute_script("return $('.labela')[" + str(index) + "].innerHTML;").split(":")[0]
        if index >= 6:
            siblings = browser.execute_script("return $('.labela').siblings('a');")
            value = []
            for sibl in siblings:
                temp = {}
                temp["id"] = sibl.get_attribute("href").split("=")[1]
                temp["text"] = sibl.get_attribute("innerHTML")
                value.append(temp)
        else:
            value = browser.execute_script("return $('.labela')[" + str(index) + "].nextSibling.data;").strip()
        meta[key] = value
        index+=1
    #print(meta)
    f_json.write(str(meta))

    f_json.close()

    try:
        div = browser.find_element_by_xpath('//div[@class="kontener"]/following-sibling::div')
        txt = div.get_attribute("innerHTML")
    except NoSuchElementException:
        try:
            frame = browser.find_element_by_xpath('//div[@class="kontener"]/following-sibling::iframe')
            browser.switch_to_frame(frame)
            txt = browser.find_element_by_tag_name("html").get_attribute("innerHTML")
        except NoSuchElementException:
            print("We have lost the battle!")
            continue

    f_txt.write(txt)
    f_txt.close()

    #break

browser.close()