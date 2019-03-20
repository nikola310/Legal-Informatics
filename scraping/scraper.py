from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import tkinter as tk
from tkinter import filedialog
import time

browser = webdriver.Chrome(executable_path="chromedriver.exe")

def remove_unsupported_file_chars(filename):
    return filename.replace("/","").replace("\\","").replace(":","").replace("*","").replace("?","").replace("\"","").replace("<","").replace(">","").replace("|","")

def get_judgement_identifiers():

    global folderPath

    root = tk.Tk()
    root.withdraw() 
    folderPath = filedialog.askdirectory() 

    browser.get("http://sudovi.me/")
    browser.find_element_by_xpath("//select[@id='izaberi_sud']/option[@value='sudovi-crne-gore']").click()
    browser.find_element_by_xpath('//a[@href="/odluke/"]').click()

    access_search_form()

    browser.quit()

def access_search_form():

    browser.find_element_by_xpath('//a[@id="odluke_detaljna_pretraga"]').click()

    try:
        WebDriverWait(browser, 5).until(ec.visibility_of_element_located((By.ID, 'odluke_forma_vrsta')))  
        selects = browser.find_elements_by_xpath('//select[@id="odluke_forma_vrsta"]/option')
    except TimeoutException:
        browser.quit()

    try:
        WebDriverWait(browser, 5).until(ec.visibility_of_element_located((By.XPATH, '//select[@name="vrsta_odluke"]/option[@value="O"]')))
        browser.find_element_by_xpath('//select[@name="vrsta_odluke"]/option[@value="O"]').click()
    except TimeoutException:
        browser.quit()

    get_judgement_identifiers_for_case_types(selects)


def get_judgement_identifiers_for_case_types(selects):
    
    for select in selects:

        if select.get_attribute('value') == "" or select.get_attribute('value') != "U":
            continue

        select.click()
        time.sleep(1)
        browser.find_element_by_xpath('//input[@id="odluke_forma_submit"]').click()

        judgement_elements = 50
        while(True):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                WebDriverWait(browser, 30).until(ec.visibility_of_element_located((By.XPATH, '//a[@id="ucitaj_odluke_pretraga"][@name="'+str(judgement_elements)+'"]')))
                browser.execute_script("$('a[#ucitaj_odluke_pretraga][name=\""+str(judgement_elements)+"\"]').trigger('click')")
                judgement_elements+=50
            except TimeoutException:
                break

        write_judgement_identifiers_to_file(select)
        
def write_judgement_identifiers_to_file(select):

    if not browser.find_elements_by_xpath("//div[contains(text(), 'Nema podataka za tražene uslove.')]"):

        f_names = open(folderPath+"/"+remove_unsupported_file_chars(select.text.strip())+".txt", "w+", encoding = "UTF-8")

        elements = browser.execute_script("return $('.pogledajte_odluku')")
        for element in elements:
            f_names.write(element.get_attribute("name")+"\n")

        f_names.close()

if __name__ == "__main__":
    get_judgement_identifiers()