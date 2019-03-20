from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import tkinter as tk
from tkinter import filedialog
import time
import os

browser = webdriver.Chrome(executable_path="chromedriver.exe")

url = "http://sudovi.me/odluka_prikaz.php?id="

def find_judgement_ids_files():
    root = tk.Tk()
    root.withdraw() 
    judgementIdsPath = filedialog.askdirectory() 

    for ids_file_name in os.listdir(judgementIdsPath):
        if ids_file_name.endswith(".txt"):
            read_judgement_ids_file(judgementIdsPath, ids_file_name)

    browser.close()

def read_judgement_ids_file(judgementIdsPath, ids_file_name):
    judgement_data_folder_name = ids_file_name.replace(".txt","")
    judgement_data_folder_path = judgementIdsPath+"/"+judgement_data_folder_name
    if not os.path.exists(judgement_data_folder_path):
        os.makedirs(judgement_data_folder_path)

    ids_file = open(judgementIdsPath+"/"+ids_file_name, "r")
    get_textAndmeta(ids_file,judgement_data_folder_path)
    ids_file.close()

def get_textAndmeta(ids_file,judgement_data_folder_path):
    ids = ids_file.readlines()
    for id in ids:
        idStrip = id.rstrip()

        json_path = judgement_data_folder_path + "/" + "presuda_meta_" + idStrip + ".json"
        html_path = judgement_data_folder_path + "/" + "presuda_html_" + idStrip + ".txt"

        if not os.path.isfile(json_path) or not os.path.isfile(html_path):
            browser.get(url+idStrip)

        if not os.path.isfile(json_path):
            json_file = open(json_path, "w+", encoding = "UTF-8")
            get_meta(json_file)
            json_file.close()

        if not os.path.isfile(html_path):
            html_file = open(html_path, "w+", encoding = "UTF-8")
            get_text(html_file)
            html_file.close()

def get_meta(json_file):
    indexes = range(len(browser.find_elements_by_class_name("labela")))
    meta = {}
    for index in indexes:
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

    json_file.write(str(meta))


def get_text(html_file):
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
            return

    html_file.write(txt)

if __name__ == "__main__":
    find_judgement_ids_files()