#packages
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
import time

#-----------------------------------------------------
data = pd.read_excel('Data for backyard_for upload.xlsx', sheet_name='Sheet1')
offset = 7 #excel rij - 2, laatste getal in site, reeks die je wil toevoegen - 1
species = 'Backyard poultry'
username = 'wannes.dewulf@ugent.be'
password = 'wannesdewulf12'
subcategorie = [8,18,24,36,39,45,49,55,58,64]
countrydownarrows = 19
grid = [45,47,69,70]
boxes = [5]
#----------------------------------------------------

# Open site
# open google driver
driver = webdriver.Chrome()

def inloggen():
    # officiele site
    driver.get('https://biocheckgent.com/en/user/login?destination=/en/dashboard')

    # test site
    # driver.get('https://biocheck.release.entityone.be/en/user/login')
    # time.sleep(5)

    #input credentials
    driver.find_element("id", "edit-name").send_keys(username, Keys.TAB, password, Keys.RETURN)

inloggen()

numberofrows = data.shape[0]

#functions to click on the correct places in the site
def starting_clicks(titel):
    driver.find_element(By.LINK_TEXT, 'Surveys').click()
    driver.find_element(By.LINK_TEXT, species).click()
    driver.find_element(By.XPATH, '//*[@id="edit-submit"]').click()
    wait(driver, 7).until(EC.element_to_be_clickable((By.ID, 'edit-title-0-value'))).send_keys(titel, Keys.TAB, Keys.TAB, Keys.RETURN,
                                                               Keys.ARROW_DOWN * countrydownarrows, Keys.RETURN)
    driver.find_element(By.ID, 'edit-field-permission-value').click()
    time.sleep(1.5)
    driver.find_element(By.ID, 'edit-submit').click()

def answer_radio(id, j):
    try:
        parent_element = wait(driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id^=" + id)))
        print(parent_element)
        child_elements = parent_element.find_elements(By.CLASS_NAME, 'option')
        teller = 0
        print(child_elements)
        for k in child_elements:
            teller += 1
            print('k.text= ', k.text)
            if k.text == j:
                print('correct k= ', k.text)
                rightanswerid = id + '-' + str(teller)
                wait(driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id^=" + rightanswerid))).send_keys(
                    Keys.SPACE)

    except TimeoutException:
        print('failed input radio')
        pass

def answer_radio(id, j):
    try:
        parent_element = wait(driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id^=" + id)))
        print(parent_element)
        child_elements = parent_element.find_elements(By.CLASS_NAME, 'option')
        teller = 0
        print(child_elements)
        for k in child_elements:
            teller += 1
            print('k.text= ', k.text)
            if k.text == j:
                print('correct k= ', k.text)
                rightanswerid = id + '-' + str(teller)
                wait(driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id^=" + rightanswerid))).send_keys(
                    Keys.SPACE)

    except TimeoutException:
        print('failed input radio')
        pass

def answer_num(id):
    try:
        wait(driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id^=" + id))).send_keys(j)
    except TimeoutException:
        print('failed input num')
        pass

def answer_box(j, id):
    parent_element = wait(driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id^=" + id)))
    child_elements = parent_element.find_elements(By.CLASS_NAME, 'option')
    print('boxes')
    print('j= ', j)
    for option in j.split('/'):
        teller = 0
        print('option= ', option)
        for k in child_elements:
            teller += 1
            print('k.text= ', k.text)
            if k.text == option:
                print('correct k= ', k.text)
                rightanswerid = id + '-' + str(teller)
                wait(driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id^=" + rightanswerid))).send_keys(Keys.SPACE)

def answer_grid(j, id):
    teller = 1
    for option in j.split('/'):
        id2 = id + '-' + str(teller)
        print(id2)
        answer_radio(id2, option)
        teller += 1
        print('option= ', option)

#apply row by row

for i in range(offset, numberofrows):
    #input is all answers for 1 biocheck
    input = data.values[i]
    titel = 'Automatic answer '+ '(' + str(i+1) + ') ' + str(input[0])
    input = input[1:]
    starting_clicks(titel)

    answercount = 0

    for j in input:

        if answercount in subcategorie:
            driver.find_element(By.ID, 'edit-next').click()
            print('newcat')

        print('\n', j)

        #options: radio buttons question, numeric question, no question, grid question (question doesn't start with XX.) multiple options questions


        #radio
        if (isinstance(j, str)) and not (answercount in grid) and not (answercount in boxes):
            id = 'edit-answer-' + str(answercount) + '-answer'
            print(id)
            answer_radio(id, j)

        #boxes
        if (answercount in boxes):
            id = 'edit-answer-' + str(answercount) + '-answer'
            answer_box(j, id)

        #grid
        if (answercount in grid):
            id = 'edit-answer-' + str(answercount) + '-answer'
            print('grid')
            answer_grid(j, id)

        #numeric
        if (isinstance(j,int) or isinstance(j,float)) and not (j != j):
            print('numeric')
            print(answercount)
            id = 'edit-answer-' + str(answercount) + '-answer'
            print(id)
            answer_num(id)

        time.sleep(1.2)
        answercount += 1

    driver.find_element(By.ID, 'edit-next').click()
    wait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id^=" + 'edit-fictional-0'))).send_keys(Keys.SPACE)
    driver.find_element(By.ID, 'edit-next').click()
    driver.find_element(By.ID, 'edit-submit').click()
    time.sleep(2)