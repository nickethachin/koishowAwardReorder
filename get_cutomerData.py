from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import os
import urllib.request
import json

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

options = Options()
#options.headless = True
driver = webdriver.Chrome(options=options)

# Open website
driver.get('https://koishow.net/chiangmai/index.php#')
clearConsole()
print(driver.title)

#Logging in
driver.find_element(By.XPATH, '//*[@id="bt_login"]/a').click()
WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'usrnm')))
driver.find_element(By.ID, 'usrnm').send_keys("adminusername")
driver.find_element(By.ID, 'psw').send_keys("adminpassword")
driver.find_element(By.ID, 'login').click()


WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'bt_admin')))
driver.find_element(By.ID, 'bt_admin').click()
WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'bt_verify')))
driver.find_element(By.ID, 'bt_verify').click()

WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tbl_list"]/tbody')))

# driver.find_element(By.CLASS_NAME, 'hand').click()
jsonFile = open("customerData.json", "w")

customerBtn = driver.find_elements(By.CLASS_NAME, 'hand')
customerList = []
i = 0
for btn in customerBtn:
    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable(btn))
    ActionChains(driver).move_to_element(element).click().perform()
    senderName = btn.text
    senderFishs = []
    # driver.implicitly_wait(3)
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#showReport > table > tbody > tr:nth-child(1) > td:nth-child(4) > div')))
    sender = driver.find_element(By.CSS_SELECTOR, '#showReport > table > tbody > tr:nth-child(1) > td:nth-child(4) > div')
    while sender.text != senderName:
        driver.implicitly_wait(2)
        sender = driver.find_element(By.CSS_SELECTOR, '#showReport > table > tbody > tr:nth-child(1) > td:nth-child(4) > div')

    fishDetails = driver.find_elements(By.XPATH, '//*[@id="showReport"]/table/tbody/tr/td[3]/div')
    for x in fishDetails:
        senderFishs.append(x.text[6:12])
    print("===========")
    print(senderName)
    print(senderFishs)
    cusJson = {
    'id': i,
    'name': senderName,
    'fishs': senderFishs
    }
    customerList.append(cusJson)

jsonString = json.dumps(customerList)
jsonFile.write(jsonString)
jsonFile.close()
driver.close()

print("Exiting..")
os._exit(0)