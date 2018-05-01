##################################
#           README               #
##################################
# Inputs transactions from a CSV into YNAB.

# For debugging, set to 1.
verbose = 1

import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv

username = sys.argv[1]
password = sys.argv[2]
userGuid = sys.argv[3]
accountGuid = sys.argv[4]

if verbose: 
	print("USERNAME: " + username)
	print("PASSWORD: " + password)
	print("User GUID: " + userGuid)
	print("Account GUID: " + accountGuid)

# INPUT VALIDATION
if username == "":
	print("Username is missing.")
	quit()

if password == "":
	print("Password is missing.")
	quit()

if userGuid == "":
	print("User GUID is missing.")
	quit()

if accountGuid == "":
	print("Account GUID is missing.")
	quit()

transactions = []

# Load CSV File
with open('chase.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
    	if len(row) != 4:
    		raise ValueError('Invalid format');
    	else:
    		transactions.append(row);

driver = webdriver.Chrome(executable_path=r"chromedriver")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get('https://app.youneedabudget.com/users/login')

# Select username field.
currentElement = driver.switch_to_active_element()
currentElement.send_keys(username)

currentElement.send_keys(Keys.TAB)

# Select password field.
currentElement = driver.switch_to_active_element()
currentElement.send_keys(password)

currentElement.send_keys(Keys.RETURN)

time.sleep(2)

driver.get('https://app.youneedabudget.com/' + userGuid + '/accounts/' + accountGuid)

time.sleep(2)

currentElement = driver.find_element_by_class_name('add-transaction')
currentElement.click();

# For each item,
for transaction in transactions:

	# The Date.
	currentElement = driver.switch_to_active_element()
	currentElement.send_keys(transaction[0])

	# The Payee.
	currentElement.send_keys(Keys.TAB)
	currentElement = driver.switch_to_active_element()
	currentElement.send_keys(transaction[1])

	# The Memo.
	currentElement.send_keys(Keys.TAB)
	currentElement = driver.switch_to_active_element()
	currentElement.send_keys(Keys.TAB)
	currentElement = driver.switch_to_active_element()
	currentElement.send_keys(transaction[2])

	# Determine if adding / subtracting, to determine if we do 1 or 2 tabs.
	amount = float(transaction[3])

	if amount > 0:
		currentElement.send_keys(Keys.TAB)
		currentElement = driver.switch_to_active_element()
		currentElement.send_keys(Keys.TAB)
	else:
		currentElement.send_keys(Keys.TAB)

	currentElement = driver.switch_to_active_element()

	currentElement.send_keys(str(abs(amount)))

	currentElement.send_keys(Keys.RETURN)

	time.sleep(2)

# Closes driver
driver.quit()
