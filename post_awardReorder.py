from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import os
import sys
import urllib.request
import json

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def saveJson():
	jsonFile = open('awardData.json', "w")
	jsonString = json.dumps(awardData, indent=4)
	jsonFile.write(jsonString)
	jsonFile.close()

def loadJson():
	jsonFile = open('awardData.json')
	data = json.load(jsonFile)
	jsonFile.close()
	return(data)

options = Options()
#options.headless = True
driver = webdriver.Chrome(options=options)
actions = ActionChains(driver)

driver.get('https://koishow.net/chiangmai/index.php#')
clearConsole()
print(driver.title)
driver.find_element(By.XPATH, '//*[@id="bt_login"]/a').click()

##login
WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'usrnm')))
driver.find_element(By.ID, 'usrnm').send_keys("adminusername")
driver.find_element(By.ID, 'psw').send_keys("adminpassword")
driver.find_element(By.ID, 'login').click()

def navtoAwardList():
	WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'bt_admin')))
	driver.find_element(By.ID, 'bt_admin').click()

	WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="admin_menu"]/li[5]/a')))
	driver.find_element(By.XPATH, '//*[@id="admin_menu"]/li[5]/a').click()

	WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="showListCer"]')))

navtoAwardList()

count = 0
awardData = loadJson()
try:
    for award in awardData:
        name = award['name']
        status = award['status']
        if status == "uncheck":
            try:
                driver.find_element(By.XPATH, f"//*[contains(text(), '{name}')]")
                award['status'] = "Found"
            except:
                award['status'] = "NotFound"
            saveJson()
            print(f"{award['id']} - {award['status']} :: {award['name']}")
        else:
            print(f"{award['id']} - SKIPPED :: {award['name']}")

    awardData = loadJson()

    for award in awardData:
        print("======================")
        name = award['name']
        if award['status'] == "Done":
            print(f"------ Skipped {award['id']} ------")
            continue

        elif award['status'] == "Found":
            
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{name}')]")))
            el = driver.find_element(By.XPATH, f"//*[contains(text(), '{name}')]")
            elInput = el.find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.TAG_NAME, 'input')
            elValue = elInput.get_attribute("value")

            #if old order id didn't match actual order id
            if int(elValue) != int(award['id']):
                print("wrong order id, inputing new one")
                elInput.clear()

                driver.implicitly_wait(4)
                elInput.send_keys(f"{award['id']}");
                driver.find_element(By.ID, 'bt_admin').click()
                count+=1
                print(f"waiting({count}) for editing order id...")
                WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="showListCer"]')))
                driver.find_element(By.ID, 'bt_admin').click()
                award['status'] = "Done"
                # saveJson()
                print(f"{award['id']} - {award['status']} :: {award['name']}")
                if count > 5:
                    count = 0
                    driver.refresh()
                    navtoAwardList()
            else:
                print('Order ID matched')
                award['status'] = "Done"
                # saveJson()
                print(f"{award['id']} - {award['status']} :: {award['name']}")

        elif award['status'] == "NotFound":
            #Adding
            continue
            form_nameEng = driver.find_element(By.ID, "nm_en").send_keys(f"{award['name']}")
            form_awardType = driver.find_element(By.ID, "cer_nm_type").send_keys(f"{award['awardType']}")
            form_koiSize = driver.find_element(By.ID, "koi_size").send_keys(f"{award['koiSize']}")
            form_koiType = Select(driver.find_element(By.ID, "koi_type")).select_by_value(str(award['koiType']))
            form_cerType = Select(driver.find_element(By.ID, "cer_type")).select_by_value(str(award['cerType']))
            form_submit  = driver.find_element(By.ID, "bt_add_cer").click()
            count+=1
            print(f"waiting({count}) for adding...")
            driver.implicitly_wait(1)
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{name}')]")))
            #Refresh and navigate back
            if count > 5:
                count = 0
                driver.refresh()
                navtoAwardList()
            #Fixing order
            el = driver.find_element(By.XPATH, f"//*[contains(text(), '{name}')]")
            elInput = el.find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.TAG_NAME, 'input')
            elValue = elInput.get_attribute("value")
            print("Fixing order id")
            elInput.clear()
            elInput.send_keys(f"{award['id']}");
            driver.find_element(By.ID, 'bt_admin').click()
            print("waiting for editing order id...")
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="showListCer"]')))
            driver.find_element(By.ID, 'bt_admin').click()
            #Done
            award['status'] = "Done"
            # saveJson()
            print(f"{award['id']} - {award['status']} :: {award['name']}")

        else:
            print(award['status'])

        saveJson()
except:
    try:
        driver.close()
        os.execv(sys.executable, [sys.executable, __file__] + sys.argv)
    except:
        os.execv(sys.executable, [sys.executable, __file__] + sys.argv)

print('______________________')
del awardData
awardData = loadJson()
for award in awardData:
	print(f"{award['id']} - [{award['status']}] :: {award['name']} - ")
driver.close()

print("Exiting..")
os._exit(0)