from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

id_search = ['odluke_forma_odjeljenje', 'odluke_forma_vrsta']

# python scraper.py >> names.txt

'''
odeljenje_values = ['2', '3']
krivicni_values = ['Kr', 'Kr-S']
gradjansko_values = ['R']
vrsta_odluke = 'O'
'''

name="vrsta_odluke"

browser = webdriver.Chrome(executable_path="chromedriver.exe")

browser.get("http://sudovi.me/")
browser.find_element_by_xpath("//select[@id='izaberi_sud']/option[@value='sudovi-crne-gore']").click()
browser.find_element_by_xpath('//a[@href="'+'/odluke/'+'"]').click()
browser.find_element_by_xpath('//a[@id="'+'odluke_detaljna_pretraga'+'"]').click()

try:
    WebDriverWait(browser, 5).until(ec.visibility_of_element_located((By.XPATH, '//select[@id="odluke_forma_vrsta"]/option[@value="K-S"]')))
    
    browser.find_element_by_xpath('//select[@id="odluke_forma_vrsta"]/option[@value="K-S"]').click() #K
except TimeoutException:
    browser.quit()

try:
    WebDriverWait(browser, 5).until(ec.visibility_of_element_located((By.XPATH, '//select[@name="vrsta_odluke"]/option[@value="O"]')))
except TimeoutException:
    browser.quit()


browser.find_element_by_xpath('//select[@name="vrsta_odluke"]/option[@value="O"]').click()
browser.find_element_by_xpath('//input[@id="odluke_forma_submit"]').click()

try:
    WebDriverWait(browser, 10).until(ec.visibility_of_element_located((By.ID, 'ucitaj_odluke_pretraga')))
except TimeoutException:
    browser.quit()

while True:    
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #try:
    #WebDriverWait(browser, 10).until(ec.visibility_of_element_located((By.ID, 'ucitaj_odluke_pretraga')))
    #except TimeoutException:
    #    browser.quit()
    
    try:
        elem = browser.find_element_by_id("ucitaj_odluke_pretraga")
    except NoSuchElementException:
        break

    if elem is None:
        break
        
    #browser.find_element_by_class_name("wrapper").send_keys(Keys.END)
    
    try:
        WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.ID, 'ucitaj_odluke_pretraga')))
    except TimeoutException:
        browser.quit()
    
    elem.click()
    time.sleep(3)

for element in browser.find_elements_by_class_name("pogledajte_odluku"):
    print(element.get_attribute("name"))

browser.quit()