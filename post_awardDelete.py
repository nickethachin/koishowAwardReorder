from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions
import os
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
wait = WebDriverWait(driver, 2)
ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)

driver.get('https://koishow.net/chiangmai/index.php#')
clearConsole()
print(driver.title)
driver.find_element(By.XPATH, '//*[@id="bt_login"]/a').click()

##login
wait.until(EC.presence_of_element_located((By.ID, 'usrnm')))
driver.find_element(By.ID, 'usrnm').send_keys("adminusername")
driver.find_element(By.ID, 'psw').send_keys("adminpassword")
driver.find_element(By.ID, 'login').click()

def navtoAwardList():
	wait.until(EC.presence_of_element_located((By.ID, 'bt_admin')))
	driver.find_element(By.ID, 'bt_admin').click()

	wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="admin_menu"]/li[5]/a')))
	driver.find_element(By.XPATH, '//*[@id="admin_menu"]/li[5]/a').click()

	wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="showListCer"]')))

navtoAwardList()

awardData = loadJson()

for i in range(len(awardData)):
	if i < 631:
		continue
	print(f"______________{i}________________")
	driver.implicitly_wait(2)
	wait.until(EC.presence_of_element_located((By.XPATH, f"//*[@id='showListCer']/div/div/div[{i+2}]")))
	try:
		row = driver.find_element(By.XPATH, f"//*[@id='showListCer']/div/div/div[{i+2}]")
		wait.until(EC.presence_of_element_located((By.TAG_NAME, 'span')))
		eleSpans = row.find_elements(By.TAG_NAME, 'span')
		eleName = eleSpans[1].text
		eleInputs = row.find_elements(By.TAG_NAME, 'input')
		eleOrder = eleInputs[0]
		eleOrderValue = eleOrder.get_attribute("value")
		eleDelete = eleInputs[2]
	except:
		row = driver.find_element(By.XPATH, f"//*[@id='showListCer']/div/div/div[{i+2}]")
		driver.implicitly_wait(10)
		eleSpans = row.find_elements(By.TAG_NAME, 'span')
		eleName = eleSpans[1].text
		eleInputs = row.find_elements(By.TAG_NAME, 'input')
		eleOrder = eleInputs[0]
		eleOrderValue = eleOrder.get_attribute("value")
		eleDelete = eleInputs[2]

	dataName = awardData[int(eleOrderValue)-1]['name']

	print(eleName, eleOrderValue, eleDelete.text)
	print(f"Found order {eleOrderValue} with name '{eleName}'")
	print(f"In data order {eleOrderValue} name is '{dataName}'")

	if eleName == dataName:
		print("Order is matched with the data")
	else:
		print("Order mismatch deleting......")
		eleDelete.click()
		wait.until(EC.alert_is_present())
		driver.switch_to.alert.accept()
		print("Deleted")

rows = driver.find_elements(By.XPATH, "//*[@id='showListCer']/div/div/div")
#Delete button //*[@id="showListCer"]/div/div/div/form/div[3]/input[2]
last = 0
for row in rows:
	# print(row.text)
	rowOrder = row.find_element(By.XPATH, "./form/div[1]/span[1]").text[:-1]
	rowValue = row.find_element(By.XPATH, "./form/div[2]/input").get_attribute("value")
	if rowValue == last:
		print(rowOrder, rowValue)
	last = rowValue


driver.close()
print("Exiting..")
os._exit(0)